from pathlib import Path

import numpy as np

from scripts.medical_fhe_pipeline import (
    DEFAULT_MODEL_PATH,
    build_demo_triage_model,
    extract_xray_features,
    list_image_paths,
    load_grayscale_image,
    load_triage_model,
    plaintext_linear_logit,
    sigmoid,
)


def test_extract_xray_features_shape_and_range():
    image = np.linspace(0.0, 1.0, 32 * 32, dtype=np.float64).reshape(32, 32)
    features = extract_xray_features(image)

    assert features.shape == (10,)
    assert np.all(np.isfinite(features))
    assert np.all(features >= 0.0)
    assert np.all(features <= 1.0)


def test_plaintext_triage_score_is_stable():
    image = np.full((32, 32), 0.5, dtype=np.float64)
    features = extract_xray_features(image)
    model = build_demo_triage_model()

    logit = plaintext_linear_logit(features, model)
    probability = sigmoid(logit)

    assert isinstance(logit, float)
    assert 0.0 <= probability <= 1.0


def test_model_artifact_loads_and_matches_demo_features():
    model = load_triage_model(DEFAULT_MODEL_PATH)
    demo_model = build_demo_triage_model()

    assert model.feature_names == demo_model.feature_names
    assert len(model.weights) == len(demo_model.feature_names)
    assert 0.0 <= model.threshold <= 1.0


def test_sample_data_can_be_loaded_if_present():
    data_dir = Path("data/chestxray_sample")
    if not data_dir.exists():
        return

    image_paths = list_image_paths(data_dir)
    assert image_paths

    image = load_grayscale_image(image_paths[0])
    assert image.shape == (32, 32)
    assert 0.0 <= float(image.min()) <= float(image.max()) <= 1.0
