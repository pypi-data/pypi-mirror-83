import os
import requests
import yaml

from savvihub.api.types import SavviHubUser
from savvihub.common.constants import DEFAULT_CONFIG_PATH, CUR_DIR, DEFAULT_SAVVIHUBFILE_YAML
from savvihub.common.experiment import Experiment


class Value:
    def __init__(self, global_config_yml=None, savvihub_file_yml=None, env=None, computed=None, default_value=None):
        self.global_config_yml = global_config_yml
        self.savvihub_file_yml = savvihub_file_yml
        self.env = env
        self.computed = computed
        self.default_value = default_value


def get_experiment(token=None, **kwargs):
    if not token:
        return

    from savvihub.api.savvihub import SavviHubClient
    client = SavviHubClient(token=token)

    try:
        savvihub_experiment = client.experiment_read(raise_error=True)
    except requests.exceptions.HTTPError as e:
        print(f"Http Error: {e}")
        return
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error:{e}")
        return
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
        return
    except requests.exceptions.TooManyRedirects as e:
        print(f"Too many Redirects Error: {e}")
        return
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    from savvihub.common.experiment import Experiment
    return Experiment.from_given(savvihub_experiment, client)


def get_my_info(token=None, **kwargs):
    from savvihub.api.savvihub import SavviHubClient
    client = SavviHubClient(token=token)
    return client.get_my_info()


class Context:
    token = Value(global_config_yml=".token", env="EXPERIMENT_ACCESS_TOKEN", default_value=None)
    parallel = Value(env="PARALLEL", default_value=20)
    workspace = Value(savvihub_file_yml=".workspace")
    project = Value(savvihub_file_yml=".project")

    me: SavviHubUser = Value(computed=get_my_info)
    experiment: Experiment = Value(computed=get_experiment)

    def __init__(self, login_required=False, experiment_required=False, savvihub_filename=DEFAULT_SAVVIHUBFILE_YAML):
        attrs = dict()
        for key in dir(self):
            attr = getattr(self, key)
            if isinstance(attr, Value):
                attrs[key] = attr

        data = dict()

        global_config = self.load_global_config_file()

        savvihub_filename = os.path.join(CUR_DIR, savvihub_filename)
        savvihub_yml_config = self.load_experiment_config_file(savvihub_filename)

        for key, attr in attrs.items():
            # Set default value
            data[key] = attr.default_value

            # Load from file
            if attr.global_config_yml and global_config:
                value = global_config.get(attr.global_config_yml, None)
                if value is not None:
                    data[key] = value

            if attr.savvihub_file_yml and savvihub_yml_config:
                value = savvihub_yml_config.get(attr.savvihub_file_yml, None)
                if value is not None:
                    data[key] = value

            # Load from env
            if attr.env:
                value = os.environ.get(attr.env, None)
                if value is not None:
                    data[key] = value

        # calculate computed
        for key, attr in attrs.items():
            if attr.computed:
                value = attr.computed(**data)
                if value:
                    data[key] = value

        for k, v in data.items():
            setattr(self, k, v)

        if login_required and self.me is None:
            if self.token:
                raise Exception('Login required. You should call `savvi init` first.')
            else:
                raise Exception('Token expired. You should call `savvi init` first.')

        if experiment_required and self.experiment is None:
            raise Exception('Experiment token required.')

    @staticmethod
    def load_global_config_file():
        try:
            with open(DEFAULT_CONFIG_PATH, "r") as f:
                global_config = yaml.full_load(f)
                if global_config:
                    return global_config
        except FileNotFoundError:
            return

    @staticmethod
    def load_experiment_config_file(experiment_yml):
        try:
            if not experiment_yml:
                return
            with open(experiment_yml, "r") as f:
                experiment_config = yaml.full_load(f)
                if experiment_config:
                    return experiment_config
        except FileNotFoundError:
            return
