import os
import logging
import json
from time import time
from glob import glob
from hashlib import sha256

logger = logging.getLogger(__name__)  # Same name as calling module
logger.addHandler(logging.NullHandler())  # No output unless configured by calling program
CACHED_BLOB_TIME = 60 * 60  # 60 minutes in seconds


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
        if elapsed_time > self.timeout:  # cache is stale
            logger.info(f'Found stale cached blob. {obj}')
            os.remove(blob_filepath)
            return None
        logger.info(f'Found good cached blob. {obj}')
        blob = json.loads(open(blob_filepath).read())
        return blob

    def cache_blob(self, obj, blob):
        logger.info(f'Caching blob. {obj} {blob}')
        blob_filepath, path_exists = self.get_cached_blob_filepath(obj)
        if path_exists:  # save a new cache if an old one exists
            os.remove(blob_filepath)
            return self.cache_blob(obj, blob)
        with open(blob_filepath, 'w') as f:
            f.write(json.dumps(blob))
