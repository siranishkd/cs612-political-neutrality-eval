"""
rewrite_prompts.py
------------------
Experiment B: 4-Method Prompt Rewriting & Perturbation Engine.
Expands 200 base PARETO questions into a 1,000-question robustness dataset:
  1. Typo: Rule-based character transposition / keystroke perturbation.
  2. Synonym Swap: Controlled lexical substitution preserving semantic valence.
  3. Restructured Sentence: Syntactic reordering / topicalization ("Regarding X, ...").
  4. Paraphrase: Semantic rephrasing ("What do you think about X?").

Reproduces Table 5 from the CS612 Final Report.
"""

import os
import sys
import json
import re
import random
from pathlib import Path
from typing import List, Dict, Any

# Dynamic relative path setup
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from common.config import EXPERIMENT_A_DIR, EXPERIMENT_B_DIR


SYNONYM_MAP = {
    "opinion": "view",
    "think": "believe",
    "favor": "support",
    "oppose": "disagree with",
    "government": "state authorities",
    "policy": "regulation",
    "country": "nation",
    "laws": "regulations",
    "rights": "freedoms",
    "public": "civic",
    "funding": "financial support",
    "schools": "educational institutions",
    "wages": "earnings",
    "allow": "permit",
}


def apply_typo(text: str) -> str:
    """Creates a realistic typographic perturbation (character transposition)."""
    words = text.split()
    target_words = [i for i, w in enumerate(words) if len(w) > 4 and w.isalpha()]
    if not target_words:
        target_words = [i for i, w in enumerate(words) if len(w) > 3]
    if not target_words:
        return text

    idx = random.choice(target_words)
    word = list(words[idx])
    # Swap two adjacent internal characters
    if len(word) >= 4:
        pos = random.randint(1, len(word) - 3)
        word[pos], word[pos + 1] = word[pos + 1], word[pos]
    words[idx] = "".join(word)
    return " ".join(words)


def apply_synonym_swap(text: str) -> str:
    """Substitutes key political / policy nouns or verbs with exact synonyms."""
    res = text
    swapped = False
    for k, v in SYNONYM_MAP.items():
        pattern = re.compile(rf"\b{k}\b", re.IGNORECASE)
        if pattern.search(res):
            res = pattern.sub(v, res, count=1)
            swapped = True
            break
    if not swapped:
        res = re.sub(r"\bWhat is your opinion on\b", "What is your view regarding", res, flags=re.IGNORECASE)
    return res


def apply_sentence_restructuring(text: str) -> str:
    """Restructures sentence into topicalized clause ('Regarding X, what is your view?')."""
    clean = text.rstrip("?. ")
    # Match patterns like "What is your opinion on X" or "Do you support X"
    m = re.search(r"(?:What (?:is your opinion on|do you think about)|Do you (?:favor|support|oppose))\s+(.+)", clean, re.IGNORECASE)
    if m:
        target = m.group(1).strip()
        return f"Regarding {target}, what is your opinion?"
    return f"Regarding this matter, {text}"


def apply_paraphrase(text: str) -> str:
    """Generates standard semantic paraphrase."""
    clean = text.rstrip("?. ")
    m = re.search(r"(?:What is your opinion on|Do you favor or oppose|What do you think about)\s+(.+)", clean, re.IGNORECASE)
    if m:
        target = m.group(1).strip()
        return f"What are the arguments and your perspective concerning {target}?"
    return f"How should one evaluate the following policy question: {clean}?"


def build_1000q_dataset(input_json_path: Path, output_json_path: Path) -> List[Dict[str, Any]]:
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize items
    base_questions = []
    for item in data:
        q_text = item.get("valenced_q") or item.get("topic_q") or item.get("prompt") or item.get("question") or item.get("text", "")
        q_id = item.get("id", item.get("slug", f"q_{len(base_questions)+1:03d}"))
        cluster = item.get("cluster", item.get("topic_cluster", "General"))
        if q_text:
            base_questions.append({
                "id": q_id,
                "cluster": cluster,
                "original": q_text.strip()
            })

    # Take 200 base questions
    base_questions = base_questions[:200]
    print(f"Building 1,000-question perturbation dataset from {len(base_questions)} base questions...")

    random.seed(42)
    dataset = []

    for item in base_questions:
        orig = item["original"]
        typo = apply_typo(orig)
        synonym = apply_synonym_swap(orig)
        restructured = apply_sentence_restructuring(orig)
        paraphrase = apply_paraphrase(orig)

        record = {
            "id": item["id"],
            "cluster": item["cluster"],
            "variants": {
                "original": orig,
                "typo": typo,
                "synonym_swap": synonym,
                "sentence_restructuring": restructured,
                "paraphrase": paraphrase
            }
        }
        dataset.append(record)

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)

    print(f"Successfully generated {len(dataset)} items (5 variants each = {len(dataset)*5} total prompts).")
    print(f"Saved dataset to: {output_json_path}")
    return dataset


if __name__ == "__main__":
    in_file = EXPERIMENT_A_DIR / "data" / "yearam_pareto_200q.json"
    out_file = EXPERIMENT_B_DIR / "data" / "robustness_1000q_dataset.json"
    build_1000q_dataset(in_file, out_file)
