import os
import logging
import json
from time import time
from glob import glob
from hashlib import sha256
from random import randint

logger = logging.getLogger(__name__)  # Same name as calling module
logger.addHandler(logging.NullHandler())  # No output unless configured by calling program
CACHED_BLOB_TIME = 3 * 60 * 60  # 3 hours in seconds


def hash_obj(obj):
    val = obj
    if not isinstance(obj, str):
        val = obj.pre_hash()
    result = sha256(val.encode())
    result = result.hexdigest()
    return result


class FileSystemCache:

    def __init__(self, timeout=CACHED_BLOB_TIME):
        self.timeout = timeout

    def clear_blob(self, obj):
        blob_filepath, path_exists = self.get_cached_blob_filepath(obj)
        if path_exists:
            logger.info(f'Clearing cached blob. {blob_filepath}')
            try:
                os.remove(blob_filepath)
            except FileNotFoundError:
                pass

    def get_cached_blob_filepath(self, obj):
        path_base = f'.pangea_api_cache/v1/pangea_api_cache__{hash_obj(obj)}'
        os.makedirs(os.path.dirname(path_base), exist_ok=True)
        paths = sorted(glob(f'{path_base}__*.json'))
        if paths:
            return paths[-1], True
        timestamp = int(time())
        blob_filepath = f'{path_base}__{timestamp}.json'
        return blob_filepath, False

    def get_cached_blob(self, obj):
        logger.info(f'Getting cached blob. {obj}')
        blob_filepath, path_exists = self.get_cached_blob_filepath(obj)
        if not path_exists:  # cache not found
            logger.info(f'No cached blob found. {obj}')
            return None
        timestamp = int(blob_filepath.split('__')[-1].split('.json')[0])
        elapsed_time = int(time()) - timestamp
        if elapsed_time > (self.timeout + randint(0, CACHED_BLOB_TIME // 10)):  # cache is stale
            logger.info(f'Found stale cached blob. {obj}')
            os.remove(blob_filepath)
            return None
        logger.info(f'Found good cached blob. {obj}')
        try:
            blob = json.loads(open(blob_filepath).read())
            return blob
        except FileNotFoundError:
            return None

    def cache_blob(self, obj, blob):
        logger.info(f'Caching blob. {obj} {blob}')
        blob_filepath, path_exists = self.get_cached_blob_filepath(obj)
        if path_exists:  # save a new cache if an old one exists
            try:
                os.remove(blob_filepath)
            except FileNotFoundError:
                pass
            return self.cache_blob(obj, blob)
        with open(blob_filepath, 'w') as f:
            f.write(json.dumps(blob))
