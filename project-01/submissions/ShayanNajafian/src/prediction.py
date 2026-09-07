"""Trusted model loading, strict input validation, and prediction helpers."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_model_bundle(model_path: Path, metadata_path: Path):
    """Load the trusted project model after checking its recorded checksum."""
    model_path = Path(model_path)
    metadata_path = Path(metadata_path)
    if not model_path.is_file():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not metadata_path.is_file():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    expected_hash = metadata.get("model_sha256")
    actual_hash = _sha256(model_path)
    if not expected_hash or actual_hash != expected_hash:
        raise ValueError("The model checksum does not match its metadata.")

    # Joblib files can execute code. Load only the trusted artifact in this repo.
    pipeline = joblib.load(model_path)
    expected_classes = sorted(int(code) for code in metadata["class_labels"])
    actual_classes = [int(code) for code in pipeline.classes_]
    if actual_classes != expected_classes:
        raise ValueError("The model classes do not match the metadata.")
    return pipeline, metadata


def validate_student_input(
    values: Mapping[str, Any],
    metadata: Mapping[str, Any],
) -> pd.DataFrame:
    """Return one ordered model row or reject an invalid submission."""
    if not isinstance(values, Mapping):
        raise ValueError("Input must map feature names to values.")

    features = list(metadata["features_in_order"])
    input_schema = metadata["input_schema"]
    missing = [feature for feature in features if feature not in values]
    unexpected = sorted(set(values) - set(features))
    errors: list[str] = []

    if missing:
        errors.append(f"Missing answers: {', '.join(missing)}")
    if unexpected:
        errors.append(f"Unexpected answers: {', '.join(unexpected)}")

    clean_row: dict[str, int] = {}
    for feature in features:
        if feature not in values:
            continue
        value = values[feature]
        if isinstance(value, (bool, np.bool_)) or not isinstance(
            value,
            (int, float, np.integer, np.floating),
        ):
            errors.append(f"{feature} must be a numeric integer code")
            continue
        if not np.isfinite(value) or float(value) != int(value):
            errors.append(f"{feature} must be a finite integer code")
            continue

        clean_value = int(value)
        allowed_values = input_schema[feature]["allowed_values"]
        if clean_value not in allowed_values:
            errors.append(
                f"{feature} must be one of {allowed_values}; "
                f"received {clean_value}"
            )
            continue
        clean_row[feature] = clean_value

    if errors:
        raise ValueError("; ".join(errors))
    return pd.DataFrame([clean_row], columns=features)


def predict_stress(
    values: Mapping[str, Any],
    pipeline,
    metadata: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one submission and return its class and probabilities."""
    model_input = validate_student_input(values, metadata)
    predicted_code = int(pipeline.predict(model_input)[0])
    probabilities = pipeline.predict_proba(model_input)[0]
    class_labels = metadata["class_labels"]

    probability_map = {
        class_labels[str(int(code))]: float(probability)
        for code, probability in zip(pipeline.classes_, probabilities)
    }
    if not np.isclose(sum(probability_map.values()), 1.0):
        raise ValueError("Model probabilities do not sum to one.")

    return {
        "predicted_code": predicted_code,
        "predicted_label": class_labels[str(predicted_code)],
        "probabilities": probability_map,
    }
