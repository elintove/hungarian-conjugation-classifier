from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ObjectCase:
    text: str
    label: str
    object_type: str
    difficulty: str


DEFINITE_OBJECTS = [
    ObjectCase("a könyvet", "definite", "definite_article", "easy"),
    ObjectCase("az almát", "definite", "definite_article", "easy"),
    ObjectCase("a filmet", "definite", "definite_article", "easy"),
    ObjectCase("az autót", "definite", "definite_article", "easy"),
    ObjectCase("a levelet", "definite", "definite_article", "easy"),
    ObjectCase("az újságot", "definite", "definite_article", "easy"),
    ObjectCase("a vacsorát", "definite", "definite_article", "easy"),
    ObjectCase("az előadást", "definite", "definite_article", "easy"),
    ObjectCase("a piros labdát", "definite", "modified_definite_np", "easy"),
    ObjectCase("az új telefont", "definite", "modified_definite_np", "easy"),
    ObjectCase("a régi házat", "definite", "modified_definite_np", "easy"),
    ObjectCase("az utolsó kérdést", "definite", "modified_definite_np", "easy"),
    ObjectCase("ezt a könyvet", "definite", "demonstrative", "easy"),
    ObjectCase("azt a filmet", "definite", "demonstrative", "easy"),
    ObjectCase("ezt az almát", "definite", "demonstrative", "easy"),
    ObjectCase("azt a levelet", "definite", "demonstrative", "easy"),
    ObjectCase("ezt a feladatot", "definite", "demonstrative", "easy"),
    ObjectCase("azt az üzenetet", "definite", "demonstrative", "easy"),
    ObjectCase("ezt", "definite", "demonstrative_pronoun", "tricky"),
    ObjectCase("azt", "definite", "demonstrative_pronoun", "tricky"),
    ObjectCase("emezt", "definite", "demonstrative_pronoun", "tricky"),
    ObjectCase("amazt", "definite", "demonstrative_pronoun", "tricky"),
    ObjectCase("Pétert", "definite", "proper_noun", "easy"),
    ObjectCase("Annát", "definite", "proper_noun", "easy"),
    ObjectCase("Katalint", "definite", "proper_noun", "easy"),
    ObjectCase("Gábort", "definite", "proper_noun", "easy"),
    ObjectCase("Esztert", "definite", "proper_noun", "easy"),
    ObjectCase("Lászlót", "definite", "proper_noun", "easy"),
    ObjectCase("őt", "definite", "third_person_pronoun", "easy"),
    ObjectCase("őket", "definite", "third_person_pronoun", "easy"),
    ObjectCase("magát", "definite", "third_person_pronoun", "tricky"),
    ObjectCase("magukat", "definite", "third_person_pronoun", "tricky"),
    ObjectCase("mindet", "definite", "definite_quantifier", "tricky"),
    ObjectCase("mindkettőt", "definite", "definite_quantifier", "tricky"),
    ObjectCase("mindegyiket", "definite", "definite_quantifier", "tricky"),
    ObjectCase("az összeset", "definite", "definite_quantifier", "tricky"),
    ObjectCase("valamennyit", "definite", "definite_quantifier", "tricky"),
    ObjectCase("az egészet", "definite", "definite_quantifier", "tricky"),
    ObjectCase("a többit", "definite", "definite_quantifier", "tricky"),
    ObjectCase("a legtöbbet", "definite", "definite_quantifier", "tricky"),
]


