from __future__ import annotations
import json
from typing import Dict, List, Optional
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
def build_eval_dataset(
    questions:     List[str],
    answers:       List[str],
    contexts:      List[List[str]],
    ground_truths: Optional[List[str]] = None,
) -> Dataset:
    data: Dict[str, list] = {
        "question": questions,
        "answer":   answers,
        "contexts": contexts,
    }
    if ground_truths:
        data["ground_truth"] = ground_truths
    return Dataset.from_dict(data)
def run_ragas_evaluation(
    questions:     List[str],
    answers:       List[str],
    contexts:      List[List[str]],
    ground_truths: Optional[List[str]] = None,
) -> Dict[str, Optional[float]]:
    metrics = [faithfulness, answer_relevancy, context_precision]
    if ground_truths:
        metrics.append(context_recall)
    dataset = build_eval_dataset(questions, answers, contexts, ground_truths)
    result  = evaluate(dataset=dataset, metrics=metrics)
    scores: Dict[str, Optional[float]] = {
        "faithfulness":      result.get("faithfulness"),
        "answer_relevancy":  result.get("answer_relevancy"),
        "context_precision": result.get("context_precision"),
    }
    if ground_truths:
        scores["context_recall"] = result.get("context_recall")
    return scores
def evaluate_single(
    question:    str,
    answer:      str,
    contexts:    List[str],
    ground_truth: Optional[str] = None,
) -> Dict[str, Optional[float]]:
    """
    Convenience wrapper to evaluate a single question-answer pair.
    Wraps inputs into lists and calls run_ragas_evaluation().
    """
    return run_ragas_evaluation(
        questions=[question],
        answers=[answer],
        contexts=[contexts],
        ground_truths=[ground_truth] if ground_truth else None,
    )
# ── Save results to JSON ──────────────────────────────────────────────────────
def save_eval_results(
    scores:      Dict[str, Optional[float]],
    output_path: str = "eval_results.json",
) -> None:
    """Persist evaluation scores to a JSON file for tracking over time."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2, default=str)
    print(f"[evaluation] Results saved → {output_path}")
# ── CLI entry point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Quick smoke test with dummy data
    sample_scores = run_ragas_evaluation(
        questions=["What are transformers used for in NLP?"],
        answers=[
            "Transformers are used for tasks like translation, summarization, "
            "and question answering [1]. They rely on self-attention mechanisms [2]."
        ],
        contexts=[[
            "Transformers revolutionised NLP by replacing RNNs with attention mechanisms.",
            "Self-attention allows the model to weigh the importance of each token.",
        ]],
        ground_truths=[
            "Transformers are used for translation, summarisation, and QA using self-attention."
        ],
    )
    print("Evaluation scores:", sample_scores)
    save_eval_results(sample_scores)