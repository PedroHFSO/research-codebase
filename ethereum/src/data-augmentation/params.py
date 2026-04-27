from dataclasses import dataclass


@dataclass
class PipelineParams:
    # Seed sampling
    few_shot_k: int = 3
    random_seed: int = 42

    # Generation
    model: str = "meta-llama/Llama-3.3-70B-Instruct"
    temperature: float = 0.8
    top_p: float = 0.95
    top_k: int = 50
    n_samples: int = 10
    max_tokens: int = 4096
