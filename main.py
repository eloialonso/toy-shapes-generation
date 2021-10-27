import multiprocessing
from pathlib import Path
from pprint import pprint

import hydra
import numpy as np
from omegaconf import DictConfig
from tqdm import tqdm


@hydra.main(config_path="config", config_name="default")
def main(cfg: DictConfig):
    
    png_dir = Path(cfg.png_dir)
    yaml_dir = Path(cfg.yaml_dir)
    png_dir.mkdir(exist_ok=True, parents=True)
    yaml_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"Generating {cfg.nb_images} random images.\nConfig : ")
    pprint(dict(cfg.generator))
    print(f"\n\n- Images location : {png_dir}\n- Layout location : {yaml_dir}\n\n")

    generator = hydra.utils.instantiate(cfg.generator) 
    
    filenames_png = [png_dir / f"image_{i:0{len(str(cfg.nb_images))}d}.png" for i in range(cfg.nb_images)]
    filenames_yaml = [yaml_dir / f"image_{i:0{len(str(cfg.nb_images))}d}.yaml" for i in range(cfg.nb_images)]
    
    chunks_png = list(map(lambda array: array.tolist(), np.array_split(filenames_png, cfg.workers)))
    chunks_yaml = list(map(lambda array: array.tolist(), np.array_split(filenames_yaml, cfg.workers)))

    processes = []
    for chunk_png, chunk_yaml in zip(chunks_png, chunks_yaml):
        p = multiprocessing.Process(target=generate_and_save_random_images, args=(generator, chunk_png, chunk_yaml))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    

def generate_and_save_random_images(generator, filenames_image, filenames_layout):
    assert len(filenames_image) == len(filenames_layout)
    for filename_image, filename_layout in zip(tqdm(filenames_image), filenames_layout):
        layout = generator.generate_random_layout()
        layout.savefig(filename_image)
        layout.dump(filename_layout)


if __name__ == "__main__":
    main()
