"""
Medical image FHE demo with TenSEAL.

Case study: a hospital/client encrypts a compact chest X-ray feature vector,
an untrusted cloud service evaluates a linear triage score on ciphertext, and
only the client decrypts the result.

This is an educational prototype, not a diagnostic model.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageOps

try:
    import tenseal as ts
except ImportError:  # TenSEAL is optional for tests and documentation builds.
    ts = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "chestxray_sample"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "triage_linear_model.json"

FEATURE_NAMES = [
    "mean_intensity",
    "std_intensity",
    "upper_left_mean",
    "upper_right_mean",
    "lower_left_mean",
    "lower_right_mean",
    "center_mean",
    "edge_energy",
    "bright_ratio",
    "dark_ratio",
]


@dataclass(frozen=True)
class LinearTriageModel:
    name: str
    feature_names: list[str]
    weights: list[float]
    bias: float
    threshold: float = 0.5
    description: str = ""


@dataclass(frozen=True)
class InferenceResult:
    image: str
    plaintext_logit: float
    plaintext_probability: float
    encrypted_logit: float | None
    encrypted_probability: float | None
    abs_logit_error: float | None
    triage_flag: bool
    features: dict[str, float]


def list_image_paths(data_dir: Path) -> list[Path]:
    suffixes = {".jpg", ".jpeg", ".png", ".bmp"}
    return sorted(path for path in data_dir.iterdir() if path.suffix.lower() in suffixes)


def load_grayscale_image(path: Path, size: int = 32) -> np.ndarray:
    image = Image.open(path)
    image = ImageOps.grayscale(image)
    image = image.resize((size, size), Image.Resampling.BILINEAR)
    arr = np.asarray(image, dtype=np.float64) / 255.0
    return arr


def extract_xray_features(image: np.ndarray) -> np.ndarray:
    if image.ndim != 2:
        raise ValueError("Expected a single-channel grayscale image.")

    h, w = image.shape
    h2, w2 = h // 2, w // 2
    center = image[h // 4 : 3 * h // 4, w // 4 : 3 * w // 4]

    dx = np.diff(image, axis=1)
    dy = np.diff(image, axis=0)
    edge_energy = (float(np.mean(np.abs(dx))) + float(np.mean(np.abs(dy)))) / 2.0

    features = np.array(
        [
            float(np.mean(image)),
            float(np.std(image)),
            float(np.mean(image[:h2, :w2])),
            float(np.mean(image[:h2, w2:])),
            float(np.mean(image[h2:, :w2])),
            float(np.mean(image[h2:, w2:])),
            float(np.mean(center)),
            edge_energy,
            float(np.mean(image > 0.78)),
            float(np.mean(image < 0.18)),
        ],
        dtype=np.float64,
    )
    return features


def build_demo_triage_model() -> LinearTriageModel:
    # Fixed, explainable weights for a reproducible privacy demo. They are not
    # fitted labels and must not be interpreted as clinical evidence.
    weights = [
        -1.15,  # global brightness
        1.25,  # contrast
        -0.35,
        -0.35,
        0.25,
        0.25,
        -0.55,
        3.20,  # structural edges
        0.60,
        0.90,
    ]
    return LinearTriageModel(
        name="demo_xray_linear_triage",
        feature_names=FEATURE_NAMES.copy(),
        weights=weights,
        bias=0.10,
        threshold=0.5,
        description=(
            "Fixed educational weights for privacy-preserving X-ray triage scoring. "
            "Not trained for clinical diagnosis."
        ),
    )


def validate_model(model: LinearTriageModel) -> None:
    if len(model.feature_names) != len(model.weights):
        raise ValueError(
            "Model feature_names and weights must have the same length: "
            f"{len(model.feature_names)} != {len(model.weights)}"
        )
    if model.feature_names != FEATURE_NAMES:
        raise ValueError(
            "Model feature order does not match the feature extractor. "
            f"Expected {FEATURE_NAMES}, got {model.feature_names}"
        )
    if not 0.0 <= model.threshold <= 1.0:
        raise ValueError(f"Model threshold must be in [0, 1], got {model.threshold}")


def load_triage_model(path: Path = DEFAULT_MODEL_PATH) -> LinearTriageModel:
    if not path.exists():
        return build_demo_triage_model()

    payload = json.loads(path.read_text(encoding="utf-8"))
    model = LinearTriageModel(
        name=str(payload.get("name", "unnamed_linear_triage_model")),
        feature_names=list(payload["feature_names"]),
        weights=[float(value) for value in payload["weights"]],
        bias=float(payload["bias"]),
        threshold=float(payload.get("threshold", 0.5)),
        description=str(payload.get("description", "")),
    )
    validate_model(model)
    return model


def save_triage_model(model: LinearTriageModel, path: Path) -> None:
    validate_model(model)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(model), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def plaintext_linear_logit(features: np.ndarray, model: LinearTriageModel) -> float:
    validate_model(model)
    weights = np.asarray(model.weights, dtype=np.float64)
    return float(np.dot(features, weights) + model.bias)


def create_ckks_context():
    if ts is None:
        raise RuntimeError(
            "TenSEAL is not installed. Install dependencies with `pip install -r requirements.txt`."
        )

    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60],
    )
    context.global_scale = 2**40
    context.generate_galois_keys()
    return context


def encrypted_linear_logit(
    features: np.ndarray,
    model: LinearTriageModel,
    context,
) -> float:
    encrypted_features = ts.ckks_vector(context, features.tolist())
    encrypted_logit = encrypted_features.dot(model.weights) + model.bias
    return float(encrypted_logit.decrypt()[0])


def run_inference(
    image_paths: Iterable[Path],
    model: LinearTriageModel,
    use_encryption: bool = True,
) -> list[InferenceResult]:
    context = create_ckks_context() if use_encryption else None
    results: list[InferenceResult] = []

    for image_path in image_paths:
        image = load_grayscale_image(image_path)
        features = extract_xray_features(image)
        plaintext_logit = plaintext_linear_logit(features, model)
        plaintext_probability = sigmoid(plaintext_logit)

        encrypted_logit: float | None = None
        encrypted_probability: float | None = None
        abs_logit_error: float | None = None

        if use_encryption:
            encrypted_logit = encrypted_linear_logit(features, model, context)
            encrypted_probability = sigmoid(encrypted_logit)
            abs_logit_error = abs(encrypted_logit - plaintext_logit)

        probability_for_flag = (
            encrypted_probability if encrypted_probability is not None else plaintext_probability
        )

        results.append(
            InferenceResult(
                image=str(image_path.relative_to(PROJECT_ROOT)),
                plaintext_logit=plaintext_logit,
                plaintext_probability=plaintext_probability,
                encrypted_logit=encrypted_logit,
                encrypted_probability=encrypted_probability,
                abs_logit_error=abs_logit_error,
                triage_flag=probability_for_flag >= model.threshold,
                features={
                    name: float(value)
                    for name, value in zip(model.feature_names, features, strict=True)
                },
            )
        )

    return results


def write_reports(results: list[InferenceResult], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "medical_fhe_results.json"
    csv_path = output_dir / "medical_fhe_results.csv"

    json_path.write_text(
        json.dumps([asdict(result) for result in results], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "image",
            "plaintext_probability",
            "encrypted_probability",
            "abs_logit_error",
            "triage_flag",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "image": result.image,
                    "plaintext_probability": result.plaintext_probability,
                    "encrypted_probability": result.encrypted_probability,
                    "abs_logit_error": result.abs_logit_error,
                    "triage_flag": result.triage_flag,
                }
            )


def print_summary(results: list[InferenceResult], encrypted: bool) -> None:
    mode = "TenSEAL CKKS encrypted inference" if encrypted else "plaintext dry run"
    print(f"Mode: {mode}")
    print(f"Images processed: {len(results)}")
    print()
    print(f"{'image':36} {'probability':>12} {'flag':>8} {'abs_err':>12}")
    print("-" * 72)
    for result in results:
        probability = (
            result.encrypted_probability
            if result.encrypted_probability is not None
            else result.plaintext_probability
        )
        error = "n/a" if result.abs_logit_error is None else f"{result.abs_logit_error:.2e}"
        print(
            f"{Path(result.image).name:36} "
            f"{probability:12.4f} "
            f"{str(result.triage_flag):>8} "
            f"{error:>12}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a TenSEAL CKKS demo for privacy-preserving X-ray feature scoring."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--plaintext-only",
        action="store_true",
        help="Skip TenSEAL and run only plaintext preprocessing/scoring.",
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write JSON/CSV results under outputs/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = load_triage_model(args.model_path)
    image_paths = list_image_paths(args.data_dir)
    if not image_paths:
        raise FileNotFoundError(f"No images found in {args.data_dir}")

    use_encryption = not args.plaintext_only
    results = run_inference(image_paths, model, use_encryption=use_encryption)
    print_summary(results, encrypted=use_encryption)

    if args.write_report:
        write_reports(results, args.output_dir)
        print()
        print(f"Wrote reports to {args.output_dir}")


if __name__ == "__main__":
    main()
