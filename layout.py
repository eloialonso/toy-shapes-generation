from pathlib import Path
from typing import List

import hydra
import matplotlib.pyplot as plt
import numpy as np
import yaml


class Layout:
    def __init__(self, image_size: int) -> None:
        self.image_size = image_size
        self.shapes = []
    
    def add(self, target: str, position: List[int], size: int, angle: int, color: str) -> None:
        shape = {
            "_target_": target,
            "position": position,
            "size": size,
            "angle": angle,
            "color": color,
        }
        self.shapes.append(shape)

    def dump(self, filename: Path = None) -> None:
        todump = {
            "image_size": list(self.image_size),
            "shapes": self.shapes
        }
        if filename is None:
            return yaml.dump(todump) 
        with filename.open('w') as f:
            yaml.dump(todump, f)
    
    def load(self, filename: Path) -> None:
        with filename.open('r') as f:
            loaded_yaml = yaml.load(f, yaml.Loader)
        self.image_size = loaded_yaml["image_size"]
        self.shapes = loaded_yaml["shapes"]

    def build(self):
        for shape in self.shapes:
            yield hydra.utils.instantiate(shape)
    
    def savefig(self, filename: Path):
        plt.figure(figsize=(self.image_size[0] + 1, self.image_size[1] + 1), dpi=1)
        ax = plt.gca()
        plt.axis("off")
        ax.imshow(np.ones((self.image_size[0], self.image_size[1], 3)))
        for shape in self.build():
            ax.add_patch(shape.draw())
        plt.tight_layout()
        plt.savefig(filename, bbox_inches="tight", pad_inches=0, dpi=1)
        plt.close()
