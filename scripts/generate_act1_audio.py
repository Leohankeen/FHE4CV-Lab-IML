"""Generate Act 1 AI narration from storyboard voiceover directions.

Install the optional provider first:
    python -m pip install edge-tts

Then generate all four MP3 files:
    python scripts/generate_act1_audio.py
"""

from __future__ import annotations

import argparse
import ast
import asyncio
import json
import re
import tempfile
from pathlib import Path

import av
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "scripts" / "act1_audio_manifest.json"
TIMED_SEGMENT_PATTERN = re.compile(
    r'<!-- AUDIO_SEGMENT id="([^"]+)" duration="([0-9.]+)" -->\s*'
    r"```text\s*(.+?)\s*```",
    flags=re.DOTALL,
)
TIMED_SAMPLE_RATE = 24_000
TARGET_SPEECH_FILL = 0.965
MIN_SPEECH_FILL = 0.94
MAX_SPEECH_FILL = 0.985


def extract_voiceover(storyboard_path: Path) -> str:
    markdown = storyboard_path.read_text(encoding="utf-8")
    sections = re.findall(
        r'-\s+\*\*Lời thoại AI \(Audio Voiceover\):\*\*\s*"(.+?)"'
        r'\s*(?=\n-\s+\*\*Hoạt ảnh Manim)',
        markdown,
        flags=re.DOTALL,
    )
    if not sections:
        raise ValueError(f"No AI voiceover blocks found in {storyboard_path}")

    cleaned = []
    for section in sections:
        text = re.sub(r"`([^`]+)`", r"\1", section)
        text = re.sub(r"\s+", " ", text).strip()
        cleaned.append(text)
    return "\n\n".join(cleaned)


def extract_timed_segments(storyboard_path: Path) -> list[dict]:
    markdown = storyboard_path.read_text(encoding="utf-8")
    return [
        {
            "id": segment_id,
            "duration": float(duration),
            "text": re.sub(r"\s+", " ", text).strip(),
        }
        for segment_id, duration, text in TIMED_SEGMENT_PATTERN.findall(markdown)
    ]


