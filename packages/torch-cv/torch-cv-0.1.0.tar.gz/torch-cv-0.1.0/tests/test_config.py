import pytest

from torchcv.config import read_config
from .data.create_configs import *

CONFIG_DIR = "/tmp/torch-cv-test/config/"
create_empty_config()
create_none_config()
create_join_config()


@pytest.mark.xfail
def test_raise_exception_when_file_is_empty():
    read_config(os.path.join(CONFIG_DIR, "empty.yml"))


def test_none_constructor():
    config = read_config(os.path.join(CONFIG_DIR, "none.yml"))
    assert config.field0 is None


def test_join_constructor():
    config = read_config(os.path.join(CONFIG_DIR, "join.yml"))
    assert config.field0 == 'a/b/c'
