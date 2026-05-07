from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

import gradio as gr
import joblib
from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_DIR = Path("models/baseline")

LABEL_TEXT = {
    "definite": "Definite conjugation",
    "indefinite": "Indefinite conjugation",
}

EXAMPLES = [
    "[VERB] a könyvet.",
    "[VERB] egy könyvet.",
    "A tanár [VERB] mindenkit.",
    "A tanár [VERB] mindet.",
    "Tegnap este [VERB] Pétert.",
    "Ma nem [VERB] semmit.",
]


embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
classifier = joblib.load(MODEL_DIR / "classifier.joblib")
label_to_id = joblib.load(MODEL_DIR / "label_to_id.joblib")
id_to_label = {label_id: label for label, label_id in label_to_id.items()}


def predict(sentence: str) -> tuple[dict[str, float], str]:
    sentence = sentence.strip()
    if not sentence:
        return {}, "Enter a Hungarian sentence with `[VERB]` marking the missing verb."

    embedding = embedding_model.encode(
        [sentence],
        normalize_embeddings=True,
    )

    probabilities = classifier.predict_proba(embedding)[0]
    scores = {
        LABEL_TEXT[id_to_label[index]]: float(probability)
        for index, probability in enumerate(probabilities)
    }

    best_index = int(probabilities.argmax())
    best_label = id_to_label[best_index]
    confidence = probabilities[best_index]

    explanation = (
        f"Prediction: **{LABEL_TEXT[best_label]}**\n\n"
        f"Confidence: **{confidence:.2%}**\n\n"
        "The model uses multilingual sentence embeddings and a Logistic Regression classifier "
        "trained on masked Hungarian sentence contexts."
    )
    return scores, explanation


with gr.Blocks(title="Hungarian Conjugation Classifier") as demo:
    gr.Markdown(
        """
        # Hungarian Definite vs. Indefinite Conjugation Classifier

        Enter a Hungarian sentence where the missing verb is written as `[VERB]`.
        The model predicts whether the context requires definite or indefinite conjugation.
        """
    )

    with gr.Row():
        sentence_input = gr.Textbox(
            label="Sentence",
            placeholder="Example: [VERB] a könyvet.",
            lines=2,
        )

    with gr.Row():
        predict_button = gr.Button("Classify", variant="primary")

    with gr.Row():
        label_output = gr.Label(label="Prediction scores", num_top_classes=2)
        explanation_output = gr.Markdown()

    gr.Examples(
        examples=EXAMPLES,
        inputs=sentence_input,
        label="Try examples",
    )

    predict_button.click(
        fn=predict,
        inputs=sentence_input,
        outputs=[label_output, explanation_output],
    )
    sentence_input.submit(
        fn=predict,
        inputs=sentence_input,
        outputs=[label_output, explanation_output],
    )


if __name__ == "__main__":
    demo.launch()
