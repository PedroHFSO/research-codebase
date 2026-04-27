import logging
import re
import json
import os
import random
import requests
from pathlib import Path
from typing import List

from params import PipelineParams

logger = logging.getLogger(__name__)

_DATASET_DIR = Path(__file__).parent.parent.parent / "data" / "smartbugs-wild-master"
_CONTRACT_PATHS: List[Path] = []

_MIN_CONTRACT_SIZE = 50

def _load_contract_index() -> List[Path]:
    global _CONTRACT_PATHS
    if not _CONTRACT_PATHS:
        all_paths = sorted(_DATASET_DIR.rglob("*.sol"))
        _CONTRACT_PATHS = [p for p in all_paths if p.stat().st_size >= _MIN_CONTRACT_SIZE]
        logger.info(
            "Indexed %d contracts (%d skipped below %d bytes)",
            len(_CONTRACT_PATHS),
            len(all_paths) - len(_CONTRACT_PATHS),
            _MIN_CONTRACT_SIZE,
        )
    return _CONTRACT_PATHS

def get_llm_credentials() -> dict:
    return {
        "url": "https://api.deepinfra.com/v1/openai/chat/completions",
        "api_key": os.environ["DEEPINFRA_API_KEY"],
    }

def build_prompt(params: PipelineParams, examples_json: str) -> str:
    prompt = f'''You are a professional Solidity smart contract generator.
    Below are {params.few_shot_k} example Solidity contracts for reference:

    {examples_json}

    Generate {params.n_samples} new, diverse Solidity smart contracts. Requirements:
    1. Each contract must be complete and syntactically valid Solidity.
    2. Use pragma solidity ^0.8.0 or later.
    3. Include an SPDX license identifier.
    4. Vary contract types (e.g. ERC20, ERC721, Multisig, Vault, Staking, Governance, Ownable).

    Respond with ONLY a valid JSON array — no markdown, no commentary:
    [{{"source_code": "<full solidity source>", "contract_type": "<type>"}}]
    '''
    return prompt

def build_json(contract_path: Path) -> dict:
    return {"source_code": contract_path.read_text(encoding="utf-8", errors="ignore")}

def sample_contracts(params: PipelineParams) -> str:
    random.seed(params.random_seed)
    logger.info("Sampling %d contracts (seed=%d)", params.few_shot_k, params.random_seed)
    paths = _load_contract_index()
    ids = random.sample(range(len(paths)), params.few_shot_k)
    contract_list = []
    for i in ids:
        path = paths[i]
        logger.debug("Reading contract [%d] %s", i, path.name)
        contract_list.append(build_json(path))
    sources = [c["source_code"] for c in contract_list]
    duplicates = len(sources) - len(set(sources))
    if duplicates:
        logger.warning("%d duplicate contract(s) detected in sample", duplicates)
    logger.info("Sampling complete — %d contracts loaded", len(contract_list))
    return json.dumps(contract_list)

def parse_response(text: str) -> List[dict]:
    text = text.strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1])
    return json.loads(text)

def run(params: PipelineParams) -> List[dict]:
    credentials = get_llm_credentials()
    examples_json = sample_contracts(params)
    prompt = build_prompt(params, examples_json)

    logger.info("Calling DeepInfra: model=%s, n_samples=%d", params.model, params.n_samples)
    response = requests.post(
        credentials["url"],
        headers={
            "Authorization": f"Bearer {credentials['api_key']}",
            "Content-Type": "application/json",
        },
        json={
            "model": params.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": params.temperature,
            "top_p": params.top_p,
            "top_k": params.top_k,
            "max_tokens": params.max_tokens,
        },
    )
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]
    contracts = parse_response(content)
    logger.info("Received %d contracts from model", len(contracts))
    return contracts
