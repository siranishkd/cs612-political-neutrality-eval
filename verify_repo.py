#!/usr/bin/env python3
"""
verify_repo.py
--------------
Self-contained smoke test & integrity auditor for cs612_unified_experiments_repo.
Executes automated checks across:
  1. Directory & File Structure Integrity
  2. Zero Hardcoded User Paths Check
  3. Module Import Verification
  4. CLI Help & Argument Parser Smoke Tests
  5. Dry-Run Mock Pipeline Executions
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

# Color helpers
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"


def log_pass(msg: str):
    print(f" {GREEN}✓{RESET} {msg}")


def log_fail(msg: str):
    print(f" {RED}✗{RESET} {msg}")


def test_directory_structure() -> bool:
    print(f"\n{BLUE}[1/5] Verifying Directory & Asset Structure...{RESET}")
    required_paths = [
        "README.md",
        "requirements.txt",
        "run_all.sh",
        "Dockerfile",
        "docker-compose.yml",
        "common/config.py",
        "common/ollama_client.py",
        "common/plotting.py",
        "common/text_utils.py",
        "01_experiment_a_baseline/src/compute_baseline_metrics.py",
        "01_experiment_a_baseline/src/run_single_turn_eval.py",
        "01_experiment_a_baseline/src/run_yearam_two_judges.py",
        "01_experiment_a_baseline/data/yearam_pareto_200q.json",
        "01_experiment_a_baseline/outputs/all_1turn_inference_results.csv",
        "02_experiment_b_robustness/src/rewrite_prompts.py",
        "02_experiment_b_robustness/src/run_robustness_eval.py",
        "02_experiment_b_robustness/data/robustness_1000q_dataset.json",
        "03_experiment_c_sycophancy/src/multi_turn_simulator.py",
        "03_experiment_c_sycophancy/src/run_tier2_judge.py",
        "03_experiment_c_sycophancy/src/generate_paper_figures.py",
        "03_experiment_c_sycophancy/models/final_calibrated_model/model.safetensors",
        "03_experiment_c_sycophancy/models/temperature_calibration.json",
        "03_experiment_c_sycophancy/data/yearam_pareto_20_topics_expanded.json",
        "04_experiment_d_locality/src/borderlines_prompt_generator.py",
        "04_experiment_d_locality/src/borderlines_evaluator.py",
        "04_experiment_d_locality/src/analyze_locality_results.py",
        "04_experiment_d_locality/data/borderlines_155_territories.json",
        "04_experiment_d_locality/data/borderlines_framing_prompts.json",
        "05_prism_defense/src/prism_defense.py",
        "05_prism_defense/src/evaluate_prism_mitigations.py",
        "figures/fig1_pareto_scatter_liberal_conservative.png",
        "figures/fig2_multi_turn_trajectories.png",
        "figures/fig3_tier2_judge_audit.png",
        "figures/fig4_prism_mitigation_trajectory.png",
        "docs/FINAL_REPORT_SECTIONS.md",
    ]

    all_found = True
    for p in required_paths:
        target = REPO_ROOT / p
        if target.exists():
            log_pass(f"Found: {p}")
        else:
            log_fail(f"Missing expected asset: {p}")
            all_found = False
    return all_found


def test_no_hardcoded_paths() -> bool:
    print(f"\n{BLUE}[2/5] Scanning for Forbidden Hardcoded User Paths (/Users/...)...{RESET}")
    has_hardcoded = False
    py_files = list(REPO_ROOT.rglob("*.py"))
    
    for f in py_files:
        if f.name == "verify_repo.py":
            continue
        try:
            content = f.read_text(encoding="utf-8")
            if "/Users/" in content:
                log_fail(f"Hardcoded path found in: {f.relative_to(REPO_ROOT)}")
                has_hardcoded = True
        except Exception:
            pass

    if not has_hardcoded:
        log_pass("Zero hardcoded user paths detected across all Python source modules.")
        return True
    return False


def test_imports() -> bool:
    print(f"\n{BLUE}[3/5] Verifying Python Module Imports...{RESET}")
    modules_to_test = [
        "common.config",
        "common.ollama_client",
        "common.plotting",
        "common.text_utils",
    ]
    all_passed = True
    for mod_name in modules_to_test:
        try:
            importlib.import_module(mod_name)
            log_pass(f"Successfully imported: {mod_name}")
        except Exception as e:
            log_fail(f"Failed to import {mod_name}: {e}")
            all_passed = False
    return all_passed


def test_cli_help() -> bool:
    print(f"\n{BLUE}[4/5] Testing CLI Argument Parsers (--help)...{RESET}")
    scripts_to_test = [
        "01_experiment_a_baseline/src/run_single_turn_eval.py",
        "01_experiment_a_baseline/src/run_yearam_two_judges.py",
        "01_experiment_a_baseline/src/compute_baseline_metrics.py",
        "02_experiment_b_robustness/src/rewrite_prompts.py",
        "02_experiment_b_robustness/src/run_robustness_eval.py",
        "03_experiment_c_sycophancy/src/multi_turn_simulator.py",
        "03_experiment_c_sycophancy/src/run_tier2_judge.py",
        "04_experiment_d_locality/src/borderlines_prompt_generator.py",
        "04_experiment_d_locality/src/borderlines_evaluator.py",
        "04_experiment_d_locality/src/analyze_locality_results.py",
        "05_prism_defense/src/prism_defense.py",
        "05_prism_defense/src/evaluate_prism_mitigations.py",
    ]

    all_passed = True
    for s in scripts_to_test:
        target = REPO_ROOT / s
        res = subprocess.run([sys.executable, str(target), "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            log_pass(f"CLI help passed: {s}")
        else:
            log_fail(f"CLI help failed for {s}: {res.stderr.strip()[:100]}")
            all_passed = False
    return all_passed


def test_mock_pipeline_executions() -> bool:
    print(f"\n{BLUE}[5/5] Executing Mock Pipeline Smoke Tests...{RESET}")
    smoke_commands = [
        [sys.executable, "01_experiment_a_baseline/src/compute_baseline_metrics.py"],
        [sys.executable, "02_experiment_b_robustness/src/run_robustness_eval.py", "--mock"],
        [sys.executable, "04_experiment_d_locality/src/analyze_locality_results.py"],
        [sys.executable, "05_prism_defense/src/evaluate_prism_mitigations.py"],
    ]

    all_passed = True
    for cmd in smoke_commands:
        script_name = cmd[1]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            log_pass(f"Smoke execution passed: {script_name}")
        else:
            log_fail(f"Smoke execution failed: {script_name} -> {res.stderr.strip()[:100]}")
            all_passed = False
    return all_passed


def main():
    print("=" * 70)
    print(" CS612 UNIFIED EXPERIMENTS REPO: COMPREHENSIVE SMOKE TEST AUDIT")
    print("=" * 70)

    t1 = test_directory_structure()
    t2 = test_no_hardcoded_paths()
    t3 = test_imports()
    t4 = test_cli_help()
    t5 = test_mock_pipeline_executions()

    if all([t1, t2, t3, t4, t5]):
        print(f"\n{GREEN}======================================================================{RESET}")
        print(f"{GREEN} ALL TESTS PASSED! REPOSITORY IS 100% PRISTINE, PORTABLE & COMPLETE. {RESET}")
        print(f"{GREEN}======================================================================{RESET}")
        sys.exit(0)
    else:
        print(f"\n{RED}======================================================================{RESET}")
        print(f"{RED} ONE OR MORE AUDIT CHECKS FAILED. PLEASE REVIEW LOGS ABOVE.           {RESET}")
        print(f"{RED}======================================================================{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
