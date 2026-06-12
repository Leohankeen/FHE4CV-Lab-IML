"""
Benchmark TenSEAL encrypted scoring for the medical FHE demo.

The benchmark reports per-image timing for:
- plaintext preprocessing and scoring,
- CKKS vector encryption,
- encrypted dot product on the simulated server,
- client-side decryption,
- CKKS logit error versus plaintext.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

try:
    from medical_fhe_pipeline import (
        DEFAULT_DATA_DIR,
        DEFAULT_MODEL_PATH,
        DEFAULT_OUTPUT_DIR,
        create_ckks_context,
        extract_xray_features,
        list_image_paths,
        load_grayscale_image,
        load_triage_model,
        plaintext_linear_logit,
        sigmoid,
        ts,
    )
except ImportError:
    from scripts.medical_fhe_pipeline import (
        DEFAULT_DATA_DIR,
        DEFAULT_MODEL_PATH,
        DEFAULT_OUTPUT_DIR,
        create_ckks_context,
        extract_xray_features,
        list_image_paths,
        load_grayscale_image,
        load_triage_model,
        plaintext_linear_logit,
        sigmoid,
        ts,
    )


@dataclass(frozen=True)
class BenchmarkRow:
    image: str
    preprocess_ms: float
    encrypt_ms: float
    encrypted_dot_ms: float
    decrypt_ms: float
    total_encrypted_ms: float
    plaintext_probability: float
    encrypted_probability: float
    abs_logit_error: float
    ciphertext_bytes: int
    triage_flag: bool


def now() -> float:
    return time.perf_counter()


def summarize(values: list[float]) -> dict[str, float]:
    return {
        "min": min(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "max": max(values),
    }


def benchmark(data_dir: Path, model_path: Path) -> list[BenchmarkRow]:
    if ts is None:
        raise RuntimeError(
            "TenSEAL is not installed. Install dependencies with `pip install -r requirements.txt`."
        )

    model = load_triage_model(model_path)
    context = create_ckks_context()
    rows: list[BenchmarkRow] = []

    for image_path in list_image_paths(data_dir):
        t0 = now()
        image = load_grayscale_image(image_path)
        features = extract_xray_features(image)
        plaintext_logit = plaintext_linear_logit(features, model)
        plaintext_probability = sigmoid(plaintext_logit)
        preprocess_ms = (now() - t0) * 1000.0

        t1 = now()
        encrypted_features = ts.ckks_vector(context, features.tolist())
        ciphertext_bytes = len(encrypted_features.serialize())
        encrypt_ms = (now() - t1) * 1000.0

        t2 = now()
        encrypted_logit_vector = encrypted_features.dot(model.weights) + model.bias
        encrypted_dot_ms = (now() - t2) * 1000.0

        t3 = now()
        encrypted_logit = float(encrypted_logit_vector.decrypt()[0])
        decrypt_ms = (now() - t3) * 1000.0

        encrypted_probability = sigmoid(encrypted_logit)
        rows.append(
            BenchmarkRow(
                image=str(image_path),
                preprocess_ms=preprocess_ms,
                encrypt_ms=encrypt_ms,
                encrypted_dot_ms=encrypted_dot_ms,
                decrypt_ms=decrypt_ms,
                total_encrypted_ms=encrypt_ms + encrypted_dot_ms + decrypt_ms,
                plaintext_probability=plaintext_probability,
                encrypted_probability=encrypted_probability,
                abs_logit_error=abs(encrypted_logit - plaintext_logit),
                ciphertext_bytes=ciphertext_bytes,
                triage_flag=encrypted_probability >= model.threshold,
            )
        )

    return rows


def write_benchmark(rows: list[BenchmarkRow], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "benchmark_tenseal.csv"
    json_path = output_dir / "benchmark_tenseal_summary.json"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))

    summary = {
        "images": len(rows),
        "preprocess_ms": summarize([row.preprocess_ms for row in rows]),
        "encrypt_ms": summarize([row.encrypt_ms for row in rows]),
        "encrypted_dot_ms": summarize([row.encrypted_dot_ms for row in rows]),
        "decrypt_ms": summarize([row.decrypt_ms for row in rows]),
        "total_encrypted_ms": summarize([row.total_encrypted_ms for row in rows]),
        "abs_logit_error": summarize([row.abs_logit_error for row in rows]),
        "ciphertext_bytes": summarize([float(row.ciphertext_bytes) for row in rows]),
    }
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def print_table(rows: list[BenchmarkRow]) -> None:
    print(f"{'image':24} {'enc_ms':>9} {'dot_ms':>9} {'dec_ms':>9} {'err':>10} {'bytes':>9}")
    print("-" * 78)
    for row in rows:
        print(
            f"{Path(row.image).name:24} "
            f"{row.encrypt_ms:9.2f} "
            f"{row.encrypted_dot_ms:9.2f} "
            f"{row.decrypt_ms:9.2f} "
            f"{row.abs_logit_error:10.2e} "
            f"{row.ciphertext_bytes:9d}"
        )

    total = [row.total_encrypted_ms for row in rows]
    errors = [row.abs_logit_error for row in rows]
    print()
    print(f"Mean encrypted total: {np.mean(total):.2f} ms")
    print(f"Mean abs logit error: {np.mean(errors):.2e}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark TenSEAL CKKS encrypted scoring.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--model-path", type=Path, default=DEFAULT_MODEL_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--write-report", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = benchmark(args.data_dir, args.model_path)
    if not rows:
        raise FileNotFoundError(f"No images found in {args.data_dir}")

    print_table(rows)
    if args.write_report:
        write_benchmark(rows, args.output_dir)
        print()
        print(f"Wrote benchmark files to {args.output_dir}")


if __name__ == "__main__":
    main()
