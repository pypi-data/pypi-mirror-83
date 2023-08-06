import os
import time
from collections import defaultdict

import typer

from savvihub.api.savvihub import SavviHubClient
from savvihub.api.uploader import Downloader, Uploader
from savvihub.common.context import Context


artifact_app = typer.Typer()


@artifact_app.callback()
def main():
    return


@artifact_app.command()
def upload(
    watch: bool = typer.Option(False, "-w", "--watch"),
    output_path_arg: str = typer.Argument("."),
):
    output_path = os.path.abspath(output_path_arg)
    if not os.path.exists(output_path) or not os.path.isdir(output_path):
        typer.echo("Must specify directory as an upload path")
        return

    context = Context()
    hashmap = None
    while True:
        files = Uploader.get_files_to_upload(output_path, hashmap)
        hashmap = Uploader.get_hashmap(output_path)

        typer.echo(f'Find {len(files)} files to upload.')
        with typer.progressbar(length=len(files)) as progress:
            Uploader.parallel_upload(context, output_path, files, context.experiment.output_volume_id, log=typer.echo, callback=lambda: progress.update(1))

        typer.echo(f'Uploaded {len(files)} files in {os.path.abspath(output_path)}')

        if not watch:
            return

        time.sleep(10)


@artifact_app.command()
def download(
    prefix: str = typer.Option("", "--prefix"),
    watch: bool = typer.Option(False, "-w", "--watch"),
    output_path_arg: str = typer.Argument("."),
):
    output_path = os.path.abspath(output_path_arg)
    if os.path.exists(output_path):
        if not os.path.isdir(output_path):
            typer.echo("Must specify directory as an download path")
            return
        if len(os.listdir(output_path)) > 0:
            typer.echo("Must specify empty directory as an output path")
            return
    else:
        os.mkdir(output_path)

    context = Context()
    client = SavviHubClient(token=context.token)

    hashmap = defaultdict(lambda: "")
    while True:
        files = client.volume_file_list(context.experiment.output_volume_id, prefix=prefix)
        files = [file for file in files if hashmap[file.path] != file.hash]
        if len(files) > 0:
            typer.echo(f'{len(files)} files to downloaded')

        with typer.progressbar(length=len(files)) as progress:
            for file in files:
                hashmap[file.path] = file.hash
            Downloader.parallel_download(context, output_path, files, log=typer.echo, callback=lambda: progress.update(1))

        typer.echo(f'Downloaded {len(files)} files in {output_path}')

        if not watch:
            return

        time.sleep(10)


@artifact_app.command()
def sync(
    watch: bool = typer.Option(..., "-w", "--watch"),
    output_path_arg: str = typer.Argument("."),
):
    output_path = os.path.abspath(output_path_arg)
    if os.path.exists(output_path):
        if not os.path.isdir(output_path):
            typer.echo("Must specify empty directory as an output path")
            return
        if len(os.listdir(output_path)) > 0:
            typer.echo("Must specify empty directory as an output path")
            return
    else:
        os.mkdir(output_path)

    context = Context()

    files = Downloader.get_files_to_download(context, context.experiment.output_volume_id)
    typer.echo(f'Download {len(files)} files to {output_path}')

    with typer.progressbar(length=len(files)) as progress:
        Downloader.parallel_download(context, output_path, files, log=typer.echo, callback=lambda: progress.update(1))

    files = Uploader.get_files_to_upload(output_path)
    with typer.progressbar(length=len(files)) as progress:
        typer.echo(f'Find {len(files)} files to upload.')
        Uploader.parallel_upload(context, output_path, files, context.experiment.output_volume_id, log=typer.echo, callback=lambda: progress.update(1))

    typer.echo(f'Uploaded {len(files)} files in {os.path.abspath(output_path)}')
