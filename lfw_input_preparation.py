"""This module defines scripts to automate the preparation of lfw image-folder structures that will be used by OpenDR.

In order to avoid deleting or overwriting existing directories, this module requires pre-cleaned environments. This
means that the user should manually delete any directory that is ment to be created by the script, before the execution.

Globals:
    LFW_DIR: Relative path of LFW dataset. This directory should contain directly the 5749 directories of LFW people
    TARGET_TRAIN_DIR: Relative path of the image-folder for the train data
    TARGET_TEST_DIR: Relative path of the image-folder for the test data
"""

import os
import shutil

from config import LFW_DIR
from config import TRAIN_DIR
from config import TEST_DIR


TARGET_TRAIN_DIR = TRAIN_DIR
TARGET_TEST_DIR = TEST_DIR

# assert os.path.isdir(LFW_DIR), "Please define the LFW directory first"
# assert not os.path.exists(TARGET_TRAIN_DIR), "The specified directory exists. Please remove it manually and re-run."
# assert not os.path.exists(TARGET_TEST_DIR), "The specified directory exists. Please remove it manually and re-run."

# Ideally those paths should not change
FINAL_TARGET_TRAIN_DIR = os.path.join(TARGET_TRAIN_DIR, "images")
FINAL_TARGET_TEST_DIR = os.path.join(TARGET_TEST_DIR, "images")
_PEOPLE_FILE = "data/lfw/people.txt"
_PAIRS_FILE = "data/lfw/pairs.txt"
_PEOPLE_DEV_TEST_FILE = "data/lfw/peopleDevTest.txt"
_PEOPLE_DEV_TRAIN_FILE = "data/lfw/peopleDevTrain.txt"
_PAIRS_DEV_TEST_FILE = "data/lfw/pairsDevTest.txt"
_PAIRS_DEV_TRAIN_FILE = "data/lfw/pairsDevTrain.txt"

os.makedirs(TARGET_TRAIN_DIR, exist_ok=True)
os.makedirs(TARGET_TEST_DIR, exist_ok=True)


def parse_people_dev_train():
    with open(_PEOPLE_DEV_TRAIN_FILE, "r") as people_file:
        no_people = int(people_file.readline().strip())
        people = [tuple(line.split()) for line in people_file.readlines()]
    assert len(people) == no_people, "An error occurred while parsing the people-dev-train file"
    return people


def generate_train_input(min_samples_per_person=3, max_people=100):
    people = parse_people_dev_train()

    # Keep only people with more than `min_samples_per_person` images
    people = list(filter(lambda x: int(x[1]) >= min_samples_per_person, people))

    if len(people) > max_people:
        # Keep the first `max_people` people
        people = people[:max_people]

    for p_id, person in enumerate(people, 1):
        to_dir = os.path.join(FINAL_TARGET_TRAIN_DIR, str(p_id))
        os.makedirs(to_dir, exist_ok=True)

        for i in range(1, int(person[1])+1):
            img_name = f"{person[0]}_{i:0>4}.jpg"
            from_path = os.path.join(LFW_DIR, person[0], img_name)
            to_path = os.path.join(to_dir, img_name)

            shutil.copy2(from_path, to_path)
            print(f"{from_path}  -->  {to_path}")


if __name__ == "__main__":
    generate_train_input()
