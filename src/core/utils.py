# utils.py
import yaml
from pathlib import Path
from .config import AppConfig
from pydantic import ValidationError

import torch

def load_config_from_yaml(config_path: Path) -> AppConfig:
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)

    try:
        app_config = AppConfig(**config_dict)
        return app_config
    except ValidationError as e:
        print(f"❌ Configuration Error in '{config_path}':")
        print(e)
        raise


def load_sentences(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        sentences = [line.strip() for line in f if line.strip()]
    return sentences


def save_output(output_path: str, output: torch.Tensor):
    Path(output_path).mkdir(parents=True, exist_ok=True)
    torch.save(output['final_embeddings'], Path(output_path) / "final_embeddings.pt")
    torch.save(output['hidden_embeddings'], Path(output_path) / "hidden_embeddings.pt")
    
    with open(Path(output_path) / "contexts.txt", "w", encoding="utf-8") as f:
        for context in output['valid_contexts']:
            f.write(f"{context}\n")
            
    with open(Path(output_path) / "indices.txt", "w", encoding="utf-8") as f:
        for index in output['valid_indices']:
            f.write(f"{index}\n")
    print(f"Embeddings and associated data saved to {output_path}")


def save_metrics(output_path: str, layer, metrics: dict):
    Path(output_path).mkdir(parents=True, exist_ok=True)
    torch.save(metrics, Path(output_path) / f"metrics_layer-{layer}.pt")

    
def save_landscape(output_path: str, layer, landscape: dict):
    Path(output_path).mkdir(parents=True, exist_ok=True)
    torch.save(landscape, Path(output_path) / f"landscape_layer-{layer}.pt")
    