import os

from opendr.engine.data import Image
from opendr.engine.datasets import ExternalDataset
from opendr.perception.face_recognition import FaceRecognitionLearner

from config import TRAIN_DIR
from config import TEST_DIR
from config import PRETRAINED_MODEL_DIR
from config import LFW_DIR
from models import Diff
from md_generator import Generator
from lfw_input_preparation import FINAL_TARGET_TRAIN_DIR


def discover_image_paths(root):
    root = os.path.join(root, "images")
    assert os.path.exists(root), "Couldn't find `images` directory"
    paths = []
    people = os.listdir(root)
    for person in people:
        cwd = os.path.join(root, person)
        new_paths = [os.path.abspath(os.path.join(cwd, img)) for img in os.listdir(cwd)]
        paths.extend(new_paths)
    return paths


def id_to_path(person_id: str):
    person_dir = os.path.join(FINAL_TARGET_TRAIN_DIR, person_id)
    if os.path.exists(person_dir):
        img = os.listdir(person_dir)[0]
        img = os.path.join(FINAL_TARGET_TRAIN_DIR, person_id, img)
        img = os.path.abspath(img)
    else:
        img = person_id
    return img


def test_recognizer(recognizer):
    diff_list = []
    paths = discover_image_paths(TEST_DIR)
    for path in paths:
        img = Image.open(path)
        res = recognizer.infer(img)
        img2 = id_to_path(res.description)
        conf = res.confidence
        diff = Diff(path, img2, conf)
        diff_list.append(diff)
    return diff_list


def recognizer_factory():
    recognizer = FaceRecognitionLearner(
                                        backbone='mobilefacenet',
                                        mode='backbone_only',
                                        device='cpu',
                                        batch_size=10)

    # recognizer.download(PRETRAINED_MODEL_DIR)
    recognizer.load(PRETRAINED_MODEL_DIR)
    recognizer.fit_reference(TRAIN_DIR, save_path=PRETRAINED_MODEL_DIR)
    return recognizer


r = recognizer_factory()
diffs = test_recognizer(r)

generator = Generator("5")
generator.auto(diffs)
