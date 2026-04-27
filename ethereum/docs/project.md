# LLM-Based Data Augmentation for Solidity Smart Contracts

LLM pipeline to expand a seed dataset of Solidity smart contracts using few-shot in-context learning, inspired by the UniGen framework (ICLR 2025). The augmented dataset feeds back into a vulnerability detection ML pipeline based on CodeBERT embeddings of EVM bytecode.

**LLM provider:** DeepInfra (current baseline), other providers under evaluation.

**Seed data:** SmartBugs Wild — 47,398 unique real-world Solidity contracts extracted from Ethereum mainnet (`ethereum/data/smartbugs-wild-master/`). Used as the few-shot example pool.

---

## Experiment Goal

Test whether LLM-generated synthetic Solidity contracts, when added to the training set, improve the performance of a CodeBERT-based smart contract vulnerability detector.

---

## High-Level Roadmap

### Phase 1 — Seed Curation
Select a representative subset of contracts from SmartBugs Wild to serve as few-shot examples. Filter by size, pragma version, and structural diversity.

### Phase 2 — Generation Loop
Use the curated seed to construct few-shot prompts and generate new contracts via the LLM. Apply a UniGen-inspired diversity-promoting selection mechanism to vary which seed examples are used across generations.

### Phase 3 — Quality Gate
Compile each generated contract with `solc`. Discard any that fail to compile. Only compilable contracts advance.

### Phase 4 — Vulnerability Labeling
Run Slither and/or Mythril on the compilable contracts to produce vulnerability labels consistent with the original dataset's labeling scheme.

### Phase 5 — ML Pipeline Evaluation
Merge labeled synthetic contracts with the original training data. Re-train and evaluate the CodeBERT-based vulnerability detector. Compare against the baseline (no augmentation) to measure impact.

---

## Documents

- [Parameter Schema](parameter-schema.md) — v1 CLI parameter schema: seed sampling and generation knobs, with rationale for inclusions and exclusions
