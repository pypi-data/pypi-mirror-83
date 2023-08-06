import os
import tempfile
import time
from collections import defaultdict
from urllib.parse import urlparse

import typer

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.api.uploader import Downloader, Uploader

volume_app = typer.Typer()


class PathException(Exception):
    pass


def refine_path(path_arg, raise_if_not_empty=False, raise_if_not_exist=False):
    if path_arg.startswith("savvihub://"):
        return path_arg, True

    path = os.path.abspath(path_arg)
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise PathException(f"Must specify directory: {path_arg}")
        if raise_if_not_empty and len(os.listdir(path)) > 0:
            raise PathException(f"Must specify empty directory: {path_arg}")
    else:
        if raise_if_not_exist:
            raise PathException(f"Must specify directory: {path_arg}")
        os.mkdir(path)

    return path, False


def split_remote_path(remote_path):
    u = urlparse(remote_path)
    volume_id = u.netloc
    prefix = u.path
    return volume_id, prefix


@volume_app.callback()
def main():
    return


@volume_app.command()
def cp(
    source_path_arg: str = typer.Argument(...),
    dest_path_arg: str = typer.Argument(...),
    watch: bool = typer.Option(False, "-w", "--watch"),
):
    try:
        source_path, is_source_remote = refine_path(source_path_arg, raise_if_not_exist=True)
        dest_path, is_dest_remote = refine_path(dest_path_arg, raise_if_not_empty=True)
    except PathException as e:
        typer.echo(str(e))
        return

    context = Context()
    client = SavviHubClient(token=context.token)

    hashmap = defaultdict(lambda: "")

    while True:
        if is_source_remote and is_dest_remote:
            # remote -> remote
            source_volume_id, source_prefix = split_remote_path(source_path)
            dest_volume_id, dest_prefix = split_remote_path(dest_path)
            files = Downloader.get_files_to_download(context, source_volume_id)
            files = [file for file in files if hashmap[file.path] != file.hash]

            if len(files) > 0:
                tmp_dir = tempfile.mkdtemp()
                Downloader.parallel_download(context, tmp_dir, files, progressable=typer.progressbar)
                Uploader.parallel_upload(context, tmp_dir, files, dest_volume_id, progressable=typer.progressbar)

                for file in files:
                    hashmap[file.path] = file.hash

        elif is_source_remote and not is_dest_remote:
            # remote -> local
            source_volume_id, source_prefix = split_remote_path(source_path)
            files = Downloader.get_files_to_download(context, source_volume_id, prefix=source_prefix)
            files = [file for file in files if hashmap[file.path] != file.hash]

            typer.echo(f'Find {len(files)} files to download.')
            if len(files) > 0:
                Downloader.parallel_download(context, dest_path, files, progressable=typer.progressbar)

                for file in files:
                    hashmap[file.path] = file.hash

        elif not is_source_remote and is_dest_remote:
            # local -> remote
            dest_volume_id, dest_prefix = split_remote_path(dest_path)
            files = Uploader.get_files_to_upload(source_path, hashmap)
            files = [f'{os.path.join(dest_prefix, file)}' for file in files]

            typer.echo(f'Find {len(files)} files to upload.')
            if len(files) > 0:
                Uploader.parallel_upload(context, source_path, files, dest_volume_id, progressable=typer.progressbar)

                hashmap = Uploader.get_hashmap(source_path)
        else:
            typer.echo('Cannot copy volume from local to local')
            return

        if not watch:
            return

        time.sleep(10)
