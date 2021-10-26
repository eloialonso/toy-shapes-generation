import numpy as np

from layout import Layout


class SimpleGenerator:
    def __init__(self, size: int, can_overlap: bool, can_rotate: bool, can_go_out: bool, min_size: float, max_size: float) -> None:
        assert 0 <= min_size <= 1 and min_size <= max_size <= 1
        self.image_size = [size, size]
        self.can_overlap = can_overlap
        self.can_rotate = can_rotate
        self.can_go_out = can_go_out 
        self.min_size = int(min_size * min(self.image_size))
        self.max_size = int(max_size * min(self.image_size))
        self.min_pos = 0 if can_go_out else self.max_size
        self.max_pos = min(self.image_size) if can_go_out else min(self.image_size) - self.max_size

    def generate_random_layout(self):
        colors = ["red", "green", "blue"]
        shapes = ["shape.Square", "shape.Circle", "shape.Triangle"]
        np.random.shuffle(colors)
        np.random.shuffle(shapes)
        positions, sizes = sample_n_pos_size(3, self.min_pos, self.max_pos, self.min_size, self.max_size, self.can_overlap)
        # angles = (np.random.rand(3) * (2 * np.pi if self.can_rotate else 0)).tolist()
        angles = (np.random.randint(0, 360, 3) if self.can_rotate else np.zeros(3, dtype=int)).tolist()
        layout = Layout(self.image_size)
        for shape, position, size, angle, color in zip(shapes, positions, sizes, angles, colors):
            layout.add(shape, position, size, angle, color)   
        return layout


def sample_n_pos_size(n, min_pos, max_pos, min_size, max_size, overlap=False):
    sample = lambda n: (min_pos + (max_pos - min_pos) * np.random.rand(n, 2), min_size + (max_size - min_size) * np.random.rand(n))
    sample = lambda n: (np.random.randint(min_pos, max_pos, (n, 2)), np.random.randint(min_size, max_size, n))

    if overlap:
        pos, size = sample(n)
        return pos.tolist(), size.tolist()

    pos, size = np.zeros((n, 2), dtype=int), np.zeros(n, dtype=int)
    i = 0
    while i < n:
        nb_trials = 0
        while True:
            p, s = sample(1)
            pos[i] = p
            size[i] = s
            nb_trials += 1
            if not is_overlap(pos[:i+1].reshape(-1, 2), size[:i+1].reshape(-1, 1)):
                i += 1
                break
            if nb_trials > 100:
                i -= 1
                break

    return pos.tolist(), size.tolist()     
        

def is_overlap(positions, sizes):
    for i, pos in enumerate(positions):
        dist = np.delete(np.sqrt(np.square(positions - pos).sum(1)), i)
        size = np.delete(sizes, i)
        if np.any(dist < size + sizes[i]):
            return True
    return False