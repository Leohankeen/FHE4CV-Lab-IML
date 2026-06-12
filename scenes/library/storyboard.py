from pathlib import Path

from manim import *

from .constants import COLOR_MATH


def scene_time(scene):
    renderer = getattr(scene, "renderer", None)
    if renderer is not None and hasattr(renderer, "time"):
        return float(renderer.time)
    return float(getattr(scene, "time", 0.0))


class StoryboardScene(Scene):
    """Scene base for long-form, content-driven storyboard pacing."""

    def add_optional_sound(self, sound_path):
        if Path(sound_path).exists():
            self.add_sound(sound_path)

    def play_section_beats(
        self,
        section_start,
        section_duration,
        section_label,
        beats,
        accent,
    ):
        remaining = section_duration - (scene_time(self) - section_start)
        if remaining <= 0:
            return

        beat_duration = remaining / len(beats)
        for index, beat in enumerate(beats, start=1):
            heading, bullets, footer = self._normalize_beat(beat)
            self.play_content_beat(
                section_label=section_label,
                heading=heading,
                bullets=bullets,
                footer=footer,
                duration=beat_duration,
                index=index,
                total=len(beats),
                accent=accent,
            )

    def play_content_beat(
        self,
        section_label,
        heading,
        bullets,
        footer,
        duration,
        index,
        total,
        accent,
    ):
        start = scene_time(self)

        section = Text(section_label, font_size=21, color=accent).to_corner(UL).shift(DOWN * 0.72)
        counter = Text(f"{index:02d} / {total:02d}", font_size=19, color=GREY_B)
        counter.to_corner(UR).shift(DOWN * 0.74)
        heading_mob = Text(heading, font_size=35, color=WHITE)
        heading_mob.next_to(section, DOWN, aligned_edge=LEFT, buff=0.22)
        rule = Line(LEFT * 5.9, RIGHT * 5.9, color=GREY_D, stroke_width=2)
        rule.next_to(heading_mob, DOWN, buff=0.22)

        bullet_rows = VGroup()
        for bullet in bullets:
            marker = Square(side_length=0.13, color=accent, fill_opacity=0.8)
            text = Text(bullet, font_size=25, color=COLOR_MATH)
            row = VGroup(marker, text).arrange(RIGHT, buff=0.22)
            bullet_rows.add(row)
        bullet_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        bullet_rows.next_to(rule, DOWN, aligned_edge=LEFT, buff=0.42)

        footer_mob = None
        if footer:
            footer_mob = Text(footer, font_size=21, color=GREY_B)
            footer_mob.to_edge(DOWN, buff=0.48)

        track = Line(LEFT * 5.8, RIGHT * 5.8, color=GREY_D, stroke_width=3)
        track.to_edge(DOWN, buff=0.23)
        progress = Dot(track.get_start(), radius=0.055, color=accent)

        fixed = VGroup(section, counter, heading_mob, rule, track, progress)
        if footer_mob:
            fixed.add(footer_mob)

        intro_time = min(1.4, duration * 0.08)
        outro_time = min(1.0, duration * 0.06)
        reveal_time = min(0.8, duration * 0.04)
        emphasis_time = min(1.0, duration * 0.05)
        moving_time = max(
            0.1,
            (duration - intro_time - outro_time - len(bullets) * (reveal_time + emphasis_time))
            / max(1, len(bullets)),
        )

        self.play(
            FadeIn(section),
            FadeIn(counter),
            Write(heading_mob),
            Create(rule),
            FadeIn(track),
            FadeIn(progress),
            *([FadeIn(footer_mob)] if footer_mob else []),
            run_time=intro_time,
        )

        for bullet_index, row in enumerate(bullet_rows, start=1):
            self.play(FadeIn(row, shift=RIGHT * 0.18), run_time=reveal_time)
            self.play(Indicate(row[1], color=accent, scale_factor=1.015), run_time=emphasis_time)
            self.play(
                progress.animate.move_to(track.point_from_proportion(bullet_index / len(bullet_rows))),
                run_time=moving_time,
                rate_func=linear,
            )

        all_mobjects = VGroup(fixed, bullet_rows)
        self.play(FadeOut(all_mobjects), run_time=outro_time)

        leftover = duration - (scene_time(self) - start)
        if leftover > 0.01:
            self.wait(leftover)

    @staticmethod
    def _normalize_beat(beat):
        if len(beat) == 2:
            return beat[0], beat[1], None
        return beat
