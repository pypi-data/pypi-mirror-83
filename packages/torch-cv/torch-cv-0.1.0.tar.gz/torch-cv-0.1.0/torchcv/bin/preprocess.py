from torchcv.engine import PREPROCESS_ENGINE
from ..config import read_config


def preprocess(config_path: str, engine: dict = PREPROCESS_ENGINE):
    config = read_config(config_path)

    for function in config:
        if function == "paths":
            continue
        if function in engine.keys():
            preprocessor = engine[function](**config[function])
            print(preprocessor)
            preprocessor()
        else:
            raise NotImplementedError(
                "{} has not been implemented. Available preprocessing functions are {}".format(function, engine.keys())
            )