def extract_beats(source_path: Path, method_names: list[str]) -> list[tuple]:
    tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    methods = {
        node.name: node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    beats = []
    for method_name in method_names:
        method = methods.get(method_name)
        if method is None:
            raise ValueError(f"Missing beat method {method_name} in {source_path}")
        returned = next(
            (
                node.value
                for node in ast.walk(method)
                if isinstance(node, ast.Return) and node.value is not None
            ),
            None,
        )
        if returned is None:
            raise ValueError(f"Beat method {method_name} has no return value")
        beats.extend(ast.literal_eval(returned))
    return beats


BRIDGES = (
    (
        "Let us unpack why these details belong together. "
        "In an encrypted system, representation, permitted operations, and key ownership "
        "cannot be designed independently. A decision made at this point will affect "
        "precision, memory, latency, and the operations available later in the circuit."
    ),
    (
        "Now connect this idea to implementation. Microsoft SEAL exposes explicit objects "
        "and metadata because the library cannot silently repair an incompatible circuit. "
        "The developer must know what level, scale, layout, and cryptographic capability "
        "each value carries before requesting the next operation."
    ),
    (
        "A useful mental test is to compare the encrypted path with ordinary plaintext "
        "computation. The mathematical goal may be the same, but the cloud cannot inspect "
        "a hidden value or improvise around a mismatch. The full evaluation schedule must "
        "therefore be prepared before private data enters the system."
    ),
    (
        "From a systems perspective, this is where cryptography meets numerical engineering. "
        "Security alone is not enough, and numerical accuracy alone is not enough. A usable "
        "design preserves the trust boundary while keeping approximation error and resource "
        "consumption inside a budget that the application can tolerate."
    ),
    (
        "Keep the data flow in view while considering this point. The client prepares and "
        "eventually reveals values, while the server receives only the capabilities needed "
        "for evaluation. This separation explains why apparently small choices in encoding "
        "or key generation can have large consequences for the complete deployment."
    ),
)


def narration_for_scene(scene: dict) -> str:
    storyboard_path = ROOT / scene["storyboard"]
    timed_segments = extract_timed_segments(storyboard_path)
    if timed_segments:
        return "\n\n".join(segment["text"] for segment in timed_segments)

    source_path = ROOT / scene["source"]
    beats = extract_beats(source_path, scene["beat_methods"])
    intro = extract_voiceover(storyboard_path)

    paragraphs = [
        (
            f"Welcome to {scene['title']}. "
            f"This lesson is part of Act One, the mathematical and cryptographic foundation "
            f"for privacy-preserving computer vision. {intro} "
            "As the diagrams change, follow the relationship between the visible numerical "
            "idea and the encrypted object that Microsoft SEAL actually manipulates."
        )
    ]

    for index, beat in enumerate(beats, start=1):
        heading, bullets, footer = beat
        first, second, third = bullets
        bridge = BRIDGES[(index - 1) % len(BRIDGES)]
        paragraphs.append(
            " ".join(
                [
                    f"Topic {index}. {heading}.",
                    f"First, {first}",
                    "This establishes the starting condition for the operation shown on screen.",
                    f"Second, {second}",
                    "This changes what the encrypted pipeline must preserve or prepare.",
                    f"Third, {third}",
                    bridge,
                    f"The main takeaway is this: {footer}",
                    "Pause for a moment and relate that takeaway to the current diagram before "
                    "we continue to the next concept.",
                ]
            )
        )

    paragraphs.append(
        "This completes the lesson. The important result is not a list of isolated terms, "
        "but a connected model of data representation, allowed arithmetic, parameter state, "
        "and key capability. We will use that model throughout the remaining encrypted "
        "computer-vision scenes."
    )
    return "\n\n".join(paragraphs)


def decode_mono_s16(path: Path) -> np.ndarray:
    samples = []
    with av.open(str(path)) as container:
        stream = container.streams.audio[0]
        resampler = av.AudioResampler(
            format="s16",
            layout="mono",
            rate=TIMED_SAMPLE_RATE,
        )
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
    window_size = round(0.05 * TIMED_SAMPLE_RATE)
    usable_size = len(samples) - len(samples) % window_size
    if usable_size <= 0:
        return 0.0
    windows = samples[:usable_size].reshape(-1, window_size).astype(np.float64)
    rms = np.sqrt(np.mean(windows * windows, axis=1))
    active_windows = np.flatnonzero(rms > 80)
    if len(active_windows) == 0:
        return 0.0
    return (active_windows[-1] + 1) * window_size / TIMED_SAMPLE_RATE


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


async def synthesize_segment(
    edge_tts,
    text: str,
    output_path: Path,
    voice: str,
    rate: str,
) -> np.ndarray:
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(str(output_path))
    return decode_mono_s16(output_path)


def encode_mp3(samples: np.ndarray, output_path: Path) -> None:
    temporary_path = output_path.with_suffix(".timed.tmp.mp3")
    with av.open(str(temporary_path), mode="w") as container:
        stream = container.add_stream("libmp3lame", rate=TIMED_SAMPLE_RATE)
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
            frame.sample_rate = TIMED_SAMPLE_RATE
            for packet in stream.encode(frame):
                container.mux(packet)
        for packet in stream.encode(None):
            container.mux(packet)
    temporary_path.replace(output_path)


async def synthesize_timed_scene(
    edge_tts,
    scene: dict,
    segments: list[dict],
    voice: str,
    rate: str,
) -> None:
    output_path = ROOT / scene["output"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    timeline = []
    transcript_lines = []
    cursor = 0.0
    target_speech_fill = float(scene.get("target_speech_fill", TARGET_SPEECH_FILL))
    min_speech_fill = float(scene.get("min_speech_fill", MIN_SPEECH_FILL))
    max_speech_fill = float(scene.get("max_speech_fill", MAX_SPEECH_FILL))
    target_wpm = scene.get("target_wpm")
    target_wpm = float(target_wpm) if target_wpm is not None else None
    target_wpm_tolerance = float(scene.get("target_wpm_tolerance", 0.025))

    with tempfile.TemporaryDirectory(prefix="act1_scene_audio_") as temp_dir:
        temp_root = Path(temp_dir)
        for index, segment in enumerate(segments):
            segment_path = temp_root / f"{index:02d}_{segment['id']}.mp3"
            selected_rate = rate
            speech = await synthesize_segment(
                edge_tts,
                segment["text"],
                segment_path,
                voice,
                selected_rate,
            )
            target_samples = round(segment["duration"] * TIMED_SAMPLE_RATE)
            word_count = len(segment["text"].split())
            target_speech_duration = (
                word_count * 60.0 / target_wpm
                if target_wpm is not None
                else segment["duration"] * target_speech_fill
            )
            speech_duration = active_audio_duration(speech)
            speech_fill = speech_duration / segment["duration"]
            measured_wpm = word_count * 60.0 / speech_duration

            needs_refit = (
                abs(measured_wpm - target_wpm) / target_wpm > target_wpm_tolerance
                if target_wpm is not None
                else speech_fill < min_speech_fill or speech_fill > max_speech_fill
            )
            if needs_refit:
                selected_rate = fitted_rate(
                    selected_rate,
                    speech_duration,
                    target_speech_duration,
                )
                speech = await synthesize_segment(
                    edge_tts,
                    segment["text"],
                    segment_path,
                    voice,
                    selected_rate,
                )
                speech_duration = active_audio_duration(speech)
                speech_fill = speech_duration / segment["duration"]
                measured_wpm = word_count * 60.0 / speech_duration

            if (
                target_wpm is not None
                and abs(measured_wpm - target_wpm) / target_wpm
                > target_wpm_tolerance
            ):
                raise ValueError(
                    f"Audio segment {segment['id']} measured {measured_wpm:.1f} wpm, "
                    f"outside the {target_wpm:.1f} wpm target tolerance."
                )
            if len(speech) > target_samples or speech_fill > 1.0:
                raise ValueError(
                    f"Audio segment {segment['id']} is {speech_duration:.2f}s, "
                    f"longer than its {segment['duration']:.2f}s slot. "
                    "Shorten its text or increase --rate."
                )
            padded = np.pad(speech, (0, target_samples - len(speech)))
            timeline.append(padded)
            transcript_lines.append(
                f"[{cursor:06.2f} - {cursor + segment['duration']:06.2f}] "
                f"{segment['id']} | rate={selected_rate} | "
                f"speech={speech_duration:.2f}s | fill={speech_fill * 100:.1f}% | "
                f"wpm={measured_wpm:.1f}\n"
                f"{segment['text']}"
            )
            print(
                f"{segment['id']}: rate={selected_rate} "
                f"speech={speech_duration:.2f}/{segment['duration']:.2f}s "
                f"({speech_fill * 100:.1f}%, {measured_wpm:.1f} wpm)"
            )
            cursor += segment["duration"]

    encode_mp3(np.concatenate(timeline), output_path)
    output_path.with_suffix(".txt").write_text(
        "\n\n".join(transcript_lines),
        encoding="utf-8",
    )
    print(
        f"Generated synchronized {output_path.relative_to(ROOT)} "
        f"({cursor:.2f} seconds, {len(segments)} segments)"
    )


async def synthesize_scene(edge_tts, scene, voice: str, rate: str) -> None:
    storyboard_path = ROOT / scene["storyboard"]
    timed_segments = extract_timed_segments(storyboard_path)
    if timed_segments:
        await synthesize_timed_scene(edge_tts, scene, timed_segments, voice, rate)
        return

    output_path = ROOT / scene["output"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    narration = narration_for_scene(scene)
    transcript_path = output_path.with_suffix(".txt")
    transcript_path.write_text(narration, encoding="utf-8")
    communicate = edge_tts.Communicate(narration, voice=voice, rate=rate)
    await communicate.save(str(output_path))
    print(
        f"Generated {output_path.relative_to(ROOT)} "
        f"({len(narration.split())} narration words)"
    )


async def run(scene_id: str | None, voice: str | None, rate: str) -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise SystemExit(
            "edge-tts is not installed. Run: python -m pip install edge-tts"
        ) from exc

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    selected_voice = voice or manifest["suggested_voice"]
    scenes = manifest["scenes"]
    if scene_id:
        scenes = [scene for scene in scenes if scene["id"] == scene_id]
        if not scenes:
            raise SystemExit(f"Unknown scene id: {scene_id}")

    for scene in scenes:
        await synthesize_scene(edge_tts, scene, selected_voice, rate)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", help="Generate one scene id from the manifest.")
    parser.add_argument("--voice", help="Override the manifest Edge TTS voice.")
    parser.add_argument("--rate", default="-12%", help="Edge TTS speaking-rate adjustment.")
    args = parser.parse_args()
    asyncio.run(run(args.scene, args.voice, args.rate))


if __name__ == "__main__":
    main()
