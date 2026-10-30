#!/usr/bin/env bash
# ==============================================================================
# CS612 Unified Experiments Master Execution Runner
# Evaluates Political Neutrality, Robustness, Sycophancy, and Locality Biases
# ==============================================================================

set -euo pipefail

# Determine repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

MODE="${1:-mock}"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}====================================================================${NC}"
echo -e "${BLUE}  CS612 AI SYSTEMS & EVALUATION: UNIFIED EXPERIMENT RUNNER          ${NC}"
echo -e "${BLUE}  Mode: ${MODE}                                                     ${NC}"
echo -e "${BLUE}====================================================================${NC}"

if [[ "${MODE}" != "mock" && "${MODE}" != "full" ]]; then
    echo -e "${RED}Invalid mode '${MODE}'. Usage: ./run_all.sh [mock|full]${NC}"
    exit 1
fi

PYTHON_CMD="python3"

# Step 1: Smoke Test & Import Verification
echo -e "\n${GREEN}[Step 1/7] Running Repository Smoke Test & Import Verification...${NC}"
${PYTHON_CMD} verify_repo.py

# Step 2: Experiment A (Single-Turn PARETO Baseline)
echo -e "\n${GREEN}[Step 2/7] Running Experiment A (Baseline Political Neutrality)...${NC}"
${PYTHON_CMD} 01_experiment_a_baseline/src/compute_baseline_metrics.py
if [[ "${MODE}" == "mock" ]]; then
    ${PYTHON_CMD} 01_experiment_a_baseline/src/run_single_turn_eval.py --backend mock --mock_classifier
else
    ${PYTHON_CMD} 01_experiment_a_baseline/src/run_single_turn_eval.py --backend ollama
fi

# Step 3: Experiment B (Robustness & Perturbation Analysis)
echo -e "\n${GREEN}[Step 3/7] Running Experiment B (1,000-Question Perturbation Analysis)...${NC}"
${PYTHON_CMD} 02_experiment_b_robustness/src/rewrite_prompts.py
${PYTHON_CMD} 02_experiment_b_robustness/src/run_robustness_eval.py --mock

# Step 4: Experiment C (Multi-Turn Sycophancy Simulation & Tier-2 Judge)
echo -e "\n${GREEN}[Step 4/7] Running Experiment C (Multi-Turn Sycophancy & Epistemic Concession)...${NC}"
if [[ "${MODE}" == "mock" ]]; then
    ${PYTHON_CMD} 03_experiment_c_sycophancy/src/multi_turn_simulator.py --backend mock --max_topics 1 --turns 2 --cooldown_sec 0.0 --output_dir 03_experiment_c_sycophancy/outputs/test_mock
    ${PYTHON_CMD} 03_experiment_c_sycophancy/src/run_tier2_judge.py --simulation_file 03_experiment_c_sycophancy/outputs/multi_turn_simulation_llama-3.1-8b-instruct_latest.json --judge_provider mock
else
    ${PYTHON_CMD} 03_experiment_c_sycophancy/src/multi_turn_simulator.py --backend ollama --max_topics 5 --turns 10
    ${PYTHON_CMD} 03_experiment_c_sycophancy/src/run_tier2_judge.py --simulation_file 03_experiment_c_sycophancy/outputs/multi_turn_simulation_llama-3.1-8b-instruct_latest.json --judge_provider ollama
fi

# Step 5: Experiment D (Model Locality on 155 Disputed Territories)
echo -e "\n${GREEN}[Step 5/7] Running Experiment D (Geopolitical Neutrality & BorderLines)...${NC}"
${PYTHON_CMD} 04_experiment_d_locality/src/borderlines_prompt_generator.py
${PYTHON_CMD} 04_experiment_d_locality/src/borderlines_evaluator.py --backend mock --max_samples 5
${PYTHON_CMD} 04_experiment_d_locality/src/analyze_locality_results.py

# Step 6: PRISM Defense (Constitutional & Reflection Critic Mitigation)
echo -e "\n${GREEN}[Step 6/7] Running PRISM Defense Framework Evaluation...${NC}"
${PYTHON_CMD} 05_prism_defense/src/prism_defense.py --mode full_prism --backend mock --max_conversations 1 --cooldown_sec 0.0 --output_dir 05_prism_defense/outputs/test_mock
${PYTHON_CMD} 05_prism_defense/src/evaluate_prism_mitigations.py

# Step 7: Publication Figure Generation
echo -e "\n${GREEN}[Step 7/7] Generating Publication Figures (Figures 1-10)...${NC}"
${PYTHON_CMD} 03_experiment_c_sycophancy/src/generate_paper_figures.py

echo -e "\n${GREEN}====================================================================${NC}"
echo -e "${GREEN}  ALL EXPERIMENTS & EVALUATIONS COMPLETED SUCCESSFULLY!             ${NC}"
echo -e "${GREEN}====================================================================${NC}"
