import os
import requests
import logging
import json
from time import time
from glob import glob

DEFAULT_ENDPOINT = 'https://pangea.gimmebio.com'


logger = logging.getLogger(__name__)  # Same name as calling module
logger.addHandler(logging.NullHandler())  # No output unless configured by calling program


def clean_url(url):
    if url[-1] == '/':
        url = url[:-1]
    return url


class TokenAuth(requests.auth.AuthBase):
    """Attaches MetaGenScope Token Authentication to the given Request object."""

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        """Add authentication header to request."""
        request.headers['Authorization'] = f'Token {self.token}'
        return request

    def __str__(self):
        """Return string representation of TokenAuth."""
        return self.token


class Knex:
    CACHED_BLOB_TIME = 15 * 60  # 60 minutes in seconds

    def __init__(self, endpoint_url=DEFAULT_ENDPOINT):
        self.endpoint_url = endpoint_url
        self.endpoint_url += '/api'
        self.auth = None
        self.headers = {'Accept': 'application/json'}

    def _logging_info(self, **kwargs):
        base = {'endpoint_url': self.endpoint_url, 'headers': self.headers}
        base.update(kwargs)
        return base

    def _clean_url(self, url):
        url = clean_url(url)
        url = url.replace(self.endpoint_url, '')
        if url[0] == '/':
            url = url[1:]
        return url

    def add_auth_token(self, token):
        self.auth = TokenAuth(token)

    def get_login_cache_filepath(self, username):
        path_base =  f'.pangea_api_cache/v1/pangea_api_cache__auth_token__{username}'
        os.makedirs(os.path.dirname(path_base), exist_ok=True)
        paths = sorted(glob(f'{path_base}__*.json'))
        if paths:
            return paths[-1], True
        timestamp = int(time())
        blob_filepath = f'{path_base}__{timestamp}.json'
        return blob_filepath, False

    def cache_login_blob(self, username, blob):
        logger.info(f'Caching blob. {blob}')
        blob_filepath, path_exists = self.get_login_cache_filepath(username)
        if path_exists:  # save a new cache if an old one exists
            os.remove(blob_filepath)
            return self.cache_blob(blob)
        with open(blob_filepath, 'w') as f:
            f.write(json.dumps(blob))

    def get_cached_login_blob(self, username):
        logger.info(f'Getting cached login. {self}')
        blob_filepath, path_exists = self.get_login_cache_filepath(username)
        if not path_exists:  # cache not found
            logger.info(f'No cached login found. {self}')
            return None
        timestamp = int(blob_filepath.split('__')[-1].split('.json')[0])
        elapsed_time = int(time()) - timestamp
        if elapsed_time > self.CACHED_BLOB_TIME:  # cache is stale
            logger.info(f'Found stale cached login. {self}')
            os.remove(blob_filepath)
            return None
        logger.info(f'Found good cached login. {self}')
        blob = json.loads(open(blob_filepath).read())
        return blob

    def login(self, username, password):
        d = self._logging_info(email=username, password='*' * len(password))
        logger.info(f'Sending log in request. {d}')
        blob = self.get_cached_login_blob(username)
        if not blob:
            response = requests.post(
                f'{self.endpoint_url}/auth/token/login',
                headers=self.headers,
                json={
                    'email': username,
                    'password': password,
                }
            )
            response.raise_for_status()
            logger.info(f'Received log in response. {response.json()}')
            blob = response.json()
            self.cache_login_blob(username, blob)
        self.add_auth_token(blob['auth_token'])
        return self

    def _handle_response(self, response, json_response=True):
        try:
            response.raise_for_status()
        except:
            logger.error(f'Request failed. {response}')
            raise
        if json_response:
            return response.json()
        return response

    def get(self, url, **kwargs):
        url = self._clean_url(url)
        d = self._logging_info(url=url, auth_token=self.auth)
        logger.info(f'Sending GET request. {d}')
        response = requests.get(
            f'{self.endpoint_url}/{url}',
            headers=self.headers,
            auth=self.auth,
        )
        return self._handle_response(response, **kwargs)

    def post(self, url, json={}, **kwargs):
        url = self._clean_url(url)
        d = self._logging_info(url=url, auth_token=self.auth, json=json)
        logger.info(f'Sending POST request. {d}')
        response = requests.post(
            f'{self.endpoint_url}/{url}',
            headers=self.headers,
            auth=self.auth,
            json=json
        )
        return self._handle_response(response, **kwargs)

    def put(self, url, json={}, **kwargs):
        url = self._clean_url(url)
        d = self._logging_info(url=url, auth_token=self.auth, json=json)
        logger.info(f'Sending PUT request. {d}')
        response = requests.put(
            f'{self.endpoint_url}/{url}',
            headers=self.headers,
            auth=self.auth,
            json=json
        )
        return self._handle_response(response, **kwargs)

    def delete(self, url, **kwargs):
        url = self._clean_url(url)
        d = self._logging_info(url=url, auth_token=self.auth)
        logger.info(f'Sending DELETE request. {d}')
        response = requests.delete(
            f'{self.endpoint_url}/{url}',
            headers=self.headers,
            auth=self.auth,
        )
        return self._handle_response(response, **kwargs)
