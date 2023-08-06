from datetime import datetime

import typer
from terminaltables import AsciiTable
import inquirer

from savvihub.common.context import Context
from savvihub.savvihub_cli.inquirer import get_choices, parse_id
from savvihub.api.savvihub import SavviHubClient
from savvihub.common.constants import CUR_DIR, INQUIRER_NAME_IMAGE, INQUIRER_NAME_RESOURCE, \
    INQUIRER_NAME_COMMAND, WEB_HOST, INQUIRER_NAME_DATASET, INQUIRER_NAME_DATASET_REF, \
    INQUIRER_NAME_DATASET_MOUNT_PATH, DEFAULT_SAVVIHUBFILE_YAML
from savvihub.savvihub_cli.errors import get_error_message
from savvihub.common.utils import *
from savvihub.savvihub_cli.yml_loader import ExperimentYmlLoader

experiment_app = typer.Typer()


@experiment_app.callback()
def main():
    """
    Perform your experiment with Savvihub
    """
    return


@experiment_app.command()
def init(
    slug: str = typer.Argument(..., help="Type workspace/project as an argument"),
    file: str = typer.Option(DEFAULT_SAVVIHUBFILE_YAML, "--file", "-f"),
):
    """
    Initialize a new experiment configuration file with workspace/project
    """
    # Remove old config file if exists
    config_file_path = os.path.join(CUR_DIR, file)
    remove_file(config_file_path)

    workspace_slug, project_slug = slug.split("/")
    context = Context(login_required=True)
    client = SavviHubClient(token=context.token)

    workspace = client.workspace_read(workspace_slug)
    if workspace is None:
        typer.echo(f'Cannot find workspace {workspace}.')
        return

    project = client.project_read(workspace_slug, project_slug)
    if project is None:
        owner, repo = get_github_repo()
        create_new_project = typer.prompt(f'Create new project with github.com/{owner}/{repo}? [Y/n] ')
        if create_new_project.lower().strip().startswith('y'):
            if not context.me.github_authorized:
                typer.echo(f'You should authorize github first.\nhttp://{WEB_HOST}/github/authorize/')
                return
            client.project_github_create(workspace_slug, project_slug, owner, repo, raise_error=True)
            typer.echo(f'Project created successfully.\nhttp://{WEB_HOST}/{workspace_slug}/{project_slug}')

    data = {
        'workspace': workspace_slug,
        'project': project_slug,
    }

    make_file(config_file_path)
    yml_loader = ExperimentYmlLoader(config_file_path)
    yml_loader.write(data)

    typer.echo(f"Experiment config successfully made in {config_file_path}")


@experiment_app.command()
def data_mount(
    file: str = typer.Option(DEFAULT_SAVVIHUBFILE_YAML, "--file", "-f"),
):
    """
    Mount data to experiment
    """
    config_file_path = os.path.join(CUR_DIR, file)
    if not os.path.exists(config_file_path):
        raise Exception('Initialize experiment with this command: $ savvi experiment init SLUG')

    context = Context(savvihub_filename=file)
    client = SavviHubClient(token=context.token)

    yml_loader = ExperimentYmlLoader(file)

    questions = [
        inquirer.List(
            INQUIRER_NAME_DATASET,
            message="Please choose a dataset",
            choices=get_choices(client, 'dataset', yml_loader),
        ),
        inquirer.Text(
            INQUIRER_NAME_DATASET_REF,
            message="Dataset ref",
            default=yml_loader.data.get('dataset_mount_ref', 'latest'),
        ),
        inquirer.Text(
            INQUIRER_NAME_DATASET_MOUNT_PATH,
            message="Dataset mount path",
            default=yml_loader.data.get('dataset_mount_path', 'input'),
        ),
    ]

    answers = inquirer.prompt(questions)
    dataset_mount_id = parse_id(answers.get(INQUIRER_NAME_DATASET))

    yml_loader.update_and_write({
        'data_mount_infos': {
            'id': dataset_mount_id,
            'ref': answers.get(INQUIRER_NAME_DATASET_REF),
            'mount_path': answers.get(INQUIRER_NAME_DATASET_MOUNT_PATH),
        }
    })


