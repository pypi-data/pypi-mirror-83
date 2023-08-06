import yaml
import os

import pkgutil


def load_config():
    # load default config
    default_config = _load_default_config()

    # load user config
    config = _load_user_config()

    # merge config
    return _merge_config(config, default_config)


def _load_user_config():
    home = os.environ['HOME']
    CONFIG_FILE = os.path.join(home, '.jupyterflow.yaml')
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return yaml.safe_load(f)
    return {}



def _load_default_config():
    data = pkgutil.get_data(__name__, "templates/default_config.yaml")
    return yaml.safe_load(data)


def _merge_config(config, default):
    default.update(config)
    return default