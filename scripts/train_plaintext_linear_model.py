"""
Train/export a plaintext linear model for the FHE demo.

This script supports two modes:
1. Real labels: pass --labels-csv with columns image,label.
2. Demo labels: omit --labels-csv and the script creates deterministic pseudo
   labels from image features. This is useful for classroom/demo workflows only.

The exported JSON model can be consumed by scripts/medical_fhe_pipeline.py and
scripts/benchmark_tenseal.py.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

try:
    from medical_fhe_pipeline import (
        DEFAULT_DATA_DIR,
        DEFAULT_MODEL_PATH,
        FEATURE_NAMES,
        LinearTriageModel,
        extract_xray_features,
        list_image_paths,
        load_grayscale_image,
        save_triage_model,
    )
except ImportError:
    from scripts.medical_fhe_pipeline import (
        DEFAULT_DATA_DIR,
        DEFAULT_MODEL_PATH,
        FEATURE_NAMES,
        LinearTriageModel,
        extract_xray_features,
        list_image_paths,
        load_grayscale_image,
        save_triage_model,
    )


def load_dataset(data_dir: Path) -> tuple[list[Path], np.ndarray]:
    paths = list_image_paths(data_dir)
    if not paths:
        raise FileNotFoundError(f"No images found in {data_dir}")

    features = [extract_xray_features(load_grayscale_image(path)) for path in paths]
    return paths, np.vstack(features)


def load_labels(labels_csv: Path, image_paths: list[Path]) -> np.ndarray:
    labels_by_name: dict[str, int] = {}
    with labels_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"image", "label"}
        if not required.issubset(reader.fieldnames or set()):
            raise ValueError("labels CSV must contain columns: image,label")
        for row in reader:
            labels_by_name[Path(row["image"]).name] = int(row["label"])

    missing = [path.name for path in image_paths if path.name not in labels_by_name]
    if missing:
        raise ValueError(f"Missing labels for: {missing}")

    return np.asarray([labels_by_name[path.name] for path in image_paths], dtype=np.int64)


def make_demo_labels(features: np.ndarray) -> np.ndarray:
    # Pseudo labels produce a non-trivial separator for demos. They are not
    # medical labels and must be replaced for real experiments.
    risk_proxy = (
        1.8 * features[:, FEATURE_NAMES.index("std_intensity")]
        + 2.4 * features[:, FEATURE_NAMES.index("edge_energy")]
        + 0.8 * features[:, FEATURE_NAMES.index("dark_ratio")]
        - 0.7 * features[:, FEATURE_NAMES.index("mean_intensity")]
    )
    threshold = float(np.median(risk_proxy))
    return (risk_proxy >= threshold).astype(np.int64)


def train_logistic_regression(features: np.ndarray, labels: np.ndarray) -> tuple[np.ndarray, float]:
    if len(np.unique(labels)) < 2:
        raise ValueError("Training labels must contain at least two classes.")

    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
    except ImportError as exc:
        raise RuntimeError(
            "scikit-learn is required for training. Install dependencies with "
            "`pip install -r requirements.txt`."
        ) from exc

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    classifier = LogisticRegression(C=1.0, solver="liblinear", random_state=7)
    classifier.fit(scaled, labels)

    # Fold standardization into a single raw-feature linear model:
    # coef * ((x - mean) / scale) + intercept.
    coef_scaled = classifier.coef_[0]
    scale = np.where(scaler.scale_ == 0.0, 1.0, scaler.scale_)
    weights = coef_scaled / scale
    bias = float(classifier.intercept_[0] - np.sum(coef_scaled * scaler.mean_ / scale))
    return weights.astype(float), bias


def build_model(weights: np.ndarray, bias: float, labels_source: str) -> LinearTriageModel:
    return LinearTriageModel(
        name="trained_xray_linear_triage",
        feature_names=FEATURE_NAMES.copy(),
        weights=[float(value) for value in weights],
        bias=float(bias),
        threshold=0.5,
        description=(
            "Plaintext logistic-regression model exported for TenSEAL encrypted scoring. "
            f"Labels source: {labels_source}. Not validated for clinical use."
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train/export a linear model for FHE scoring.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--labels-csv", type=Path, default=None)
    parser.add_argument("--output-model", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Train and print weights without writing the model JSON.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_paths, features = load_dataset(args.data_dir)
    if args.labels_csv:
        labels = load_labels(args.labels_csv, image_paths)
        labels_source = str(args.labels_csv)
    else:
        labels = make_demo_labels(features)
        labels_source = "deterministic pseudo-labels from image statistics"

    weights, bias = train_logistic_regression(features, labels)
    model = build_model(weights, bias, labels_source)

    print(f"Images: {len(image_paths)}")
    print(f"Positive labels: {int(labels.sum())}/{len(labels)}")
    print(f"Bias: {model.bias:.6f}")
    print("Weights:")
    for name, weight in zip(model.feature_names, model.weights, strict=True):
        print(f"  {name:18} {weight: .6f}")

    if not args.dry_run:
        save_triage_model(model, args.output_model)
        print()
        print(f"Wrote model to {args.output_model}")


if __name__ == "__main__":
    main()
