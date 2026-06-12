"""Validate storyboard audio manifests and their referenced scene files.

Examples:
    python scripts/validate_audio.py `
        --manifest scripts/audio_manifest/act1_audio_manifest.json
    python scripts/validate_audio.py `
        --manifest scripts/audio_manifest/act2_audio_manifest.json
    python scripts/validate_audio.py `
        --manifest scripts/audio_manifest/act3_audio_manifest.json `
        --scene scene_01_cryptoface_scene
    python scripts/validate_audio.py --all --check-audio
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOICEOVER_PATTERN = re.compile(
    r'-\s+\*\*Lời thoại AI \(Audio Voiceover\):\*\*\s*(.+?)'
    r'\s*(?=\n-\s+\*\*Hoạt ảnh Manim)',
    flags=re.DOTALL,
)
SCENE_AUDIO_PATTERN = re.compile(
    r"""["'](\.?/?assets/audio/[^"']+\.mp3)["']""",
)
CHAPTER_CALLS = {"run_chapter", "play_section_beats", "play_timed_section"}


def project_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else ROOT / path


def load_manifest(path: Path) -> dict:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise ValueError(f"{path}: manifest root must be a JSON object.")
    return manifest


def voiceover_block_count(storyboard_path: Path) -> int:
    markdown = storyboard_path.read_text(encoding="utf-8")
    count = len(VOICEOVER_PATTERN.findall(markdown))
    if count == 0:
        raise ValueError(f"{storyboard_path}: no AI voiceover blocks found.")
    return count


def output_path(spec: str | dict) -> str:
    if isinstance(spec, str):
        return spec
    if isinstance(spec, dict) and isinstance(spec.get("path"), str):
        return spec["path"]
    raise ValueError(f"Invalid audio output specification: {spec!r}")


def output_duration(spec: str | dict) -> float | None:
    if isinstance(spec, str):
        return None
    duration = spec.get("target_seconds")
    if duration is None:
        return None
    duration = float(duration)
    if duration <= 0:
        raise ValueError(f"Audio target_seconds must be positive: {spec!r}")
    return duration


def manifest_audio_outputs(scene: dict) -> list[str]:
    if "output" in scene:
        return [output_path(scene["output"])]
    return [
        output_path(spec)
        for section in scene["audio_sections"]
        for spec in section
    ]


def returned_list_size(function: ast.FunctionDef) -> int:
    for node in ast.walk(function):
        if not isinstance(node, ast.Return) or node.value is None:
            continue
        if isinstance(node.value, (ast.List, ast.Tuple)):
            return len(node.value.elts)
    return 0


def find_beat_class(
    tree: ast.Module,
    source_path: Path,
    beat_methods: list[str],
) -> ast.ClassDef:
    candidates = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        method_names = {
            child.name
            for child in node.body
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        if all(name in method_names for name in beat_methods):
            candidates.append(node)
    if len(candidates) != 1:
        raise ValueError(
            f"{source_path}: expected one class containing {beat_methods}, "
            f"found {len(candidates)}."
        )
    return candidates[0]


def validate_source_structure(source_path: Path, scene: dict) -> str:
    tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    if not classes:
        raise ValueError(f"{source_path}: no scene class found.")

    beat_methods = scene.get("beat_methods")
    if not beat_methods:
        return f"source={source_path.relative_to(ROOT)} syntax=ok"
    if not isinstance(beat_methods, list) or not all(
        isinstance(name, str) and name for name in beat_methods
    ):
        raise ValueError(f"{scene['id']}: beat_methods must be a list of names.")

    target = find_beat_class(tree, source_path, beat_methods)
    methods = {
        node.name: node
        for node in target.body
        if isinstance(node, ast.FunctionDef)
    }
    beat_count = sum(returned_list_size(methods[name]) for name in beat_methods)
    chapter_count = sum(
        1
        for node in ast.walk(target)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in CHAPTER_CALLS
    )

    expected_chapters = int(scene.get("expected_chapter_calls", len(beat_methods)))
    expected_beats = scene.get("expected_beat_count")
    if chapter_count != expected_chapters:
        raise ValueError(
            f"{source_path}: expected {expected_chapters} chapter calls, "
            f"found {chapter_count}."
        )
    if expected_beats is not None and beat_count != int(expected_beats):
        raise ValueError(
            f"{source_path}: expected {expected_beats} beats, found {beat_count}."
        )

    return (
        f"class={target.name} chapters={chapter_count} "
        f"beat_methods={len(beat_methods)} beats={beat_count}"
    )


def source_audio_outputs(source_path: Path) -> set[str]:
    text = source_path.read_text(encoding="utf-8")
    return {
        path.removeprefix("./").replace("\\", "/")
        for path in SCENE_AUDIO_PATTERN.findall(text)
    }


def validate_scene(
    manifest: dict,
    scene: dict,
    check_audio: bool,
    check_source_audio_refs: bool,
) -> tuple[float, list[str]]:
    scene_id = scene.get("id")
    if not isinstance(scene_id, str) or not scene_id:
        raise ValueError("Every scene requires a non-empty id.")
    for field in ("source", "storyboard", "target_seconds"):
        if field not in scene:
            raise ValueError(f"{scene_id}: missing required field {field!r}.")

    target_seconds = float(scene["target_seconds"])
    if target_seconds <= 0:
        raise ValueError(f"{scene_id}: target_seconds must be positive.")

    source_path = project_path(scene["source"])
    storyboard_path = project_path(scene["storyboard"])
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    if not storyboard_path.exists():
        raise FileNotFoundError(storyboard_path)

    voiceover_count = voiceover_block_count(storyboard_path)
    has_output = "output" in scene
    has_sections = "audio_sections" in scene
    if has_output == has_sections:
        raise ValueError(
            f"{scene_id}: define exactly one of output or audio_sections."
        )

    if has_sections:
        sections = scene["audio_sections"]
        if not isinstance(sections, list) or len(sections) != voiceover_count:
            raise ValueError(
                f"{scene_id}: storyboard has {voiceover_count} voiceover blocks, "
                f"but manifest has {len(sections) if isinstance(sections, list) else 0} "
                "audio sections."
            )
        if any(not isinstance(section, list) or not section for section in sections):
            raise ValueError(f"{scene_id}: every audio section must contain clips.")
        for section in sections:
            for spec in section:
                output_duration(spec)

    outputs = manifest_audio_outputs(scene)
    if len(outputs) != len(set(outputs)):
        raise ValueError(f"{scene_id}: duplicate audio output paths.")

    if check_audio:
        missing = [path for path in outputs if not project_path(path).exists()]
        if missing:
            raise FileNotFoundError(
                f"{scene_id}: missing generated audio: {', '.join(missing)}"
            )

    if check_source_audio_refs and has_sections:
        expected = {path.replace("\\", "/") for path in outputs}
        actual = source_audio_outputs(source_path)
        if expected != actual:
            raise ValueError(
                f"{scene_id}: manifest/source audio mismatch. "
                f"Missing from manifest: {sorted(actual - expected)}; "
                f"unused by source: {sorted(expected - actual)}"
            )

    structure = validate_source_structure(source_path, scene)
    details = [
        f"{scene_id}: voiceovers={voiceover_count} outputs={len(outputs)} "
        f"seconds={target_seconds:g}",
        f"  {structure}",
    ]
    return target_seconds, details


def validate_manifest(
    manifest_path: Path,
    scene_id: str | None,
    check_audio: bool,
    check_source_audio_refs: bool,
) -> None:
    manifest = load_manifest(manifest_path)
    act = manifest.get("act")
    scenes = manifest.get("scenes")
    if not isinstance(act, str) or not act:
        raise ValueError(f"{manifest_path}: missing non-empty act name.")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError(f"{manifest_path}: scenes must be a non-empty list.")

    ids = [scene.get("id") for scene in scenes]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{manifest_path}: scene ids must be unique.")
    if scene_id:
        scenes = [scene for scene in scenes if scene.get("id") == scene_id]
        if not scenes:
            raise ValueError(f"{manifest_path}: unknown scene id {scene_id!r}.")

    all_outputs = []
    total_seconds = 0.0
    print(f"{act} ({manifest_path.relative_to(ROOT)})")
    for scene in scenes:
        duration, details = validate_scene(
            manifest,
            scene,
            check_audio,
            check_source_audio_refs,
        )
        total_seconds += duration
        all_outputs.extend(manifest_audio_outputs(scene))
        for detail in details:
            print(detail)

    if len(all_outputs) != len(set(all_outputs)):
        raise ValueError(f"{manifest_path}: audio outputs must be unique across scenes.")

    expected_total = manifest.get("target_seconds")
    if scene_id is None and expected_total is not None:
        expected_total = float(expected_total)
        if abs(total_seconds - expected_total) > 0.001:
            raise ValueError(
                f"{manifest_path}: scene total is {total_seconds:g}s, "
                f"expected {expected_total:g}s."
            )

    generator = ROOT / "scripts" / "generate_audio.py"
    if not generator.exists():
        raise FileNotFoundError(generator)

    print(f"Total: {total_seconds:g} seconds / {total_seconds / 60:g} minutes")


def manifest_paths(selected: Path, validate_all: bool) -> list[Path]:
    if not validate_all:
        return [project_path(selected)]
    manifest_dir = ROOT / "scripts" / "audio_manifest"
    paths = sorted(manifest_dir.glob("act*_audio_manifest.json"))
    if not paths:
        raise FileNotFoundError(
            "No scripts/audio_manifest/act*_audio_manifest.json files found."
        )
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--manifest",
        type=Path,
        help="Manifest to validate.",
    )
    parser.add_argument("--scene", help="Validate only one scene id.")
    selection.add_argument(
        "--all",
        action="store_true",
        help=(
            "Validate every scripts/audio_manifest/"
            "act*_audio_manifest.json file."
        ),
    )
    parser.add_argument(
        "--check-audio",
        action="store_true",
        help="Require every generated MP3 referenced by the manifest to exist.",
    )
    parser.add_argument(
        "--check-source-audio-refs",
        action="store_true",
        help="Require sectioned manifest outputs to match scene add_sound paths.",
    )
    args = parser.parse_args()
    if args.all and args.scene:
        parser.error("--scene cannot be combined with --all.")

    for index, path in enumerate(manifest_paths(args.manifest, args.all)):
        if not path.exists():
            raise SystemExit(f"Manifest not found: {path}")
        if index:
            print()
        validate_manifest(
            path,
            args.scene,
            args.check_audio,
            args.check_source_audio_refs,
        )


if __name__ == "__main__":
    main()
