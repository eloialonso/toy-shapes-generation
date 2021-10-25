import argparse

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from tqdm import tqdm


def main():
    args = parse_args()   
    can_overlap = False
    can_go_out = False
    can_rotate = False

    im_size = (256, 256)
    min_size = 0.1 * min(im_size)
    max_size = 0.3 * min(im_size)
    min_pos = 0 if can_go_out else max_size
    max_pos = min(im_size) if can_go_out else min(im_size) - max_size

    for i in tqdm(range(args.nb_images)):
        fig, ax = plt.subplots()
        plt.axis("off")
        ax.imshow(np.ones((im_size[0], im_size[1], 3)))

        colors = ["red", "green", "blue"]
        shapes = ["square", "circle", "triangle"]
        np.random.shuffle(colors)
        np.random.shuffle(shapes)
        
        positions, sizes = sample_n_pos_size(3, min_pos, max_pos, min_size, max_size, can_overlap)

        for c, s, pos, size in zip(colors, shapes, positions, sizes):
            angle = np.random.rand() * 2 * np.pi if can_rotate else 0
            if s == "square":
                shape = make_square(pos, size, angle, c)
            if s == "circle":
                shape = make_circle(pos, size, c)
            if s == "triangle":
                shape = make_triangle(pos, size, angle, c)
            ax.add_patch(shape)

        plt.savefig(f"images/image_{i:0{len(str(args.nb_images))}d}.png", bbox_inches="tight", pad_inches=0)
        plt.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nb-images", type=int, default=10, help="Number of images to generate.")
    return parser.parse_args()


def sample_n_pos_size(n, min_pos, max_pos, min_size, max_size, overlap=False):
    sample = lambda n: (min_pos + (max_pos - min_pos) * np.random.rand(n, 2), min_size + (max_size - min_size) * np.random.rand(n))

    if overlap:
        return sample(n)

    pos, size = np.zeros((n, 2)), np.zeros(n)
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

    return pos, size     
        

def is_overlap(positions, sizes):
    for i, pos in enumerate(positions):
        dist = np.delete(np.sqrt(np.square(positions - pos).sum(1)), i)
        size = np.delete(sizes, i)
        if np.any(dist < size + sizes[i]):
            return True
    return False


def make_square(pos, size, angle, color):
    angles = np.pi / 4 + np.pi / 2 * np.arange(4) + angle
    pts = np.array(list(map(lambda a: [np.cos(a), np.sin(a)], angles)))
    pts = size * pts + pos
    return Polygon(pts, closed=False, color=color)


def make_circle(pos, size, color):
    return plt.Circle(pos, size, fc=color, ec=color)


def make_triangle(pos, size, angle, color):
    angles = np.array([0, 2 * np.pi / 3, - 2 * np.pi / 3]) + angle
    pts = np.array(list(map(lambda a: [np.cos(a), np.sin(a)], angles)))
    pts = size * pts + pos
    return Polygon(pts, closed=False, color=color)


if __name__ == "__main__":
    main()
