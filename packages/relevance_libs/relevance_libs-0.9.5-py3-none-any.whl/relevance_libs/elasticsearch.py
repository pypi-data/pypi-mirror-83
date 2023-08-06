"""
This module provides a minimal interface for communicating with Elasticsearch instances.
"""

import os
import json
import typing
import requests


class ElasticsearchError(RuntimeError):
    """
    This error is raised when there's an error with the Elasticsearch backend.
    """


class VersionConflictError(ElasticsearchError):
    """
    This error is raised when the versioning check fails for a document update.
    """


class Elasticsearch():
    """
    This class provides a minimal stateless wrapper for Elasticsearch instances.
    """

    def __init__(self, index_url: str, *, timeout: float = 10) -> None:
        """
        The *index_url* is the URL to the target index. The *timeout* argument sets the timeout
        of HTTP requests to the instance.
        """
        self.index_url = index_url
        self.timeout = timeout

    def ping(self):
        """
        Ping the instance to make sure it's alive.
        """
        try:
            response = requests.get(self.index_url)
            if response.status_code != 404:
                try:
                    response.raise_for_status()
                except Exception as ex:
                    raise ElasticsearchError(str(ex)) from None

            try:
                body = response.json()
                version = body['version']['number'].split('.')
            except KeyError:
                url = os.path.dirname(self.index_url)
                response = requests.get(url)
                response.raise_for_status()
                body = response.json()
                version = body['version']['number'].split('.')

            if int(version[0]) < 7:
                raise EnvironmentError('minimum supported version is 7.x, got %s' %
                                       '.'.join(version))

        except KeyError:
            raise ElasticsearchError('elasticsearch does not appear to be live: %s' %
                                     self.index_url) from None

        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

    def get(self, doc_id: str, *, source: bool = True) -> dict:
        """
        Get a document from a Elasticsearch.

        The *doc_id* is the specific document identifier to retrieve.

        If *source* is `True`, only the document source is returned. Otherwise, all
        metadata is also returned.
        """
        url = '{0}/_doc/{1}'.format(self.index_url, doc_id)
        response = requests.get(url, timeout=self.timeout)

        if response.status_code == 404:
            return None

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None

        result = response.json()
        return result if not source else result['_source']

    def peek(self, request: typing.Union[dict, str]) -> dict:
        """
        Get information about a result set without actually returning the results.

        This method only returns the metadata associated with a search request, such as total
        number of hits and aggreations.

        The *request* argument is either a dictionary that translates into an Elasticsearch
        DSL query, or a string that represents an Elasticsearch query string query.
        """
        request = request or {}
        url = '{0}/_search?size=0'.format(self.index_url)
        payload = request if isinstance(request, dict) else \
            {'query': {'query_string': {'query': request}}}
        response = requests.post(url, json=payload, timeout=self.timeout)

        if response.status_code == 404:
            return None

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

        result = response.json()
        try:
            del result['hits']['hits']
        except KeyError:
            pass
        return result

    def count(self, request: typing.Union[dict, str] = None) -> int:
        """
        Get the number of matching documents for a search request.

        The *request* argument is either a dictionary that translates into an Elasticsearch
        DSL query, or a string that represents an Elasticsearch query string query.
        """
        try:
            url = '{0}/_count'.format(self.index_url)
            payload = request if isinstance(request, dict) else \
                {'query': {'query_string': {'query': request}}}
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()['count']
        except Exception:
            return 0

    def search(self, request: typing.Union[dict, str] = None, *, source: bool = True,
               ttl: str = '1m',
               size: int = None) -> typing.Generator[typing.Union[list, dict], None, None]:
        """
        Search for documents within an index.

        This method returns a generator, therefore is lazy. If the generator is not
        fully consumed, only the necessary requests will be fired, so it is relatively
        performant.

        The *request* argument is either a dictionary that translates into an Elasticsearch
        DSL query, or a string that represents an Elasticsearch query string query.

        If *source* is `True`, only the document source is returned. Otherwise, all
        metadata is also returned.

        The *ttl* arguments defines the amount of time to keep the Elasticsearch Scroll
        object between requests. If *size* is specified, the generator value will be a list
        of documents containing N documents for each page, rather than a dict for each
        document.
        """
        # pylint: disable=too-many-branches

        request = request or {}
        scroll_id = None

        while True:
            if not scroll_id:
                url = '{0}/_search?scroll={1}'.format(self.index_url, ttl)
                payload = request if isinstance(request, dict) else \
                    {'size': size or 10, 'query': {'query_string': {'query': request}}}
            else:
                root_url = os.path.dirname(self.index_url)
                root_url = root_url if not root_url.endswith(':') else self.index_url
                url = '{0}/_search/scroll'.format(root_url)

                if not size:
                    payload = {'scroll': ttl, 'scroll_id': scroll_id}
                else:
                    payload = {'scroll': ttl, 'scroll_id': scroll_id}

            response = requests.post(url, json=payload, timeout=self.timeout)

            if response.status_code == 404:
                return None

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as ex:
                raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
            except requests.exceptions.RequestException as ex:
                raise ElasticsearchError(str(ex)) from None

            data = response.json()
            if not scroll_id:
                scroll_id = data['_scroll_id']

            if not data['hits']['hits']:
                break

            try:
                if not size:
                    for hit in data['hits']['hits']:
                        result = hit if not source else hit['_source']
                        yield result
                else:
                    items = []
                    for hit in data['hits']['hits']:
                        result = hit if not source else hit['_source']
                        items.append(result)
                    yield items
            except KeyError:
                pass

    def index(self, doc: dict, doc_id: str = None, *, create: bool = False,
              refresh: bool = False, version: int = None) -> str:
        """
        Index a document in Elastic and return the document identifier.

        The *doc* argument is a dictionary containing the data to index. The optional
        *doc_id* argument is the unique document identifier to give to the document. If
        omitted, it is auto-generated by Elasticsearch item.

        The *create* argument ensures that if the document already exists, an error is
        thrown.

        If *refresh* is enabled, the index is refreshed after the document is indexed.
        If *version* is supplied, a version check occurs for the document.
        """
        url = '{0}/{1}/{2}?{3}{4}'.format(
            self.index_url,
            '_doc' if not create else '_create',
            doc_id if doc_id else '',
            'refresh=true' if refresh else 'refresh=false',
            '&version={0}&version_type=external'.format(version) if version else '',
        )
        payload = dict(doc)

        if doc_id:
            response = requests.put(url, json=payload, timeout=self.timeout)
        else:
            response = requests.post(url, json=payload, timeout=self.timeout)

        if response.status_code == 409:
            raise VersionConflictError(version)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

        result = response.json()

        if refresh:
            self.refresh_index()

        return result['_id']

    def bulk_index(self, docs: typing.List[dict], *, refresh: bool = False) -> None:
        """
        Index multiple documents in Elastic.

        The *docs* argument is a list of dicts containing the data to index.

        If *refresh* is enabled, the index is refreshed after the documents are indexed.
        """
        payload = []
        for doc in docs:
            if '_id' and '_source' in doc:
                payload.append(json.dumps({'index': {'_id': doc['_id']}}))
                payload.append(json.dumps(doc['_source']))
            else:
                payload.append(json.dumps({'index': {}}))
                payload.append(json.dumps(doc))
        payload = '\n'.join(payload) + '\n'

        url = '{0}/_bulk'.format(self.index_url)
        response = requests.post(
            url, data=payload,
            headers={'Content-Type': 'application/x-ndjson'},
            timeout=self.timeout,
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

        if refresh:
            self.refresh_index()

    def refresh_index(self) -> None:
        """
        Refresh an index manually.

        The *index_url* argument is the URL to the Elasticsearch index. If omitted, the
        global setting is used instead.
        """
        url = '{0}/_refresh'.format(self.index_url)
        response = requests.get(url, timeout=self.timeout)

        if response.status_code == 404:
            raise FileNotFoundError('index does not exist')

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

    def create_index(self) -> None:
        """
        Create an index.
        """
        response = requests.put(self.index_url, timeout=self.timeout)

        if response.status_code == 400 and 'already' in response.text and 'exists' in response.text:
            raise FileExistsError('index already exists')

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

    def delete_index(self) -> None:
        """
        Delete an index.
        """
        response = requests.delete(self.index_url, timeout=self.timeout)

        if response.status_code == 404:
            raise FileNotFoundError('index does not exist')

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

    def set_mapping(self, mapping: dict) -> None:
        """
        Set the mapping for an index.

        The *mapping* argument is a dictionary with the same structure as an
        Elasticsearch mapping request.
        """
        url = '{0}/_mapping'.format(self.index_url)
        response = requests.put(url, json=mapping, timeout=self.timeout)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

    def get_mapping(self) -> dict:
        """
        Get the mapping for an index.
        """
        url = '{0}/_mapping'.format(self.index_url)
        response = requests.get(url, timeout=self.timeout)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            raise ElasticsearchError('%s: %s' % (ex, ex.response.content)) from None
        except requests.exceptions.RequestException as ex:
            raise ElasticsearchError(str(ex)) from None

        data = response.json()
        index_name = list(data.keys())[0]
        properties = data[index_name]['mappings']

        return properties
