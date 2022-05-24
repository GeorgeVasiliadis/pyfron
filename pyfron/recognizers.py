import os

from opendr.perception.face_recognition import FaceRecognitionLearner

from .env import Config

models = [
    {}
]


def recognizer_factory(config: Config, model_id: int = 0):

    kwargs = {}
    if model_id < len(models):
        kwargs = models[model_id]

    recognizer = FaceRecognitionLearner(
                                        backbone='mobilefacenet',
                                        mode='backbone_only',
                                        device='cpu',
                                        batch_size=10,
                                        **kwargs
    )

    recognizer.download(config.MODELS_DIR)
    recognizer.load(config.MODELS_DIR)
    save_path = os.path.join(config.MODELS_DIR, str(model_id))
    recognizer.fit_reference(config.REFERENCE_DB_DIR, save_path=save_path)
    return recognizer