INDEFINITE_OBJECTS = [
    ObjectCase("egy könyvet", "indefinite", "indefinite_article", "easy"),
    ObjectCase("egy almát", "indefinite", "indefinite_article", "easy"),
    ObjectCase("egy filmet", "indefinite", "indefinite_article", "easy"),
    ObjectCase("egy autót", "indefinite", "indefinite_article", "easy"),
    ObjectCase("egy levelet", "indefinite", "indefinite_article", "easy"),
    ObjectCase("egy újságot", "indefinite", "indefinite_article", "easy"),
    ObjectCase("egy vacsorát", "indefinite", "indefinite_article", "easy"),
    ObjectCase("egy előadást", "indefinite", "indefinite_article", "easy"),
    ObjectCase("könyvet", "indefinite", "bare_noun", "easy"),
    ObjectCase("almát", "indefinite", "bare_noun", "easy"),
    ObjectCase("filmet", "indefinite", "bare_noun", "easy"),
    ObjectCase("autót", "indefinite", "bare_noun", "easy"),
    ObjectCase("levelet", "indefinite", "bare_noun", "easy"),
    ObjectCase("újságot", "indefinite", "bare_noun", "easy"),
    ObjectCase("vacsorát", "indefinite", "bare_noun", "easy"),
    ObjectCase("előadást", "indefinite", "bare_noun", "easy"),
    ObjectCase("valakit", "indefinite", "indefinite_pronoun", "easy"),
    ObjectCase("valamit", "indefinite", "indefinite_pronoun", "easy"),
    ObjectCase("bárkit", "indefinite", "indefinite_pronoun", "easy"),
    ObjectCase("bármit", "indefinite", "indefinite_pronoun", "easy"),
    ObjectCase("akárkit", "indefinite", "indefinite_pronoun", "tricky"),
    ObjectCase("akármit", "indefinite", "indefinite_pronoun", "tricky"),
    ObjectCase("néhányat", "indefinite", "indefinite_pronoun", "tricky"),
    ObjectCase("egyvalakit", "indefinite", "indefinite_pronoun", "tricky"),
    ObjectCase("mindenkit", "indefinite", "universal_pronoun", "tricky"),
    ObjectCase("mindent", "indefinite", "universal_pronoun", "tricky"),
    ObjectCase("mindenfélét", "indefinite", "universal_pronoun", "tricky"),
    ObjectCase("minden egyes dolgot", "indefinite", "universal_pronoun", "tricky"),
    ObjectCase("senkit", "indefinite", "negative_pronoun", "tricky"),
    ObjectCase("semmit", "indefinite", "negative_pronoun", "tricky"),
    ObjectCase("semmifélét", "indefinite", "negative_pronoun", "tricky"),
    ObjectCase("egy embert sem", "indefinite", "negative_pronoun", "tricky"),
    ObjectCase("egy dolgot sem", "indefinite", "negative_pronoun", "tricky"),
    ObjectCase("néhány könyvet", "indefinite", "quantified_indefinite_np", "medium"),
    ObjectCase("több almát", "indefinite", "quantified_indefinite_np", "medium"),
    ObjectCase("sok filmet", "indefinite", "quantified_indefinite_np", "medium"),
    ObjectCase("kevés hibát", "indefinite", "quantified_indefinite_np", "medium"),
    ObjectCase("pár kérdést", "indefinite", "quantified_indefinite_np", "medium"),
    ObjectCase("néhány levelet", "indefinite", "quantified_indefinite_np", "medium"),
]




@dataclass(frozen=True)
class TemplateCase:
    text: str
    subject_type: str
    subject: str = ""


NOUN_SUBJECTS = [
    "A tanár",
    "A diák",
    "A gyerek",
    "A szomszéd",
    "Anna",
    "Péter",
    "Katalin",
    "Gábor",
    "A diákok",
    "A szülők",
]


PRONOUN_SUBJECTS = [
    "Én",
    "Te",
    "Mi",
    "Ők",
]


NO_SUBJECT_TEMPLATES = [
    TemplateCase("[VERB] {object}.", "none"),
    TemplateCase("Ma [VERB] {object}.", "none"),
    TemplateCase("Tegnap [VERB] {object}.", "none"),
    TemplateCase("Gyakran [VERB] {object}.", "none"),
    TemplateCase("Otthon [VERB] {object}.", "none"),
    TemplateCase("Reggel [VERB] {object}.", "none"),
    TemplateCase("Este [VERB] {object}.", "none"),
    TemplateCase("Most [VERB] {object}.", "none"),
    TemplateCase("{object_cap} [VERB].", "none"),
    TemplateCase("{object_cap} ma [VERB].", "none"),
    TemplateCase("{object_cap} tegnap [VERB].", "none"),
    TemplateCase("{object_cap} gyakran [VERB].", "none"),
    TemplateCase("Az iskolában [VERB] {object}.", "none"),
    TemplateCase("A boltban [VERB] {object}.", "none"),
    TemplateCase("A parkban [VERB] {object}.", "none"),
    TemplateCase("Később [VERB] {object}.", "none"),
]


NO_SUBJECT_NEGATIVE_TEMPLATES = [
    TemplateCase("Nem [VERB] {object}.", "none"),
    TemplateCase("Ma nem [VERB] {object}.", "none"),
    TemplateCase("Soha nem [VERB] {object}.", "none"),
    TemplateCase("{object_cap} nem [VERB].", "none"),
    TemplateCase("{object_cap} ma nem [VERB].", "none"),
]


NOUN_SUBJECT_PATTERNS = [
    "{subject} [VERB] {object}.",
    "{subject} ma [VERB] {object}.",
    "{subject} gyakran [VERB] {object}.",
    "{subject} az iskolában [VERB] {object}.",
    "{object_cap} {subject_lower} [VERB].",
    "{object_cap} ma {subject_lower} [VERB].",
]


NOUN_SUBJECT_NEGATIVE_PATTERNS = [
    "{subject} nem [VERB] {object}.",
    "{subject} ma nem [VERB] {object}.",
    "{object_cap} {subject_lower} nem [VERB].",
]


