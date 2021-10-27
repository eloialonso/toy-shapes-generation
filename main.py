import multiprocessing
from pathlib import Path

import hydra
import numpy as np
from omegaconf import DictConfig
from tqdm import tqdm


@hydra.main(config_path="config", config_name="default")
def main(cfg: DictConfig):
    
    output_dir = Path(cfg.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    generator = hydra.utils.instantiate(cfg.generator) 

    filenames = [output_dir / f"image_{i:0{len(str(cfg.nb_images))}d}" for i in range(cfg.nb_images)]

    processes = []
    for chunk in list(map(lambda array: array.tolist(), np.array_split(filenames, cfg.workers))):
        p = multiprocessing.Process(target=generate_and_save_random_images, args=(generator, chunk))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    

def generate_and_save_random_images(generator, filenames):
    for filename in tqdm(filenames):
        layout = generator.generate_random_layout()
        layout.savefig(filename.with_suffix(".png"))
        layout.dump(filename.with_suffix(".yaml"))


if __name__ == "__main__":
    main()
