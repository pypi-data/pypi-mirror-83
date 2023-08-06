from subprocess import call

from .data.create_images import create_images
from .data.create_configs import create_preprocess_config

create_images()
create_preprocess_config()

CMD = "/tmp/.tox/python/bin/tcv"
CONFIG = "/tmp/torch-cv-test/config/preprocess.yml"


def test_preprocess():
    code = call(["sh", CMD, f"--config={CONFIG}", "--function=preprocess"])
    assert code == 0