@experiment_app.command()
def list(
        file: str = typer.Option(DEFAULT_SAVVIHUBFILE_YAML, "--file", "-f"),
):
    """
    List of experiments
    """
    context = Context(file)
    client = SavviHubClient(token=context.token)
    yml_loader = ExperimentYmlLoader(file)

    workspace = yml_loader.data.get('workspace')
    project = yml_loader.data.get('project')

    experiments = client.experiment_list(workspace, project, raise_error=True)
    table = AsciiTable([
        ['Number', 'Status', 'Message'],
        *[[e.number, e.status, e.message] for e in experiments],
    ])
    typer.echo(table.table)


@experiment_app.command()
def log(
    file: str = typer.Option(DEFAULT_SAVVIHUBFILE_YAML, "--file", "-f"),
    experiment_number: int = typer.Argument(...),
):
    """
    View experiment logs
    """
    context = Context()
    client = SavviHubClient(token=context.token)
    yml_loader = ExperimentYmlLoader(file)

    workspace = yml_loader.data.get('workspace')
    project = yml_loader.data.get('project')

    logs = client.experiment_log(workspace, project, experiment_number, raise_error=True)
    for log in logs:
        print(datetime.fromtimestamp(log.timestamp), log.message)


@experiment_app.command()
def run(
    file: str = typer.Option(DEFAULT_SAVVIHUBFILE_YAML, "--file", "-f"),
    command: str = typer.Option(None, "-c")
):
    """
    Run an experiment in Savvihub
    """
    if not is_committed():
        raise Exception('You should commit diffs before run an experiment!')

    config_file_path = os.path.join(CUR_DIR, file)
    if not os.path.exists(config_file_path):
        raise Exception('Initialize experiment with this command: $ savvi experiment init SLUG')

    context = Context()
    client = SavviHubClient(token=context.token)

    yml_loader = ExperimentYmlLoader(file)

    questions = [
        inquirer.List(
            INQUIRER_NAME_IMAGE,
            message="Please choose a kernel image",
            choices=get_choices(client, 'image', yml_loader),
        ),
        inquirer.List(
            INQUIRER_NAME_RESOURCE,
            message="Please choose a kernel resource",
            choices=get_choices(client, 'resource', yml_loader),
        ),
    ]
    if not command:
        questions.append(
            inquirer.Text(
                INQUIRER_NAME_COMMAND,
                message="Start command",
                default="python main.py",
            )
        )

    answers = inquirer.prompt(questions)
    image_id = parse_id(answers.get(INQUIRER_NAME_IMAGE))
    resource_spec_id = parse_id(answers.get(INQUIRER_NAME_RESOURCE))

    if not command:
        command = answers.get(INQUIRER_NAME_COMMAND)

    yml_loader.update_and_write({
        'image_id': image_id,
        'resource_spec_id': resource_spec_id,
        'start_command': command,
    })

    res = client.experiment_create(
        workspace=yml_loader.data.get('workspace'),
        project=yml_loader.data.get('project'),
        image_id=int(yml_loader.data.get('image_id')),
        resource_spec_id=int(yml_loader.data.get('resource_spec_id')),
        branch=get_git_revision_hash(),
        dataset_mount_infos=[{
            'id': int(dataset_mount_info.get('id')),
            'ref': dataset_mount_info.get('ref'),
            'mount_path': dataset_mount_info.get('mount_path'),
        } for dataset_mount_info in (yml_loader.data.get('data_mount_infos') or [])],
        start_command=yml_loader.data.get('start_command'),
    )

    res_data = res.json()
    if res.status_code == 400:
        typer.echo(get_error_message(res_data))
        return
    res.raise_for_status()

    experiment_number = res_data.get('number')
    typer.echo(f"Experiment {experiment_number} is running. Check the experiment status at below link")
    typer.echo(f"{WEB_HOST}/{yml_loader.data.get('workspace')}/{yml_loader.data.get('project')}/"
               f"experiments/{experiment_number}")
    return


if __name__ == "__main__":
    experiment_app()
