"""Static validation for the 60-minute Act 1 Manim storyboard."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENES = (
    ("scene_01_he_foundations.py", "HomomorphicEncryptionFoundations"),
    ("scene_02_ckks_encoding.py", "CKKSEncodingAndParameters"),
    ("scene_03_ciphertext_operations.py", "CiphertextOperations"),
    ("scene_04_keys_and_seal_pipeline.py", "KeysAndSEALPipeline"),
)


def returned_list_size(function: ast.FunctionDef) -> int:
    for node in ast.walk(function):
        if isinstance(node, ast.Return) and isinstance(node.value, ast.List):
            return len(node.value.elts)
    return 0


def validate_scene(filename: str, class_name: str) -> int:
    path = ROOT / "scenes" / "01_math_crypto" / filename
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    target = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == class_name
    )

    chapter_calls = [
        node
        for node in ast.walk(target)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"run_chapter", "play_section_beats", "play_timed_section"}
    ]
    beat_methods = [
        node
        for node in target.body
        if isinstance(node, ast.FunctionDef) and node.name.endswith("_beats")
    ]
    beat_count = sum(returned_list_size(method) for method in beat_methods)

    if len(chapter_calls) != 3:
        raise ValueError(f"{filename}: expected 3 chapters, found {len(chapter_calls)}")
    if len(beat_methods) != 3 or beat_count != 15:
        raise ValueError(
            f"{filename}: expected 3 beat methods / 15 beats, "
            f"found {len(beat_methods)} / {beat_count}"
        )

    duration = len(chapter_calls) * 300
    print(f"{class_name}: chapters=3 beats={beat_count} seconds={duration}")
    return duration


def validate_manifest() -> None:
    path = ROOT / "scripts" / "act1_audio_manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    scenes = manifest.get("scenes", [])
    if len(scenes) != 4:
        raise ValueError("Audio manifest must contain four scenes.")
    if sum(scene["target_seconds"] for scene in scenes) != 3600:
        raise ValueError("Audio manifest target duration must total 3600 seconds.")
    for scene in scenes:
        storyboard = ROOT / scene["storyboard"]
        if not storyboard.exists():
            raise FileNotFoundError(storyboard)
        source = ROOT / scene["source"]
        if not source.exists():
            raise FileNotFoundError(source)
    generator = ROOT / "scripts" / "generate_act1_audio.py"
    if not generator.exists():
        raise FileNotFoundError(generator)


def main() -> None:
    total = sum(validate_scene(*scene) for scene in SCENES)
    validate_manifest()
    if total != 3600:
        raise ValueError(f"Expected 3600 total seconds, found {total}.")
    print(f"Act 1 total: {total} seconds / {total / 60:.1f} minutes")


if __name__ == "__main__":
    main()
