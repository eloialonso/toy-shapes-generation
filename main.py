import argparse
from pathlib import Path

import hydra
from omegaconf import DictConfig
from tqdm import tqdm


@hydra.main(config_path="config", config_name="default")
def main(cfg: DictConfig):
    
    output_dir = Path(cfg.output_dir)
    png_dir = output_dir / "png"
    yaml_dir = output_dir / "yaml"
    for dir in [output_dir, png_dir, yaml_dir]:
        dir.mkdir(exist_ok=True)
    
    generator = hydra.utils.instantiate(cfg.generator) 

    for i in tqdm(range(cfg.nb_images)):
        layout = generator.generate_random_layout()
        stem = f"image_{i:0{len(str(cfg.nb_images))}d}"
        layout.savefig(png_dir / f"{stem}.png")
        layout.dump(yaml_dir / f"{stem}.yaml")
        

if __name__ == "__main__":
    main()
