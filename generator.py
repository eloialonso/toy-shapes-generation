from functools import partial
from typing import List

import numpy as np
from numpy.random.mtrand import choice

from layout import Layout


class SimpleGenerator:
    def __init__(self, size: int, can_overlap: bool, can_rotate: bool, can_go_out: bool, min_relative_size: float = None, max_relative_size: float = None, possible_relative_sizes: List[float] = None, possible_angles: List[int] = None) -> None:
        self.image_size = [size, size]
        self.can_overlap = can_overlap
        self.can_rotate = can_rotate
        self.can_go_out = can_go_out 
        
        if possible_relative_sizes is None:
            assert min_relative_size is not None and max_relative_size is not None
            assert 0 <= min_relative_size <= 1 and min_relative_size <= max_relative_size <= 1
            min_size = int(min_relative_size * min(self.image_size))
            max_size = int(max_relative_size * min(self.image_size))
            self.possible_sizes = np.arange(min_size, max_size + 1) # [6, 10, 13]
        
        else:
            assert min_relative_size is None and max_relative_size is None
            self.possible_sizes = [int(size * min(self.image_size)) for size in possible_relative_sizes]
            max_size = max(self.possible_sizes)
        
        min_pos = 0 if can_go_out else max_size
        max_pos = min(self.image_size) if can_go_out else min(self.image_size) - max_size
        self.possible_positions = [[x, y] for x in np.arange(min_pos, max_pos) for y in np.arange(min_pos, max_pos)]

        if possible_angles is not None:
            assert can_rotate
            self.possible_angles = possible_angles
        else:
            self.possible_angles = list(range(360)) if can_rotate else [0]

    def generate_random_layout(self):
        colors = ["red", "green", "blue"]
        shapes = ["shape.Square", "shape.Circle", "shape.Triangle"]
        np.random.shuffle(colors)
        np.random.shuffle(shapes)
        
        positions, sizes, angles = sample_shapes_in_choices(3, self.possible_positions, self.possible_sizes, self.possible_angles, self.can_overlap)
        # angles = (np.random.randint(0, 360, 3) if self.can_rotate else np.zeros(3, dtype=int)).tolist()
        
        layout = Layout(self.image_size)
        for shape, position, size, angle, color in zip(shapes, positions, sizes, angles, colors):
            layout.add(shape, position, size, angle, color)   
        
        return layout


# def sample_shapes_in_range(n, min_pos, max_pos, min_size, max_size, can_overlap):
#     if can_overlap:
#         positions = np.random.randint(min_pos, max_pos, (n, 2))
#         sizes = np.random.randint(min_size, max_size, n)
#         return positions.tolist(), sizes.tolist()
    
#     sampler = partial(sample_shapes_in_range, min_pos=min_pos, max_pos=max_pos, min_size=min_size, max_size=max_size, can_overlap=True)
#     return sample_shapes_with_no_overlap(n, sampler)


def sample_shapes_in_choices(n, possible_positions, possible_sizes, possible_angles, can_overlap):
    if can_overlap:
        pos_idxs = np.random.choice(np.arange(len(possible_positions)), n, replace=False)
        positions = np.array(possible_positions)[pos_idxs]
        sizes = np.random.choice(possible_sizes, n, replace=True)
        angles = np.random.choice(possible_angles, n, replace=True)
        return positions.tolist(), sizes.tolist(), angles.tolist()
    sampler = partial(sample_shapes_in_choices, possible_positions=possible_positions, possible_sizes=possible_sizes, possible_angles=possible_angles, can_overlap=True)
    return sample_shapes_with_no_overlap(n, sampler)


def sample_shapes_with_no_overlap(n, sampler):
    positions, sizes, angles = np.zeros((n, 2), dtype=int), np.zeros(n, dtype=int), np.zeros(n, dtype=int)
    i = 0
    while i < n:
        nb_trials = 0
        while True:
            pos, size, angle = sampler(1)
            positions[i] = np.array(pos)
            sizes[i] = np.array(size)
            angles[i] = np.array(angle)
            nb_trials += 1
            if not is_overlap(positions[:i+1].reshape(-1, 2), sizes[:i+1].reshape(-1, 1)):
                i += 1
                break
            if nb_trials > 100:
                i -= 1
                break
    return positions.tolist(), sizes.tolist(), angles.tolist()
     

def is_overlap(positions, sizes):
    for i, pos in enumerate(positions):
        dist = np.delete(np.sqrt(np.square(positions - pos).sum(1)), i)
        size = np.delete(sizes, i)
        if np.any(dist < size + sizes[i]):
            return True
    return False