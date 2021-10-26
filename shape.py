from typing import List

import matplotlib.patches as patches
import numpy as np


class Shape:
    def __init__(self, position: List[float], size: float, angle: float, color: str) -> None:
        self.position = np.array(position)
        self.size = size
        self.angle = angle * np.pi / 180
        self.color = color
    
    def draw(self) -> patches.Patch:
        raise NotImplementedError


class Circle(Shape):
    def __init__(self, position, size, angle, color) -> None:
        super().__init__(position, size, angle, color)
    
    def draw(self) -> patches.Patch:
        return patches.Circle(self.position, radius=self.size, color=self.color)


class Square(Shape):
    def __init__(self, position, size, color, angle) -> None:
        super().__init__(position, size, angle, color)
    
    def draw(self) -> patches.Patch:
        angles = np.pi / 4 + np.pi / 2 * np.arange(4) + self.angle
        pts = np.array(list(map(lambda a: [np.cos(a), np.sin(a)], angles)))
        pts = self.position + self.size * pts
        return patches.Polygon(pts, closed=False, color=self.color)


class Triangle(Shape):
    def __init__(self, position, size, color, angle) -> None:
        super().__init__(position, size, angle, color)
        
    def draw(self) -> patches.Patch:
        angles = np.array([0, 2 * np.pi / 3, - 2 * np.pi / 3]) + self.angle
        pts = np.array(list(map(lambda a: [np.cos(a), np.sin(a)], angles)))
        pts = self.position + self.size * pts
        return patches.Polygon(pts, closed=False, color=self.color)
