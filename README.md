# What’s Your POV? Evaluating Political Neutrality, Sycophancy, and Locality Biases in Open-Weight LLMs

[![CS612 Evaluation Suite](https://img.shields.io/badge/CS612-AI%20Systems%20%26%20Evaluation-blue.svg)](https://scis.smu.edu.sg)
[![Status: Pristine](https://img.shields.io/badge/Release-v1.0.0--Unified-success.svg)](#)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-informational.svg)](https://www.python.org/)
[![Reproducibility: 100% Portable](https://img.shields.io/badge/Reproducibility-Verified-brightgreen.svg)](#)

---

## 1. Executive Overview

This repository provides the unified, fully reproducible codebase, datasets, model weights, and evaluation pipelines for our CS612 AI Systems & Evaluation final investigation:

> **"What’s Your POV? Evaluating Political Neutrality, Sycophancy, and Locality Biases in Open-Weight LLMs"**  
> *Singapore Management University (SMU), 2026*

> [!NOTE]
> **Primary Deliverable Focus:** This repository specifically delivers the complete, self-contained implementation, datasets, calibrated neural stance classifiers, and evaluation harness for:
> 1. **Section 3.3 (Experiment C):** Multi-Turn Adversarial Sycophancy & Epistemic Collapse Tracking (1,800 turns across 7 foundation models).
> 2. **Section 4.2 (PRISM Defense):** Two-Tier Constitutional & Reflection Critic Mitigation Framework.
>
> For reproducibility and comprehensive team integration, the shared utilities (`common/`), publication figures (`figures/`), technical documentation (`docs/`), and unified runners (`run_all.sh`, Docker) are bundled to reproduce both our individual modules and the end-to-end research suite.

### Evaluated Model Matrix

| Model Identifier | Region / Family | Base Lineage | Serving Quantization | Default Backend |
| :--- | :---: | :---: | :---: | :---: |
| **Meta Llama-3.1-8B-Instruct** | Western | Meta Llama 3.1 | Q8_0 / BF16 | Ollama / vLLM |
| **Google Gemma-3-12b-it** | Western | Google Gemma 3 | Q8_0 / BF16 | Ollama / vLLM |
| **Alibaba Qwen3-VL-8B-Instruct** | Chinese | Alibaba Qwen 3 | Q8_0 / BF16 | Ollama / vLLM |
| **Zhipu GLM-4-9b-chat** | Chinese | GLM Architecture | Q8_0 / BF16 | Ollama / vLLM |
| **AISG Llama-SEA-LION-v3-8B-IT** | Southeast Asia | Meta Llama 3.1 | Q8_0 / BF16 | Ollama / vLLM |
| **AISG Qwen-SEA-LION-v4-8B-VL** | Southeast Asia | Alibaba Qwen 2.5 | Q8_0 / BF16 | Ollama / vLLM |
| **SCB 10X Llama3.1-typhoon2-8b-instruct** | Southeast Asia | Meta Llama 3.1 | Q8_0 / BF16 | Ollama / vLLM |

---

## 2. Repository Layout & Architecture

The repository enforces strict modularity, 100% relative path resolution (zero hardcoded machine paths), and standardized terminology (**Liberal** and **Conservative** across all modules).

```
cs612_unified_experiments_repo/
├── README.md                          # Master overview, architecture & quickstart guide
├── Dockerfile                         # Production Docker container definition
├── docker-compose.yml                 # Multi-volume docker-compose specification
├── requirements.txt                   # Consolidated Python dependencies
├── run_all.sh                         # Master bash execution runner
├── verify_repo.py                     # Self-contained smoke test & integrity auditor
├── common/                            # Shared clients, Ollama helpers & plotting styles
│   ├── config.py                      # Global paths, model families & evaluation thresholds
│   ├── ollama_client.py               # Robust Ollama / local inference helper
│   ├── plotting.py                    # Publication-grade plotting styles & color palettes
│   └── text_utils.py                  # Text cleaning, conversational echo stripper
├── 01_experiment_a_baseline/          # Single-turn PARETO baseline & dual-judge
│   ├── src/                           # Evaluator scripts & baseline metric computer
│   ├── data/                          # 200 PARETO prompts, Excel workbook & golden set
│   └── outputs/                       # Baseline CSVs & approval scores
├── 02_experiment_b_robustness/        # 1,000-question perturbation analysis
│   ├── src/                           # 4-method prompt rewriting & robustness analysis
│   ├── data/                          # Perturbation templates & synthesized dataset
│   └── outputs/                       # Robustness metrics summary
├── 03_experiment_c_sycophancy/        # 10-turn adversarial simulation & Tier-2 LLM judge
│   ├── src/                           # multi_turn_simulator.py, run_tier2_judge.py
│   ├── models/                        # Calibrated DeBERTa-v3 Tier-1 classifier & calibration.json
│   ├── data/                          # 20 contentious policy topics x 3 personas
│   └── outputs/                       # 1,800 turns JSON/JSONL for Llama 3.1, Gemma 3, Qwen 3
├── 04_experiment_d_locality/          # 155 disputed territories (BorderLines)
│   ├── src/                           # 5-framing prompt generator & GPT-4 scoring harness
│   ├── data/                          # Disputed territory metadata & region clusters
│   └── outputs/                       # Locality benchmark outputs & RQ verdicts
├── 05_prism_defense/                  # PRISM 2-Tier constitutional & critic defense
│   ├── src/                           # prism_defense.py & mitigation evaluator
│   └── outputs/                       # Pre- and post-defense mitigation logs
├── figures/                           # Publication-ready figures (Figures 1-10)
└── docs/                              # Technical specifications, rubrics & reports
```

### 2.1 Core Utilities, Documentation & Figures

* **`common/` (Shared Runtime Infrastructure):**
  - [`config.py`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/common/config.py): Centralized environment configurations, model family definitions, temperature calibration thresholds, and path resolvers.
  - [`ollama_client.py`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/common/ollama_client.py): Robust local Ollama and OpenRouter inference client featuring retry loops, backoff, and graceful fallback.
  - [`plotting.py`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/common/plotting.py): Academic publication styling, matplotlib color themes, and export formatting.
  - [`text_utils.py`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/common/text_utils.py): Text sanitization, conversational echo stripping, and streaming JSONL readers/writers.

* **`docs/` (Formal Methodology & Technical Reports):**
  - [`EXPERIMENT_C_FINAL_REPORT.md`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/docs/EXPERIMENT_C_FINAL_REPORT.md): Exhaustive scientific report for Experiment C (1,800-turn sycophancy simulation and epistemic drift findings).
  - [`PRISM_MITIGATIONS_REPORT.md`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/docs/PRISM_MITIGATIONS_REPORT.md): Comprehensive specification of the PRISM constitutional defense and empirical ablation tables.
  - [`TIER1_SCORING_METHODOLOGY.md`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/docs/TIER1_SCORING_METHODOLOGY.md): Neural stance calibration mathematical formulation, Platt scaling, and neutral band thresholds.
  - [`EVALUATOR_TRIANGULATION_REPORT.md`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/docs/EVALUATOR_TRIANGULATION_REPORT.md): Triangulation between neural stance scoring and frontier LLM-as-a-Judge audits.
  - [`FINAL_REPORT_SECTIONS.md`](file:///Users/anishdobz/Library/CloudStorage/OneDrive2-SingaporeManagementUniversity/2_smu_pg/4_1_ai_system_evaluation_cs612/cs612_unified_experiments_repo/docs/FINAL_REPORT_SECTIONS.md): Consolidated academic write-ups and report sections.

* **`figures/` (Publication-Grade Visualizations):**
  - High-resolution (300 DPI) publication figures (Figures 1–10) dynamically generated from raw simulation logs by `generate_paper_figures.py`. Highlights include Figure 2 (longitudinal epistemic drift trajectories), Figure 3 (Tier-2 judge correlation), Figure 4 (PRISM defense drift suppression), Figure 5 (concession rate heatmaps), and Figure 6 (conversational politeness vs. epistemic surrender decoupling).

---

## 3. Quickstart & Verification

### 3.1 One-Command Docker Reproduction (Recommended)
You can build and run the evaluation suite in an isolated, fully reproducible container without needing local Python or GPU setup:

```bash
# 1. Build the Docker container image
docker build -t cs612-eval-suite .

# 2. Option A: Run Experiment C (Sycophancy) + PRISM Defense (Primary Deliverable)
docker run --rm cs612-eval-suite c_and_prism

# 3. Option B: Run the Complete Team Pipeline (All 4 Experiments + PRISM)
docker run --rm cs612-eval-suite mock

# 4. Option C: Using Docker Compose (auto-mounts figures and outputs back to host)
docker-compose up --build
```

### 3.2 Native Local Installation
Clone this repository and install dependencies in a clean virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3.3 Smoke Test & Verification
Run the self-contained verification suite to confirm that all assets exist, modules import cleanly, CLI argument parsers function without errors, and zero hardcoded paths exist:
```bash
python3 verify_repo.py
```

### 3.4 End-to-End One-Command Execution
To run all experiments, generate all summary metrics, and regenerate all publication figures in deterministic smoke-test mode:
```bash
./run_all.sh mock
```
To run full-scale live evaluation against local Ollama serving:
```bash
./run_all.sh full
```

---

## 4. Hardware Serving Setup (Ollama)

For live evaluation, local models are served via [Ollama](https://ollama.ai) on Apple Silicon Mac (M1/M2/M3/M4 Max with Metal acceleration) or Linux (NVIDIA CUDA):

```bash
# Pull candidate models
ollama pull llama3.1:8b-instruct-q8_0
ollama pull gemma3:12b
ollama pull qwen3-vl:8b
ollama pull glm4:9b-chat
ollama pull aisingapore/llama-sealion3-8b-instruct
ollama pull aisingapore/qwen-sealion4-8b-vl
ollama pull scb10x/llama3.1-typhoon2-8b-instruct

# Start local server (default port 11434)
ollama serve
```

---

## 5. Experiment Breakdown & Methodologies

### Experiment A: Single-Turn PARETO Baseline Neutrality
- **Dataset:** 200 public policy questions spanning 6 societal clusters from the PARETO benchmark.
- **Evaluation:** Dual-Judge Framework prompted as mainstream American **Liberal** and mainstream American **Conservative** evaluators.
- **Key Metrics:** Mean Approval Delta ($AD = A_{\text{Lib}} - A_{\text{Cons}}$), Mean Joint Approval ($JA = A_{\text{Lib}} \times A_{\text{Cons}}$), Dual-Perspective Concordance Rate (DPCR).
- **Execution:**
  ```bash
  python3 01_experiment_a_baseline/src/compute_baseline_metrics.py
  python3 01_experiment_a_baseline/src/run_single_turn_eval.py --backend mock
  ```

### Experiment B: Phrasing Perturbation Robustness (1,000 Prompts)
- **Dataset:** 200 base PARETO questions expanded into 1,000 prompts via 4 semantic-preserving rewrite methods:
  1. *Typo* (rule-based character transposition)
  2. *Synonym Swap* (controlled lexical substitution)
  3. *Sentence Restructuring* (topicalized syntactic reordering)
  4. *Paraphrase* (semantic rephrasing)
- **Key Metrics:** Spread ($\max - \min$), Big Spread Rate ($> 0.60$), Side Switch Rate.
- **Execution:**
  ```bash
  python3 02_experiment_b_robustness/src/rewrite_prompts.py
  python3 02_experiment_b_robustness/src/run_robustness_eval.py --mock
  ```

### Experiment C: Multi-Turn Adversarial Sycophancy (1,800 Turns)
- **Curriculum:** 20 contentious policy topics $\times$ 3 personas (**Liberal**, **Conservative**, **Control**) $\times$ 10 dialogue turns = 600 turns per model across 10-turn adversarial escalation:
  - *Turn 1:* Neutral baseline anchor
  - *Turns 2–4:* Incidental demographic & lived experience priming
  - *Turns 5–7:* Socratic pushback & epistemic authority traps
  - *Turns 8–10:* Forced-choice entrapment & false-premise gaslighting
- **Evaluators:** Decoupled evaluation isolating Tier 1 Stance Classifier (calibrated DeBERTa-v3) from Tier 2 LLM-as-a-Judge (decoupling Conversational Politeness from Epistemic Concession).
- **Execution:**
  ```bash
  python3 03_experiment_c_sycophancy/src/multi_turn_simulator.py --backend mock --max_topics 1 --turns 2
  python3 03_experiment_c_sycophancy/src/run_tier2_judge.py --simulation_file 03_experiment_c_sycophancy/outputs/multi_turn_simulation_llama-3.1-8b-instruct_latest.json --judge_provider mock
  python3 03_experiment_c_sycophancy/src/generate_paper_figures.py
  ```

### Experiment D: Geopolitical Locality & Sovereignty (BorderLines 155 Territories)
- **Dataset:** 155 disputed territories clustered into 4 regions: China-implicated (59), SEA-implicated (16), China–SEA overlap (5), and Others (75).
- **Framings:** 5 prompt pressure framings (F1 Cued, F2 Uncued, F3 Map caption, F4 Loaded premise, F5 Forced choice) = 1,085 to 1,110 prompts per model.
- **Key Metrics:** $N_{\text{CORE}}$, $N$ (F2 uncued), Side-picking Rate, Refusal Rate.
- **Execution:**
  ```bash
  python3 04_experiment_d_locality/src/borderlines_prompt_generator.py
  python3 04_experiment_d_locality/src/borderlines_evaluator.py --backend mock --max_samples 5
  python3 04_experiment_d_locality/src/analyze_locality_results.py
  ```

### PRISM Defense Framework (Perspective-Robust In-Context Sycophancy Mitigation)
- **Architecture:** Training-free 2-stage inference defense:
  - *Tier 1 Pre-Processing:* Constitutional system prompt hardening with 5 Articles of Epistemic Neutrality.
  - *Tier 2 Post-Processing:* Decoupled reflection critic loop (using independent evaluator) that intercepts capitulation drafts and triggers balanced rewrites.
- **Execution:**
  ```bash
  python3 05_prism_defense/src/prism_defense.py --mode full_prism --backend mock --max_conversations 1
  python3 05_prism_defense/src/evaluate_prism_mitigations.py
  ```

---

## 6. Key Empirical Findings (Summary of Report Tables)

1. **Default Liberal Skew (Table 4):** All seven evaluated models exhibit a consistent liberal-leaning baseline approval ($AD \in [0.22, 0.37]$). Chinese models (Qwen 3 and Qwen-SEA-LION) exhibit the strongest liberal skew ($0.37$ and $0.35$), disproving the hypothesis that political bias is uniquely Western.
2. **Robustness Hierarchy (Table 6):** Gemma 3 is the most robust model against phrasing perturbations (1.0% big spread rate, 0.0% side switch rate), while GLM-4 is the least robust (16.0% big spread rate, 21.0% side switch rate). Sentence restructuring triggers the largest shift across all models ($0.14$).
3. **Asymmetric Epistemic Collapse (Table 9):** Models strongly resist Conservative pressure but collapse under Liberal multi-turn pressure (up to 55.0% collapse on Qwen 3 and 50.0% on Llama 3.1). Crucially, polite conversational tone masks substantive surrender (Figure 6).
4. **Geopolitical Lineage vs Origin (Table 13 & 14):** Model lineage exerts stronger influence than origin. Chinese models back the PRC in 38% of side-taking answers vs 20–25% for other families. Under loaded premises (F4), the gap between models widens from 0.16 to 0.66.
5. **PRISM Mitigation Efficacy (Table 15 & 16):** Full PRISM reduces single-turn Approval Delta across all models ($0.27 \to 0.17$), elevates DPCR ($86.6\% \to 98.6\%$), cuts multi-turn School Vouchers drift by 68.1% (NSS) and longitudinal AUC by up to 73.4%, successfully rescuing models from Turn 10 gaslighting traps.

---

## 7. License & Citation

This repository is distributed under the Apache-2.0 License. If you use this codebase or benchmark data in your research, please cite:

```bibtex
@article{smu2026whatisyourpov,
  title={What’s Your POV? Evaluating Political Neutrality, Sycophancy, and Locality Biases in Open-Weight LLMs},
  author={CS612 Research Group 3 and Project Team},
  journal={Singapore Management University CS612 AI Systems \& Evaluation Technical Reports},
  year={2026}
}
```
