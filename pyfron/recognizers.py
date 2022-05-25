import os
import json

from opendr.perception.face_recognition import FaceRecognitionLearner

from .env import Config

models = {
    "mobilefacenet": {
        "backbone": "mobilefacenet",
        "mode": "backbone_only",
        "device": "cpu",
        "batch_size": 10
    },

    "ir_50": {
        "backbone": "ir_50",
        "mode": "backbone_only",
        "device": "cpu",
        "batch_size": 10
    },

    "exp1": {
        "backbone": "mobilefacenet",
        "network_head": "am_softmax",
        "mode": "backbone_only",
        "device": "cpu",
        "batch_size": 10
    },

    "exp2": {
        "backbone": "mobilefacenet",
        "network_head": "classifier",
        "mode": "backbone_only",
        "device": "cpu",
        "batch_size": 10
    },

    "exp3": {
            "backbone": "ir_50",
            "network_head": "sphereface",
            "mode": "backbone_only",
            "device": "cpu",
            "batch_size": 10
        }
}


def print_available_recognizers():
    print("--- Available Models ---")
    print(json.dumps(models, indent=4))
    print(f"Consider registering a new model by manually editing {__file__}:models dictionary.")


def recognizer_factory(config: Config, model_id: str = ""):

    default = "mobilefacenet"
    model_id = model_id or default

    if model_id not in models:
        print(f"The specified model '{model_id}' is not registered in {__file__}. Default model is used instead.")
        model_id = default

    recognizer = FaceRecognitionLearner(**models[model_id])

    recognizer.download(config.MODELS_DIR)
    recognizer.load(config.MODELS_DIR)
    save_path = os.path.join(config.MODELS_DIR, model_id)
    recognizer.fit_reference(config.REFERENCE_DB_DIR, save_path=save_path)
    return recognizer