PRONOUN_SUBJECT_PATTERNS = [
    "{subject} [VERB] {object}.",
    "{subject} ma [VERB] {object}.",
    "{object_cap} {subject_lower} [VERB].",
]


PRONOUN_SUBJECT_NEGATIVE_PATTERNS = [
    "{subject} nem [VERB] {object}.",
    "{subject} ma nem [VERB] {object}.",
    "{object_cap} {subject_lower} nem [VERB].",
]


SPLIT_TEMPLATES = {
    "train": {
        "none": NO_SUBJECT_TEMPLATES[:12],
        "noun": NO_SUBJECT_TEMPLATES[:0],
        "pronoun": NO_SUBJECT_TEMPLATES[:0],
    },
    "validation": {
        "none": [
            TemplateCase("Délután [VERB] {object}.", "none"),
            TemplateCase("Hétvégén [VERB] {object}.", "none"),
            TemplateCase("{object_cap} délután [VERB].", "none"),
            TemplateCase("A teremben [VERB] {object}.", "none"),
        ],
        "noun": NO_SUBJECT_TEMPLATES[:0],
        "pronoun": NO_SUBJECT_TEMPLATES[:0],
    },
    "test": {
        "none": [
            TemplateCase("Minden nap [VERB] {object}.", "none"),
            TemplateCase("Tegnap este [VERB] {object}.", "none"),
            TemplateCase("{object_cap} az iskolában [VERB].", "none"),
            TemplateCase("Azt hiszem, [VERB] {object}.", "none"),
        ],
        "noun": NO_SUBJECT_TEMPLATES[:0],
        "pronoun": NO_SUBJECT_TEMPLATES[:0],
    },
}


FIELDNAMES = [
    "sentence",
    "label",
    "object_type",
    "object",
    "difficulty",
    "subject_type",
    "subject",
    "template_id",
    "split",
]


def capitalize_first(text: str) -> str:
    return text[:1].upper() + text[1:]


def subject_inside_sentence(text: str) -> str:
    if text in PRONOUN_SUBJECTS or text.startswith(("A ", "Az ")):
        return text[:1].lower() + text[1:]
    return text


def is_negative_object(obj: ObjectCase) -> bool:
    return obj.object_type == "negative_pronoun"


def make_noun_templates(split: str) -> list[TemplateCase]:
    patterns = NOUN_SUBJECT_PATTERNS
    if split == "validation":
        patterns = [
            "{subject} délután [VERB] {object}.",
            "{object_cap} délután {subject_lower} [VERB].",
        ]
    elif split == "test":
        patterns = [
            "{subject} tegnap este [VERB] {object}.",
            "{object_cap} az iskolában {subject_lower} [VERB].",
        ]

    return [
        TemplateCase(pattern, "noun", subject)
        for subject in NOUN_SUBJECTS
        for pattern in patterns
    ]


def make_pronoun_templates(split: str) -> list[TemplateCase]:
    patterns = PRONOUN_SUBJECT_PATTERNS
    if split == "validation":
        patterns = [
            "{subject} délután [VERB] {object}.",
            "{object_cap} délután {subject_lower} [VERB].",
        ]
    elif split == "test":
        patterns = [
            "{subject} tegnap este [VERB] {object}.",
            "{object_cap} az iskolában {subject_lower} [VERB].",
        ]

    return [
        TemplateCase(pattern, "pronoun", subject)
        for subject in PRONOUN_SUBJECTS
        for pattern in patterns
    ]


def negative_versions(templates: list[TemplateCase], subject_type: str) -> list[TemplateCase]:
    if subject_type == "none":
        return NO_SUBJECT_NEGATIVE_TEMPLATES

    patterns = (
        NOUN_SUBJECT_NEGATIVE_PATTERNS
        if subject_type == "noun"
        else PRONOUN_SUBJECT_NEGATIVE_PATTERNS
    )
    subjects = NOUN_SUBJECTS if subject_type == "noun" else PRONOUN_SUBJECTS
    return [
        TemplateCase(pattern, subject_type, subject)
        for subject in subjects
        for pattern in patterns
    ]


def make_candidates(
    objects: list[ObjectCase],
    split: str,
    subject_type: str,
) -> list[dict[str, str]]:
    if subject_type == "none":
        templates = SPLIT_TEMPLATES[split]["none"]
    elif subject_type == "noun":
        templates = make_noun_templates(split)
    elif subject_type == "pronoun":
        templates = make_pronoun_templates(split)
    else:
        raise ValueError(f"Unknown subject type: {subject_type}")

    rows = []
    for obj in objects:
        active_templates = negative_versions(templates, subject_type) if is_negative_object(obj) else templates
        for index, template in enumerate(active_templates):
            subject_lower = subject_inside_sentence(template.subject)
            sentence = template.text.format(
                object=obj.text,
                object_cap=capitalize_first(obj.text),
                subject=template.subject,
                subject_lower=subject_lower,
            )
            rows.append(
                {
                    "sentence": sentence,
                    "label": obj.label,
                    "object_type": obj.object_type,
                    "object": obj.text,
                    "difficulty": obj.difficulty,
                    "subject_type": template.subject_type,
                    "subject": template.subject,
                    "template_id": f"{split}_{subject_type}_{index:03d}",
                    "split": split,
                }
            )
    return rows


