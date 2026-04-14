# LLM-Based Data Augmentation for Solidity Smart Contracts

LLM pipeline to expand a seed dataset of Solidity smart contracts using few-shot in-context learning, inspired by the UniGen framework (ICLR 2025). The augmented dataset feeds back into a vulnerability detection ML pipeline based on CodeBERT embeddings of EVM bytecode.

**Goal arc:**
1. Generate compilable Solidity contracts (`solc` as quality gate)
2. Label generated contracts for vulnerabilities (Slither / Mythril)
3. Evaluate improvements in the ML vulnerability detection pipeline

**LLM provider:** DeepInfra (current baseline), other providers under evaluation.

**Seed data:** `ethereum/data/` — dataset selection TBD.

**Implementation:** Marimo notebook, built from scratch.

---

## Documents

_Topic documents will be added here as cycles progress._
