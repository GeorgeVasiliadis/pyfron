from dataclasses import dataclass


@dataclass
class Diff:
    img: str                # Path of the base image that has been tested
    reference_img: str      # Path of a reference image that is similar to the base image
    conf: float             # The confidence of similarity between base and reference images
