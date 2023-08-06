import os

import yaml

from ._utils import DotDict


def _none_constructor(loader, node):
    return None


def _join_constructor(loader, node):
    fields = loader.construct_sequence(node)
    return os.path.join(*fields)


def read_config(yaml_path: str) -> DotDict:
    yaml_path = os.path.abspath(yaml_path)

    yaml.add_constructor("!none", _none_constructor)
    yaml.add_constructor("!join", _join_constructor)

    with open(yaml_path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    if config is None:
        raise ValueError("Config file cannot be empty")

    return DotDict(config)
