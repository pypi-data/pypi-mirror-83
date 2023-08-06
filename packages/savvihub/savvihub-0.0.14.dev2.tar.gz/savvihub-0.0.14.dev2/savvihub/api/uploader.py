import os

from requests_futures.sessions import FuturesSession

from savvihub.api.file_object import FileObject
from savvihub.api.savvihub import SavviHubClient
from savvihub.api.types import SavviHubFileObject
from savvihub.common.utils import wait_all_futures, calculate_crc32c


def default_hooks():
    def fn(resp, **kwargs):
        resp.raise_for_status()
    return {
        'response': fn,
    }


class Downloader:
    @classmethod
    def get_files_to_download(cls, context, volume_id):
        client = SavviHubClient(token=context.token)
        files = client.volume_file_list(volume_id)
        return files

    @classmethod
    def parallel_download(cls, context, path, files, log=None, callback=None):
        session = FuturesSession(max_workers=context.parallel)
        futures = []
        for file in files:
            file_object = FileObject(file)
            if file.path.endswith('/'):
                continue
            future = session.get(
                file.download_url.url, stream=True, hooks=file_object.download_hooks(path, log=log, callback=callback)
            )
            futures.append(future)
        wait_all_futures(futures)


class Uploader:
    @classmethod
    def get_files_to_upload(cls, base_path, hashmap=None):
        files = []
        for root, _, files_ in os.walk(base_path):
            for name in files_:
                name = os.path.join(os.path.abspath(root), name)
                name = name[len(base_path) + 1:] if name.startswith(base_path) else name
                if hashmap and hashmap[name] == calculate_crc32c(os.path.join(base_path, name)):
                    continue
                files.append(name)
            return files

    @classmethod
    def get_hashmap(cls, base_path):
        files = cls.get_files_to_upload(base_path)
        hashmap = dict()
        for file in files:
            path = os.path.join(base_path, file)
            hashmap[file] = calculate_crc32c(path)
        return hashmap

    @classmethod
    def parallel_upload(cls, context, base_path, files, volume_id, *, log=None, callback=None):
        session = FuturesSession(max_workers=context.parallel)
        client = SavviHubClient(token=context.token, session=session)

        futures = []
        for file in files:
            future = client.volume_file_create(
                volume_id,
                file,
                is_dir=False,
                hooks=default_hooks()
            )
            futures.append(future)
        resps = wait_all_futures(futures)

        futures = []
        for i, resp in enumerate(resps):
            file_object = FileObject(SavviHubFileObject(resp.json()))
            future = session.put(
                file_object.upload_url.url,
                data=file_object.upload_chunks(base_path),
                headers={
                    'content-type': 'application/octet-stream',
                },
                hooks=file_object.upload_hooks(log=log, callback=callback),
            )
            futures.append(future)
        wait_all_futures(futures)

        futures = []
        for file in files:
            future = client.volume_file_uploaded(
                volume_id,
                file,
                is_dir=False,
            )
            futures.append(future)
        wait_all_futures(futures)

