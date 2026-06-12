import os
import sys

from manim import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene, scene_time


class CiphertextOperations(StoryboardScene):
    """15-minute visual lesson on ciphertext structure and CKKS operations."""

    MOTION_TIME = 1.15
    CONTENT_TOP = 2.15
    CONTENT_BOTTOM = -2.6
    ANATOMY_DURATIONS = (53.98, 60.09, 58.25, 63.32, 60.56)
    ARITHMETIC_DURATIONS = (57.60, 62.22, 60.83, 58.52, 60.83)
    ADVANCED_DURATIONS = (60.55, 61.02, 58.25, 58.71, 61.47)

    @staticmethod
    def fit_text(text, max_width):
        if text.width > max_width:
            text.scale_to_fit_width(max_width)
        return text

    @classmethod
    def motion_step(cls, duration, actions):
        return min(cls.MOTION_TIME, max(0.82, duration / max(1, actions * 10)))

    def card(self, label, color, width=2.0, height=0.78, font_size=22):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.09,
            color=color,
            fill_color=color,
            fill_opacity=0.13,
        )
        text = Text(label, font_size=font_size, color=WHITE)
        self.fit_text(text, width - 0.22)
        text.move_to(box)
        return VGroup(box, text)

    def slot_row(self, values, color=COLOR_CIPHERTEXT, cell_size=0.68):
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

    def coefficient_card(self, label, color, width=3.25):
        box = RoundedRectangle(
            width=width,
            height=1.55,
            corner_radius=0.12,
            color=color,
            fill_color=color,
            fill_opacity=0.08,
        )
        title = Text(label, font_size=23, color=color).next_to(box.get_top(), DOWN, buff=0.16)
        limbs = VGroup(
            *[
                VGroup(
                    *[
                        Dot(radius=0.045, color=shade)
                        for _ in range(6)
                    ]
                ).arrange(RIGHT, buff=0.14)
                for shade in (BLUE_C, PURPLE_C, YELLOW_D)
            ]
        ).arrange(DOWN, buff=0.16).move_to(box).shift(DOWN * 0.16)
        return VGroup(box, title, limbs)

    def keep_demo_alive(self, demo, accent, duration):
        if duration <= 0.05:
            return
        visible_family_ids = {
            id(member)
            for root in self.mobjects
            for member in root.get_family()
        }
        candidates = [
            mob
            for mob in demo
            if id(mob) in visible_family_ids
            and 0.25 < mob.width < 6.2
            and 0.12 < mob.height < 3.7
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
            cue_time = min(1.1, duration - elapsed)
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
            self.remove(mobject)

    def play_timed_section(
        self,
        section_start,
        section_duration,
        section_label,
        beats,
        accent,
        beat_durations,
    ):
        remaining = section_duration - (scene_time(self) - section_start)
        durations = list(beat_durations)
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
            "anatomy"
            if "Anatomy" in section_label
            else "arithmetic"
            if "Arithmetic" in section_label
            else "advanced"
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

    def open_lesson(self, audio_path):
        self.camera.background_color = "#101214"
        self.add_optional_sound(audio_path)
        act = Text("ACT 1 | MATHEMATICS AND CRYPTOGRAPHY", font_size=25, color=YELLOW_D)
        title = Text("Scene 03 - Ciphertext Operations", font_size=42, color=WHITE)
        subtitle = Text("From encoded slots to planned encrypted arithmetic", font_size=23, color=GREY_B)
        group = VGroup(act, title, subtitle).arrange(DOWN, buff=0.3)
        self.fit_text(group, 11.4)
        self.play(FadeIn(act, shift=DOWN * 0.12), Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(group), run_time=1.0)

    # ------------------------------------------------------------------
    # 3.1 Ciphertext anatomy
    # ------------------------------------------------------------------

    def demo_anatomy_1(self, accent, duration):
        step = self.motion_step(duration, 7)
        shell = RoundedRectangle(
            width=7.35,
            height=2.25,
            corner_radius=0.2,
            color=RED_C,
            fill_color=RED_C,
            fill_opacity=0.08,
        ).shift(RIGHT * 0.55)
        shell_label = Text("one CKKS ciphertext", font_size=22, color=RED_C)
        shell_label.next_to(shell, UP, buff=0.2)
        c0 = self.coefficient_card("c0(X)", RED_C, width=3.0).move_to(LEFT * 1.15)
        c1 = self.coefficient_card("c1(X)", RED_C, width=3.0).move_to(RIGHT * 2.25)
        rns_labels = VGroup(
            *[
                VGroup(
                    Dot(radius=0.055, color=color),
                    Text(label, font_size=17, color=color),
                ).arrange(RIGHT, buff=0.13)
                for label, color in (("q2", BLUE_C), ("q1", PURPLE_C), ("q0", YELLOW_D))
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 4.75 + DOWN * 0.16)
        rns_title = Text("RNS rows", font_size=17, color=GREY_B).next_to(
            rns_labels,
            UP,
            aligned_edge=LEFT,
            buff=0.16,
        )
        size = Text("size = 2", font_size=21, color=GREEN_C).next_to(shell, DOWN, buff=0.24)

        self.play(
            FadeIn(shell, scale=0.96),
            FadeIn(shell_label),
            FadeIn(rns_title),
            FadeIn(rns_labels),
            run_time=step,
        )
        self.play(FadeIn(c0[0]), FadeIn(c1[0]), run_time=step)
        self.play(FadeIn(c0[1]), FadeIn(c1[1]), run_time=step)
        self.play(
            LaggedStart(
                *(FadeIn(row, shift=RIGHT * 0.12) for row in c0[2]),
                lag_ratio=0.14,
            ),
            run_time=step,
        )
        self.play(
            LaggedStart(
                *(FadeIn(row, shift=LEFT * 0.12) for row in c1[2]),
                lag_ratio=0.14,
            ),
            run_time=step,
        )
        self.play(
            Indicate(rns_labels[0], color=BLUE_C),
            Indicate(VGroup(c0[2][0], c1[2][0]), color=BLUE_C),
            run_time=step,
        )
        self.play(FadeIn(size), Circumscribe(VGroup(c0, c1), color=accent), run_time=step)
        return VGroup(shell, shell_label, c0, c1, rns_title, rns_labels, size)

    def demo_anatomy_2(self, accent, duration):
        step = self.motion_step(duration, 8)
        c0 = self.card("c0", RED_C, 1.1, 0.68, 22).move_to(LEFT * 4.8 + UP * 0.35)
        plus = Text("+", font_size=32, color=WHITE).next_to(c0, RIGHT, buff=0.22)
        c1 = self.card("c1", RED_C, 1.1, 0.68, 22).next_to(plus, RIGHT, buff=0.22)
        multiply = Text("x", font_size=28, color=YELLOW_D).next_to(c1, RIGHT, buff=0.22)
        key_target = self.card("s(X)", GREEN_C, 1.2, 0.68, 21).next_to(multiply, RIGHT, buff=0.22)
        arrow = Arrow(key_target.get_right(), RIGHT * 2.2 + UP * 0.35, buff=0.18, color=accent)
        result = self.card("encoded message", BLUE_C, 2.35, 0.76, 20).move_to(RIGHT * 3.65 + UP * 0.35)
        error = VGroup(*[Dot(radius=0.045, color=GREY_B) for _ in range(7)]).arrange(RIGHT, buff=0.09)
        error.next_to(result, DOWN, buff=0.28)
        error_label = Text("+ small error", font_size=18, color=GREY_B).next_to(error, RIGHT, buff=0.18)
        client = RoundedRectangle(
            width=2.2,
            height=1.0,
            corner_radius=0.12,
            color=GREEN_C,
            fill_opacity=0.07,
        ).move_to(LEFT * 1.0 + DOWN * 1.45)
        client_label = Text("trusted client", font_size=18, color=GREEN_C).next_to(client, DOWN, buff=0.12)
        moving_key = key_target.copy().move_to(client)
        key_trace = Text("s(X)", font_size=20, color=GREY_B).move_to(key_target)

        self.play(FadeIn(c0), FadeIn(plus), FadeIn(c1), FadeIn(multiply), run_time=step)
        self.play(FadeIn(client), FadeIn(client_label), FadeIn(moving_key), run_time=step)
        self.play(Transform(moving_key, key_target), run_time=step)
        self.play(GrowArrow(arrow), FadeIn(result, shift=LEFT * 0.15), run_time=step)
        self.play(LaggedStart(*(FadeIn(dot) for dot in error), lag_ratio=0.08), FadeIn(error_label), run_time=step)
        self.play(Circumscribe(result, color=BLUE_C), run_time=step)
        self.play(
            Transform(moving_key, key_target.copy().move_to(client)),
            FadeIn(key_trace),
            run_time=step,
        )
        self.play(Indicate(client, color=GREEN_C), run_time=step)
        return VGroup(
            c0,
            plus,
            c1,
            multiply,
            key_target,
            arrow,
            result,
            error,
            error_label,
            client,
            client_label,
            moving_key,
            key_trace,
        )

    def demo_anatomy_3(self, accent, duration):
        step = self.motion_step(duration, 8)
        ciphertext = RoundedRectangle(
            width=4.5,
            height=2.45,
            corner_radius=0.16,
            color=RED_C,
            fill_color=RED_C,
            fill_opacity=0.08,
        ).move_to(LEFT * 2.7)
        components = VGroup(
            self.card("c0", RED_C, 1.25, 0.66, 21),
            self.card("c1", RED_C, 1.25, 0.66, 21),
        ).arrange(RIGHT, buff=0.28).move_to(ciphertext).shift(UP * 0.32)
        slots = self.slot_row(["z0", "z1", "z2", "z3"], BLUE_C, 0.48)
        slots.move_to(ciphertext).shift(DOWN * 0.65)

        size_icon = VGroup(
            Text("size", font_size=18, color=GREY_B),
            VGroup(Dot(color=RED_C), Dot(color=RED_C)).arrange(RIGHT, buff=0.22),
        ).arrange(RIGHT, buff=0.25)
        scale_track = Rectangle(width=2.4, height=0.18, color=GREY_D)
        scale_fill = Rectangle(
            width=1.65,
            height=0.18,
            color=YELLOW_D,
            fill_color=YELLOW_D,
            fill_opacity=0.8,
            stroke_width=0,
        ).move_to(scale_track).align_to(scale_track, LEFT)
        scale_icon = VGroup(
            Text("scale 2^40", font_size=18, color=GREY_B),
            VGroup(scale_track, scale_fill),
        ).arrange(RIGHT, buff=0.22)
        level_icon = VGroup(
            Text("parms ID", font_size=18, color=GREY_B),
            VGroup(
                *[
                    Rectangle(
                        width=0.45,
                        height=0.22,
                        color=color,
                        fill_color=color,
                        fill_opacity=0.55,
                    )
                    for color in (BLUE_C, PURPLE_C, YELLOW_D)
                ]
            ).arrange(RIGHT, buff=0.08),
        ).arrange(RIGHT, buff=0.22)
        state = VGroup(size_icon, scale_icon, level_icon).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.48,
        ).move_to(RIGHT * 2.65)
        connectors = VGroup(
            *[
                Arrow(ciphertext.get_right(), item.get_left(), buff=0.18, color=GREY_C)
                for item in state
            ]
        )

        self.play(FadeIn(ciphertext), FadeIn(components), run_time=step)
        self.play(FadeIn(slots), run_time=step)
        for connector, item in zip(connectors, state):
            self.play(GrowArrow(connector), FadeIn(item, shift=LEFT * 0.12), run_time=step)
        self.play(Indicate(size_icon, color=RED_C), run_time=step)
        self.play(Indicate(scale_icon, color=YELLOW_D), run_time=step)
        self.play(Indicate(level_icon, color=BLUE_C), run_time=step)
        return VGroup(ciphertext, components, slots, state, connectors)

    def demo_anatomy_4(self, accent, duration):
        step = self.motion_step(duration, 9)
        left_a = self.card("ciphertext A", RED_C, 2.2, 0.7, 20).move_to(LEFT * 4.25 + UP * 0.75)
        left_b = self.card("ciphertext B", RED_C, 2.2, 0.7, 20).move_to(LEFT * 4.25 + DOWN * 0.75)
        state_a = Text("level 3 | scale S", font_size=17, color=BLUE_C).next_to(left_a, RIGHT, buff=0.18)
        state_b = Text("level 2 | scale 2S", font_size=17, color=YELLOW_D).next_to(left_b, RIGHT, buff=0.18)
        gate = Circle(radius=0.55, color=YELLOW_D, fill_color=YELLOW_D, fill_opacity=0.08).move_to(RIGHT * 0.55)
        plus = Text("+", font_size=38, color=YELLOW_D).move_to(gate)
        arrows = VGroup(
            Arrow(state_a.get_right(), gate.get_left() + UP * 0.16, buff=0.18, color=GREY_C),
            Arrow(state_b.get_right(), gate.get_left() + DOWN * 0.16, buff=0.18, color=GREY_C),
        )
        output = self.card("sum", GREEN_C, 1.8, 0.76, 22).move_to(RIGHT * 4.1)
        output_arrow = Arrow(gate.get_right(), output.get_left(), buff=0.18, color=GREEN_C)
        mismatch = Text("metadata mismatch", font_size=21, color=RED_C).next_to(gate, DOWN, buff=0.45)
        align_arrow = Arrow(state_b.get_top(), state_a.get_bottom(), buff=0.12, color=GREEN_C)
        aligned_b = Text("level 3 | scale S", font_size=17, color=GREEN_C).move_to(state_b)

        self.play(FadeIn(left_a), FadeIn(left_b), FadeIn(state_a), FadeIn(state_b), run_time=step)
        self.play(FadeIn(gate), FadeIn(plus), GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=step)
        self.play(FadeIn(mismatch, shift=UP * 0.1), Flash(gate, color=RED_C), run_time=step)
        self.play(GrowArrow(align_arrow), run_time=step)
        self.play(Transform(state_b, aligned_b), FadeOut(mismatch), run_time=step)
        self.play(
            gate.animate.set_stroke(GREEN_C).set_fill(GREEN_C, opacity=0.1),
            plus.animate.set_color(GREEN_C),
            run_time=step,
        )
        self.play(GrowArrow(output_arrow), FadeIn(output, shift=LEFT * 0.12), run_time=step)
        self.play(Circumscribe(VGroup(state_a, state_b), color=GREEN_C), run_time=step)
        self.play(Indicate(output, color=GREEN_C), run_time=step)
        return VGroup(
            left_a,
            left_b,
            state_a,
            state_b,
            gate,
            plus,
            arrows,
            output,
            output_arrow,
            mismatch,
            align_arrow,
        )

    def demo_anatomy_5(self, accent, duration):
        step = self.motion_step(duration, 10)
        divider = DashedLine(UP * 2.0, DOWN * 2.15, color=GREY_D).shift(RIGHT * 0.55)
        client_label = Text("trusted client", font_size=21, color=GREEN_C).move_to(LEFT * 4.75 + UP * 1.8)
        server_label = Text("server", font_size=21, color=BLUE_C).move_to(RIGHT * 4.55 + UP * 1.8)
        ciphertext = self.card("ciphertext", RED_C, 1.85, 0.72, 20).move_to(LEFT * 5.0 + UP * 0.45)
        serialize = self.card("serialize", YELLOW_D, 1.55, 0.72, 19).move_to(LEFT * 2.85 + UP * 0.45)
        secret = VGroup(
            self.card("secret key", GREEN_C, 1.85, 0.68, 19),
            Text("stays with client", font_size=17, color=GREEN_C),
        ).arrange(DOWN, buff=0.14).move_to(LEFT * 4.55 + DOWN * 1.25)
        packets = VGroup(
            *[
                Rectangle(
                    width=0.36,
                    height=0.34,
                    color=RED_C,
                    fill_color=RED_C,
                    fill_opacity=0.28,
                )
                for _ in range(6)
            ]
        ).arrange(RIGHT, buff=0.08).move_to(LEFT * 0.75 + UP * 0.45)
        load = self.card("load", BLUE_C, 1.35, 0.72, 19).move_to(RIGHT * 2.15 + UP * 0.45)
        context = RoundedRectangle(
            width=2.15,
            height=1.12,
            corner_radius=0.14,
            color=BLUE_C,
            fill_color=BLUE_C,
            fill_opacity=0.07,
        ).move_to(RIGHT * 4.65 + UP * 0.45)
        context_label = Text(
            "compatible\nSEALContext",
            font_size=17,
            color=BLUE_C,
            line_spacing=0.8,
        ).move_to(context)
        restored = self.card("loaded ciphertext", RED_C, 2.15, 0.68, 18).move_to(RIGHT * 4.65 + DOWN * 1.2)
        arrows = VGroup(
            Arrow(ciphertext.get_right(), serialize.get_left(), buff=0.12, color=YELLOW_D),
            Arrow(serialize.get_right(), packets.get_left(), buff=0.12, color=RED_C),
            Arrow(packets.get_right(), load.get_left(), buff=0.12, color=accent),
            Arrow(load.get_right(), context.get_left(), buff=0.12, color=BLUE_C),
            Arrow(context.get_bottom(), restored.get_top(), buff=0.12, color=RED_C),
        )
        transfer_label = Text(
            "bytes cross\nboundary",
            font_size=15,
            color=GREY_B,
            line_spacing=0.72,
        ).move_to(RIGHT * 0.55 + DOWN * 0.32)

        self.play(FadeIn(divider), FadeIn(client_label), FadeIn(server_label), FadeIn(secret), run_time=step)
        self.play(FadeIn(ciphertext), GrowArrow(arrows[0]), FadeIn(serialize), run_time=step)
        self.play(GrowArrow(arrows[1]), TransformFromCopy(ciphertext, packets), run_time=step)
        self.play(GrowArrow(arrows[2]), FadeIn(transfer_label), run_time=step)
        self.play(packets.animate.move_to(load.get_left() + LEFT * 0.45), FadeIn(load), run_time=step)
        self.play(GrowArrow(arrows[3]), FadeIn(context), FadeIn(context_label), run_time=step)
        self.play(FadeOut(packets), GrowArrow(arrows[4]), FadeIn(restored, shift=UP * 0.1), run_time=step)
        self.play(Indicate(secret, color=GREEN_C), run_time=step)
        self.play(Circumscribe(VGroup(context, restored), color=BLUE_C), run_time=step)
        return VGroup(
            divider,
            client_label,
            server_label,
            ciphertext,
            serialize,
            secret,
            packets,
            load,
            context,
            context_label,
            restored,
            arrows,
            transfer_label,
        )

    # ------------------------------------------------------------------
    # 3.2 Arithmetic and maintenance
    # ------------------------------------------------------------------

    def demo_arithmetic_1(self, accent, duration):
        step = self.motion_step(duration, 8)
        first_inputs = VGroup(
            self.card("c0", RED_C, 1.3, 0.62, 21),
            self.card("d0", BLUE_C, 1.3, 0.62, 21),
        ).arrange(DOWN, buff=0.28).move_to(LEFT * 2.75 + UP * 0.45)
        second_inputs = VGroup(
            self.card("c1", RED_C, 1.3, 0.62, 21),
            self.card("d1", BLUE_C, 1.3, 0.62, 21),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 2.1 + UP * 0.45)
        pluses = VGroup(
            Text("+", font_size=30, color=YELLOW_D).next_to(first_inputs, LEFT, buff=0.22),
            Text("+", font_size=30, color=YELLOW_D).next_to(second_inputs, LEFT, buff=0.22),
        )
        output = VGroup(
            self.card("c0 + d0", GREEN_C, 2.0, 0.68, 18),
            self.card("c1 + d1", GREEN_C, 2.0, 0.68, 18),
        )
        output[0].move_to(LEFT * 2.75 + DOWN * 1.2)
        output[1].move_to(RIGHT * 2.1 + DOWN * 1.2)
        paths = VGroup(
            Arrow(first_inputs.get_bottom(), output[0].get_top(), buff=0.14, color=GREEN_C),
            Arrow(second_inputs.get_bottom(), output[1].get_top(), buff=0.14, color=GREEN_C),
        )
        divider = Line(UP * 1.55, DOWN * 1.75, color=GREY_D).shift(LEFT * 0.3)
        size = Text("two outputs = size 2", font_size=20, color=GREEN_C).move_to(RIGHT * 4.55 + DOWN * 1.2)

        self.play(FadeIn(divider), FadeIn(first_inputs), FadeIn(second_inputs), FadeIn(pluses), run_time=step)
        self.play(GrowArrow(paths[0]), run_time=step)
        self.play(TransformFromCopy(first_inputs, output[0]), run_time=step)
        self.play(GrowArrow(paths[1]), run_time=step)
        self.play(TransformFromCopy(second_inputs, output[1]), run_time=step)
        self.play(FadeIn(size, shift=UP * 0.1), run_time=step)
        self.play(Indicate(output[0], color=GREEN_C), run_time=step)
        self.play(Indicate(output[1], color=GREEN_C), run_time=step)
        return VGroup(first_inputs, second_inputs, pluses, output, paths, divider, size)

    def demo_arithmetic_2(self, accent, duration):
        step = self.motion_step(duration, 8)
        divider = Line(UP * 1.85, DOWN * 1.85, color=GREY_D)
        ct_left = self.card("encrypted x", RED_C, 2.0, 0.75, 20).move_to(LEFT * 4.1 + UP * 0.45)
        pt_weight = VGroup(
            Circle(radius=0.48, color=GREEN_C, fill_color=GREEN_C, fill_opacity=0.1),
            Text("w", font_size=28, color=GREEN_C),
        ).move_to(LEFT * 1.7 + UP * 0.45)
        pt_weight[1].move_to(pt_weight[0])
        ct_right = self.card("encrypted x", RED_C, 2.0, 0.75, 20).move_to(RIGHT * 1.7 + UP * 0.45)
        ct_weight = self.card("encrypted w", RED_C, 2.0, 0.75, 19).move_to(RIGHT * 4.15 + UP * 0.45)
        multiply_left = Text("x", font_size=30, color=YELLOW_D).move_to(LEFT * 2.9 + UP * 0.45)
        multiply_right = Text("x", font_size=30, color=YELLOW_D).move_to(RIGHT * 2.9 + UP * 0.45)
        left_track = Rectangle(width=2.6, height=0.18, color=GREY_D)
        left_fill = Rectangle(
            width=0.9,
            height=0.18,
            color=GREEN_C,
            fill_opacity=0.8,
            stroke_width=0,
        )
        left_fill.move_to(left_track).align_to(left_track, LEFT)
        left_meter = VGroup(
            Text("public weight", font_size=18, color=GREEN_C),
            VGroup(left_track, left_fill),
        ).arrange(DOWN, buff=0.18).move_to(LEFT * 2.9 + DOWN * 1.1)
        right_track = Rectangle(width=2.6, height=0.18, color=GREY_D)
        right_fill = Rectangle(
            width=2.2,
            height=0.18,
            color=RED_C,
            fill_opacity=0.8,
            stroke_width=0,
        )
        right_fill.move_to(right_track).align_to(right_track, LEFT)
        right_meter = VGroup(
            Text("both operands private", font_size=18, color=RED_C),
            VGroup(right_track, right_fill),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 2.9 + DOWN * 1.1)

        self.play(FadeIn(divider), run_time=step)
        self.play(FadeIn(ct_left), FadeIn(pt_weight), FadeIn(multiply_left), run_time=step)
        self.play(FadeIn(ct_right), FadeIn(ct_weight), FadeIn(multiply_right), run_time=step)
        self.play(FadeIn(left_meter[0]), FadeIn(left_meter[1][0]), run_time=step)
        self.play(GrowFromEdge(left_meter[1][1], LEFT), run_time=step)
        self.play(FadeIn(right_meter[0]), FadeIn(right_meter[1][0]), run_time=step)
        self.play(GrowFromEdge(right_meter[1][1], LEFT), run_time=step)
        self.play(Indicate(pt_weight, color=GREEN_C), run_time=step)
        self.play(Circumscribe(VGroup(ct_right, ct_weight), color=RED_C), run_time=step)
        return VGroup(
            divider,
            ct_left,
            pt_weight,
            ct_right,
            ct_weight,
            multiply_left,
            multiply_right,
            left_meter,
            right_meter,
        )

    def demo_arithmetic_3(self, accent, duration):
        step = self.motion_step(duration, 9)
        left = VGroup(self.card("c0", RED_C, 1.15, 0.64), self.card("c1", RED_C, 1.15, 0.64)).arrange(RIGHT, buff=0.16)
        right = VGroup(self.card("d0", BLUE_C, 1.15, 0.64), self.card("d1", BLUE_C, 1.15, 0.64)).arrange(RIGHT, buff=0.16)
        left.move_to(LEFT * 3.95 + UP * 0.7)
        right.move_to(LEFT * 3.95 + DOWN * 0.7)
        gate = Circle(radius=0.55, color=YELLOW_D, fill_opacity=0.08).move_to(LEFT * 1.35)
        times = Text("x", font_size=34, color=YELLOW_D).move_to(gate)
        outputs = VGroup(
            self.card("e0", GREEN_C, 1.25, 0.7, 22),
            self.card("e1", GREEN_C, 1.25, 0.7, 22),
            self.card("e2", GREEN_C, 1.25, 0.7, 22),
        ).arrange(RIGHT, buff=0.22).move_to(RIGHT * 2.75 + UP * 0.35)
        terms = VGroup(
            Text("c0 d0", font_size=14, color=GREY_B),
            Text("cross terms", font_size=14, color=GREY_B),
            Text("c1 d1", font_size=14, color=GREY_B),
        )
        for term, output in zip(terms, outputs):
            self.fit_text(term, output.width * 0.92)
            term.next_to(output, DOWN, buff=0.18)
        arrow = Arrow(gate.get_right(), outputs.get_left(), buff=0.18, color=accent)
        scale_before = Text("scale S", font_size=20, color=YELLOW_D).move_to(LEFT * 1.35 + DOWN * 1.25)
        scale_after = Text("scale S^2", font_size=22, color=RED_C).move_to(RIGHT * 2.75 + DOWN * 1.25)

        self.play(FadeIn(left), FadeIn(right), run_time=step)
        self.play(FadeIn(gate), FadeIn(times), FadeIn(scale_before), run_time=step)
        self.play(GrowArrow(arrow), run_time=step)
        for output, term in zip(outputs, terms):
            self.play(FadeIn(output, shift=LEFT * 0.12), FadeIn(term), run_time=step)
        self.play(TransformFromCopy(scale_before, scale_after), run_time=step)
        self.play(Circumscribe(outputs, color=GREEN_C), run_time=step)
        self.play(Indicate(scale_after, color=RED_C), run_time=step)
        return VGroup(
            left,
            right,
            gate,
            times,
            outputs,
            terms,
            arrow,
            scale_before,
            scale_after,
        )

    def demo_arithmetic_4(self, accent, duration):
        step = self.motion_step(duration, 9)
        enlarged = VGroup(
            self.card("e0", RED_C, 1.25, 0.7, 22),
            self.card("e1", RED_C, 1.25, 0.7, 22),
            self.card("e2", RED_C, 1.25, 0.7, 22),
        ).arrange(RIGHT, buff=0.18).move_to(LEFT * 3.65 + UP * 0.45)
        key = self.card("RelinKeys", GREEN_C, 2.0, 0.72, 20).move_to(LEFT * 1.2 + DOWN * 1.25)
        switch = RoundedRectangle(
            width=2.1,
            height=1.25,
            corner_radius=0.15,
            color=YELLOW_D,
            fill_color=YELLOW_D,
            fill_opacity=0.08,
        ).move_to(RIGHT * 0.35 + UP * 0.45)
        switch_label = Text("key switch", font_size=21, color=YELLOW_D).move_to(switch)
        input_arrow = Arrow(enlarged.get_right(), switch.get_left(), buff=0.2, color=accent)
        key_arrow = Arrow(key.get_top(), switch.get_bottom(), buff=0.18, color=GREEN_C)
        reduced = VGroup(
            self.card("r0", BLUE_C, 1.35, 0.72, 22),
            self.card("r1", BLUE_C, 1.35, 0.72, 22),
        ).arrange(RIGHT, buff=0.2).move_to(RIGHT * 3.7 + UP * 0.45)
        output_arrow = Arrow(switch.get_right(), reduced.get_left(), buff=0.2, color=BLUE_C)
        lock_body = RoundedRectangle(
            width=0.55,
            height=0.4,
            corner_radius=0.06,
            color=GREEN_C,
            fill_color=GREEN_C,
            fill_opacity=0.08,
            stroke_width=4,
        ).shift(DOWN * 0.15)
        lock_shackle = Arc(
            radius=0.19,
            start_angle=0,
            angle=PI,
            color=GREEN_C,
            stroke_width=4,
        ).shift(UP * 0.08)
        lock_legs = VGroup(
            Line(LEFT * 0.19 + UP * 0.08, LEFT * 0.19 + DOWN * 0.03, color=GREEN_C, stroke_width=4),
            Line(RIGHT * 0.19 + UP * 0.08, RIGHT * 0.19 + DOWN * 0.03, color=GREEN_C, stroke_width=4),
        )
        lock = VGroup(lock_body, lock_shackle, lock_legs).move_to(RIGHT * 3.3 + DOWN * 1.0)
        note = Text("ciphertext remains encrypted", font_size=17, color=GREEN_C)
        note.next_to(lock, RIGHT, buff=0.22)

        self.play(FadeIn(enlarged), run_time=step)
        self.play(FadeIn(switch), FadeIn(switch_label), GrowArrow(input_arrow), run_time=step)
        self.play(FadeIn(key), GrowArrow(key_arrow), run_time=step)
        self.play(enlarged[2].animate.move_to(switch), run_time=step)
        self.play(FadeOut(enlarged[2]), Flash(switch, color=GREEN_C), run_time=step)
        self.play(GrowArrow(output_arrow), FadeIn(reduced, shift=LEFT * 0.12), run_time=step)
        self.play(FadeIn(lock), FadeIn(note), run_time=step)
        self.play(Circumscribe(reduced, color=BLUE_C), run_time=step)
        self.play(Indicate(lock, color=GREEN_C), run_time=step)
        return VGroup(
            enlarged,
            key,
            switch,
            switch_label,
            input_arrow,
            key_arrow,
            reduced,
            output_arrow,
            lock,
            note,
        )

    def demo_arithmetic_5(self, accent, duration):
        step = self.motion_step(duration, 8)
        stages = VGroup(
            self.card("multiply", RED_C, 2.1, 0.75, 21),
            self.card("relinearize", GREEN_C, 2.1, 0.75, 20),
            self.card("rescale", BLUE_C, 2.1, 0.75, 21),
        ).arrange(RIGHT, buff=1.0).move_to(UP * 0.85)
        arrows = VGroup(
            Arrow(stages[0].get_right(), stages[1].get_left(), buff=0.15, color=GREY_C),
            Arrow(stages[1].get_right(), stages[2].get_left(), buff=0.15, color=GREY_C),
        )

        def state_panel(component_count, scale_label, level_count, color):
            components = VGroup(
                *[Dot(color=color, radius=0.075) for _ in range(component_count)]
            ).arrange(RIGHT, buff=0.16)
            scale_text = Text(
                scale_label,
                font_size=17,
                color=RED_C if "S^2" in scale_label else BLUE_C,
            )
            levels = VGroup(
                *[
                    Rectangle(
                        width=0.38,
                        height=0.17,
                        color=PURPLE_C,
                        fill_color=PURPLE_C,
                        fill_opacity=0.55,
                    )
                    for _ in range(level_count)
                ]
            ).arrange(RIGHT, buff=0.07)
            rows = VGroup(
                VGroup(Text("components", font_size=15, color=GREY_B), components).arrange(RIGHT, buff=0.2),
                VGroup(Text("scale", font_size=15, color=GREY_B), scale_text).arrange(RIGHT, buff=0.2),
                VGroup(Text("levels", font_size=15, color=GREY_B), levels).arrange(RIGHT, buff=0.2),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            panel = RoundedRectangle(
                width=2.75,
                height=1.55,
                corner_radius=0.1,
                color=color,
                fill_color=color,
                fill_opacity=0.05,
            )
            rows.move_to(panel)
            return VGroup(panel, rows)

        snapshots = VGroup(
            state_panel(3, "S^2", 3, RED_C),
            state_panel(2, "S^2", 3, GREEN_C),
            state_panel(2, "near S", 2, BLUE_C),
        )
        for snapshot, stage in zip(snapshots, stages):
            snapshot.next_to(stage, DOWN, buff=0.42)

        self.play(FadeIn(stages[0]), FadeIn(snapshots[0], shift=UP * 0.1), run_time=step)
        self.play(GrowArrow(arrows[0]), FadeIn(stages[1]), run_time=step)
        self.play(TransformFromCopy(snapshots[0], snapshots[1]), run_time=step)
        self.play(Indicate(snapshots[1][1][0], color=GREEN_C), run_time=step)
        self.play(GrowArrow(arrows[1]), FadeIn(stages[2]), run_time=step)
        self.play(TransformFromCopy(snapshots[1], snapshots[2]), run_time=step)
        self.play(Indicate(snapshots[2][1][1], color=BLUE_C), run_time=step)
        self.play(Indicate(snapshots[2][1][2], color=PURPLE_C), run_time=step)
        return VGroup(stages, arrows, snapshots)

    # ------------------------------------------------------------------
    # 3.3 Levels, rotations, and reductions
    # ------------------------------------------------------------------

    def demo_advanced_1(self, accent, duration):
        step = self.motion_step(duration, 8)
        levels = VGroup()
        for index, width in enumerate((5.6, 5.2, 4.8, 4.4)):
            bar = RoundedRectangle(
                width=width,
                height=0.56,
                corner_radius=0.08,
                color=(BLUE_C, PURPLE_C, YELLOW_D, GREEN_C)[index],
                fill_opacity=0.08,
            )
            label = Text(f"level {3 - index}", font_size=18, color=WHITE).move_to(bar)
            levels.add(VGroup(bar, label))
        levels.arrange(DOWN, buff=0.28).move_to(LEFT * 2.0)
        ct_a = self.card("A", RED_C, 0.9, 0.48, 19).move_to(levels[0].get_left() + RIGHT * 0.65)
        ct_b = self.card("B", YELLOW_D, 0.9, 0.48, 19).move_to(levels[1].get_right() + LEFT * 0.65)
        aligned_a = ct_a.copy().move_to(levels[1].get_left() + RIGHT * 0.65)
        drop_arrow = Arrow(ct_a.get_bottom(), aligned_a.get_top(), buff=0.08, color=BLUE_C)
        switch_label = Text("mod switch A down", font_size=17, color=BLUE_C).next_to(
            drop_arrow,
            LEFT,
            buff=0.18,
        )
        aligned_label = Text("aligned at level 2", font_size=18, color=GREEN_C)
        plus = Circle(radius=0.48, color=GREEN_C, fill_opacity=0.08).move_to(RIGHT * 3.75 + UP * 0.15)
        plus_text = Text("+", font_size=34, color=GREEN_C).move_to(plus)
        combine_arrow = Arrow(levels[1].get_right(), plus.get_left(), buff=0.18, color=GREEN_C)
        aligned_label.next_to(combine_arrow, UP, buff=0.18)
        output = self.card("A + B", GREEN_C, 1.55, 0.62, 20).next_to(plus, DOWN, buff=0.45)

        self.play(LaggedStart(*(FadeIn(level, shift=DOWN * 0.08) for level in levels), lag_ratio=0.12), run_time=step)
        self.play(FadeIn(ct_a), FadeIn(ct_b), run_time=step)
        self.play(GrowArrow(drop_arrow), FadeIn(switch_label), run_time=step)
        self.play(Transform(ct_a, aligned_a), run_time=step)
        self.play(FadeIn(aligned_label, shift=UP * 0.08), run_time=step)
        self.play(FadeIn(plus), FadeIn(plus_text), GrowArrow(combine_arrow), run_time=step)
        self.play(FadeIn(output, shift=UP * 0.1), run_time=step)
        self.play(Circumscribe(VGroup(ct_a, ct_b), color=GREEN_C), run_time=step)
        self.play(Indicate(output, color=GREEN_C), run_time=step)
        return VGroup(
            levels,
            ct_a,
            ct_b,
            drop_arrow,
            switch_label,
            aligned_label,
            plus,
            plus_text,
            combine_arrow,
            output,
        )

    def demo_advanced_2(self, accent, duration):
        step = self.motion_step(duration, 8)
        divider = Line(UP * 1.9, DOWN * 2.0, color=GREY_D)
        left_title = Text("mod switch", font_size=24, color=BLUE_C).move_to(LEFT * 3.3 + UP * 1.65)
        right_title = Text("CKKS rescale", font_size=24, color=YELLOW_D).move_to(RIGHT * 3.3 + UP * 1.65)
        left_before = VGroup(*[self.card(f"q{i}", BLUE_C, 0.72, 0.48, 16) for i in (2, 1, 0)]).arrange(RIGHT, buff=0.1)
        right_before = VGroup(*[self.card(f"q{i}", YELLOW_D, 0.72, 0.48, 16) for i in (2, 1, 0)]).arrange(RIGHT, buff=0.1)
        left_before.move_to(LEFT * 3.3 + UP * 0.65)
        right_before.move_to(RIGHT * 3.3 + UP * 0.65)
        left_after_primes = VGroup(*[self.card(f"q{i}", BLUE_C, 0.72, 0.48, 16) for i in (2, 1)]).arrange(RIGHT, buff=0.1)
        right_after_primes = VGroup(*[self.card(f"q{i}", YELLOW_D, 0.72, 0.48, 16) for i in (2, 1)]).arrange(RIGHT, buff=0.1)
        left_after_primes.move_to(LEFT * 3.3 + DOWN * 0.45)
        right_after_primes.move_to(RIGHT * 3.3 + DOWN * 0.45)
        left_scale_before = Text("scale S", font_size=19, color=GREEN_C).next_to(left_before, UP, buff=0.18)
        right_scale_before = Text("scale S^2", font_size=19, color=RED_C).next_to(right_before, UP, buff=0.18)
        left_scale_after = Text("scale S unchanged", font_size=19, color=GREEN_C).next_to(left_after_primes, DOWN, buff=0.25)
        right_scale_after = Text("scale near S", font_size=19, color=GREEN_C).next_to(right_after_primes, DOWN, buff=0.25)
        arrows = VGroup(
            Arrow(left_before.get_bottom(), left_after_primes.get_top(), buff=0.14, color=BLUE_C),
            Arrow(right_before.get_bottom(), right_after_primes.get_top(), buff=0.14, color=YELLOW_D),
        )
        drop_labels = VGroup(
            Text("drop q0", font_size=16, color=BLUE_C).next_to(arrows[0], RIGHT, buff=0.12),
            Text("drop q0 + divide scale", font_size=16, color=YELLOW_D).next_to(arrows[1], RIGHT, buff=0.12),
        )

        self.play(FadeIn(divider), FadeIn(left_title), FadeIn(right_title), run_time=step)
        self.play(FadeIn(left_scale_before), FadeIn(right_scale_before), FadeIn(left_before), FadeIn(right_before), run_time=step)
        self.play(GrowArrow(arrows[0]), FadeIn(drop_labels[0]), run_time=step)
        self.play(TransformFromCopy(left_before[:2], left_after_primes), FadeIn(left_scale_after), run_time=step)
        self.play(GrowArrow(arrows[1]), FadeIn(drop_labels[1]), run_time=step)
        self.play(TransformFromCopy(right_before[:2], right_after_primes), FadeIn(right_scale_after), run_time=step)
        self.play(Indicate(left_scale_after, color=BLUE_C), run_time=step)
        self.play(Indicate(right_scale_after, color=GREEN_C), run_time=step)
        return VGroup(
            divider,
            left_title,
            right_title,
            left_before,
            right_before,
            left_after_primes,
            right_after_primes,
            left_scale_before,
            right_scale_before,
            left_scale_after,
            right_scale_after,
            arrows,
            drop_labels,
        )

    def demo_advanced_3(self, accent, duration):
        step = self.motion_step(duration, 9)
        source = self.slot_row([1, 2, 3, 4], RED_C, 0.78).move_to(LEFT * 3.3 + UP * 0.45)
        target = self.slot_row([4, 1, 2, 3], BLUE_C, 0.78).move_to(RIGHT * 3.3 + UP * 0.45)
        arc = CurvedArrow(
            source.get_right() + UP * 0.15,
            target.get_left() + UP * 0.15,
            angle=-TAU / 5,
            color=YELLOW_D,
        )
        key = self.card("GaloisKeys", GREEN_C, 2.2, 0.72, 20).move_to(DOWN * 1.2)
        key_beam = Arrow(key.get_top(), arc.get_center() + DOWN * 0.05, buff=0.15, color=GREEN_C)
        moving = source.copy()
        labels = VGroup(
            Text("before", font_size=18, color=GREY_B).next_to(source, DOWN, buff=0.22),
            Text("rotate right by 1", font_size=18, color=YELLOW_D).next_to(arc, UP, buff=0.15),
            Text("after", font_size=18, color=GREY_B).next_to(target, DOWN, buff=0.22),
        )

        self.play(FadeIn(source), FadeIn(labels[0]), run_time=step)
        self.play(Create(arc), FadeIn(labels[1]), run_time=step)
        self.play(FadeIn(key), run_time=step)
        self.play(GrowArrow(key_beam), Flash(key, color=GREEN_C), run_time=step)
        self.play(moving.animate.move_to(target), run_time=step)
        self.play(Transform(moving, target), FadeIn(labels[2]), run_time=step)
        self.play(FadeOut(moving), FadeIn(target), run_time=step)
        self.play(Indicate(target[0], color=YELLOW_D), run_time=step)
        self.play(Circumscribe(target, color=BLUE_C), run_time=step)
        return VGroup(source, target, arc, key, key_beam, moving, labels)

    def demo_advanced_4(self, accent, duration):
        step = self.motion_step(duration, 10)
        features = self.slot_row([1, 2, 3, 4], BLUE_C, 0.62).move_to(LEFT * 3.65 + UP * 0.9)
        weights = self.slot_row([2, 1, 0, 3], GREEN_C, 0.62).move_to(LEFT * 3.65 + DOWN * 0.15)
        multiply = Text("slot-wise x", font_size=20, color=YELLOW_D).move_to(LEFT * 3.65 + UP * 0.36)
        products = self.slot_row([2, 2, 0, 12], RED_C, 0.62).move_to(RIGHT * 2.75 + UP * 0.9)
        first_partial = self.slot_row([14, 4, 2, 12], YELLOW_D, 0.62).move_to(RIGHT * 2.75 + DOWN * 0.15)
        final = self.slot_row([16, 16, 16, 16], GREEN_C, 0.62).move_to(RIGHT * 2.75 + DOWN * 1.2)
        product_arrow = Arrow(features.get_right(), products.get_left(), buff=0.22, color=accent)
        reduce_one = CurvedArrow(
            products.get_bottom(),
            first_partial.get_top(),
            angle=PI / 3,
            color=YELLOW_D,
        )
        reduce_two = CurvedArrow(
            first_partial.get_bottom(),
            final.get_top(),
            angle=PI / 3,
            color=GREEN_C,
        )
        labels = VGroup(
            Text("products", font_size=17, color=RED_C).next_to(products, UP, buff=0.16),
            Text("rotate 1 + add", font_size=17, color=YELLOW_D).next_to(first_partial, RIGHT, buff=0.2),
            Text("rotate 2 + add", font_size=17, color=GREEN_C).next_to(final, RIGHT, buff=0.2),
        )

        self.play(FadeIn(features), FadeIn(weights), FadeIn(multiply), run_time=step)
        self.play(GrowArrow(product_arrow), run_time=step)
        self.play(TransformFromCopy(VGroup(features, weights), products), FadeIn(labels[0]), run_time=step)
        self.play(Create(reduce_one), run_time=step)
        self.play(TransformFromCopy(products, first_partial), FadeIn(labels[1]), run_time=step)
        self.play(Create(reduce_two), run_time=step)
        self.play(TransformFromCopy(first_partial, final), FadeIn(labels[2]), run_time=step)
        self.play(LaggedStart(*(Indicate(cell, color=GREEN_C) for cell in final), lag_ratio=0.1), run_time=step)
        self.play(Circumscribe(final, color=GREEN_C), run_time=step)
        self.play(Indicate(products, color=RED_C), run_time=step)
        return VGroup(
            features,
            weights,
            multiply,
            products,
            first_partial,
            final,
            product_arrow,
            reduce_one,
            reduce_two,
            labels,
        )

    def demo_advanced_5(self, accent, duration):
        step = self.motion_step(duration, 10)
        input_node = self.card("input slots", BLUE_C, 1.7, 0.62, 18).move_to(LEFT * 5.0 + UP * 0.55)
        multiply_nodes = VGroup(
            *[
                Circle(
                    radius=0.42,
                    color=RED_C,
                    fill_color=RED_C,
                    fill_opacity=0.1,
                )
                for _ in range(3)
            ]
        ).arrange(RIGHT, buff=1.25).move_to(LEFT * 1.1 + UP * 0.55)
        multiply_labels = VGroup(*[Text("x", font_size=25, color=RED_C).move_to(node) for node in multiply_nodes])
        output_node = self.card("output", GREEN_C, 1.55, 0.62, 19).move_to(RIGHT * 5.0 + UP * 0.55)
        path_nodes = VGroup(input_node, *multiply_nodes, output_node)
        arrows = VGroup(
            *[
                Arrow(path_nodes[index].get_right(), path_nodes[index + 1].get_left(), buff=0.12, color=GREY_C)
                for index in range(len(path_nodes) - 1)
            ]
        )
        rescale_marks = VGroup(
            *[
                Text("rescale", font_size=15, color=YELLOW_D).next_to(node, DOWN, buff=0.18)
                for node in multiply_nodes
            ]
        )
        rotation = CurvedArrow(
            multiply_nodes[1].get_bottom() + DOWN * 0.6,
            multiply_nodes[2].get_bottom() + DOWN * 0.6,
            angle=PI / 2,
            color=PURPLE_C,
        )
        rotation_label = Text("rotation", font_size=16, color=PURPLE_C).next_to(rotation, DOWN, buff=0.12)
        counters = VGroup(
            VGroup(Text("depth", font_size=18, color=GREY_B), Text("3", font_size=25, color=RED_C)).arrange(RIGHT, buff=0.25),
            VGroup(Text("levels", font_size=18, color=GREY_B), Text("3", font_size=25, color=YELLOW_D)).arrange(RIGHT, buff=0.25),
            VGroup(Text("rotations", font_size=18, color=GREY_B), Text("1, 2", font_size=25, color=PURPLE_C)).arrange(RIGHT, buff=0.25),
            VGroup(Text("scale", font_size=18, color=GREY_B), Text("2^40", font_size=25, color=BLUE_C)).arrange(RIGHT, buff=0.25),
        ).arrange(RIGHT, buff=0.7).move_to(DOWN * 1.55)
        ready = Text("circuit planned before evaluation", font_size=22, color=GREEN_C).next_to(counters, DOWN, buff=0.3)

        self.play(FadeIn(input_node), run_time=step)
        for arrow, node, label, mark in zip(arrows[:3], multiply_nodes, multiply_labels, rescale_marks):
            self.play(GrowArrow(arrow), FadeIn(node), FadeIn(label), run_time=step)
            self.play(FadeIn(mark), run_time=step * 0.75)
        self.play(GrowArrow(arrows[-1]), FadeIn(output_node), run_time=step)
        self.play(Create(rotation), FadeIn(rotation_label), run_time=step)
        self.play(LaggedStart(*(FadeIn(counter, shift=UP * 0.1) for counter in counters), lag_ratio=0.12), run_time=step)
        self.play(FadeIn(ready, shift=UP * 0.1), run_time=step)
        self.play(Circumscribe(VGroup(path_nodes, arrows), color=accent), run_time=step)
        self.play(Indicate(ready, color=GREEN_C), run_time=step)
        return VGroup(
            input_node,
            multiply_nodes,
            multiply_labels,
            output_node,
            arrows,
            rescale_marks,
            rotation,
            rotation_label,
            counters,
            ready,
        )

    @staticmethod
    def anatomy_beats():
        return [
            ("Open a ciphertext", [], "A fresh CKKS ciphertext commonly contains two RNS polynomial components."),
            ("Decryption combines components", [], "Only the trusted client applies the secret-key polynomial."),
            ("Metadata controls legal operations", [], "Size, scale, and parameter identity travel with the polynomial data."),
            ("Align state before addition", [], "Related values are not addable until their metadata is compatible."),
            ("Serialization moves bytes, not authority", [], "A compatible context can load ciphertext bytes without receiving the secret key."),
        ]

    @staticmethod
    def arithmetic_beats():
        return [
            ("Add matching components", [], "Ciphertext addition keeps the standard two-component shape."),
            ("Public and private weights cost differently", [], "Ciphertext-plaintext multiplication is cheaper than protecting both operands."),
            ("Multiplication grows ciphertext state", [], "Two size-two ciphertexts produce three components and a squared scale."),
            ("Relinearization removes the extra component", [], "RelinKeys reduce representation size without decrypting the value."),
            ("Maintenance steps solve different problems", [], "Multiply, relinearize, and rescale must occur in the planned order."),
        ]

    @staticmethod
    def advanced_beats():
        return [
            ("Meet at a compatible level", [], "Operands generally descend to the same modulus-chain level before combination."),
            ("Mod switch is not rescale", [], "Both drop a prime, but CKKS rescale also normalizes the scale."),
            ("Rotate packed slots", [], "GaloisKeys authorize cyclic movement without revealing slot values."),
            ("Build a packed dot product", [], "Slot products become a sum through staged rotate-and-add reductions."),
            ("Plan the circuit before evaluation", [], "Depth, levels, scale, and rotations are design inputs, not runtime discoveries."),
        ]

    def construct(self):
        first_start = scene_time(self)
        self.open_lesson("assets/audio/01_math_crypto/scene_03_ciphertext_operations.mp3")
        self.play_timed_section(
            first_start,
            300,
            "00:00 - 05:00 | Ciphertext Anatomy",
            self.anatomy_beats(),
            RED_C,
            self.ANATOMY_DURATIONS,
        )

        second_start = scene_time(self)
        self.play_timed_section(
            second_start,
            300,
            "05:00 - 10:00 | Arithmetic and Maintenance",
            self.arithmetic_beats(),
            YELLOW_D,
            self.ARITHMETIC_DURATIONS,
        )

        third_start = scene_time(self)
        self.play_timed_section(
            third_start,
            300,
            "10:00 - 15:00 | Levels, Rotations, and Reductions",
            self.advanced_beats(),
            BLUE_C,
            self.ADVANCED_DURATIONS,
        )
