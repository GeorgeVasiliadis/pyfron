import os
from dataclasses import dataclass


# noinspection PyPep8Naming
@dataclass
class Config:
    _ENV: str = ""
    _REFERENCE_DB_DIR: str = "data/reference"
    _TEST_DIR: str = "data/test"
    _MODELS_DIR: str = "models"
    _REPORTS_DIR: str = "reports"

    @property
    def ENV(self):
        return self._ENV

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
    os.makedirs(config.REFERENCE_DB_DIR, exist_ok=True)
    os.makedirs(os.path.join(config.REFERENCE_DB_DIR, "images"), exist_ok=True)

    os.makedirs(config.TEST_DIR, exist_ok=True)

    os.makedirs(config.MODELS_DIR, exist_ok=True)
    os.makedirs(config.REPORTS_DIR, exist_ok=True)


def assertions(config: Config):
    assert os.path.exists(config.REFERENCE_DB_DIR) and \
        "images" in os.listdir(config.REFERENCE_DB_DIR), \
        f"Bad structure of REFERENCE_DB_DIR. Please see {__file__}"

    assert os.path.exists(config.TEST_DIR), \
        f"Bad structure of TEST_DIR. Please see {__file__}"

    assert os.path.exists(config.MODELS_DIR),\
        f"Please create {config.MODELS_DIR} or rename the MODELS_DIR in {__file__}"

    assert os.path.exists(config.REPORTS_DIR), \
        f"Please create {config.REPORTS_DIR} or rename the REPORTS_DIR in {__file__}"


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

    return config
