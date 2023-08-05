
import os
import logging
import json
from time import time
from glob import glob
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)  # Same name as calling module
logger.addHandler(logging.NullHandler())  # No output unless configured by calling program


class RemoteObjectError(Exception):
    pass


class RemoteObjectOverwriteError(RemoteObjectError):
    pass


class RemoteObject:
    CACHED_BLOB_TIME = 60 * 60  # 60 minutes in seconds
    optional_remote_fields = []

    def __init__(self, *args, **kwargs):
        self._already_fetched = False
        self._modified = False
        self._deleted = False
        self.blob = None
        self.uuid = None

    def __setattr__(self, key, val):
        if hasattr(self, 'deleted') and self._deleted:
            logger.error(f'Attribute cannot be set, RemoteObject has been deleted. {self}')
            raise RemoteObjectError('This object has been deleted.')
        super(RemoteObject, self).__setattr__(key, val)
        if key in self.remote_fields or key == self.parent_field:
            logger.info(f'Setting RemoteObject modified. key "{key}"')
            super(RemoteObject, self).__setattr__('_modified', True)

    def get_cached_blob_filepath(self):
        path_base = f'.pangea_api_cache/pangea_api_cache__{hash(self)}'
        os.makedirs(os.path.dirname(path_base), exist_ok=True)
        paths = sorted(glob(f'{path_base}__*.json'))
        if paths:
            return paths[-1], True
        timestamp = int(time())
        blob_filepath = f'{path_base}__{timestamp}.json'
        return blob_filepath, False

    def get_cached_blob(self):
        logger.info(f'Getting cached blob. {self}')
        blob_filepath, path_exists = self.get_cached_blob_filepath()
        if not path_exists:  # cache not found
            logger.info(f'No cached blob found. {self}')
            return None
        timestamp = int(blob_filepath.split('__')[-1].split('.json')[0])
        elapsed_time = int(time()) - timestamp
        if elapsed_time > self.CACHED_BLOB_TIME:  # cache is stale
            logger.info(f'Found stale cached blob. {self}')
            os.remove(blob_filepath)
            return None
        logger.info(f'Found good cached blob. {self}')
        blob = json.loads(open(blob_filepath).read())
        return blob

    def cache_blob(self, blob):
        logger.info(f'Caching blob. {blob}')
        blob_filepath, path_exists = self.get_cached_blob_filepath()
        if path_exists:  # save a new cache if an old one exists
            os.remove(blob_filepath)
            return self.cache_blob(blob)
        with open(blob_filepath, 'w') as f:
            f.write(json.dumps(blob))

    def load_blob(self, blob):
        logger.info(f'Loading blob. {blob}')
        if self._deleted:
            logger.error(f'Cannot load blob, RemoteObject has been deleted. {self}')
            raise RemoteObjectError('This object has been deleted.')
        for field in self.remote_fields:
            current = getattr(self, field, None)
            try:
                new = blob[field]
            except KeyError:
                if field not in self.optional_remote_fields:
                    logger.error(f'Blob being loaded is missing key. {field}')
                    raise KeyError(f'Key {field} is missing for object {self} (type {type(self)}) in blob: {blob}')
                new = None
            if current and current != new:
                is_overwrite = True
                if isinstance(current, dict) and isinstance(new, dict):
                    append_only = True
                    for k, v in current.items():
                        if (k not in new) or (new[k] != v):
                            append_only = False
                        break
                    if append_only:
                        is_overwrite = False
                if is_overwrite:
                    logger.error(f'Loading blob would overwrite key. {field}')
                    raise RemoteObjectOverwriteError((
                        f'Loading blob would overwrite field "{field}":\n\t'
                        f'current: "{current}" (type: "{type(current)}")\n\t'
                        f'new: "{new}" (type: "{type(new)}")'
                    ))
            setattr(self, field, new)

    def get(self):
        """Fetch the object from the server."""
        if self._deleted:
            logger.error(f'Cannot GET blob, RemoteObject has been deleted. {self}')
            raise RemoteObjectError('This object has been deleted.')
        if not self._already_fetched:
            logger.info(f'Fetching RemoteBlob. {self}')
            self._get()
            self._already_fetched = True
            self._modified = False
        else:
            logger.info(f'RemoteObject has already been fetched. {self}')
        return self

    def create(self):
        """Create this object on the server."""
        if self._deleted:
            logger.error(f'Cannot create blob, RemoteObject has been deleted. {self}')
            raise RemoteObjectError('This object has been deleted.')
        if not self._already_fetched:
            logger.info(f'Creating RemoteBlob. {self}')
            self._create()
            self._already_fetched = True
            self._modified = False
        else:
            logger.info(f'RemoteObject has already been fetched. {self}')
        return self

    def save(self):
        """Assuming the object exists on the server make the server-side object
        match the state of this object.
        """
        if self._deleted:
            logger.error(f'Cannot save blob, RemoteObject has been deleted. {self}')
            raise RemoteObjectError('This object has been deleted.')
        if not self._already_fetched:
            msg = 'Attempting to SAVE an object which has not been fetched is disallowed.'
            raise RemoteObjectError(msg)
        if self._modified:
            logger.info(f'Saving RemoteBlob. {self}')
            blob_filepath, path_exists = self.get_cached_blob_filepath()
            if path_exists:
                logger.info(f'Clearing cached blob. {blob_filepath}')
                os.remove(blob_filepath)
            self._save()
            self._modified = False
        else:
            logger.info(f'RemoteBlob has not been modified. Nothing to save. {self}')

    def idem(self):
        """Make the state of this object match the server."""
        if self._deleted:
            raise RemoteObjectError('This object has been deleted.')
        if not self._already_fetched:
            try:
                self.get()
            except HTTPError:
                self.create()
        else:
            self.save()
        return self

    def delete(self):
        logger.info(f'Deleting RemoteBlob. {self}')
        self.knex.delete(self.nested_url())
        self._already_fetched = False
        self._deleted = True
