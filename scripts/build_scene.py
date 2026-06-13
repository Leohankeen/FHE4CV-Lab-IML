"""Build any Manim scene from a Python file under scenes/.

From the project root:
    python scripts/build_scene.py scenes/01_math_crypto/scene_01_he_foundations.py

From the scripts directory:
    python build_scene.py scenes/01_math_crypto/scene_01_he_foundations.py

If a file defines multiple Scene classes, select one explicitly:
    python scripts/build_scene.py scenes/example.py --class-name ExampleScene
"""

from __future__ import annotations

import argparse
import ast
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCENES_ROOT = ROOT / "scenes"
MANIFEST_DIR = ROOT / "scripts" / "audio_manifest"
GENERATOR = ROOT / "scripts" / "generate_audio.py"
MANIM_CONFIG = ROOT / "configs" / "manim.cfg"
MEDIA_DIR = ROOT / "media"
DELIVERABLE_DIR = ROOT / "deliverables" / "scene_clips"
DEFAULT_BGM = ROOT / "assets" / "audio" / "bgm.mp3"
QUALITY_FLAGS = {
    "l": "ql",
    "m": "qm",
    "h": "qh",
    "k": "qk",
}


def run_command(command: list[str], dry_run: bool = False) -> None:
    print("$ " + subprocess.list2cmdline(command))
    if not dry_run:
        subprocess.run(command, cwd=ROOT, check=True)


def resolve_scene_path(raw_path: str) -> Path:
    supplied = Path(raw_path)
    candidates = [supplied] if supplied.is_absolute() else [
        Path.cwd() / supplied,
        ROOT / supplied,
    ]
    scene_path = next(
        (candidate.resolve() for candidate in candidates if candidate.exists()),
        None,
    )
    if scene_path is None:
        raise FileNotFoundError(f"Scene file not found: {raw_path}")
    if scene_path.suffix.lower() != ".py":
        raise ValueError(f"Scene path must point to a .py file: {scene_path}")
    try:
        scene_path.relative_to(SCENES_ROOT.resolve())
    except ValueError as exc:
        raise ValueError(
            f"Scene file must be inside {SCENES_ROOT}: {scene_path}"
        ) from exc
    return scene_path


def base_name(base: ast.expr) -> str:
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return base.attr
    if isinstance(base, ast.Subscript):
        return base_name(base.value)
    return ""


def discover_scene_classes(scene_path: Path) -> list[str]:
    tree = ast.parse(scene_path.read_text(encoding="utf-8"), filename=str(scene_path))
    classes = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        if any(base_name(base).endswith("Scene") for base in node.bases):
            classes.append(node.name)
    if not classes:
        raise ValueError(
            f"No class inheriting from Scene was found in {scene_path}."
        )
    return classes


def select_scene_class(scene_path: Path, requested: str | None) -> str:
    classes = discover_scene_classes(scene_path)
    if requested:
        if requested not in classes:
            raise ValueError(
                f"{requested!r} is not a Scene class in {scene_path}. "
                f"Available classes: {', '.join(classes)}"
            )
        return requested
    if len(classes) > 1:
        raise ValueError(
            f"{scene_path} defines multiple Scene classes: {', '.join(classes)}. "
            "Use --class-name to select one."
        )
    return classes[0]


