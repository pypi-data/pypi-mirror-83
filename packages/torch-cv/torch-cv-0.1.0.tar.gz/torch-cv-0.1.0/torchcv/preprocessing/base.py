import os
from typing import AnyStr, Tuple


class BasePreprocessingClass:
    def __init__(self) -> None:
        self.verbose = os.environ["VERBOSE"]

    def __call__(self, *args, **kwargs) -> None:
        raise NotImplementedError("Call function has not been updated yet")

    def __str__(self) -> AnyStr:
        return "Base Preprocessing class"

    def _read_csv(self, path: str):
        import pandas as pd
        return pd.read_csv(path)

    @staticmethod
    def _get_lists(src: str, filetype: str = "jpg") -> Tuple[list, list]:
        import glob
        images, categories = [], []

        for cat in glob.glob(src + "/*"):
            image_list = glob.glob(cat + f"/*.{filetype}")
            cat_list = [os.path.basename(cat)] * len(image_list)

            images += glob.glob(cat + f"/*.{filetype}")
            categories += cat_list

        return images, categories

    @staticmethod
    def _get_max_threads():
        return int(os.popen('grep -c cores /proc/cpuinfo').read())

    def _check_num_threads(self, n: int):
        if n == -1:
            n = self._get_max_threads()
        else:
            assert n <= self._get_max_threads(), "Number of Threads must be less than {}".format(self._get_max_threads())
            assert n > 0, "Number of threads should be at least 1"

        return n
