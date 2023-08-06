import os

from savvihub.api.types import SavviHubFileObject
from savvihub.common.utils import read_in_chunks


class FileObject(SavviHubFileObject):
    def __init__(self, file_object: SavviHubFileObject, base_path):
        super().__init__(file_object.dict)
        self.base_path = base_path
        self.full_path = os.path.join(base_path, self.path)

    def upload_chunks(self, *, callback=None):
        return read_in_chunks(self.full_path, callback=callback)

    def upload_hooks(self, *, log=None):
        def fn(resp, **kwargs):
            resp.raise_for_status()
        return {
            'response': fn,
        }

    def download_hooks(self, *, callback=None):
        def fn(resp, **kwargs):
            os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
            with open(self.full_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
                    if callback:
                        callback(chunk)
        return {
            'response': fn,
        }
