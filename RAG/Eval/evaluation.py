
  faithfulness       — Is the answer grounded in the retrieved context?
                       (measures hallucination, no ground truth needed)
  answer_relevancy   — Is the answer actually relevant to the question?
                       (no ground truth needed)
  context_precision  — Of the retrieved chunks, how many were actually useful?
                       (no ground truth needed)
  context_recall     — Was all necessary information retrieved?
                       (REQUIRES ground truth reference answers)
Usage:
  from Eval.evaluation import run_ragas_evaluation, save_eval_results
  scores = run_ragas_evaluation(
      questions=["What is transformer attention?"],
      answers=["Attention allows models to..."],
      contexts=[["Paper 1 passage...", "Paper 2 passage..."]],
  )
  save_eval_results(scores, "eval_results.json")
"""
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
# ── Build HuggingFace Dataset from RAG outputs ────────────────────────────────
def build_eval_dataset(
    questions:     List[str],
    answers:       List[str],
    contexts:      List[List[str]],
    ground_truths: Optional[List[str]] = None,
) -> Dataset:
    """
    Build a HuggingFace Dataset compatible with RAGAS evaluate().
    Args:
        questions:     List of user queries
        answers:       Corresponding RAG-generated answers
        contexts:      Retrieved passages per query (list of lists of strings)
        ground_truths: Optional reference answers (needed for context_recall)
    Returns:
        A HuggingFace Dataset with the expected RAGAS column schema
    """
    data: Dict[str, list] = {
        "question": questions,
        "answer":   answers,
        "contexts": contexts,  # list of list[str] — one sublist per question
    }
    if ground_truths:
        data["ground_truth"] = ground_truths
    return Dataset.from_dict(data)
# ── Run RAGAS Evaluation ──────────────────────────────────────────────────────
def run_ragas_evaluation(
    questions:     List[str],
    answers:       List[str],
    contexts:      List[List[str]],
    ground_truths: Optional[List[str]] = None,
) -> Dict[str, Optional[float]]:
    """
    Run the RAGAS evaluation suite on RAG pipeline outputs.
    Args:
        questions:     User queries
        answers:       RAG-generated answers (from chain.answer_query)
        contexts:      Retrieved passages used to generate each answer
                       Each element is a list of strings (one per retrieved doc)
        ground_truths: Reference answers for context_recall metric (optional)
    Returns:
        Dict mapping metric name → score (0.0–1.0), or None if not computed.
    Example:
        {
          "faithfulness":      0.91,
          "answer_relevancy":  0.88,
          "context_precision": 0.76,
          "context_recall":    0.83,   # only if ground_truths provided
        }
    """
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
# ── Helper: evaluate a single RAG response ────────────────────────────────────
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