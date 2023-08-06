import sys
from pathlib import Path, PosixPath
from typing import Dict

from ruamel.yaml import YAML

from cognite.airworkflow.util import env


def load_yaml(path: Path) -> Dict:
    yaml = YAML(typ="safe").load(path)
    assert isinstance(yaml, dict)
    return yaml


def get_url_dict() -> Dict:
    working_path = env.get_env_value("PWD")
    ROOT_DIR = PosixPath(working_path)
    config_path = ROOT_DIR / "repoconfig.yaml"
    yamlload = load_yaml(config_path)
    try:
        urldict = yamlload["Projectproperties"]["projecturl"]
        filtered_dict = {k: v for k, v in urldict.items() if v}
        return filtered_dict
    except KeyError:
        sys.exit(1)
