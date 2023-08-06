import os

from .preprocess import preprocess

CONFIG = os.environ["CONFIG"]
VERBOSE = os.environ["VERBOSE"]
FUNCTION = os.environ["FUNCTION"]


def call():
    if FUNCTION == "preprocess":
        preprocess(CONFIG)


if __name__ == '__main__':
    call()
