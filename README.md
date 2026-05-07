# RagozóMeter: Hungarian Conjugation Classifier

This project trains embedding-based classifiers to predict whether a masked Hungarian transitive verb context requires **definite** or **indefinite** conjugation.

Example:

```text
[VERB] a könyvet.      -> definite
[VERB] egy könyvet.    -> indefinite
[VERB] mindet.         -> definite
[VERB] mindent.        -> indefinite
```

The project was developed for Assignment 1 in Information Retrieval (5LN712), Uppsala University.

## Links

- GitHub repository: `[insert GitHub link]`
- Hugging Face dataset: `[insert Hugging Face dataset link]`
- Hugging Face demo Space: <https://huggingface.co/spaces/elintove/RagozoMeter>

## Project Overview

Hungarian has two object conjugation patterns for transitive verbs. The correct choice depends on the definiteness and grammatical type of the object, not simply on whether an object is present. For example, definite noun phrases and definite quantifiers require definite conjugation, while forms such as `mindenkit` and `mindent` trigger indefinite conjugation.

The task is framed as binary text classification:

```text
Input:  Hungarian sentence context with [VERB]
Output: definite or indefinite
```

## Dataset

The dataset is custom generated with `generate_dataset.py`.

Final dataset size:

- 1,200 total examples
- 600 definite examples
- 600 indefinite examples
- 960 training examples
- 120 validation examples
- 120 test examples

The generator controls subject distribution to better reflect Hungarian pro-drop behavior:

- 65% no explicit subject
- 27.5% noun or proper-name subject
- 7.5% pronoun subject

The dataset includes easy, medium, and tricky object categories such as definite articles, bare nouns, proper nouns, definite quantifiers, universal pronouns, negative pronouns, and demonstrative pronouns.

## Models

All classifiers use the same sentence embedding model:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Three classifiers were compared:

- Logistic Regression
- Linear SVM
- Random Forest

The best final model was **Logistic Regression**, with:

- Test accuracy: 0.85
- Macro F1: 0.85

## Results

| Model | Accuracy, 800 | Macro F1, 800 | Accuracy, 1200 | Macro F1, 1200 |
|---|---:|---:|---:|---:|
| Logistic Regression | 0.74 | 0.73 | **0.85** | **0.85** |
| Linear SVM | 0.80 | 0.80 | 0.84 | 0.84 |
| Random Forest | 0.81 | 0.81 | 0.84 | 0.84 |

The 1,200-example dataset improved all models, especially Logistic Regression. Object-type analysis showed that performance varied across grammatical categories, especially for rare or tricky object types.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate the dataset:

```bash
python generate_dataset.py --total 1200
```

Train the classifiers:

```bash
python train_baseline.py
python train_linear_svm.py
python train_random_forest.py
```

Run the Gradio app:

```bash
python app.py
```

## Files

```text
app.py                     Gradio demo for Hugging Face Spaces
generate_dataset.py        Custom dataset generator
train_baseline.py          Logistic Regression experiment
train_linear_svm.py        Linear SVM experiment
train_random_forest.py     Random Forest experiment
data/                      Train, validation, test, and full CSV files
models/                    Saved classifiers and metrics
IRass1_report_revised.tex  LaTeX report
```

## Limitations

The dataset consists of controlled, generated sentence contexts rather than naturally occurring corpus examples. The model also showed lower confidence for some unseen names and rare constructions. Future work could add more lexical variation, placeholder-based proper-name examples, multi-clause sentences, and comparison with Hungarian-specific transformer models such as huBERT or PULI-BERT.
