from dataclasses import dataclass


@dataclass
class Diff:
    img1: str
    img2: str
    conf: float
