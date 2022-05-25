import os
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ImageDir:
    path: str
    extensions: Tuple[str] = (".jpg", ".jpeg")

    @property
    def contents(self) -> List[str]:
        files_of_interest = []
        for content in os.listdir(self.path):
            content = os.path.join(self.path, content)
            if os.path.isfile(content):
                for extension in self.extensions:
                    if content.lower().endswith(extension):
                        files_of_interest.append(content)
        return files_of_interest

    def __len__(self):
        return len(self.contents)

    def __str__(self):
        return str(self.contents)

    def __bool__(self):
        return bool(self.contents)


@dataclass
class ImageBase:
    path: str

    @property
    def contents(self) -> List[ImageDir]:
        person_dir_list = []
        for content in os.listdir(self.path):
            content = os.path.join(self.path, content)
            if os.path.isdir(content):
                person_dir_list.append(ImageDir(content))
        return person_dir_list

    def __len__(self):
        return len(self.contents)

    def __str__(self):
        dirs = [image_dir.path for image_dir in self.contents]
        return str(dirs)

    def __bool__(self):
        return bool(self.contents)


@dataclass
class Diff:
    img: str                # Path of the base image that has been tested
    reference_img: str      # Path of a reference image that is similar to the base image
    conf: float             # The confidence of similarity between base and reference images
