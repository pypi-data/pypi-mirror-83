import glob
import os
from typing import List

import cv2
from torch.utils.data import DataLoader, Dataset

from .base import BasePreprocessingClass


class ResizeHelper(Dataset):
    def __init__(self, images: List[str], dest: str, size: int = 224) -> None:
        super(ResizeHelper, self).__init__()

        self.dest = dest
        self.size = size
        self.images = images

    def __getitem__(self, item):
        image = self.images[item]
        category = os.path.basename(os.path.dirname(image))
        os.makedirs(os.path.join(self.dest, category), exist_ok=True)

        self._resize(image, category, size=self.size)

        return image

    def __len__(self):
        return len(self.images)

    def _resize(self, image: str, category: str, size: int = 224):
        image = os.path.abspath(image)
        file_name = os.path.basename(image)
        dest_path = os.path.join(self.dest, category, file_name)

        image = cv2.imread(image)
        image = cv2.resize(image, (size, size))

        cv2.imwrite(dest_path, image)


class ResizeImages(BasePreprocessingClass):
    def __init__(self, src: str, dest: str, size: int = 224, filetype: str = "jpg", num_workers: int = 1,
                 batch_size: int = 32):
        super(ResizeImages, self).__init__()

        num_workers = self._check_num_threads(num_workers)
        images, _ = self._get_lists(src, filetype)

        self.dest = dest
        self.ds = ResizeHelper(images, dest, size)
        self.dl = DataLoader(self.ds, batch_size=batch_size, num_workers=num_workers)

    def __call__(self, ):
        import time
        start = time.time()

        for _ in enumerate(self.dl):
            continue

        print("Time taken = {:0.3f}s\n".format(time.time() - start))

    def __str__(self):
        return "Resizing images to size - {} at {}".format(self.ds.size, self.dest)
