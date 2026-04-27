# Pipeline Parameter Schema (v1)

## Seed Sampling

| Parameter | Type | Default | Description |
|---|---|---|---|
| `few_shot_k` | int | 3 | Contracts sampled from SmartBugs Wild per generation prompt |
| `random_seed` | int \| None | 42 | Random seed for reproducibility; set to None for non-deterministic runs |

## Generation

| Parameter | Type | Default | Description |
|---|---|---|---|
| `model` | str | *(required)* | DeepInfra model ID |
| `temperature` | float | 0.8 | Sampling temperature |
| `top_p` | float | 0.95 | Nucleus sampling threshold |
| `top_k` | int | 50 | Top-k vocabulary cutoff |
| `n_samples` | int | 100 | Total contracts to generate |
| `max_tokens` | int | 4096 | Per-call token budget (safeguard only) |

## Deferred

The following were considered and explicitly excluded from v1:

- `solc_version` — deferred; not needed for the vertical slice
- `output_dir`, `run_name` — run management; easy to add when needed
- `repetition_penalty` / `frequency_penalty` — risk suppressing legitimate syntactic repetition in Solidity
- stop sequences — hardcoded implementation detail, not a user-facing parameter