def load_manifest_entries() -> list[tuple[Path, dict]]:
    entries = []
    if not MANIFEST_DIR.exists():
        return entries
    for manifest_path in sorted(MANIFEST_DIR.glob("*.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for scene in manifest.get("scenes", []):
            entries.append((manifest_path, scene))
    return entries


def audio_manifest_for_scene(scene_path: Path) -> tuple[Path, str] | None:
    matches = []
    for manifest_path, scene in load_manifest_entries():
        source = scene.get("source")
        scene_id = scene.get("id")
        if not source or not scene_id:
            continue
        source_path = (ROOT / source).resolve()
        if source_path == scene_path:
            matches.append((manifest_path, scene_id))
    if len(matches) > 1:
        locations = ", ".join(str(path.relative_to(ROOT)) for path, _ in matches)
        raise ValueError(
            f"Multiple audio manifests reference {scene_path}: {locations}"
        )
    return matches[0] if matches else None


def generate_scene_audio(
    scene_path: Path,
    skip_audio: bool,
    dry_run: bool,
) -> None:
    if skip_audio:
        print("Audio generation skipped.")
        return
    match = audio_manifest_for_scene(scene_path)
    if match is None:
        print("No audio manifest entry found; rendering with existing scene audio.")
        return
    if not GENERATOR.exists():
        raise FileNotFoundError(GENERATOR)
    manifest_path, scene_id = match
    print(
        "Generating audio from "
        f"{manifest_path.relative_to(ROOT)} for {scene_id}."
    )
    run_command(
        [
            sys.executable,
            str(GENERATOR),
            "--manifest",
            str(manifest_path),
            "--scene",
            scene_id,
        ],
        dry_run,
    )


def manim_command(
    scene_path: Path,
    class_name: str,
    quality: str,
    preview: bool,
    disable_caching: bool,
) -> list[str]:
    quality_flag = QUALITY_FLAGS[quality]
    flag = f"-p{quality_flag}" if preview else f"-{quality_flag}"
    command = [sys.executable, "-m", "manim"]
    if MANIM_CONFIG.exists():
        command.extend(["-c", str(MANIM_CONFIG)])
    command.append(flag)
    if disable_caching:
        command.append("--disable_caching")
    command.extend([str(scene_path), class_name])
    return command


def find_rendered_video(class_name: str, render_started: float) -> Path:
    video_root = MEDIA_DIR / "videos"
    candidates = [
        path
        for path in video_root.rglob(f"{class_name}.mp4")
        if path.stat().st_mtime >= render_started - 2
    ]
    if not candidates:
        raise FileNotFoundError(
            f"Manim completed but no new {class_name}.mp4 was found under {video_root}."
        )
    return max(candidates, key=lambda path: path.stat().st_mtime)


def final_output_path(scene_path: Path, class_name: str) -> Path:
    DELIVERABLE_DIR.mkdir(parents=True, exist_ok=True)
    relative = scene_path.relative_to(SCENES_ROOT)
    prefix = "_".join(relative.with_suffix("").parts)
    return DELIVERABLE_DIR / f"{prefix}_{class_name}_Final.mp4"


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def mix_background_music(
    raw_video: Path,
    final_output: Path,
    bgm_path: Path,
    skip_bgm: bool,
    dry_run: bool,
) -> None:
    if skip_bgm or not bgm_path.exists() or not ffmpeg_available():
        reason = "disabled" if skip_bgm else "BGM or ffmpeg unavailable"
        print(f"Background music {reason}; copying the Manim video.")
        if not dry_run:
            shutil.copy2(raw_video, final_output)
        return

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(raw_video),
        "-stream_loop",
        "-1",
        "-i",
        str(bgm_path),
        "-filter_complex",
        (
            "[0:a]volume=2.5[voice];"
            "[1:a]volume=0.12[bgm];"
            "[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2"
        ),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(final_output),
    ]
    try:
        run_command(command, dry_run)
    except subprocess.CalledProcessError:
        print("FFmpeg mixing failed; keeping the original Manim audio.")
        if not dry_run:
            shutil.copy2(raw_video, final_output)


def build_scene(args: argparse.Namespace) -> None:
    scene_path = resolve_scene_path(args.scene_path)
    class_name = select_scene_class(scene_path, args.class_name)
    print(f"Scene file: {scene_path.relative_to(ROOT)}")
    print(f"Scene class: {class_name}")

    generate_scene_audio(scene_path, args.skip_audio, args.dry_run)

    render_started = time.time()
    command = manim_command(
        scene_path,
        class_name,
        args.quality,
        args.preview,
        not args.use_cache,
    )
    run_command(command, args.dry_run)

    if args.dry_run:
        output = final_output_path(scene_path, class_name)
        print(f"Dry run complete. Final output would be: {output.relative_to(ROOT)}")
        return

    raw_video = find_rendered_video(class_name, render_started)
    output = final_output_path(scene_path, class_name)
    mix_background_music(
        raw_video,
        output,
        project_bgm_path(args.bgm),
        args.skip_bgm,
        False,
    )
    print(f"Build complete: {output.relative_to(ROOT)}")


def project_bgm_path(raw_path: str | None) -> Path:
    if raw_path is None:
        return DEFAULT_BGM
    path = Path(raw_path)
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scene_path",
        help="Path to a Python scene file inside the scenes directory.",
    )
    parser.add_argument(
        "--class-name",
        help="Scene class to render when the file defines more than one.",
    )
    parser.add_argument(
        "--quality",
        choices=sorted(QUALITY_FLAGS),
        default="h",
        help="Manim quality: l, m, h, or k. Defaults to h.",
    )
    parser.add_argument(
        "--no-preview",
        dest="preview",
        action="store_false",
        help="Do not open the rendered video after Manim finishes.",
    )
    parser.add_argument(
        "--use-cache",
        action="store_true",
        help="Allow Manim to reuse cached animations.",
    )
    parser.add_argument(
        "--skip-audio",
        action="store_true",
        help="Do not regenerate narration from an audio manifest.",
    )
    parser.add_argument(
        "--skip-bgm",
        action="store_true",
        help="Do not mix assets/audio/bgm.mp3 into the rendered video.",
    )
    parser.add_argument(
        "--bgm",
        help="Override the background-music path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the audio, Manim, and output steps without executing them.",
    )
    parser.set_defaults(preview=True)
    return parser.parse_args()


def main() -> None:
    try:
        build_scene(parse_args())
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Error: {exc}") from exc


if __name__ == "__main__":
    main()
