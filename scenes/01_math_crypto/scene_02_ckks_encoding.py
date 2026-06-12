import os
import sys

from manim import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene, scene_time


class CKKSEncodingAndParameters(StoryboardScene):
    """15-minute visual lesson on CKKS encoding, packing, and parameters."""

    MOTION_TIME = 1.2
    CONTENT_TOP = 2.15
    CONTENT_BOTTOM = -2.65
    APPROXIMATION_DURATIONS = (56.29, 60.09, 61.48, 56.86, 61.48)
    PACKING_DURATIONS = (62.86, 58.25, 60.55, 58.25, 60.09)
    PARAMETER_DURATIONS = (59.08, 59.54, 58.15, 60.00, 63.23)

    @staticmethod
    def fit_text(text, max_width):
        if text.width > max_width:
            text.scale_to_fit_width(max_width)
        return text

    @classmethod
    def motion_step(cls, duration, actions):
        return min(cls.MOTION_TIME, max(0.85, duration / max(1, actions * 9)))

    def card(self, label, color, width=2.1, height=0.82, font_size=23):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            color=color,
            fill_color=color,
            fill_opacity=0.14,
        )
        text = Text(label, font_size=font_size, color=WHITE, line_spacing=0.8)
        self.fit_text(text, width - 0.22)
        text.move_to(box)
        return VGroup(box, text)

    def slot_row(self, values, color=COLOR_PLAINTEXT, cell_size=0.72):
        cells = VGroup()
        for value in values:
            square = Square(
                side_length=cell_size,
                color=color,
                fill_color=color,
                fill_opacity=0.12,
            )
            label = Text(str(value), font_size=18, color=WHITE).move_to(square)
            cells.add(VGroup(square, label))
        cells.arrange(RIGHT, buff=0.08)
        return cells

    @staticmethod
    def meter(label, width, color):
        name = Text(label, font_size=18, color=GREY_B)
        track = Rectangle(width=3.1, height=0.18, color=GREY_D, fill_opacity=0.12)
        fill = Rectangle(
            width=width,
            height=0.18,
            color=color,
            fill_color=color,
            fill_opacity=0.78,
            stroke_width=0,
        )
        fill.move_to(track).align_to(track, LEFT)
        return VGroup(name, VGroup(track, fill)).arrange(RIGHT, buff=0.2)

    def keep_demo_alive(self, demo, accent, duration):
        if duration <= 0.05:
            return
        candidates = [
            mob
            for mob in demo
            if 0.2 < mob.width < 6.4
            and 0.12 < mob.height < 3.8
            and mob.get_top()[1] < self.CONTENT_TOP + 0.2
            and mob.get_bottom()[1] > self.CONTENT_BOTTOM - 0.2
        ]
        if not candidates:
            self.wait(duration)
            return

        cues = []
        elapsed = 0.0
        index = 0
        while elapsed < duration - 0.05:
            cue_time = min(1.15, duration - elapsed)
            target = candidates[index % len(candidates)]
            cues.append(
                target.animate(run_time=cue_time, rate_func=there_and_back)
                .set_stroke(color=accent, opacity=0.95)
            )
            elapsed += cue_time
            index += 1
        self.play(Succession(*cues, lag_ratio=1), run_time=duration)

    def clear_beat(self):
        for mobject in list(self.mobjects):
            if mobject is not getattr(self, "lesson_title", None):
                self.remove(mobject)

    def play_timed_section(
        self,
        section_start,
        section_duration,
        section_label,
        beats,
        accent,
        beat_durations=None,
    ):
        remaining = section_duration - (scene_time(self) - section_start)
        if remaining <= 0:
            return

        durations = (
            list(beat_durations)
            if beat_durations is not None
            else [remaining / len(beats)] * len(beats)
        )
        if len(durations) != len(beats):
            raise ValueError("Each storyboard beat needs one timeline duration.")
        durations[-1] += remaining - sum(durations)

        for index, (beat, duration) in enumerate(zip(beats, durations), start=1):
            heading, bullets, footer = self._normalize_beat(beat)
            self.play_content_beat(
                section_label=section_label,
                heading=heading,
                bullets=bullets,
                footer=footer,
                duration=duration,
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
        section_key = (
            "approximation"
            if "Approximation" in section_label
            else "packing"
            if "Packing" in section_label
            else "parameters"
        )
        heading_mob = Text(heading, font_size=32, color=WHITE)
        self.fit_text(heading_mob, 10.8)
        heading_mob.to_edge(UP, buff=0.72)
        rule = Line(LEFT * 5.8, RIGHT * 5.8, color=GREY_D, stroke_width=2)
        rule.next_to(heading_mob, DOWN, buff=0.2)
        footer_mob = Text(footer, font_size=20, color=GREY_B)
        self.fit_text(footer_mob, 11.0)
        footer_mob.to_edge(DOWN, buff=0.5)

        self.play(
            FadeIn(heading_mob, shift=UP * 0.12),
            Create(rule),
            run_time=0.85,
            rate_func=smooth,
        )
        demo = getattr(self, f"demo_{section_key}_{index}")(
            accent,
            max(8.0, duration - 3.4),
        )
        self.play(FadeIn(footer_mob, shift=UP * 0.12), run_time=0.55)
        self.bring_to_front(heading_mob, rule, footer_mob)

        remaining = duration - (scene_time(self) - start) - 0.75
        self.keep_demo_alive(demo, accent, remaining)
        self.play(
            FadeOut(VGroup(heading_mob, rule, demo, footer_mob)),
            run_time=0.75,
            rate_func=smooth,
        )
        self.clear_beat()
        leftover = duration - (scene_time(self) - start)
        if leftover > 0.01:
            self.wait(leftover)

    def open_lesson(self, lesson_title, audio_path):
        self.camera.background_color = "#101214"
        self.add_optional_sound(audio_path)
        act = Text("ACT 1 | MATHEMATICS AND CRYPTOGRAPHY", font_size=25, color=YELLOW_D)
        title = Text(lesson_title, font_size=42, color=WHITE)
        self.fit_text(title, 11.4)
        title.move_to(DOWN * 0.1)
        act.next_to(title, UP, buff=0.5)
        rule = Line(LEFT * 5.5, RIGHT * 5.5, color=GREY_D)
        rule.next_to(title, DOWN, buff=0.4)
        self.play(FadeIn(act, shift=DOWN * 0.12), Write(title), run_time=1.5)
        self.play(Create(rule), run_time=0.5)
        self.wait(0.8)
        self.play(
            FadeOut(act),
            FadeOut(rule),
            FadeOut(title),
            run_time=1,
        )
        self.lesson_title = None
        return title

    # ------------------------------------------------------------------
    # 2.1 Approximation and scale
    # ------------------------------------------------------------------

    def demo_approximation_1(self, accent, duration):
        step = self.motion_step(duration, 6)
        line = NumberLine(
            x_range=[3.13, 3.15, 0.005],
            length=9,
            include_numbers=False,
            color=GREY_C,
        ).shift(DOWN * 0.15)
        tick_labels = VGroup(
            *[
                Text(label, font_size=17, color=GREY_B).next_to(line.n2p(value), DOWN, buff=0.16)
                for value, label in ((3.13, "3.13"), (3.14, "3.14"), (3.15, "3.15"))
            ]
        )
        exact = Dot(line.n2p(3.14159265), color=BLUE_C, radius=0.1)
        decoded = Dot(line.n2p(3.1415), color=YELLOW_D, radius=0.1)
        legend = VGroup(
            VGroup(Dot(color=BLUE_C, radius=0.07), Text("original", font_size=18, color=BLUE_C)).arrange(RIGHT, buff=0.14),
            VGroup(Dot(color=YELLOW_D, radius=0.07), Text("decoded", font_size=18, color=YELLOW_D)).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(LEFT * 4.5 + UP * 1.15)
        error = DoubleArrow(exact.get_center(), decoded.get_center(), buff=0, color=RED_C)
        tolerance = Line(
            line.n2p(3.1405),
            line.n2p(3.1425),
            color=GREEN_C,
            stroke_width=10,
        ).shift(UP * 0.58)
        tolerance_label = Text("accepted tolerance", font_size=19, color=GREEN_C)
        tolerance_label.next_to(tolerance, UP, buff=0.12)
        self.play(Create(line), FadeIn(tick_labels), FadeIn(exact), FadeIn(legend[0]), run_time=step)
        self.play(TransformFromCopy(exact, decoded), FadeIn(legend[1]), run_time=step)
        self.play(GrowFromCenter(error), run_time=step)
        self.play(Create(tolerance), FadeIn(tolerance_label), run_time=step)
        self.play(Indicate(decoded, color=GREEN_C), Flash(tolerance, color=GREEN_C), run_time=step)
        self.play(Circumscribe(VGroup(exact, decoded), color=accent), run_time=step)
        return VGroup(
            line,
            tick_labels,
            exact,
            decoded,
            legend,
            error,
            tolerance,
            tolerance_label,
        )

    def demo_approximation_2(self, accent, duration):
        step = self.motion_step(duration, 7)
        value = self.card("3.14159265", BLUE_C, 2.0, 0.78, 24).move_to(LEFT * 4.8)
        scale = VGroup(
            Circle(radius=0.72, color=YELLOW_D, fill_opacity=0.08),
            Text("x 2^40", font_size=23, color=YELLOW_D),
        ).move_to(LEFT * 1.5)
        scale[1].move_to(scale[0])
        round_gate = self.card("round", PURPLE_C, 1.6, 0.78, 22).move_to(RIGHT * 1.25)
        encoded = self.card("3454217652...", RED_C, 2.35, 0.78, 21).move_to(RIGHT * 4.45)
        arrows = VGroup(
            Arrow(value.get_right(), scale.get_left(), buff=0.16, color=accent),
            Arrow(scale.get_right(), round_gate.get_left(), buff=0.16, color=accent),
            Arrow(round_gate.get_right(), encoded.get_left(), buff=0.16, color=accent),
        )
        token = Dot(value.get_center(), color=BLUE_C, radius=0.09)
        precision = VGroup(*[Line(ORIGIN, UP * (0.25 + i * 0.04), color=GREEN_C) for i in range(8)])
        precision.arrange(RIGHT, buff=0.08).next_to(scale, DOWN, buff=0.5)
        self.play(FadeIn(value), FadeIn(token), FadeIn(scale), run_time=step)
        self.play(GrowArrow(arrows[0]), MoveAlongPath(token, arrows[0]), Rotate(scale[0], PI), run_time=step)
        self.play(FadeIn(round_gate), GrowArrow(arrows[1]), MoveAlongPath(token, arrows[1]), run_time=step)
        self.play(LaggedStart(*(Create(mark) for mark in precision), lag_ratio=0.08), run_time=step)
        self.play(FadeIn(encoded), GrowArrow(arrows[2]), MoveAlongPath(token, arrows[2]), run_time=step)
        self.play(FadeOut(token), run_time=step * 0.55)
        self.play(Indicate(precision, color=GREEN_C), Circumscribe(encoded, color=accent), run_time=step)
        return VGroup(value, scale, round_gate, encoded, arrows, token, precision)

    def demo_approximation_3(self, accent, duration):
        step = self.motion_step(duration, 7)
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 4, 1],
            x_length=4.2,
            y_length=2.2,
            tips=False,
            axis_config={"color": GREY_C, "include_numbers": False},
        ).move_to(LEFT * 3.35 + DOWN * 0.1)
        heights = [1.2, 2.8, 1.8, 3.2, 1.0]
        stems = VGroup(
            *[
                Line(axes.c2p(i + 0.7, 0), axes.c2p(i + 0.7, height), color=PURPLE_C)
                for i, height in enumerate(heights)
            ]
        )
        dots = VGroup(*[Dot(stem.get_end(), color=PURPLE_C, radius=0.08) for stem in stems])
        divider = VGroup(
            Circle(radius=0.72, color=YELLOW_D),
            Text("/ scale", font_size=22, color=YELLOW_D),
        ).move_to(0.45 * RIGHT)
        divider[1].move_to(divider[0])
        output = self.card("3.14159", GREEN_C, 1.9, 0.82, 25).move_to(RIGHT * 4.25)
        path = Arrow(divider.get_right(), output.get_left(), buff=0.18, color=accent)
        polynomial_path = Arrow(axes.get_right(), divider.get_left(), buff=0.2, color=accent)
        reference = Text("3.14159265", font_size=21, color=BLUE_C).next_to(output, UP, buff=0.4)
        error = DoubleArrow(reference.get_bottom(), output.get_top(), buff=0.06, color=RED_C)
        self.play(Create(axes), LaggedStart(*(Create(stem) for stem in stems), lag_ratio=0.08), run_time=step)
        self.play(LaggedStart(*(FadeIn(dot) for dot in dots), lag_ratio=0.08), run_time=step)
        self.play(FadeIn(divider), GrowArrow(polynomial_path), run_time=step)
        self.play(Rotate(divider[0], PI), run_time=step)
        self.play(GrowArrow(path), TransformFromCopy(dots, output), run_time=step)
        self.play(FadeIn(reference), GrowFromCenter(error), run_time=step)
        self.play(Indicate(output, color=GREEN_C), run_time=step)
        return VGroup(axes, stems, dots, divider, output, path, polynomial_path, reference, error)

    def demo_approximation_4(self, accent, duration):
        step = self.motion_step(duration, 8)
        stages = VGroup(
            self.card("encode", BLUE_C, 1.5, 0.72, 20),
            self.card("encrypt", RED_C, 1.5, 0.72, 20),
            self.card("evaluate", PURPLE_C, 1.5, 0.72, 20),
            self.card("rescale", YELLOW_D, 1.5, 0.72, 20),
        ).arrange(RIGHT, buff=0.72).shift(UP * 0.55)
        arrows = VGroup(
            *[
                Arrow(stages[i].get_right(), stages[i + 1].get_left(), buff=0.12, color=GREY_B)
                for i in range(3)
            ]
        )
        track = Rectangle(width=8.2, height=0.28, color=GREY_D, fill_opacity=0.1).shift(DOWN * 1.0)
        fills = VGroup()
        widths = [0.75, 0.55, 1.1, 0.7]
        colors = [BLUE_C, RED_C, PURPLE_C, YELLOW_D]
        left = track.get_left()
        for width, color in zip(widths, colors):
            fill = Rectangle(
                width=width,
                height=0.28,
                color=color,
                fill_color=color,
                fill_opacity=0.8,
                stroke_width=0,
            )
            fill.align_to(track, LEFT).move_to(left + RIGHT * width / 2)
            left = fill.get_right()
            fills.add(fill)
        token = Dot(stages[0].get_center(), color=WHITE, radius=0.08)
        self.play(FadeIn(stages[0]), FadeIn(token), Create(track), run_time=step)
        self.play(FadeIn(fills[0]), Flash(stages[0], color=BLUE_C), run_time=step)
        for index in range(3):
            self.play(
                GrowArrow(arrows[index]),
                FadeIn(stages[index + 1]),
                MoveAlongPath(token, arrows[index]),
                run_time=step,
            )
            self.play(FadeIn(fills[index + 1]), Flash(stages[index + 1], color=colors[index + 1]), run_time=step)
        self.play(Indicate(fills, color=accent), run_time=step)
        return VGroup(stages, arrows, track, fills, token)

    def demo_approximation_5(self, accent, duration):
        step = self.motion_step(duration, 7)
        line = NumberLine(
            x_range=[0.84, 0.9, 0.01],
            length=8.8,
            include_numbers=False,
            color=GREY_C,
        ).shift(DOWN * 0.15)
        tick_labels = VGroup(
            Text("0.84", font_size=17, color=GREY_B).next_to(line.n2p(0.84), DOWN, buff=0.16),
            Text("0.90", font_size=17, color=GREY_B).next_to(line.n2p(0.90), DOWN, buff=0.16),
        )
        baseline = Dot(line.n2p(0.872), color=BLUE_C, radius=0.1)
        fhe = Dot(line.n2p(0.869), color=RED_C, radius=0.1)
        legend = VGroup(
            VGroup(Dot(color=BLUE_C, radius=0.07), Text("plain  0.872", font_size=18, color=BLUE_C)).arrange(RIGHT, buff=0.14),
            VGroup(Dot(color=RED_C, radius=0.07), Text("FHE   0.869", font_size=18, color=RED_C)).arrange(RIGHT, buff=0.14),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(LEFT * 4.25 + UP * 1.2)
        band = Line(line.n2p(0.862), line.n2p(0.882), color=GREEN_C, stroke_width=12).shift(UP * 0.65)
        band_label = Text("accepted range", font_size=18, color=GREEN_C).next_to(band, UP, buff=0.14)
        needle = DoubleArrow(baseline.get_center(), fhe.get_center(), buff=0, color=YELLOW_D)
        threshold = Text("|error| < tolerance", font_size=24, color=GREEN_C).to_edge(DOWN, buff=1.05)
        check = Text("PASS", font_size=30, color=GREEN_C, weight=BOLD).next_to(threshold, RIGHT, buff=0.5)
        self.play(Create(line), FadeIn(tick_labels), FadeIn(baseline), FadeIn(legend[0]), run_time=step)
        self.play(Create(band), FadeIn(band_label), run_time=step)
        self.play(TransformFromCopy(baseline, fhe), FadeIn(legend[1]), run_time=step)
        self.play(GrowFromCenter(needle), run_time=step)
        self.play(Write(threshold), run_time=step)
        self.play(FadeIn(check, scale=0.8), Flash(fhe, color=GREEN_C), run_time=step)
        self.play(Circumscribe(VGroup(band, baseline, fhe), color=accent), run_time=step)
        return VGroup(
            line,
            tick_labels,
            baseline,
            fhe,
            legend,
            band,
            band_label,
            needle,
            threshold,
            check,
        )

    # ------------------------------------------------------------------
    # 2.2 SIMD packing
    # ------------------------------------------------------------------

    def demo_packing_1(self, accent, duration):
        step = self.motion_step(duration, 8)
        values = self.slot_row(["0.2", "-1.1", "3.4", "0.8", "2.0", "-0.5"], BLUE_C, 0.66)
        values.move_to(UP * 1.15 + RIGHT * 0.85)
        value_label = Text("INPUT VALUES", font_size=17, color=BLUE_C).move_to(LEFT * 4.7 + UP * 1.15)
        slots = self.slot_row(["", "", "", "", "", ""], YELLOW_D, 0.58).move_to(RIGHT * 0.85)
        slot_label = Text("ENCODED SLOTS", font_size=17, color=YELLOW_D).move_to(LEFT * 4.7)
        encoder = Arrow(values.get_bottom(), slots.get_top(), buff=0.16, color=PURPLE_C)
        encoder_label = Text("encode", font_size=17, color=PURPLE_C).next_to(encoder, RIGHT, buff=0.14)
        cipher = RoundedRectangle(
            width=5.2,
            height=0.92,
            corner_radius=0.18,
            color=RED_C,
            fill_color=RED_C,
            fill_opacity=0.08,
        ).move_to(DOWN * 1.35 + RIGHT * 0.85)
        cipher_slots = slots.copy().move_to(cipher)
        cipher_label = Text("ONE CIPHERTEXT", font_size=17, color=RED_C).move_to(LEFT * 4.7 + DOWN * 1.35)
        pack_arrow = Arrow(slots.get_bottom(), cipher.get_top(), buff=0.16, color=accent)
        self.play(
            FadeIn(value_label),
            LaggedStart(*(FadeIn(cell) for cell in values), lag_ratio=0.08),
            run_time=step,
        )
        self.play(GrowArrow(encoder), FadeIn(encoder_label), FadeIn(slot_label), run_time=step)
        self.play(
            LaggedStart(
                *(TransformFromCopy(value, slot) for value, slot in zip(values, slots)),
                lag_ratio=0.08,
            ),
            run_time=step,
        )
        self.play(Indicate(slots, color=YELLOW_D), run_time=step)
        self.play(Create(cipher), GrowArrow(pack_arrow), FadeIn(cipher_label), run_time=step)
        self.play(TransformFromCopy(slots, cipher_slots), run_time=step)
        self.play(Circumscribe(cipher, color=RED_C), run_time=step)
        return VGroup(
            values,
            value_label,
            slots,
            slot_label,
            encoder,
            encoder_label,
            cipher,
            cipher_slots,
            cipher_label,
            pack_arrow,
        )

    def demo_packing_2(self, accent, duration):
        step = self.motion_step(duration, 8)
        track = NumberLine(
            x_range=[0, 2, 1],
            length=8.0,
            include_numbers=False,
            color=GREY_C,
        ).shift(UP * 1.0)
        degrees = VGroup(
            *[
                Text(label, font_size=21, color=YELLOW_D if index == 1 else GREY_B)
                .next_to(track.n2p(index), UP, buff=0.28)
                for index, label in enumerate(("N = 4096", "N = 8192", "N = 16384"))
            ]
        )
        selector = Triangle(color=accent, fill_color=accent, fill_opacity=1).scale(0.13).rotate(PI)
        selector.next_to(track.n2p(0), DOWN, buff=0.1)
        grid = self.slot_row([""] * 8, BLUE_C, 0.55).shift(DOWN * 0.2)
        frame = SurroundingRectangle(grid, color=RED_C, buff=0.15)
        count = Text("2048", font_size=32, color=GREEN_C).next_to(grid, DOWN, buff=0.55)
        suffix = Text("complex slots", font_size=21, color=GREEN_C).next_to(count, RIGHT, buff=0.18)
        count_4096 = Text("4096", font_size=32, color=GREEN_C).move_to(count)
        count_8192 = Text("8192", font_size=32, color=GREEN_C).move_to(count)
        self.play(Create(track), FadeIn(degrees), FadeIn(selector), run_time=step)
        self.play(FadeIn(grid), Create(frame), FadeIn(count), FadeIn(suffix), run_time=step)
        self.play(selector.animate.next_to(track.n2p(1), DOWN, buff=0.1), Transform(count, count_4096), run_time=step)
        self.play(
            LaggedStart(*(cell[0].animate.set_fill(BLUE_C, opacity=0.55) for cell in grid), lag_ratio=0.06),
            run_time=step,
        )
        self.play(Indicate(degrees[1], color=YELLOW_D), run_time=step)
        self.play(selector.animate.next_to(track.n2p(2), DOWN, buff=0.1), Transform(count, count_8192), run_time=step)
        self.play(frame.animate.scale(1.08), grid.animate.scale(1.08), run_time=step)
        self.play(
            selector.animate.next_to(track.n2p(1), DOWN, buff=0.1),
            Transform(count, count_4096.copy()),
            frame.animate.scale(1 / 1.08),
            grid.animate.scale(1 / 1.08),
            run_time=step,
        )
        self.play(Circumscribe(VGroup(count, suffix), color=accent), run_time=step)
        return VGroup(degrees, track, selector, grid, frame, count, suffix)

    def demo_packing_3(self, accent, duration):
        step = self.motion_step(duration, 8)
        row_a = self.slot_row([1, 2, 3, 4], BLUE_C).move_to(LEFT * 3.5 + UP * 1.0)
        row_b = self.slot_row([10, 20, 30, 40], YELLOW_D).move_to(LEFT * 3.5 + DOWN * 0.55)
        gate = VGroup(
            Circle(radius=0.75, color=PURPLE_C, fill_opacity=0.08),
            Text("+", font_size=40, color=PURPLE_C),
        ).move_to(0.3 * RIGHT + UP * 0.2)
        gate[1].move_to(gate[0])
        output = self.slot_row([11, 22, 33, 44], GREEN_C).move_to(RIGHT * 4.0 + UP * 0.2)
        paths = VGroup(
            Arrow(row_a.get_right(), gate.get_left() + UP * 0.2, buff=0.15, color=BLUE_C),
            Arrow(row_b.get_right(), gate.get_left() + DOWN * 0.2, buff=0.15, color=YELLOW_D),
            Arrow(gate.get_right(), output.get_left(), buff=0.15, color=GREEN_C),
        )
        tokens_a = VGroup(*[Dot(cell.get_center(), color=BLUE_C, radius=0.06) for cell in row_a])
        tokens_b = VGroup(*[Dot(cell.get_center(), color=YELLOW_D, radius=0.06) for cell in row_b])
        self.play(FadeIn(row_a), FadeIn(row_b), FadeIn(tokens_a), FadeIn(tokens_b), run_time=step)
        self.play(FadeIn(gate), GrowArrow(paths[0]), GrowArrow(paths[1]), run_time=step)
        self.play(tokens_a.animate.move_to(gate), tokens_b.animate.move_to(gate), run_time=step)
        self.play(Rotate(gate[0], PI), run_time=step)
        self.play(GrowArrow(paths[2]), run_time=step)
        self.play(LaggedStart(*(FadeIn(cell) for cell in output), lag_ratio=0.08), run_time=step)
        self.play(LaggedStart(*(Flash(cell, color=GREEN_C) for cell in output), lag_ratio=0.08), run_time=step)
        self.play(Circumscribe(output, color=accent), run_time=step)
        return VGroup(row_a, row_b, gate, output, paths, tokens_a, tokens_b)

    def demo_packing_4(self, accent, duration):
        step = self.motion_step(duration, 7)
        data = self.slot_row([5, 8, 2, 9, 4, 7], RED_C, 0.68).shift(DOWN * 0.25)
        mask = self.slot_row([1, 0, 1, 0, 1, 0], GREEN_C, 0.68).next_to(data, UP, buff=0.55)
        result = self.slot_row([5, 0, 2, 0, 4, 0], YELLOW_D, 0.68).next_to(data, DOWN, buff=0.65)
        multiply = Text("x", font_size=30, color=YELLOW_D).next_to(data, LEFT, buff=0.45)
        arrow = Arrow(data.get_bottom(), result.get_top(), buff=0.16, color=accent)
        self.play(FadeIn(data), run_time=step)
        self.play(LaggedStart(*(FadeIn(cell, shift=DOWN * 0.12) for cell in mask), lag_ratio=0.08), run_time=step)
        self.play(FadeIn(multiply), run_time=step)
        self.play(
            LaggedStart(
                *(
                    data[index][0].animate.set_fill(RED_C, opacity=0.05 if index % 2 else 0.4)
                    for index in range(6)
                ),
                lag_ratio=0.08,
            ),
            run_time=step,
        )
        self.play(GrowArrow(arrow), TransformFromCopy(data, result), run_time=step)
        self.play(
            LaggedStart(*(Indicate(result[index], color=GREEN_C) for index in (0, 2, 4)), lag_ratio=0.12),
            run_time=step,
        )
        self.play(Circumscribe(VGroup(mask, result), color=accent), run_time=step)
        return VGroup(data, mask, result, multiply, arrow)

    def demo_packing_5(self, accent, duration):
        step = self.motion_step(duration, 11)
        original = self.slot_row([1, 2, 3, 4], RED_C).move_to(LEFT * 3.45 + UP * 0.65)
        rotated = self.slot_row([4, 1, 2, 3], YELLOW_D).move_to(RIGHT * 3.45 + UP * 0.65)
        rotation = Arrow(original.get_right(), rotated.get_left(), buff=0.22, color=YELLOW_D)
        rotation_label = Text("rotate by 1", font_size=19, color=YELLOW_D).next_to(rotation, UP, buff=0.12)
        key = self.card("Galois key", GREEN_C, 1.65, 0.62, 18).next_to(rotation, DOWN, buff=0.18)
        key_note = Text("enables the shift", font_size=17, color=GREEN_C).next_to(key, DOWN, buff=0.1)

        self.play(FadeIn(original), run_time=step)
        self.play(GrowArrow(rotation), FadeIn(rotation_label), FadeIn(key), run_time=step)
        self.play(Flash(key, color=GREEN_C), FadeIn(key_note), run_time=step)
        self.play(TransformFromCopy(original, rotated), run_time=step)
        self.play(Indicate(rotated, color=YELLOW_D), run_time=step)

        partial = self.slot_row([5, 3, 5, 7], BLUE_C).move_to(UP * 1.0)
        rotated_two = self.slot_row([5, 7, 5, 3], YELLOW_D).move_to(DOWN * 0.25)
        plus = Text("+", font_size=30, color=WHITE).move_to(LEFT * 2.05 + DOWN * 0.25)
        divider = Line(LEFT * 2.0, RIGHT * 2.0, color=GREY_C).shift(DOWN * 0.78)
        result = self.slot_row([10, 10, 10, 10], GREEN_C).move_to(DOWN * 1.35)
        partial_label = Text("PARTIAL SUMS", font_size=16, color=BLUE_C).next_to(partial, UP, buff=0.14)
        rotate_two_label = Text("ROTATE PARTIAL BY 2", font_size=16, color=YELLOW_D).next_to(rotated_two, UP, buff=0.14)
        result_label = Text("TOTAL IN EVERY SLOT", font_size=16, color=GREEN_C).next_to(result, DOWN, buff=0.14)
        self.play(
            FadeOut(VGroup(original, rotated, rotation, rotation_label, key, key_note)),
            FadeIn(partial),
            FadeIn(partial_label),
            run_time=step,
        )
        self.play(FadeIn(rotated_two), FadeIn(rotate_two_label), FadeIn(plus), run_time=step)
        self.play(Create(divider), run_time=step)
        self.play(
            LaggedStart(*(FadeIn(cell) for cell in result), lag_ratio=0.08),
            FadeIn(result_label),
            run_time=step,
        )
        self.play(Circumscribe(result, color=accent), run_time=step)
        return VGroup(
            partial,
            partial_label,
            rotated_two,
            rotate_two_label,
            plus,
            divider,
            result,
            result_label,
        )

    # ------------------------------------------------------------------
    # 2.3 Parameters and rescaling
    # ------------------------------------------------------------------

    def demo_parameters_1(self, accent, duration):
        step = self.motion_step(duration, 8)
        slider = NumberLine(
            x_range=[0, 2, 1],
            length=7.2,
            include_numbers=False,
            color=GREY_C,
        ).shift(UP * 1.2)
        labels = VGroup(
            Text("4096", font_size=20),
            Text("8192", font_size=20),
            Text("16384", font_size=20),
        )
        for index, label in enumerate(labels):
            label.next_to(slider.n2p(index), UP, buff=0.18)
        selector = Triangle(color=accent, fill_color=accent, fill_opacity=1).scale(0.13).rotate(PI)
        selector.next_to(slider.n2p(0), DOWN, buff=0.1)
        slots = self.slot_row([""] * 6, BLUE_C, 0.48).shift(LEFT * 3.5 + DOWN * 0.45)
        capacity = self.meter("capacity", 1.0, GREEN_C).move_to(RIGHT * 2.55 + UP * 0.15)
        cost = self.meter("memory / time", 0.8, RED_C).move_to(RIGHT * 2.55 + DOWN * 0.65)
        self.play(Create(slider), FadeIn(labels), FadeIn(selector), run_time=step)
        self.play(FadeIn(slots), FadeIn(capacity), FadeIn(cost), run_time=step)
        self.play(
            selector.animate.next_to(slider.n2p(1), DOWN, buff=0.1),
            slots.animate.scale(1.18),
            capacity[1][1].animate.stretch_to_fit_width(2.0, about_edge=LEFT),
            cost[1][1].animate.stretch_to_fit_width(1.55, about_edge=LEFT),
            run_time=step,
        )
        self.play(Indicate(labels[1], color=YELLOW_D), run_time=step)
        self.play(
            selector.animate.next_to(slider.n2p(2), DOWN, buff=0.1),
            slots.animate.scale(1.16),
            capacity[1][1].animate.stretch_to_fit_width(2.8, about_edge=LEFT),
            cost[1][1].animate.stretch_to_fit_width(2.55, about_edge=LEFT),
            run_time=step,
        )
        self.play(Indicate(capacity, color=GREEN_C), run_time=step)
        self.play(Indicate(cost, color=RED_C), run_time=step)
        self.play(Circumscribe(VGroup(slider, slots, capacity, cost), color=accent), run_time=step)
        return VGroup(slider, labels, selector, slots, capacity, cost)

    def demo_parameters_2(self, accent, duration):
        step = self.motion_step(duration, 8)
        primes = VGroup(
            *[self.card(label, color, 1.35, 0.68, 21) for label, color in zip(
                ("q3", "q2", "q1", "q0"),
                (RED_C, PURPLE_C, BLUE_C, YELLOW_D),
            )]
        ).arrange(RIGHT, buff=0.3).shift(UP * 1.2)
        levels = VGroup()
        for row, count in enumerate((4, 3, 2, 1)):
            active = VGroup(*[prime.copy().scale(0.64) for prime in primes[:count]])
            active.arrange(RIGHT, buff=0.12)
            tag = Text(f"level {3 - row}", font_size=19, color=GREY_B)
            levels.add(VGroup(tag, active).arrange(RIGHT, buff=0.35))
        levels.arrange(DOWN, aligned_edge=LEFT, buff=0.16).shift(DOWN * 0.65)
        token = Dot(levels[0].get_left() + LEFT * 0.25, color=accent, radius=0.09)
        ids = VGroup(
            *[Text(f"id {index}", font_size=17, color=GREEN_C).next_to(level, RIGHT, buff=0.25)
              for index, level in enumerate(levels)]
        )
        self.play(LaggedStart(*(FadeIn(prime) for prime in primes), lag_ratio=0.1), run_time=step)
        self.play(LaggedStart(*(FadeIn(level) for level in levels), lag_ratio=0.1), FadeIn(token), run_time=step)
        self.play(LaggedStart(*(FadeIn(item) for item in ids), lag_ratio=0.1), run_time=step)
        for level in levels[1:]:
            self.play(token.animate.move_to(level.get_left() + LEFT * 0.25), run_time=step)
        self.play(Indicate(primes, color=accent), run_time=step)
        self.play(Circumscribe(VGroup(levels, ids), color=GREEN_C), run_time=step)
        return VGroup(primes, levels, token, ids)

    def demo_parameters_3(self, accent, duration):
        step = self.motion_step(duration, 7)
        left = self.card("scale 2^40", BLUE_C, 2.0, 0.78, 23).move_to(LEFT * 4.35 + UP * 0.75)
        right = self.card("scale 2^40", BLUE_C, 2.0, 0.78, 23).move_to(LEFT * 4.35 + DOWN * 0.75)
        gate = VGroup(
            Circle(radius=0.72, color=YELLOW_D, fill_opacity=0.08),
            Text("x", font_size=38, color=YELLOW_D),
        ).move_to(LEFT * 0.8)
        gate[1].move_to(gate[0])
        output = self.card("scale 2^80", RED_C, 2.1, 0.82, 25).move_to(RIGHT * 3.7)
        paths = VGroup(
            Arrow(left.get_right(), gate.get_left() + UP * 0.2, buff=0.18, color=BLUE_C),
            Arrow(right.get_right(), gate.get_left() + DOWN * 0.2, buff=0.18, color=BLUE_C),
            Arrow(gate.get_right(), output.get_left(), buff=0.18, color=RED_C),
        )
        gauge = Rectangle(width=4.0, height=0.22, color=GREY_D).next_to(output, DOWN, buff=0.55)
        fill = Rectangle(
            width=1.8,
            height=0.22,
            color=GREEN_C,
            fill_color=GREEN_C,
            fill_opacity=0.75,
            stroke_width=0,
        ).move_to(gauge).align_to(gauge, LEFT)
        ceiling = Line(gauge.get_right() + DOWN * 0.18, gauge.get_right() + UP * 0.18, color=RED_C)
        self.play(FadeIn(left), FadeIn(right), FadeIn(gate), run_time=step)
        self.play(GrowArrow(paths[0]), GrowArrow(paths[1]), run_time=step)
        self.play(Rotate(gate[0], PI), run_time=step)
        self.play(GrowArrow(paths[2]), FadeIn(output), run_time=step)
        self.play(Create(gauge), FadeIn(fill), Create(ceiling), run_time=step)
        self.play(fill.animate.stretch_to_fit_width(3.75, about_edge=LEFT).set_color(RED_C), run_time=step)
        self.play(Flash(ceiling, color=RED_C), Indicate(output, color=RED_C), run_time=step)
        return VGroup(left, right, gate, output, paths, gauge, fill, ceiling)

    def demo_parameters_4(self, accent, duration):
        step = self.motion_step(duration, 8)
        chain = VGroup(
            *[self.card(label, color, 1.45, 0.7, 21) for label, color in zip(
                ("60 bit", "40 bit", "40 bit", "60 bit"),
                (RED_C, PURPLE_C, BLUE_C, YELLOW_D),
            )]
        ).arrange(RIGHT, buff=0.22).shift(UP * 1.15)
        scale_before = self.meter("scale 2^80", 2.9, RED_C).shift(LEFT * 2.3 + DOWN * 0.45)
        scale_after = self.meter("scale 2^40", 1.55, GREEN_C).move_to(scale_before)
        level_before = Text("level 3", font_size=22, color=GREY_B).next_to(scale_before, DOWN, buff=0.45)
        level_after = Text("level 2", font_size=22, color=GREEN_C).move_to(level_before)
        dropped = chain[-1].copy()
        drop_arrow = Arrow(chain[-1].get_bottom(), chain[-1].get_bottom() + DOWN * 1.25, color=YELLOW_D)
        self.play(LaggedStart(*(FadeIn(prime) for prime in chain), lag_ratio=0.1), run_time=step)
        self.play(FadeIn(scale_before), FadeIn(level_before), run_time=step)
        self.play(Indicate(chain[-1], color=YELLOW_D), run_time=step)
        self.play(GrowArrow(drop_arrow), dropped.animate.shift(DOWN * 1.25).set_opacity(0.15), run_time=step)
        self.play(FadeOut(chain[-1]), FadeOut(dropped), FadeOut(drop_arrow), run_time=step)
        self.play(Transform(scale_before, scale_after), Transform(level_before, level_after), run_time=step)
        self.play(chain[:-1].animate.shift(RIGHT * 0.55), run_time=step)
        self.play(Circumscribe(VGroup(chain[:-1], scale_before, level_before), color=accent), run_time=step)
        return VGroup(chain, scale_before, level_before)

    def demo_parameters_5(self, accent, duration):
        step = self.motion_step(duration, 11)
        level_names = ("start", "after multiply 1", "after multiply 2", "after multiply 3")
        level_colors = (GREEN_C, YELLOW_D, ORANGE, RED_C)
        levels = VGroup()
        for name, color in zip(level_names, level_colors):
            bar = RoundedRectangle(
                width=4.1,
                height=0.48,
                corner_radius=0.06,
                color=color,
                fill_color=color,
                fill_opacity=0.12,
            )
            label = Text(name, font_size=18, color=color).move_to(bar)
            levels.add(VGroup(bar, label))
        levels.arrange(DOWN, buff=0.34).move_to(LEFT * 3.25 + DOWN * 0.15)
        arrows = VGroup(
            *[
                Arrow(
                    levels[index].get_bottom(),
                    levels[index + 1].get_top(),
                    buff=0.08,
                    color=YELLOW_D,
                    max_tip_length_to_length_ratio=0.22,
                )
                for index in range(3)
            ]
        )
        multiply_labels = VGroup(
            *[
                Text("x", font_size=22, color=YELLOW_D).next_to(arrow, RIGHT, buff=0.12)
                for arrow in arrows
            ]
        )
        token = Dot(levels[0].get_left() + RIGHT * 0.35, color=WHITE, radius=0.09)

        config_title = Text("available parameter budget", font_size=20, color=GREY_B)
        config = VGroup(
            self.card("N = 8192", BLUE_C, 2.65, 0.62, 19),
            self.card("60 | 40 | 40 | 60", PURPLE_C, 2.65, 0.62, 19),
            self.card("scale = 2^40", YELLOW_D, 2.65, 0.62, 19),
        ).arrange(DOWN, buff=0.2)
        config_group = VGroup(config_title, config).arrange(DOWN, buff=0.25)
        config_group.move_to(RIGHT * 3.45 + UP * 0.65)

        comparison = VGroup(
            Text("depth needed: 3", font_size=19, color=WHITE),
            Text("levels available: 3", font_size=19, color=WHITE),
            Text("MATCH", font_size=23, color=GREEN_C, weight=BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(RIGHT * 3.45 + DOWN * 1.45)

        self.play(FadeIn(levels[0]), FadeIn(token), FadeIn(config_title), run_time=step)
        self.play(FadeIn(config[0]), run_time=step)
        self.play(FadeIn(config[1]), run_time=step)
        self.play(FadeIn(config[2]), run_time=step)
        for index in range(3):
            self.play(
                GrowArrow(arrows[index]),
                FadeIn(multiply_labels[index]),
                FadeIn(levels[index + 1]),
                token.animate.move_to(levels[index + 1].get_left() + RIGHT * 0.35),
                run_time=step,
            )
        self.play(FadeIn(comparison[0]), FadeIn(comparison[1]), run_time=step)
        self.play(
            FadeIn(comparison[2], scale=0.8),
            Circumscribe(config, color=GREEN_C),
            run_time=step,
        )
        return VGroup(
            levels,
            arrows,
            multiply_labels,
            token,
            config_group,
            comparison,
        )

    @staticmethod
    def approximation_beats():
        return [
            ("Approximate, not exact", ["real value", "nearby decoded value", "application tolerance"], "Correctness is numerical, not bit-for-bit equality."),
            ("Scale before rounding", ["multiply by 2^40", "preserve fractional detail", "round to ring data"], "Scale carries useful fractional precision into the polynomial."),
            ("Decode back to a number", ["polynomial coefficients", "divide by scale", "measure the residual"], "Decoding reverses the representation approximately."),
            ("Error has several sources", ["encoding", "encrypted evaluation", "rescaling"], "Small errors accumulate and must remain controlled."),
            ("Test the final tolerance", ["plaintext baseline", "FHE output", "pass or fail"], "The application decides how much error is acceptable."),
        ]

    @staticmethod
    def packing_beats():
        return [
            ("Pack a vector", ["many real values", "one polynomial", "one ciphertext"], "Packing amortizes one operation across many values."),
            ("N divided by two slots", ["increase ring degree", "increase slot count", "increase cost"], "For N = 8192, CKKS exposes 4096 complex slots."),
            ("One operation, every slot", ["two packed vectors", "single add gate", "parallel output"], "CKKS addition and multiplication act slot by slot."),
            ("Select with a plaintext mask", ["broadcast zeros and ones", "suppress positions", "keep selected slots"], "Public masks shape encrypted data without revealing it."),
            ("Rotate, then reduce", ["cyclic shift", "add rotated copies", "sum the slots"], "Galois keys enable movement between packed positions."),
        ]

    @staticmethod
    def parameter_beats():
        return [
            ("Polynomial degree changes the budget", ["more slots", "more modulus capacity", "more memory and time"], "Larger N buys capacity at a computational cost."),
            ("RNS primes form a chain", ["active prime set", "chain index", "parameter identity"], "Each level represents a different compatible ciphertext state."),
            ("Multiplication squares the scale", ["2^40 times 2^40", "scale becomes 2^80", "approach the modulus ceiling"], "Multiplication changes both the value and its metadata."),
            ("Rescale drops one prime", ["remove the last prime", "divide the scale", "move down one level"], "Rescaling restores scale while consuming chain capacity."),
            ("Parameters must fit the circuit", ["degree 8192", "60-40-40-60 chain", "initial scale 2^40"], "The SEAL example is a circuit-specific configuration, not a default."),
        ]

    def construct(self):
        first_start = scene_time(self)
        self.open_lesson(
            "Act 1.2 - CKKS Encoding and Parameters",
            "assets/audio/01_math_crypto/scene_02_ckks_encoding.mp3",
        )
        self.play_timed_section(
            first_start,
            300,
            "00:00 - 05:00 | Approximation and scale",
            self.approximation_beats(),
            BLUE_C,
            self.APPROXIMATION_DURATIONS,
        )

        second_start = scene_time(self)
        self.play_timed_section(
            second_start,
            300,
            "05:00 - 10:00 | Packing and SIMD",
            self.packing_beats(),
            GREEN_C,
            self.PACKING_DURATIONS,
        )

        third_start = scene_time(self)
        self.play_timed_section(
            third_start,
            300,
            "10:00 - 15:00 | Parameters and rescale",
            self.parameter_beats(),
            YELLOW_D,
            self.PARAMETER_DURATIONS,
        )