def sample_balanced(
    rng: random.Random,
    split: str,
    subject_type: str,
    count: int,
) -> list[dict[str, str]]:
    if count % 2 != 0:
        raise ValueError("Each subject-type count must be even to preserve label balance.")

    definite_candidates = make_candidates(DEFINITE_OBJECTS, split, subject_type)
    indefinite_candidates = make_candidates(INDEFINITE_OBJECTS, split, subject_type)
    per_label = count // 2

    if len(definite_candidates) < per_label:
        raise ValueError(f"Not enough definite {subject_type} candidates for {split}.")
    if len(indefinite_candidates) < per_label:
        raise ValueError(f"Not enough indefinite {subject_type} candidates for {split}.")

    rows = weighted_sample(rng, definite_candidates, per_label)
    rows.extend(weighted_sample(rng, indefinite_candidates, per_label))
    return rows


def candidate_weight(row: dict[str, str]) -> float:
    if row["difficulty"] == "tricky":
        return 3.0
    if row["difficulty"] == "medium":
        return 1.5
    return 1.0


def weighted_sample(
    rng: random.Random,
    candidates: list[dict[str, str]],
    count: int,
) -> list[dict[str, str]]:
    # Weighted sampling without replacement. Higher scores are more likely
    # for higher-weighted candidates, but each sentence can appear only once.
    scored_candidates = [
        (rng.random() ** (1.0 / candidate_weight(candidate)), candidate)
        for candidate in candidates
    ]
    scored_candidates.sort(key=lambda item: item[0], reverse=True)
    return [candidate for _, candidate in scored_candidates[:count]]


def split_subject_counts(total: int) -> dict[str, int]:
    no_subject = int(total * 0.65)
    noun_subject = int(total * 0.275)
    pronoun_subject = total - no_subject - noun_subject

    counts = {
        "none": no_subject,
        "noun": noun_subject,
        "pronoun": pronoun_subject,
    }

    for key, value in counts.items():
        if value % 2:
            counts[key] = value + 1

    overflow = sum(counts.values()) - total
    while overflow > 0:
        for key in ["none", "noun", "pronoun"]:
            if overflow == 0:
                break
            if counts[key] >= 2:
                counts[key] -= 2
                overflow -= 2

    return counts


def build_split(rng: random.Random, split: str, total: int) -> list[dict[str, str]]:
    counts = split_subject_counts(total)
    rows = []
    for subject_type, count in counts.items():
        rows.extend(sample_balanced(rng, split, subject_type, count))

    rng.shuffle(rows)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Hungarian conjugation dataset with a controlled subject mix."
    )
    parser.add_argument(
        "--total",
        type=int,
        default=1200,
        help="Total number of examples. Must be divisible by 20.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data"),
        help="Directory where CSV files will be written.",
    )
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.total % 20 != 0:
        raise ValueError("--total must be divisible by 20 for an 80/10/10 split.")

    rng = random.Random(args.seed)
    train_count = int(args.total * 0.8)
    validation_count = int(args.total * 0.1)
    test_count = args.total - train_count - validation_count

    train_rows = build_split(rng, "train", train_count)
    validation_rows = build_split(rng, "validation", validation_count)
    test_rows = build_split(rng, "test", test_count)
    full_rows = train_rows + validation_rows + test_rows

    write_csv(args.out_dir / "train.csv", train_rows)
    write_csv(args.out_dir / "validation.csv", validation_rows)
    write_csv(args.out_dir / "test.csv", test_rows)
    write_csv(args.out_dir / "full_dataset.csv", full_rows)

    for name, rows in [
        ("train", train_rows),
        ("validation", validation_rows),
        ("test", test_rows),
        ("full", full_rows),
    ]:
        counts = {
            subject_type: sum(row["subject_type"] == subject_type for row in rows)
            for subject_type in ["none", "noun", "pronoun"]
        }
        definite = sum(row["label"] == "definite" for row in rows)
        indefinite = sum(row["label"] == "indefinite" for row in rows)
        print(
            f"{name}: {len(rows)} rows "
            f"(definite={definite}, indefinite={indefinite}, "
            f"no_subject={counts['none']}, noun_subject={counts['noun']}, "
            f"pronoun_subject={counts['pronoun']})"
        )


if __name__ == "__main__":
    main()
