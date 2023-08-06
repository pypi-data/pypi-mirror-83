import os

import pandas as pd
from joblib import dump

from .base import BasePreprocessingClass


class CreateLabelMap(BasePreprocessingClass):
    def __init__(self, src: str, dest: str, target: str = "class"):
        super().__init__()
        self.dest = dest

        self.df = self._read_csv(src)
        self.label_list = self.df[target].unique()

    def __call__(self, *args, **kwargs):
        import time
        start = time.time()

        os.makedirs(self.dest, exist_ok=True)

        label_map = {}
        for i, label in enumerate(self.label_list):
            label_map[label] = i

        dump(label_map, os.path.join(self.dest, "label_map.pkl"))

        print("Time taken = {:0.3f}s\n".format(time.time() - start))

    def __str__(self):
        return "Saving label map to - {}".format(self.dest)
