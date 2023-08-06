import os
import cv2
import numpy as np
import random


default_dir = "/tmp/torch-cv-test/original_images/"


def create_temp_original():
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)


def create_images():
    for i in range(5):
        dest = os.path.join(default_dir, str(i))
        os.makedirs(dest, exist_ok=True)
        for j in range(10):
            h, w = random.randint(500, 1000), random.randint(500, 1000)
            img_array = np.random.randint(0, 255, size=(h, w, 3))
            cv2.imwrite(os.path.join(dest, f"{i}_{j}.jpg"), img_array)