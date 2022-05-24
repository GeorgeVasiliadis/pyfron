import os
import shutil
from typing import List
from typing import Tuple

from .env import Config

#
# def assert_image_dir(path):
#     assert os.path.exists(path), f"ImageDir {path} doesn't exist"
#     assert os.path.isdir(path), f"{path} is not a valid directory"
#     assert "images" in os.listdir(path), f"{path} MUST contain 'images' subdirectory"


def parse_people_dev_train(config: Config) -> List[Tuple[str, str]]:
    people_dev_train_file = os.path.join(config.LFW_DIR, "peopleDevTest.txt")

    with open(people_dev_train_file, "r") as people_file:
        no_people = int(people_file.readline().strip())
        people = []
        for line in people_file.readlines():
            name, count = tuple(line.split())
            people.append((name, count))
    assert len(people) == no_people, "An error occurred while parsing the people-dev-train file"
    return people


def parse_image_dir(image_dir) -> List[Tuple[str, str]]:
    info = []
    for dir_name in os.listdir(image_dir):
        files = os.listdir(os.path.join(image_dir, dir_name))
        files = list(filter(lambda x: x.endswith(".jpg"), files))
        size = len(files)
        info.append((dir_name, str(size)))
    return info


def populate_image_dir(from_image_dir: str, to_image_dir: str, min_samples_per_person=3, max_people=100):
    people = parse_image_dir(from_image_dir)

    # Keep only people with more than `min_samples_per_person` images
    people = list(filter(lambda x: int(x[1]) >= min_samples_per_person, people))

    # Keep the first `max_people` people
    people = people[:max_people]

    last_dir = len(os.listdir(to_image_dir))
    for p_id, (person, _) in enumerate(people, last_dir + 1):
        to_dir = os.path.join(to_image_dir, str(p_id))
        os.makedirs(to_dir, exist_ok=True)

        for image in os.listdir(os.path.join(from_image_dir, person)):
            from_path = os.path.join(from_image_dir, person, image)
            to_path = os.path.join(to_dir, image)

            shutil.copy2(from_path, to_path)
            print(f"{from_path}  -->  {to_path}")