from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import joblib
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)


LABEL_TO_ID = {
    "definite": 0,
    "indefinite": 1,
}

ID_TO_LABEL = {value: key for key, value in LABEL_TO_ID.items()}


def load_split(path: Path) -> tuple[list[str], list[int], pd.DataFrame]:
    data = pd.read_csv(path)
    sentences = data["sentence"].tolist()
    labels = data["label"].map(LABEL_TO_ID).tolist()
    return sentences, labels, data


def evaluate(
    classifier: LogisticRegression,
    embeddings,
    labels: list[int],
    data: pd.DataFrame,
    split_name: str,
) -> dict:
    predictions = classifier.predict(embeddings)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels,
        predictions,
        average="weighted",
        zero_division=0,
    )

    return {
        "split": split_name,
        "accuracy": accuracy_score(labels, predictions),
        "precision_weighted": precision,
        "recall_weighted": recall,
        "f1_weighted": f1,
        "confusion_matrix": confusion_matrix(labels, predictions).tolist(),
        "classification_report": classification_report(
            labels,
            predictions,
            target_names=[ID_TO_LABEL[0], ID_TO_LABEL[1]],
            zero_division=0,
            output_dict=True,
        ),
        "by_object_type": evaluate_by_object_type(data, labels, predictions),
    }


def evaluate_by_object_type(
    data: pd.DataFrame,
    labels: list[int],
    predictions,
) -> dict[str, dict[str, float | int]]:
    results = {}
    evaluation_data = data.copy()
    evaluation_data["gold_id"] = labels
    evaluation_data["prediction_id"] = predictions
    evaluation_data["correct"] = evaluation_data["gold_id"] == evaluation_data["prediction_id"]

    for object_type, group in evaluation_data.groupby("object_type"):
        group_labels = group["gold_id"].tolist()
        group_predictions = group["prediction_id"].tolist()
        precision, recall, f1, _ = precision_recall_fscore_support(
            group_labels,
            group_predictions,
            average="weighted",
            zero_division=0,
        )
        results[object_type] = {
            "accuracy": float(group["correct"].mean()),
            "precision_weighted": float(precision),
            "recall_weighted": float(recall),
            "f1_weighted": float(f1),
            "support": int(len(group)),
        }

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a baseline classifier on Hungarian conjugation embeddings."
    )
    parser.add_argument("--train-csv", type=Path, default=Path("data/train.csv"))
    parser.add_argument("--validation-csv", type=Path, default=Path("data/validation.csv"))
    parser.add_argument("--test-csv", type=Path, default=Path("data/test.csv"))
    parser.add_argument("--model-dir", type=Path, default=Path("models/linear_reg"))
    parser.add_argument(
        "--embedding-model",
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        help="Sentence embedding model from Hugging Face.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.model_dir.mkdir(parents=True, exist_ok=True)

    train_sentences, train_labels, train_data = load_split(args.train_csv)
    validation_sentences, validation_labels, validation_data = load_split(args.validation_csv)
    test_sentences, test_labels, test_data = load_split(args.test_csv)

    embedding_model = SentenceTransformer(args.embedding_model)

    train_embeddings = embedding_model.encode(
        train_sentences,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    validation_embeddings = embedding_model.encode(
        validation_sentences,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    test_embeddings = embedding_model.encode(
        test_sentences,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    classifier = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )
    classifier.fit(train_embeddings, train_labels)

    metrics = {
        "embedding_model": args.embedding_model,
        "classifier": "LogisticRegression",
        "labels": ID_TO_LABEL,
        "validation": evaluate(
            classifier,
            validation_embeddings,
            validation_labels,
            validation_data,
            "validation",
        ),
        "test": evaluate(classifier, test_embeddings, test_labels, test_data, "test"),
    }

    joblib.dump(classifier, args.model_dir / "classifier.joblib")
    joblib.dump(LABEL_TO_ID, args.model_dir / "label_to_id.joblib")

    with (args.model_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, ensure_ascii=False, indent=2)

    print("Baseline training complete.")
    print(f"Validation accuracy: {metrics['validation']['accuracy']:.3f}")
    print(f"Test accuracy: {metrics['test']['accuracy']:.3f}")
    print(f"Saved classifier and metrics to {args.model_dir}")


if __name__ == "__main__":
    main()
