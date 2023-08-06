import os

from savvihub.api.types import SavviHubFileObject
from savvihub.common.utils import read_in_chunks


class FileObject(SavviHubFileObject):
    def __init__(self, file_object: SavviHubFileObject):
        super().__init__(file_object.dict)

    def upload_chunks(self, base_path):
        return read_in_chunks(os.path.join(base_path, self.path))

    def upload_hooks(self, log=None, callback=None):
        def fn(resp, **kwargs):
            resp.raise_for_status()
            if log:
                log(f"Uploading {self.path}")
            if callback:
                callback()
        return {
            'response': fn,
        }

    def download_hooks(self, base_path, log=None, callback=None):
        def fn(resp, **kwargs):
            path = os.path.join(base_path, self.path)
            if log:
                log(f"Downloading {path}")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            if callback:
                callback()
        return {
            'response': fn,
        }
