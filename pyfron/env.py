"""
DIRECTORIES
    --> LFW_DIR: The LFW image base + the provided views. Its structure MUST look like this:

        LFW_DIR
        ├── images
        │   ├── Aaron_Eckhart
        │   ├── Aaron_Guiel
        │   ├── . . .
        │   ├── Zurab_Tsereteli
        │   └── Zydrunas_Ilgauskas
        ├── pairsDevTest.txt
        ├── pairsDevTrain.txt
        ├── pairs.txt
        ├── peopleDevTest.txt
        ├── peopleDevTrain.txt
        └── people.txt

    --> REFERENCE_DB_DIR: This directory will contain the images that the models will train on.

    --> TEST_DIR: This directory SHOULD contain the images that will be used as tests against trained model.

    --> MODELS_DIR: This directory will contain the pretrained models along with their reference-specific weights.

    --> REPORTS_DIR: This directory will contain the auto-generated reports.
"""

import os
from dataclasses import dataclass


# noinspection PyPep8Naming
@dataclass
class Config:
    _ENV: str = ""
    _LFW_DIR: str = "lfw"
    _REFERENCE_DB_DIR: str = "data/reference"
    _TEST_DIR: str = "data/test"
    _MODELS_DIR: str = "models"
    _REPORTS_DIR: str = "reports"

    @property
    def ENV(self):
        return self._ENV

    @property
    def LFW_DIR(self):
        return self._LFW_DIR

    @property
    def REFERENCE_DB_DIR(self):
        return os.path.join(self._ENV, self._REFERENCE_DB_DIR)

    @property
    def TEST_DIR(self):
        return os.path.join(self._ENV, self._TEST_DIR)

    @property
    def MODELS_DIR(self):
        return os.path.join(self._ENV, self._MODELS_DIR)

    @property
    def REPORTS_DIR(self):
        return os.path.join(self._ENV, self._REPORTS_DIR)


def structure(config: Config):
    os.makedirs(config.LFW_DIR, exist_ok=True)
    os.makedirs(os.path.join(config.LFW_DIR, "images"), exist_ok=True)

    os.makedirs(config.REFERENCE_DB_DIR, exist_ok=True)
    os.makedirs(os.path.join(config.REFERENCE_DB_DIR, "images"), exist_ok=True)

    os.makedirs(config.TEST_DIR, exist_ok=True)
    os.makedirs(os.path.join(config.TEST_DIR, "images"), exist_ok=True)

    os.makedirs(config.MODELS_DIR, exist_ok=True)
    os.makedirs(config.REPORTS_DIR, exist_ok=True)


def assertions(config: Config):

    assert os.path.exists(config.LFW_DIR) and \
        "images" in os.listdir(config.LFW_DIR) and \
        len([file for file in os.listdir(config.LFW_DIR) if file.endswith(".txt")]) >= 6, \
        f"Bad structure of LFW_DIR. Please see docstring of {__file__}"

    assert os.path.exists(config.REFERENCE_DB_DIR) and \
        "images" in os.listdir(config.REFERENCE_DB_DIR), \
        f"Bad structure of REFERENCE_DB_DIR. Please see docstring of {__file__}"

    assert os.path.exists(config.TEST_DIR) and \
        "images" in os.listdir(config.TEST_DIR), \
        f"Bad structure of TEST_DIR. Please see docstring of {__file__}"

    assert os.path.exists(config.MODELS_DIR), f"Please create {config.MODELS_DIR} or rename the MODELS_DIR " \
                                              f"in {__file__}"

    assert os.path.exists(config.REPORTS_DIR), f"Please create {config.REPORTS_DIR} or rename the REPORTS_DIR " \
                                               f"in {__file__}"


def configure_env(env) -> Config:
    config = Config(_ENV=env)

    if not os.path.exists(env):
        structure(config)

    while True:
        try:
            assertions(config)
            break
        except AssertionError as error:
            print(error)
            input("Commit changes and press <enter> to re-try")

    print("Environment was configured successfully!")
    print("--> You should now manually copy images to the appropriate directories.")
    return config
