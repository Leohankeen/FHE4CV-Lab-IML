"""Generate narration audio from storyboard AI voiceover blocks.

Install the optional provider first:
    python -m pip install edge-tts

Examples:
    python scripts/generate_audio.py
    python scripts/generate_audio.py `
        --manifest scripts/audio_manifest/act2_audio_manifest.json
    python scripts/generate_audio.py `
        --manifest scripts/audio_manifest/act2_audio_manifest.json `
        --scene scene_01_relu_barrier
    python scripts/generate_audio.py `
        --manifest scripts/audio_manifest/act3_audio_manifest.json `
        --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import tempfile
from pathlib import Path

import av
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_PATH = (
    ROOT / "scripts" / "audio_manifest" / "act1_audio_manifest.json"
)
VOICEOVER_PATTERN = re.compile(
    r'-\s+\*\*Lời thoại AI \(Audio Voiceover\):\*\*\s*(.+?)'
    r'\s*(?=\n-\s+\*\*Hoạt ảnh Manim)',
    flags=re.DOTALL,
)
TIMED_SEGMENT_PATTERN = re.compile(
    r'<!-- AUDIO_SEGMENT id="([^"]+)" duration="([0-9.]+)" -->\s*'
    r"```text\s*(.+?)\s*```",
    flags=re.DOTALL,
)
SAMPLE_RATE = 24_000
TARGET_SPEECH_FILL = 0.965
MIN_SPEECH_FILL = 0.94
MAX_SPEECH_FILL = 0.985


def project_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else ROOT / path


def clean_voiceover(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
        text = text[1:-1]
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\\text\{([^}]+)\}", r"\1", text)
    replacements = {
        r"\max": "max",
        r"\times": " times ",
        r"\oplus": " plus ",
        r"\otimes": " times ",
        r"\rightarrow": " leads to ",
        r"\leq": " less than or equal to ",
        r"\geq": " greater than or equal to ",
    }
    for source, replacement in replacements.items():
        text = text.replace(source, replacement)
    text = text.replace("$", "").replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def extract_voiceover_sections(storyboard_path: Path) -> list[str]:
    markdown = storyboard_path.read_text(encoding="utf-8")
    sections = [
        clean_voiceover(section)
        for section in VOICEOVER_PATTERN.findall(markdown)
        if section.strip()
    ]
    if not sections:
        raise ValueError(f"No AI voiceover blocks found in {storyboard_path}")
    return sections


def extract_timed_segments(storyboard_path: Path) -> list[dict]:
    markdown = storyboard_path.read_text(encoding="utf-8")
    return [
        {
            "id": segment_id,
            "duration": float(duration),
            "text": clean_voiceover(text),
        }
        for segment_id, duration, text in TIMED_SEGMENT_PATTERN.findall(markdown)
    ]


def audio_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    with av.open(str(path)) as container:
        if container.duration is not None:
            return float(container.duration / av.time_base)
        stream = container.streams.audio[0]
        if stream.duration is not None and stream.time_base is not None:
            return float(stream.duration * stream.time_base)
    return None


def normalize_output_spec(spec: str | dict, fallback_seconds: float | None = None) -> dict:
    if isinstance(spec, str):
        return {"path": spec, "target_seconds": fallback_seconds}
    if not isinstance(spec, dict) or "path" not in spec:
        raise ValueError(f"Invalid audio output specification: {spec!r}")
    target_seconds = spec.get("target_seconds", fallback_seconds)
    return {
        "path": spec["path"],
        "target_seconds": float(target_seconds) if target_seconds is not None else None,
    }


def output_target_seconds(spec: dict) -> float | None:
    if spec["target_seconds"] is not None:
        return float(spec["target_seconds"])
    return audio_duration(project_path(spec["path"]))


def split_unit(unit: str) -> tuple[str, str]:
    comma_points = [match.end() for match in re.finditer(r",\s+", unit)]
    if comma_points:
        midpoint = len(unit) / 2
        split_at = min(comma_points, key=lambda point: abs(point - midpoint))
        return unit[:split_at].strip(), unit[split_at:].strip()

    words = unit.split()
    if len(words) < 2:
        return unit, ""
    midpoint = len(words) // 2
    return " ".join(words[:midpoint]), " ".join(words[midpoint:])


def narration_units(text: str, minimum_count: int) -> list[str]:
    units = [
        part.strip()
        for part in re.split(r"(?<=[.!?;:])\s+", text)
        if part.strip()
    ]
    while len(units) < minimum_count:
        split_index = max(range(len(units)), key=lambda index: len(units[index].split()))
        left, right = split_unit(units[split_index])
        if not right:
            break
        units[split_index : split_index + 1] = [left, right]
    if len(units) < minimum_count:
        raise ValueError(
            f"Cannot split {len(text.split())} words into {minimum_count} audio clips."
        )
    return units


def split_text_by_weights(text: str, weights: list[float]) -> list[str]:
    if len(weights) == 1:
        return [text]

    units = narration_units(text, len(weights))
    word_counts = [max(1, len(unit.split())) for unit in units]
    total_words = sum(word_counts)
    total_weight = sum(weights)
    chunks = []
    start = 0
    words_before = 0
    weight_before = 0.0

    for chunk_index, weight in enumerate(weights[:-1]):
        weight_before += weight
        target_cumulative = total_words * weight_before / total_weight
        max_end = len(units) - (len(weights) - chunk_index - 1)
        cumulative = words_before
        best_end = start + 1
        best_distance = float("inf")
        for end in range(start + 1, max_end + 1):
            cumulative += word_counts[end - 1]
            distance = abs(cumulative - target_cumulative)
            if distance < best_distance:
                best_distance = distance
                best_end = end
        chunks.append(" ".join(units[start:best_end]))
        words_before += sum(word_counts[start:best_end])
        start = best_end

    chunks.append(" ".join(units[start:]))
    return chunks


def parse_rate_percent(rate: str) -> float:
    match = re.fullmatch(r"\s*([+-]?\d+(?:\.\d+)?)%\s*", rate)
    if not match:
        raise ValueError(f"Unsupported Edge TTS rate: {rate!r}")
    return float(match.group(1))


def format_rate_percent(rate_percent: float) -> str:
    rounded = int(round(max(-45.0, min(45.0, rate_percent))))
    return f"{rounded:+d}%"


def fitted_rate(base_rate: str, speech_duration: float, target_duration: float) -> str:
    base_multiplier = 1.0 + parse_rate_percent(base_rate) / 100.0
    fitted_multiplier = base_multiplier * speech_duration / target_duration
    return format_rate_percent((fitted_multiplier - 1.0) * 100.0)


def decode_mono_s16(path: Path) -> np.ndarray:
    samples = []
    with av.open(str(path)) as container:
        stream = container.streams.audio[0]
        resampler = av.AudioResampler(format="s16", layout="mono", rate=SAMPLE_RATE)
        for frame in container.decode(stream):
            for converted in resampler.resample(frame):
                samples.append(converted.to_ndarray().reshape(-1))
        for converted in resampler.resample(None):
            samples.append(converted.to_ndarray().reshape(-1))
    if not samples:
        return np.zeros(0, dtype=np.int16)
    return np.concatenate(samples).astype(np.int16, copy=False)


def active_audio_duration(samples: np.ndarray) -> float:
    """Measure speech through its final audible 50 ms window."""
    window_size = round(0.05 * SAMPLE_RATE)
    usable_size = len(samples) - len(samples) % window_size
    if usable_size <= 0:
        return 0.0
    windows = samples[:usable_size].reshape(-1, window_size).astype(np.float64)
    rms = np.sqrt(np.mean(windows * windows, axis=1))
    active_windows = np.flatnonzero(rms > 80)
    if len(active_windows) == 0:
        return 0.0
    return (active_windows[-1] + 1) * window_size / SAMPLE_RATE


def encode_mp3(samples: np.ndarray, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".generated.tmp.mp3")
    with av.open(str(temporary_path), mode="w") as container:
        stream = container.add_stream("libmp3lame", rate=SAMPLE_RATE)
        stream.layout = "mono"
        stream.bit_rate = 48_000
        frame_size = 1_152
        for start in range(0, len(samples), frame_size):
            chunk = samples[start : start + frame_size]
            frame = av.AudioFrame.from_ndarray(
                chunk.reshape(1, -1),
                format="s16",
                layout="mono",
            )
            frame.sample_rate = SAMPLE_RATE
            for packet in stream.encode(frame):
                container.mux(packet)
        for packet in stream.encode(None):
            container.mux(packet)
    temporary_path.replace(output_path)


async def synthesize_raw(edge_tts, text: str, path: Path, voice: str, rate: str) -> np.ndarray:
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(str(path))
    return decode_mono_s16(path)


async def synthesize_clip(
    edge_tts,
    text: str,
    output_path: Path,
    voice: str,
    base_rate: str,
    target_seconds: float | None,
    target_wpm: float | None,
    temp_path: Path,
) -> dict:
    selected_rate = base_rate
    speech = await synthesize_raw(edge_tts, text, temp_path, voice, selected_rate)
    word_count = len(text.split())

    if target_seconds is None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path.replace(output_path)
        speech_duration = active_audio_duration(speech)
        return {
            "rate": selected_rate,
            "speech_seconds": speech_duration,
            "target_seconds": speech_duration,
            "wpm": word_count * 60.0 / max(speech_duration, 0.001),
        }

    target_seconds = float(target_seconds)
    natural_target = (
        word_count * 60.0 / target_wpm if target_wpm is not None else target_seconds
    )
    target_speech_seconds = min(
        natural_target,
        target_seconds * TARGET_SPEECH_FILL,
    )

    for _ in range(3):
        speech_duration = active_audio_duration(speech)
        if speech_duration <= 0:
            raise ValueError(f"No audible speech generated for {output_path}")
        if abs(speech_duration - target_speech_seconds) / target_speech_seconds <= 0.025:
            break
        selected_rate = fitted_rate(
            selected_rate,
            speech_duration,
            target_speech_seconds,
        )
        speech = await synthesize_raw(
            edge_tts,
            text,
            temp_path,
            voice,
            selected_rate,
        )

    speech_duration = active_audio_duration(speech)
    target_samples = round(target_seconds * SAMPLE_RATE)
    if len(speech) > target_samples or speech_duration > target_seconds:
        raise ValueError(
            f"{output_path}: speech is {speech_duration:.2f}s but the clip slot is "
            f"{target_seconds:.2f}s. Shorten the storyboard text or increase --rate."
        )

    padded = np.pad(speech, (0, target_samples - len(speech)))
    encode_mp3(padded, output_path)
    return {
        "rate": selected_rate,
        "speech_seconds": speech_duration,
        "target_seconds": target_seconds,
        "wpm": word_count * 60.0 / max(speech_duration, 0.001),
    }


def scene_target_wpm(manifest: dict, scene: dict) -> float | None:
    value = scene.get("target_wpm", manifest.get("target_wpm"))
    return float(value) if value is not None else None


def transcript_path(manifest: dict, scene: dict, output_path: Path | None = None) -> Path:
    if scene.get("transcript"):
        return project_path(scene["transcript"])
    if output_path is not None:
        return output_path.with_suffix(".txt")
    act = manifest.get("act", "audio")
    return ROOT / "assets" / "audio" / act / f"{scene['id']}.txt"


def validate_scene_config(manifest: dict, scene: dict) -> tuple[Path, list[str]]:
    if "id" not in scene or "storyboard" not in scene:
        raise ValueError("Every scene needs id and storyboard fields.")
    storyboard_path = project_path(scene["storyboard"])
    if not storyboard_path.exists():
        raise FileNotFoundError(storyboard_path)
    if scene.get("source"):
        source_path = project_path(scene["source"])
        if not source_path.exists():
            raise FileNotFoundError(source_path)
    sections = extract_voiceover_sections(storyboard_path)

    has_single_output = "output" in scene
    has_section_outputs = "audio_sections" in scene
    if has_single_output == has_section_outputs:
        raise ValueError(
            f"{scene['id']}: define exactly one of output or audio_sections."
        )
    if has_section_outputs and len(scene["audio_sections"]) != len(sections):
        raise ValueError(
            f"{scene['id']}: storyboard has {len(sections)} voiceover blocks, but "
            f"manifest has {len(scene['audio_sections'])} audio sections."
        )
    return storyboard_path, sections


def selected_scenes(manifest: dict, scene_id: str | None) -> list[dict]:
    scenes = manifest.get("scenes", [])
    if not scenes:
        raise ValueError("Manifest contains no scenes.")
    if scene_id is None:
        return scenes
    selected = [scene for scene in scenes if scene.get("id") == scene_id]
    if not selected:
        known = ", ".join(scene.get("id", "<missing>") for scene in scenes)
        raise SystemExit(f"Unknown scene id: {scene_id}. Available scenes: {known}")
    return selected


def describe_scene(manifest: dict, scene: dict) -> None:
    _, sections = validate_scene_config(manifest, scene)
    print(f"{scene['id']}: {len(sections)} voiceover block(s)")
    if "output" in scene:
        spec = normalize_output_spec(scene["output"], scene.get("target_seconds"))
        target = output_target_seconds(spec)
        suffix = f", target={target:.3f}s" if target is not None else ""
        print(f"  full scene -> {spec['path']} ({sum(len(s.split()) for s in sections)} words{suffix})")
        return

    for index, (text, raw_specs) in enumerate(
        zip(sections, scene["audio_sections"]),
        start=1,
    ):
        specs = [normalize_output_spec(spec) for spec in raw_specs]
        targets = [output_target_seconds(spec) for spec in specs]
        known_total = sum(value for value in targets if value is not None)
        print(
            f"  section {index}: {len(text.split())} words -> {len(specs)} clip(s), "
            f"reference={known_total:.3f}s"
        )
        for spec, target in zip(specs, targets):
            suffix = f" [{target:.3f}s]" if target is not None else ""
            print(f"    {spec['path']}{suffix}")


async def synthesize_single_scene(
    edge_tts,
    manifest: dict,
    scene: dict,
    storyboard_path: Path,
    sections: list[str],
    voice: str,
    rate: str,
) -> None:
    spec = normalize_output_spec(scene["output"], scene.get("target_seconds"))
    output_path = project_path(spec["path"])
    target_seconds = output_target_seconds(spec)
    target_wpm = scene_target_wpm(manifest, scene)
    timed_segments = extract_timed_segments(storyboard_path)
    narration = "\n\n".join(
        segment["text"] for segment in timed_segments
    ) if timed_segments else "\n\n".join(sections)

    with tempfile.TemporaryDirectory(prefix="storyboard_audio_") as temp_dir:
        stats = await synthesize_clip(
            edge_tts,
            narration,
            output_path,
            voice,
            rate,
            target_seconds,
            target_wpm,
            Path(temp_dir) / "scene.mp3",
        )

    output_transcript = transcript_path(manifest, scene, output_path)
    output_transcript.parent.mkdir(parents=True, exist_ok=True)
    output_transcript.write_text(
        narration,
        encoding="utf-8",
    )
    print(
        f"Generated {output_path.relative_to(ROOT)}: "
        f"speech={stats['speech_seconds']:.2f}s, "
        f"clip={stats['target_seconds']:.2f}s, "
        f"rate={stats['rate']}, wpm={stats['wpm']:.1f}"
    )


async def synthesize_sectioned_scene(
    edge_tts,
    manifest: dict,
    scene: dict,
    sections: list[str],
    voice: str,
    rate: str,
) -> None:
    target_wpm = scene_target_wpm(manifest, scene)
    transcript_lines = []

    with tempfile.TemporaryDirectory(prefix="storyboard_audio_") as temp_dir:
        temp_root = Path(temp_dir)
        for section_index, (text, raw_specs) in enumerate(
            zip(sections, scene["audio_sections"]),
            start=1,
        ):
            specs = [normalize_output_spec(spec) for spec in raw_specs]
            targets = [output_target_seconds(spec) for spec in specs]
            weights = [target if target is not None else 1.0 for target in targets]
            chunks = split_text_by_weights(text, weights)

            for clip_index, (chunk, spec, target) in enumerate(
                zip(chunks, specs, targets),
                start=1,
            ):
                output_path = project_path(spec["path"])
                if target is None:
                    target = len(chunk.split()) * 60.0 / (target_wpm or 130.0) + 0.5
                stats = await synthesize_clip(
                    edge_tts,
                    chunk,
                    output_path,
                    voice,
                    rate,
                    target,
                    target_wpm,
                    temp_root / f"{section_index:02d}_{clip_index:02d}.mp3",
                )
                transcript_lines.append(
                    f"[section {section_index}, clip {clip_index}] "
                    f"{spec['path']} | rate={stats['rate']} | "
                    f"speech={stats['speech_seconds']:.2f}s | "
                    f"clip={stats['target_seconds']:.2f}s | "
                    f"wpm={stats['wpm']:.1f}\n{chunk}"
                )
                print(
                    f"Generated {spec['path']}: "
                    f"speech={stats['speech_seconds']:.2f}s, "
                    f"clip={stats['target_seconds']:.2f}s, "
                    f"rate={stats['rate']}, wpm={stats['wpm']:.1f}"
                )

    output_transcript = transcript_path(manifest, scene)
    output_transcript.parent.mkdir(parents=True, exist_ok=True)
    output_transcript.write_text("\n\n".join(transcript_lines), encoding="utf-8")


async def run(
    manifest_path: Path,
    scene_id: str | None,
    voice: str | None,
    rate: str | None,
    dry_run: bool,
    list_only: bool,
) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    scenes = selected_scenes(manifest, scene_id)

    if list_only:
        for scene in scenes:
            print(scene["id"])
        return

    for scene in scenes:
        describe_scene(manifest, scene)
    if dry_run:
        return

    try:
        import edge_tts
    except ImportError as exc:
        raise SystemExit(
            "edge-tts is not installed. Run: python -m pip install edge-tts"
        ) from exc

    selected_voice = voice or manifest.get(
        "suggested_voice",
        "en-US-AvaMultilingualNeural",
    )
    selected_rate = rate or manifest.get("default_rate", "-12%")
    parse_rate_percent(selected_rate)

    for scene in scenes:
        storyboard_path, sections = validate_scene_config(manifest, scene)
        if "audio_sections" in scene:
            await synthesize_sectioned_scene(
                edge_tts,
                manifest,
                scene,
                sections,
                selected_voice,
                selected_rate,
            )
        else:
            await synthesize_single_scene(
                edge_tts,
                manifest,
                scene,
                storyboard_path,
                sections,
                selected_voice,
                selected_rate,
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST_PATH,
        help=(
            "Audio manifest path. Defaults to "
            "scripts/audio_manifest/act1_audio_manifest.json."
        ),
    )
    parser.add_argument("--scene", help="Generate one scene id from the manifest.")
    parser.add_argument("--voice", help="Override the manifest Edge TTS voice.")
    parser.add_argument("--rate", help="Override the manifest speaking-rate adjustment.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate storyboard mappings without generating audio.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List scene ids from the selected manifest.",
    )
    args = parser.parse_args()
    manifest_path = project_path(args.manifest)
    if not manifest_path.exists():
        raise SystemExit(f"Manifest not found: {manifest_path}")
    asyncio.run(
        run(
            manifest_path,
            args.scene,
            args.voice,
            args.rate,
            args.dry_run,
            args.list,
        )
    )


if __name__ == "__main__":
    main()
