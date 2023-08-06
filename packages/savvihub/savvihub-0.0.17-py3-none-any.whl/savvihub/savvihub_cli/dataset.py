import os
from requests_futures.sessions import FuturesSession

import typer

from savvihub.api.savvihub import SavviHubClient
from savvihub.api.uploader import Uploader, Downloader
from savvihub.common.context import Context

dataset_app = typer.Typer()


def parse_dataset_arg(dataset_arg):
    workspace, rest = dataset_arg.split("/")
    if ":" in rest:
        dataset, ref = rest.split(":")
    else:
        dataset = rest
        ref = "latest"
    return workspace, dataset, ref


@dataset_app.callback()
def main():
    return


@dataset_app.command()
def create():
    return


@dataset_app.command()
def push(
    dataset_arg: str = typer.Argument(...),
    root_path_arg: str = typer.Argument("."),
):
    root_path = os.path.abspath(root_path_arg)
    if not os.path.exists(root_path) or not os.path.isdir(root_path):
        typer.echo("Must specify directory as an upload path")
        return

    workspace_slug, dataset_slug, ref = parse_dataset_arg(dataset_arg)
    if ref != "latest":
        typer.echo("Cannot edit dataset snapshot. You should create a new snapshot from latest status.")
        return

    # download file list
    context = Context()
    client = SavviHubClient(token=context.token)
    dataset = client.dataset_read(workspace_slug, dataset_slug)

    files = Uploader.get_files_to_upload(root_path)
    with typer.progressbar(length=len(files)) as progress:
        Uploader.parallel_upload(context, root_path, files, dataset.main_volume_id, log=typer.echo, callback=lambda: progress.update(1))

    typer.echo(f'Uploaded {len(files)} files in {os.path.abspath(root_path)}')


@dataset_app.command()
def pull(
    dataset_arg: str = typer.Argument(...),
    output_path_arg: str = typer.Argument("."),
):
    output_path = os.path.abspath(output_path_arg)
    if os.path.exists(output_path):
        if not os.path.isdir(output_path):
            typer.echo('Must specify directory as an download path')
            return
        if len(os.listdir(output_path)) > 0:
            typer.echo("Must specify empty directory as an output path")
            return
    else:
        os.mkdir(output_path)

    workspace_slug, dataset_slug, ref = parse_dataset_arg(dataset_arg)
    context = Context()

    client = SavviHubClient(token=context.token)
    if ref == 'latest':
        dataset = client.dataset_read(workspace_slug, dataset_slug, raise_error=True)
        files = client.volume_file_list(dataset.main_volume_id, raise_error=True)
    else:
        files = client.dataset_snapshot_file_list(workspace_slug, dataset_slug, ref, raise_error=True)

    with typer.progressbar(length=len(files)) as progress:
        Downloader.parallel_download(context, output_path, files, log=typer.echo, callback=lambda: progress.update(1))

    typer.echo(f'Downloaded {len(files)} files in {output_path}')


if __name__ == "__main__":
    dataset_app()