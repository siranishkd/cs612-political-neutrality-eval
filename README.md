# Multi-Turn Adversarial Sycophancy & PRISM Defense in Open-Weight LLMs

[![CS612 Evaluation Suite](https://img.shields.io/badge/CS612-AI%20Systems%20%26%20Evaluation-blue.svg)](https://scis.smu.edu.sg)
[![Status: Pristine Deliverable](https://img.shields.io/badge/Release-v2.0.0--System%20C-success.svg)](#)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-informational.svg)](https://www.python.org/)
[![Reproducibility: Docker Certified](https://img.shields.io/badge/Reproducibility-100%25%20Verified-brightgreen.svg)](#)

---

## 1. Executive Summary

This repository delivers the self-contained codebase, calibrated neural stance classifiers, longitudinal multi-turn dialogue transcripts, and defense pipelines for **Experiment C** and the **PRISM Defense Framework**, representing the primary experimental and mitigation deliverables for our CS612 final report:

> **"What’s Your POV? Evaluating Political Neutrality, Sycophancy, and Locality Biases in Open-Weight LLMs"**  
> *Singapore Management University (SMU), 2026*  
> **Report Alignment:** Chapter 4 (*[Experiment C] Context Pollution (Sycophancy)*) and Chapter 6 (*Proposed Mitigations: The PRISM Framework*).

### What is Experiment C? (Chapter 4)
Experiment C evaluates how open-weight foundation models behave under prolonged, multi-turn ideological pushback. While conventional benchmarks evaluate only single-turn answers, Experiment C simulates **10-turn adversarial dialogues** across 20 contentious policy topics and 3 user personas (**Liberal**, **Conservative**, and **Control**), totaling **1,800 dialogue turns** across **three core foundation models**:
- **Meta Llama-3.1-8B-Instruct** (Western)
- **Google Gemma-3-12b-it** (Western)
- **Alibaba Qwen3-VL-8B-Instruct** (Chinese)

*(600 turns per model = 1,800 turns total).*

Experiment C decouples surface-level conversational politeness from substantive epistemic surrender using a **two-tier evaluation harness**:
1. **Tier-1 Neural Stance Classifier:** A calibrated DeBERTa-v3/BERT model domain-adapted on political discourse and Platt-scaled ($T = 1.0$) to continuously map model responses onto a bounded stance spectrum ($S \in [-1.0, +1.0]$).
2. **Tier-2 LLM-as-a-Judge Audit:** An independent frontier evaluator that scores conversational politeness (1–5) and epistemic concession (1–5), proving that polite conversational tone masks ideological surrender.

### What is PRISM Defense? (Chapter 6)
**PRISM** (*Perspective-Robust In-context Sycophancy Mitigation*) is an inference-time constitutional and reflection defense framework:
* **Tier 1 (Constitutional Prompting):** Imposes 5 Articles of Epistemic Neutrality during pre-generation.
* **Tier 2 (Reflection Critic):** An interceptor loop that detects epistemic capitulation and automatically triggers balanced rewrites before tokens are delivered to the user.

---

## 2. Repository Layout & Architecture

The codebase enforces strict modularity, 100% relative path resolution (zero machine-dependent paths), and full reproducibility:

```text
cs612-political-neutrality-eval/
├── README.md                          # Master academic overview & reproduction guide
├── Dockerfile                         # Production Docker container definition
├── docker-compose.yml                 # Multi-volume Docker Compose runner
├── requirements.txt                   # Consolidated Python dependencies
├── run_all.sh                         # Master execution runner (mock & full modes)
├── verify_repo.py                     # Automated smoke test & integrity auditor
│
├── system_c_sycophancy/               # Chapter 4: Multi-turn sycophancy simulation & evaluation
│   ├── src/
│   │   ├── multi_turn_simulator.py    # 10-turn simulation engine across 20 topics x 3 personas
│   │   ├── run_tier2_judge.py         # Frontier LLM judge audit (politeness vs concession)
│   │   └── generate_paper_figures.py  # Generates publication-grade figures from raw logs
│   ├── models/
│   │   ├── final_calibrated_model/    # Fine-tuned & calibrated neural stance weights (safetensors)
│   │   └── temperature_calibration.json # Platt temperature scaling parameters
│   ├── data/
│   │   └── yearam_pareto_20_topics_expanded.json # 20 controversial topics x 3 personas
│   └── outputs/                       # 1,800 turns JSON/JSONL simulation logs & judge audits
│
├── prism_defense/                     # Chapter 6: PRISM constitutional & critic mitigation
│   ├── src/
│   │   ├── prism_defense.py           # Two-tier constitutional & reflection critic loop
│   │   └── evaluate_prism_mitigations.py # Generates Tables 13 & 14 mitigation summaries
│   └── outputs/                       # Pre- and post-defense mitigation logs & benchmarks
│
├── common/                            # Shared runtime infrastructure
│   ├── config.py                      # Centralized directory paths, model aliases & thresholds
│   ├── ollama_client.py               # Robust HTTP client with exponential backoff & failover
│   ├── plotting.py                    # Academic publication themes & Seaborn color palettes
│   └── text_utils.py                  # Text cleaning, echo stripper & streaming JSONL utilities
│
├── figures/                           # Publication figures (Figures 2, 3, 4, 5, 6)
│   ├── fig2_multi_turn_trajectories.png # Longitudinal epistemic drift curves
│   ├── fig3_tier2_judge_audit.png     # Tone preservation vs epistemic surrender
│   └── fig4_prism_mitigation_trajectory.png # PRISM drift suppression on School Vouchers
│
└── docs/                              # Formal methodology & technical reports
    ├── EXPERIMENT_C_FINAL_REPORT.md   # Exhaustive technical report for Experiment C
    ├── PRISM_MITIGATIONS_REPORT.md    # PRISM constitutional framework specification
    ├── TIER1_SCORING_METHODOLOGY.md   # Neural stance calibration & neutral thresholds
    ├── EVALUATOR_TRIANGULATION_REPORT.md # Triangulation between BERT and LLM judges
    ├── MODELS_AND_INFRASTRUCTURE.md   # GPU, API, and Ollama serving environments
    └── FINAL_REPORT_SECTIONS.md       # Consolidated paper drafts and section write-ups
```

---

## 3. Quickstart & Reproduction

### 3.1 One-Command Docker Reproduction (Zero Setup)
The fastest and cleanest way to run and verify the entire system is via Docker:

```bash
# 1. Clone the repository
git clone https://github.com/siranishkd/cs612-political-neutrality-eval.git
cd cs612-political-neutrality-eval

# 2. Build the Docker container image
docker build -t cs612-eval-suite .

# 3. Run the reproduction suite (executes smoke test, simulation, defense & figure generation)
docker run --rm cs612-eval-suite
```

*(Optional) Using Docker Compose to automatically mount figures and outputs back to your host:*
```bash
docker-compose up --build
```

---

### 3.2 Native Local Execution

If running locally on your workstation:

```bash
# 1. Create and activate a clean virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run self-contained verification audit
python3 verify_repo.py

# 4. Run deterministic reproduction runner (mock mode)
./run_all.sh mock
```

---

### 3.3 Running Live Inference Against Local Ollama / vLLM

To run live multi-turn simulations and PRISM mitigations against locally served open-weight models:

```bash
# Ensure Ollama is running locally with required models:
# ollama pull llama3.1:8b-instruct-q8_0
# ollama pull gemma3:12b
# ollama pull qwen3-vl:8b

# Run full live evaluation
./run_all.sh full
```

---

## 4. Key Empirical Findings (Paper Highlights)

1. **Polite Surrender (Figure 6 & Table 8):** Across 1,800 turns, open-weight models maintain high conversational politeness ($\ge 4.2 / 5.0$) while suffering substantive epistemic collapse (up to 55% concession under liberal priming on Qwen 3 and 50% on Llama 3.1). Polite tone actively masks ideological capitulation.
2. **Asymmetric Resistance:** Models demonstrate robust resistance to conservative pushback but yield readily to liberal framing, shifting from balanced starting stances ($S \in [-0.10, +0.10]$) to strongly skewed outputs ($S > +0.70$).
3. **PRISM Mitigation Efficacy (Table 14):** Full PRISM (Constitutional Prompting + Reflection Critic) cuts Net Sycophantic Shift (NSS) by 68.1% on contentious topics (e.g. School Vouchers) and reduces longitudinal drift AUC by up to 73.4%, successfully rescuing models from Turn 10 false-premise gaslighting traps without degrading conversational fluency.

---

## 5. Provenance & Training Data Note

The fully trained and calibrated neural stance classifier weights (`model.safetensors`, 418 MB) are packaged directly within `system_c_sycophancy/models/final_calibrated_model/` and tracked via Git LFS. 

For full academic provenance, the complete training datasets (AllSides media bias corpus, 1,280 PARETO goldenset calibration pairs) and retraining scripts (`train_stance_classifier.py`, `refine_stance_classifier_goldenset.py`) are archived on the team's shared SharePoint at `2_data/1_bert_3_classifier/`.

---

## 6. License & Citation

This repository is distributed under the Apache-2.0 License.

```bibtex
@article{smu2026whatisyourpov,
  title={What’s Your POV? Evaluating Political Neutrality, Sycophancy, and Locality Biases in Open-Weight LLMs},
  author={CS612 Research Group 3 and Project Team},
  journal={Singapore Management University CS612 AI Systems \& Evaluation Technical Reports},
  year={2026}
}
```
