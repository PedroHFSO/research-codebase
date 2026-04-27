# Generation Module

Entry point: `src/data-augmentation/generate.py`. Called by `pipeline.run()`, returns `List[dict]` of `{"source_code", "contract_type"}` objects consumed by the compile gate.

## Contract Index

`_load_contract_index()` walks `data/smartbugs-wild-master/` recursively via `rglob("*.sol")` and returns a sorted list of paths. Sorted for stable indexing across runs. Filtered at load time: files below 50 bytes (`_MIN_CONTRACT_SIZE`) are excluded using `stat()` — no file reads, one-time cost.

## Sampling

`sample_contracts(params)` seeds `random` with `params.random_seed` before drawing, making samples deterministic. Draws `params.few_shot_k` indices via `random.sample(range(len(paths)), k)` — no replacement. After sampling, source content is hashed to detect duplicate files in the dataset; a warning is logged but execution continues.

## Prompt

`build_prompt(params, examples_json)` embeds the serialized few-shot examples and asks the model to return `params.n_samples` contracts in a single response as a JSON array. All `n_samples` are requested in one call — simpler than N separate calls but relies on the model maintaining JSON structure across multiple outputs.

## API Call

`get_llm_credentials()` reads `DEEPINFRA_API_KEY` from the environment (loaded via `python-dotenv`) and returns the DeepInfra OpenAI-compatible endpoint URL. `run()` posts to this endpoint with all generation parameters: `model`, `temperature`, `top_p`, `top_k`, `max_tokens`.

## Response Parsing

`parse_response(text)` strips `<think>` tags (present in reasoning models), removes markdown fences if present, then deserializes JSON. Returns the parsed list upstream.

## Dev Environment

Dependencies: `textual`, `requests`, `python-dotenv` — all in `requirements.txt`, installed in `.venv` at `src/data-augmentation/.venv/`. Copy `.env.example` to `.env` and set `DEEPINFRA_API_KEY`. `load_dotenv()` is called at startup in `__main__.py`.
