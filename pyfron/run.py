import os
from typing import List

from opendr.engine.data import Image

from .env import Config
from .recognizers import recognizer_factory
from .structures import Diff
from .reports import Generator


def discover_images(image_dir) -> List[str]:
    paths = []
    people = os.listdir(image_dir)
    for person in people:
        cwd = os.path.join(image_dir, person)
        new_paths = [os.path.abspath(os.path.join(cwd, img)) for img in os.listdir(cwd)]
        paths.extend(new_paths)
    return paths


def id_to_path(reference_dir, person_id: str):
    person_dir = os.path.join(reference_dir, person_id)
    if os.path.exists(person_dir):
        img = os.listdir(person_dir)[0]
        img = os.path.join(person_dir, img)
        img = os.path.abspath(img)
    else:
        img = person_id
    return img


def test_recognizer(reference_dir, test_dir, recognizer) -> List[Diff]:
    diff_list = []
    paths = discover_images(test_dir)
    for path in paths:
        img = Image.open(path)
        res = recognizer.infer(img)
        img2 = id_to_path(reference_dir, res.description)
        conf = res.confidence
        diff = Diff(path, img2, conf)
        diff_list.append(diff)
    return diff_list


def run(config: Config, model_id: str = ""):
    reference_images_dir = os.path.join(config.REFERENCE_DB_DIR, "images")
    test_images_dir = os.path.join(config.TEST_DIR)

    if not os.listdir(test_images_dir):
        print("There are no test images")
        print("Aborting...")
        exit()

    print("Loading recognizer...")
    recognizer = recognizer_factory(config, model_id)

    print("Testing recognizer...")
    diffs = test_recognizer(reference_images_dir, test_images_dir, recognizer)

    print("Generating report...")
    generator = Generator(config.REPORTS_DIR, title=model_id)
    generator.auto(sorted(diffs, key=lambda x: x.conf, reverse=True))

