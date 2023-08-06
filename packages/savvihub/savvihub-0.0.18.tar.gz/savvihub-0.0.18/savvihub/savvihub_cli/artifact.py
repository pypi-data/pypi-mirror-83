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

    context = Context(experiment_required=True)
    experiment = context.experiment

    hashmap = None
    while True:
        files = Uploader.get_files_to_upload(output_path, hashmap)

        typer.echo(f'Find {len(files)} files to upload.')
        if len(files) > 0:
            Uploader.parallel_upload(context, output_path, files, experiment.output_volume_id, progressable=typer.progressbar)
            hashmap = Uploader.get_hashmap(output_path)

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

    context = Context(experiment_required=True)
    experiment = context.experiment

    hashmap = defaultdict(lambda: "")

    while True:
        files = Downloader.get_files_to_download(context, experiment.output_volume_id, prefix=prefix)
        files = [file for file in files if hashmap[file.path] != file.hash]

        typer.echo(f'{len(files)} files to downloaded')
        if len(files) > 0:
            Downloader.parallel_download(context, output_path, files, progressable=typer.progressbar)
            for file in files:
                hashmap[file.path] = file.hash

        if not watch:
            return

        time.sleep(10)
