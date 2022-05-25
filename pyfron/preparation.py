import os
import shutil
from typing import List

from .structures import ImageDir
from .structures import ImageBase


def find_image_dirs(path) -> List[ImageDir]:
    image_base = ImageBase(path)

    if image_base:
        image_dirs = image_base.contents.copy()
    else:
        image_dirs = [ImageDir(path)]
    return image_dirs


def populate_image_dir(from_path: str, to_path: str):
    image_dirs = find_image_dirs(from_path)

    if not image_dirs:
        print(f"Couldn't find any ImageDir at {from_path}")
        return

    # Retrieved stored ImageBase
    image_base = ImageBase(to_path)
    starting_num = len(image_base) + 1

    for dir_num, image_dir in enumerate(image_dirs, starting_num):
        new_dir = os.path.join(image_base.path, str(dir_num))
        os.makedirs(new_dir, exist_ok=True)

        for image in image_dir.contents:
            shutil.copy2(image, new_dir)
            print(f"{image}  -->  {new_dir}")
