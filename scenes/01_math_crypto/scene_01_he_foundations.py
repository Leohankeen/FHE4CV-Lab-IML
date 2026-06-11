import os
import sys
from manim import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from scenes.library.constants import *
from scenes.library.ehe_primitives import (
    BootstrappingGate,
    CiphertextBlock,
    DepthMeter,
    PlaintextBlock,
)
from scenes.library.storyboard import StoryboardScene, scene_time


class HomomorphicEncryptionFoundations(StoryboardScene):
    """15-minute lesson on the motivation and mathematical shape of HE."""

    MOTION_TIME = 1.35
    CONTENT_TOP = 2.15
    CONTENT_BOTTOM = -2.65

    @staticmethod
    def fit_text(text, max_width):
        if text.width > max_width:
            text.scale_to_fit_width(max_width)
        return text

    def card(self, label, color, width=2.5, height=1.0, font_size=25):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            color=color,
            fill_color=color,
            fill_opacity=0.16,
        )
        text = Text(label, font_size=font_size, color=COLOR_MATH, line_spacing=0.8)
        self.fit_text(text, width - 0.25)
        text.move_to(box)
        return VGroup(box, text)

    @staticmethod
    def arrow_between(left, right, color=COLOR_ENCRYPTION):
        return Arrow(left.get_right(), right.get_left(), buff=0.12, color=color)

    @classmethod
    def motion_step(cls, duration, actions):
        """Keep causal actions readable without stretching them across narration."""
        return min(cls.MOTION_TIME, max(0.8, duration / max(1, actions * 8)))

    def keep_demo_alive(self, demo, accent, duration):
        """Use short focus cues during narration instead of one slow animation."""
        if duration <= 0.05:
            return

        candidates = [
            mob
            for mob in demo
            if mob.width > 0.18
            and mob.height > 0.12
            and mob.width < 5.4
            and mob.height < 3.6
            and mob.get_top()[1] < self.CONTENT_TOP + 0.2
            and mob.get_bottom()[1] > self.CONTENT_BOTTOM - 0.2
        ]
        if not candidates:
            self.wait(duration)
            return

        cue_time = min(1.25, duration)
        cues = []
        elapsed = 0.0
        index = 0
        while elapsed < duration - 0.05:
            run_time = min(cue_time, duration - elapsed)
            target = candidates[index % len(candidates)]
            cues.append(
                target.animate(run_time=run_time, rate_func=there_and_back)
                .scale(1.025)
                .set_stroke(color=accent, opacity=0.95)
            )
            elapsed += run_time
            index += 1
        self.play(Succession(*cues, lag_ratio=1), run_time=duration)

    def clear_beat(self):
        """Remove every transient object so successive experiments cannot overlap."""
        for mobject in list(self.mobjects):
            if mobject is not getattr(self, "lesson_title", None):
                self.remove(mobject)

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
        """Render one storyboard beat as a visual experiment with a visible result."""
        start = scene_time(self)
        section_key = (
            "privacy"
            if "Privacy" in section_label
            else "homomorphism"
            if "Computing" in section_label
            else "ring"
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
        demo_method = getattr(self, f"demo_{section_key}_{index}")
        demo = demo_method(accent, max(8.0, duration - 3.4))
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

    def zone(self, label, color, side):
        area = RoundedRectangle(
            width=5.7,
            height=4.2,
            corner_radius=0.15,
            color=color,
            fill_color=color,
            fill_opacity=0.045,
        ).shift(side * 3.15 + DOWN * 0.15)
        name = Text(label, font_size=21, color=color).next_to(area, UP, buff=0.12)
        return VGroup(area, name)

    def data_tile(self, color=COLOR_PLAINTEXT, rows=4, cols=4):
        pixels = VGroup()
        for row in range(rows):
            for col in range(cols):
                opacity = 0.2 + 0.13 * ((row * 3 + col * 2) % 5)
                pixel = Square(
                    side_length=0.24,
                    stroke_width=0.7,
                    stroke_color=color,
                    fill_color=color,
                    fill_opacity=opacity,
                )
                pixels.add(pixel)
        pixels.arrange_in_grid(rows=rows, cols=cols, buff=0.025)
        return pixels

    def lock_icon(self, color=COLOR_ENCRYPTION):
        shackle = Arc(radius=0.3, start_angle=0, angle=PI, color=color, stroke_width=5)
        shackle.shift(UP * 0.18)
        body = RoundedRectangle(
            width=0.72,
            height=0.58,
            corner_radius=0.08,
            color=color,
            fill_color=color,
            fill_opacity=0.2,
        ).shift(DOWN * 0.12)
        return VGroup(shackle, body)

    def eye_icon(self, color=RED_C):
        upper = ArcBetweenPoints(
            LEFT * 0.65,
            RIGHT * 0.65,
            angle=-PI / 2,
            color=color,
        )
        lower = ArcBetweenPoints(
            LEFT * 0.65,
            RIGHT * 0.65,
            angle=PI / 2,
            color=color,
        )
        pupil = Dot(radius=0.1, color=color)
        return VGroup(upper, lower, pupil)

    def demo_privacy_1(self, accent, duration):
        step = self.motion_step(duration, 6)
        client = self.zone("DATA OWNER", BLUE_C, LEFT)
        cloud = self.zone("OUTSOURCED\nCLOUD", PURPLE_C, RIGHT)
        image = self.data_tile().scale(1.15).move_to(client[0])
        server = VGroup(
            *[
                Line(LEFT * 0.65, RIGHT * 0.65, color=GREY_B)
                for _ in range(4)
            ]
        ).arrange(DOWN, buff=0.25).move_to(cloud[0])
        request = Arrow(client[0].get_right(), cloud[0].get_left(), buff=0.25, color=accent)
        observer = self.eye_icon().scale(0.9).next_to(server, RIGHT, buff=0.55)
        copied = image.copy().set_color(RED_C).move_to(server)
        question = Text("Who sees memory?", font_size=24, color=RED_A).next_to(server, DOWN, buff=0.5)
        self.play(FadeIn(client), FadeIn(cloud), FadeIn(image), run_time=step, rate_func=smooth)
        self.play(GrowArrow(request), image.animate.move_to(cloud[0].get_left() + LEFT * 0.7), run_time=step, rate_func=smooth)
        self.play(FadeIn(server), Transform(image, copied), run_time=step, rate_func=smooth)
        self.play(FadeIn(observer), observer.animate.shift(LEFT * 0.2), run_time=step, rate_func=smooth)
        scan = Line(server.get_left(), server.get_right(), color=RED_C, stroke_width=4)
        self.play(scan.animate.shift(DOWN * 1.1), Write(question), run_time=step)
        self.play(Indicate(copied, color=RED_C), Flash(observer, color=RED_C), run_time=step)
        return VGroup(client, cloud, image, server, request, observer, question, scan)

    def demo_privacy_2(self, accent, duration):
        step = self.motion_step(duration, 6)
        client = self.zone("TRUSTED CLIENT", BLUE_C, LEFT)
        cloud = self.zone("HONEST-BUT-CURIOUS CLOUD", PURPLE_C, RIGHT)
        boundary = DashedLine(UP * 2.0, DOWN * 2.25, color=GREY_B)
        key = self.lock_icon(GREEN_C).scale(0.95).move_to(client[0])
        packet = self.data_tile(RED_C, 3, 5).move_to(client[0].get_right() + LEFT * 1.0)
        route = Arrow(LEFT * 1.5, RIGHT * 1.5, color=RED_C, buff=0)
        blocked_route = Arrow(RIGHT * 1.5, LEFT * 1.5, color=GREEN_C, buff=0).shift(DOWN * 1.05)
        cloud_eye = self.eye_icon().scale(0.75).move_to(cloud[0])
        cross = Cross(cloud_eye, stroke_color=RED_C, stroke_width=5)
        self.play(FadeIn(client), FadeIn(cloud), Create(boundary), run_time=step)
        self.play(FadeIn(key), FadeIn(packet), run_time=step)
        self.play(GrowArrow(route), packet.animate.move_to(cloud[0]), run_time=step)
        self.play(FadeIn(cloud_eye), Create(cross), run_time=step)
        key_copy = key.copy()
        self.play(key_copy.animate.move_to(boundary).set_opacity(0.2), run_time=step)
        self.play(GrowArrow(blocked_route), key_copy.animate.move_to(client[0]), Indicate(key, color=GREEN_C), run_time=step)
        return VGroup(client, cloud, boundary, key, packet, route, blocked_route, cloud_eye, cross, key_copy)

    def demo_privacy_3(self, accent, duration):
        step = self.motion_step(duration, 6)
        client = self.data_tile().scale(1.05).shift(LEFT * 5)
        tunnel = RoundedRectangle(
            width=5.1,
            height=1.55,
            corner_radius=0.7,
            color=YELLOW_D,
            fill_color=YELLOW_D,
            fill_opacity=0.06,
        ).shift(LEFT * 0.65)
        lock = self.lock_icon().move_to(tunnel)
        endpoint = VGroup(
            Rectangle(width=2.2, height=2.5, color=PURPLE_C, fill_opacity=0.08),
            Text("SERVER", font_size=20, color=PURPLE_C),
        ).shift(RIGHT * 4.6)
        endpoint[1].next_to(endpoint[0], UP, buff=0.12)
        packet = client.copy()
        clear_copy = client.copy().set_color(RED_C)
        memory = VGroup(*[Line(LEFT * 0.8, RIGHT * 0.8, color=RED_C) for _ in range(5)])
        memory.arrange(DOWN, buff=0.2).move_to(endpoint[0])
        spy = self.eye_icon().scale(0.7).next_to(endpoint, DOWN, buff=0.25)
        self.play(FadeIn(client), Create(tunnel), FadeIn(lock), run_time=step)
        self.play(packet.animate.move_to(tunnel.get_left() + RIGHT * 0.8), run_time=step)
        self.play(packet.animate.move_to(tunnel.get_right() + LEFT * 0.8), run_time=step)
        self.play(FadeIn(endpoint), packet.animate.move_to(endpoint[0]), run_time=step)
        self.play(Transform(packet, clear_copy.move_to(endpoint[0])), FadeIn(memory), FadeOut(lock), run_time=step)
        self.play(FadeIn(spy), Flash(packet, color=RED_C), run_time=step)
        return VGroup(client, tunnel, endpoint, packet, clear_copy, memory, spy)

    def demo_privacy_4(self, accent, duration):
        step = self.motion_step(duration, 7)
        client = self.zone("CLIENT", BLUE_C, LEFT)
        cloud = self.zone("CLOUD", PURPLE_C, RIGHT)
        plain = self.data_tile().move_to(client[0])
        key = self.lock_icon(GREEN_C).scale(0.7).next_to(plain, DOWN, buff=0.35)
        cipher = VGroup(*[Dot(radius=0.075, color=RED_C) for _ in range(28)])
        cipher.arrange_in_grid(rows=4, cols=7, buff=0.12).move_to(plain)
        evaluator = VGroup(
            Circle(radius=0.78, color=YELLOW_D),
            Text("f", font_size=38, color=YELLOW_D),
        ).move_to(cloud[0])
        evaluator[1].move_to(evaluator[0])
        route = Arrow(client[0].get_right(), evaluator.get_left(), buff=0.25, color=RED_C)
        result_route = Arrow(evaluator.get_left(), client[0].get_right(), buff=0.25, color=RED_C)
        score = VGroup(
            Rectangle(width=1.3, height=0.18, color=GREEN_C, fill_opacity=0.7),
            Text("0.87", font_size=25, color=GREEN_C),
        ).arrange(DOWN, buff=0.25).move_to(client[0])
        self.play(FadeIn(client), FadeIn(cloud), FadeIn(plain), FadeIn(key), run_time=step)
        self.play(Transform(plain, cipher), key.animate.scale(1.15), run_time=step)
        self.play(GrowArrow(route), plain.animate.move_to(evaluator.get_left() + LEFT * 0.45), run_time=step)
        self.play(FadeIn(evaluator), Rotate(evaluator[0], angle=PI), plain.animate.move_to(evaluator), run_time=step)
        self.play(plain.animate.set_color(RED_A).shift(UP * 0.35), Rotate(evaluator[0], angle=PI), run_time=step)
        self.play(GrowArrow(result_route), plain.animate.move_to(client[0]), run_time=step)
        self.play(Transform(plain, score), Indicate(key, color=GREEN_C), run_time=step)
        return VGroup(client, cloud, plain, key, evaluator, route, result_route, score)

    def demo_privacy_5(self, accent, duration):
        step = self.motion_step(duration, 6)
        values = VGroup(
            *[Dot(radius=0.09, color=BLUE_C) for _ in range(6)]
        ).arrange(RIGHT, buff=0.16)
        values.move_to(LEFT * 5.1)
        value_label = Text("6 values", font_size=20, color=BLUE_C)
        value_label.next_to(values, DOWN, buff=0.28)

        expanded = VGroup(
            *[
                RoundedRectangle(
                    width=1.55,
                    height=0.48,
                    corner_radius=0.06,
                    color=RED_C,
                    fill_color=RED_C,
                    fill_opacity=0.1 + 0.04 * i,
                )
                for i in range(3)
            ]
        ).arrange(DOWN, buff=0.14)
        expanded.move_to(LEFT * 2.45)
        expanded_label = Text("larger ciphertext", font_size=20, color=RED_C)
        expanded_label.next_to(expanded, DOWN, buff=0.24)
        expansion_arrow = Arrow(
            values.get_right(),
            expanded.get_left(),
            buff=0.22,
            color=accent,
        )

        plus_gate = self.card("+", GREEN_C, 1.25, 0.78, 34)
        plus_gate.move_to([0.45, 0.78, 0])
        plus_label = Text("allowed", font_size=19, color=GREEN_C)
        plus_label.next_to(plus_gate, UP, buff=0.16)
        branch_gate = self.card("if", RED_C, 1.25, 0.78, 25)
        branch_gate.move_to([0.45, -0.88, 0])
        branch_label = Text("blocked", font_size=19, color=RED_C)
        branch_label.next_to(branch_gate, DOWN, buff=0.16)
        cross = Cross(branch_gate, stroke_color=RED_C, stroke_width=5)
        operation_arrows = VGroup(
            Arrow(expanded.get_right(), plus_gate.get_left(), buff=0.18, color=GREEN_C),
            Arrow(expanded.get_right(), branch_gate.get_left(), buff=0.18, color=RED_C),
        )

        clock = Circle(radius=0.66, color=YELLOW_D).move_to([4.25, 0.78, 0])
        hand = Line(clock.get_center(), clock.get_center() + UP * 0.52, color=YELLOW_D)
        cost_label = Text("more work", font_size=20, color=YELLOW_D)
        cost_label.next_to(clock, DOWN, buff=0.22)
        cost_arrow = Arrow(
            plus_gate.get_right(),
            clock.get_left(),
            buff=0.2,
            color=YELLOW_D,
        )

        self.play(FadeIn(values), FadeIn(value_label), run_time=step)
        self.play(
            GrowArrow(expansion_arrow),
            TransformFromCopy(values, expanded),
            run_time=step,
        )
        self.play(FadeIn(expanded_label), run_time=step * 0.7)
        self.play(
            GrowArrow(operation_arrows[0]),
            GrowArrow(operation_arrows[1]),
            FadeIn(plus_gate),
            FadeIn(branch_gate),
            run_time=step,
        )
        self.play(
            FadeIn(plus_label),
            FadeIn(branch_label),
            Create(cross),
            run_time=step,
        )
        self.play(
            GrowArrow(cost_arrow),
            FadeIn(clock),
            Create(hand),
            FadeIn(cost_label),
            run_time=step,
        )
        self.play(
            Rotate(hand, angle=TAU * 2, about_point=clock.get_center()),
            Indicate(expanded, color=RED_C),
            run_time=step,
            rate_func=smooth,
        )
        return VGroup(
            values,
            value_label,
            expanded,
            expanded_label,
            expansion_arrow,
            plus_gate,
            plus_label,
            branch_gate,
            branch_label,
            cross,
            operation_arrows,
            clock,
            hand,
            cost_label,
            cost_arrow,
        )

    def demo_homomorphism_1(self, accent, duration):
        step = self.motion_step(duration, 6)
        plain_label = Text("PLAINTEXT", font_size=18, color=BLUE_C)
        plain_label.move_to([-5.15, 0.9, 0])
        cipher_label = Text("ENCRYPTED", font_size=18, color=RED_C)
        cipher_label.move_to([-5.15, -0.95, 0])

        input_value = self.card("2.0", BLUE_C, 1.05, 0.68, 27)
        input_value.move_to([-3.85, 0.9, 0])
        cipher_input = self.lock_icon(RED_C).scale(0.62)
        cipher_input.move_to([-3.85, -0.95, 0])
        plain_gate = self.card("f(x) = x^2 + 1", BLUE_C, 2.55, 0.8, 22)
        plain_gate.move_to([0, 0.9, 0])
        cipher_gate = self.card("Evaluate f", YELLOW_D, 2.55, 0.8, 22)
        cipher_gate.move_to([0, -0.95, 0])
        plain_result = self.card("5.0", GREEN_C, 1.05, 0.68, 27)
        plain_result.move_to([4.0, 0.9, 0])
        cipher_result = self.lock_icon(RED_C).scale(0.62)
        cipher_result.move_to([4.0, -0.95, 0])
        decrypted = self.card("5.0", GREEN_C, 1.05, 0.68, 27)
        decrypted.move_to(cipher_result)

        arrows = VGroup(
            Arrow(input_value.get_right(), plain_gate.get_left(), buff=0.15, color=BLUE_C),
            Arrow(plain_gate.get_right(), plain_result.get_left(), buff=0.15, color=BLUE_C),
            Arrow(cipher_input.get_right(), cipher_gate.get_left(), buff=0.15, color=RED_C),
            Arrow(cipher_gate.get_right(), cipher_result.get_left(), buff=0.15, color=RED_C),
        )
        plain_token = Dot(arrows[0].get_start(), radius=0.08, color=BLUE_C)
        cipher_token = Dot(arrows[2].get_start(), radius=0.08, color=RED_C)
        equality = Text("same numerical result", font_size=23, color=GREEN_C).to_edge(DOWN, buff=0.65)

        self.play(
            FadeIn(plain_label),
            FadeIn(cipher_label),
            FadeIn(input_value),
            FadeIn(cipher_input),
            run_time=step,
        )
        self.play(
            FadeIn(plain_gate),
            FadeIn(cipher_gate),
            GrowArrow(arrows[0]),
            GrowArrow(arrows[2]),
            FadeIn(plain_token),
            FadeIn(cipher_token),
            run_time=step,
        )
        self.play(
            MoveAlongPath(plain_token, arrows[0]),
            MoveAlongPath(cipher_token, arrows[2]),
            run_time=step,
            rate_func=smooth,
        )
        self.play(
            GrowArrow(arrows[1]),
            GrowArrow(arrows[3]),
            FadeIn(plain_result),
            FadeIn(cipher_result),
            run_time=step,
        )
        self.play(
            MoveAlongPath(plain_token, arrows[1]),
            MoveAlongPath(cipher_token, arrows[3]),
            run_time=step,
            rate_func=smooth,
        )
        self.play(Transform(cipher_result, decrypted), run_time=step)
        self.play(Write(equality), Circumscribe(VGroup(plain_result, cipher_result), color=GREEN_C), run_time=step)
        return VGroup(
            plain_label,
            cipher_label,
            input_value,
            cipher_input,
            plain_gate,
            cipher_gate,
            plain_result,
            cipher_result,
            arrows,
            plain_token,
            cipher_token,
            equality,
        )

    def demo_homomorphism_2(self, accent, duration):
        step = self.motion_step(duration, 6)
        levels = VGroup(
            *[
                Rectangle(
                    width=5.8 - i * 0.65,
                    height=0.38,
                    color=interpolate_color(GREEN_C, RED_C, i / 4),
                    fill_opacity=0.2,
                )
                for i in range(5)
            ]
        ).arrange(DOWN, buff=0.25)
        token = self.lock_icon(RED_C).scale(0.55).move_to(levels[0])
        multiply = Text("x", font_size=36, color=YELLOW_D).next_to(levels, LEFT, buff=0.45)
        bootstrap = BootstrappingGate("BOOTSTRAP").scale(0.55).next_to(levels, RIGHT, buff=0.45)
        self.play(LaggedStart(*(FadeIn(level) for level in levels), lag_ratio=0.12), FadeIn(token), run_time=step)
        self.play(FadeIn(multiply), token.animate.move_to(levels[1]), run_time=step)
        self.play(Indicate(multiply), token.animate.move_to(levels[2]), run_time=step)
        self.play(Indicate(multiply), token.animate.move_to(levels[3]), run_time=step)
        self.play(FadeIn(bootstrap), token.animate.move_to(bootstrap), run_time=step)
        self.play(token.animate.move_to(levels[0]), Flash(bootstrap, color=YELLOW_D), run_time=step)
        return VGroup(levels, token, multiply, bootstrap)

    def demo_homomorphism_3(self, accent, duration):
        step = self.motion_step(duration, 8)
        branch = VGroup(
            Text("if x > 0", font_size=25, color=RED_C),
            Rectangle(width=2.2, height=0.9, color=RED_C),
        ).shift(LEFT * 4)
        branch[0].move_to(branch[1])
        wall = Line(UP * 1.5, DOWN * 1.5, color=RED_C, stroke_width=7).shift(LEFT * 1.6)
        token = self.lock_icon(RED_C).scale(0.55).shift(LEFT * 5.5)
        add_gate = VGroup(Circle(radius=0.55, color=GREEN_C), Text("+", font_size=34, color=GREEN_C)).shift(RIGHT * 0.5 + UP)
        add_gate[1].move_to(add_gate[0])
        mul_gate = VGroup(Circle(radius=0.55, color=YELLOW_D), Text("x", font_size=34, color=YELLOW_D)).shift(RIGHT * 3.0 + DOWN * 0.7)
        mul_gate[1].move_to(mul_gate[0])
        circuit_path = VMobject(color=accent).set_points_smoothly([
            LEFT * 1.0 + DOWN * 1.8,
            RIGHT * 0.5 + UP,
            RIGHT * 3.0 + DOWN * 0.7,
            RIGHT * 5.1,
        ])
        output = token.copy().move_to(circuit_path.get_end())
        self.play(FadeIn(branch), FadeIn(token), run_time=step)
        self.play(token.animate.move_to(wall.get_center() + LEFT * 0.35), Create(wall), run_time=step)
        self.play(Wiggle(token), Flash(wall, color=RED_C), run_time=step)
        self.play(FadeIn(add_gate), FadeIn(mul_gate), Create(circuit_path), run_time=step)
        token.move_to(circuit_path.get_start())
        self.play(MoveAlongPath(token, circuit_path), run_time=step * 2)
        self.play(TransformFromCopy(token, output), Indicate(VGroup(add_gate, mul_gate), color=GREEN_C), run_time=step)
        return VGroup(branch, wall, token, add_gate, mul_gate, circuit_path, output)

    def demo_homomorphism_4(self, accent, duration):
        step = self.motion_step(duration, 6)
        feature = self.data_tile(RED_C, 4, 4).scale(1.1).shift(LEFT * 4.5)
        weights = VGroup(
            *[
                Text(f"{v:.1f}", font_size=22, color=BLUE_C)
                for v in (0.3, -0.8, 1.2, 0.5)
            ]
        )
        weights.arrange(DOWN, buff=0.16).shift(UP * 0.8)
        multiply = VGroup(Circle(radius=0.72, color=YELLOW_D), Text("x", font_size=38, color=YELLOW_D))
        multiply[1].move_to(multiply[0])
        output = VGroup(*[Dot(radius=0.09, color=RED_C) for _ in range(12)])
        output.arrange_in_grid(rows=3, cols=4, buff=0.14).shift(RIGHT * 4.5)
        feature_path = Arrow(feature.get_right(), multiply.get_left(), buff=0.15, color=RED_C)
        weight_path = Arrow(weights.get_bottom(), multiply.get_top(), buff=0.15, color=BLUE_C)
        output_path = Arrow(multiply.get_right(), output.get_left(), buff=0.15, color=RED_C)
        eye = self.eye_icon().scale(0.65).next_to(feature, DOWN, buff=0.4)
        cross = Cross(eye, stroke_color=RED_C)
        self.play(FadeIn(feature), FadeIn(weights), run_time=step)
        self.play(GrowArrow(feature_path), GrowArrow(weight_path), run_time=step)
        self.play(FadeIn(multiply), Rotate(multiply[0], angle=PI), run_time=step)
        self.play(GrowArrow(output_path), LaggedStart(*(FadeIn(dot) for dot in output), lag_ratio=0.05), run_time=step)
        self.play(FadeIn(eye), Create(cross), run_time=step)
        self.play(Indicate(weights, color=BLUE_C), Indicate(output, color=RED_C), run_time=step)
        return VGroup(feature, weights, multiply, output, feature_path, weight_path, output_path, eye, cross)

    def demo_homomorphism_5(self, accent, duration):
        step = self.motion_step(duration, 6)
        integers = VGroup(
            *[Text(str(v), font_size=26, color=BLUE_C) for v in (7, 12, 4)]
        ).arrange(DOWN, buff=0.24).move_to([-5.0, 0.75, 0])
        decimals = VGroup(
            *[
                Text(f"{v:.2f}", font_size=25, color=YELLOW_D)
                for v in (0.25, -1.4, 3.12)
            ]
        )
        decimals.arrange(DOWN, buff=0.24).move_to([-5.0, -1.25, 0])
        exact_bin = RoundedRectangle(
            width=2.5,
            height=1.75,
            color=BLUE_C,
            fill_opacity=0.08,
        ).move_to([-1.65, 0.75, 0])
        approx_bin = RoundedRectangle(
            width=2.5,
            height=1.75,
            color=YELLOW_D,
            fill_opacity=0.08,
        ).move_to([2.25, 0.75, 0])
        exact_label = Text("BFV / BGV", font_size=22, color=BLUE_C).next_to(exact_bin, UP)
        approx_label = Text("CKKS", font_size=25, color=YELLOW_D).next_to(approx_bin, UP)
        slots = VGroup(*[Square(side_length=0.38, color=YELLOW_D, fill_opacity=0.12) for _ in range(8)])
        slots.arrange_in_grid(rows=2, cols=4, buff=0.08).move_to([2.25, -1.55, 0])
        slots_label = Text("SIMD slots", font_size=19, color=YELLOW_D)
        slots_label.next_to(slots, DOWN, buff=0.16)
        slot_arrow = Arrow(
            approx_bin.get_bottom(),
            slots.get_top(),
            buff=0.18,
            color=YELLOW_D,
        )
        self.play(FadeIn(integers), FadeIn(exact_bin), FadeIn(exact_label), run_time=step)
        self.play(integers.animate.move_to(exact_bin), run_time=step)
        self.play(FadeIn(decimals), FadeIn(approx_bin), FadeIn(approx_label), run_time=step)
        self.play(decimals.animate.move_to(approx_bin), run_time=step)
        self.play(
            GrowArrow(slot_arrow),
            FadeIn(slots),
            FadeIn(slots_label),
            approx_bin.animate.set_fill(YELLOW_D, opacity=0.18),
            run_time=step,
        )
        self.play(LaggedStart(*(Indicate(slot, color=YELLOW_D) for slot in slots), lag_ratio=0.08), run_time=step)
        return VGroup(
            integers,
            decimals,
            exact_bin,
            approx_bin,
            exact_label,
            approx_label,
            slots,
            slots_label,
            slot_arrow,
        )

    def demo_ring_1(self, accent, duration):
        step = self.motion_step(duration, 6)
        vector = VGroup(
            *[
                Text(f"{v:.1f}", font_size=23, color=BLUE_C)
                for v in (0.2, -0.7, 1.1, 0.4)
            ]
        )
        vector.arrange(DOWN, buff=0.22).shift(LEFT * 5)
        axes = Axes(x_range=[0, 5, 1], y_range=[-1.5, 1.5, 0.5], x_length=5.5, y_length=2.6, tips=False)
        axes.shift(RIGHT * 0.2)
        coeffs = VGroup(*[Dot(axes.c2p(i + 1, v), color=PURPLE_C) for i, v in enumerate((0.2, -0.7, 1.1, 0.4))])
        stems = VGroup(*[Line(axes.c2p(i + 1, 0), dot.get_center(), color=PURPLE_C) for i, dot in enumerate(coeffs)])
        ring = Circle(radius=1.25, color=YELLOW_D).shift(RIGHT * 4.7)
        wrapped = coeffs.copy().arrange_in_grid(rows=2, cols=2, buff=0.35).move_to(ring)
        self.play(FadeIn(vector), run_time=step)
        self.play(Create(axes), run_time=step)
        self.play(LaggedStart(*(TransformFromCopy(value, dot) for value, dot in zip(vector, coeffs)), lag_ratio=0.12), run_time=step)
        self.play(LaggedStart(*(Create(stem) for stem in stems), lag_ratio=0.1), run_time=step)
        self.play(Create(ring), run_time=step)
        self.play(TransformFromCopy(coeffs, wrapped), Rotate(wrapped, angle=PI / 2), run_time=step)
        return VGroup(vector, axes, coeffs, stems, ring, wrapped)

    def demo_ring_2(self, accent, duration):
        step = self.motion_step(duration, 8)
        circle = Circle(radius=1.55, color=YELLOW_D).shift(DOWN * 0.25)
        ticks = VGroup(
            *[
                Dot(circle.point_from_proportion(i / 8), radius=0.045, color=GREY_B)
                for i in range(8)
            ]
        )
        powers = VGroup(
            Text("X^0", font_size=18, color=GREY_B).next_to(circle, RIGHT, buff=0.18),
            Text("X^1", font_size=18, color=GREY_B).move_to(circle.get_center() + UR * 1.75),
            Text("X^2", font_size=19, color=GREEN_C).next_to(circle, UP, buff=0.16),
            Text("X^(N-1)", font_size=18, color=GREY_B).move_to(circle.get_center() + DR * 1.78),
        )
        term = Dot(circle.point_from_proportion(0), radius=0.13, color=BLUE_C)
        label = self.card("X^(N+2)", BLUE_C, 1.8, 0.72, 22)
        label.move_to([-4.55, -0.15, 0])
        relation = Text("cross X^N  ->  change sign", font_size=22, color=YELLOW_D)
        relation.move_to([-2.85, 1.55, 0])
        reduced = self.card("-X^2", GREEN_C, 1.5, 0.72, 25)
        reduced.move_to([4.55, -0.15, 0])
        enter_arrow = Arrow(label.get_right(), term.get_center(), buff=0.18, color=BLUE_C)
        exit_arrow = Arrow(
            circle.point_from_proportion(0.25),
            reduced.get_left(),
            buff=0.18,
            color=GREEN_C,
        )
        self.play(
            Create(circle),
            LaggedStart(*(FadeIn(tick) for tick in ticks), lag_ratio=0.06),
            LaggedStart(*(FadeIn(power) for power in powers), lag_ratio=0.1),
            run_time=step,
        )
        self.play(FadeIn(label), GrowArrow(enter_arrow), FadeIn(term), run_time=step)
        self.play(MoveAlongPath(term, circle), run_time=step * 2, rate_func=linear)
        self.play(Write(relation), term.animate.set_color(RED_C), run_time=step)
        self.play(term.animate.move_to(circle.point_from_proportion(0.25)), run_time=step)
        self.play(
            GrowArrow(exit_arrow),
            FadeIn(reduced),
            Flash(term, color=GREEN_C),
            run_time=step,
        )
        return VGroup(
            circle,
            ticks,
            powers,
            term,
            label,
            relation,
            reduced,
            enter_arrow,
            exit_arrow,
        )

    def demo_ring_3(self, accent, duration):
        step = self.motion_step(duration, 7)
        secret = VGroup(*[Dot(radius=0.08, color=GREEN_C) for _ in range(9)])
        secret.arrange(RIGHT, buff=0.12).shift(LEFT * 4.6 + UP * 1.2)
        random = VGroup(*[Dot(radius=0.08, color=BLUE_C) for _ in range(12)])
        random.arrange(RIGHT, buff=0.1).shift(LEFT * 4.5 + DOWN * 0.2)
        error = VGroup(*[Dot(radius=0.035, color=GREY_B) for _ in range(18)])
        error.arrange_in_grid(rows=3, cols=6, buff=0.1).shift(LEFT * 4.5 + DOWN * 1.45)
        mixer = Annulus(inner_radius=0.6, outer_radius=1.05, color=YELLOW_D, fill_opacity=0.1)
        cipher_a = VGroup(*[Dot(radius=0.06, color=RED_C) for _ in range(15)]).arrange_in_grid(rows=3, cols=5, buff=0.12)
        cipher_b = cipher_a.copy().set_color(PURPLE_C)
        cipher_a.shift(RIGHT * 3.1 + UP * 0.7)
        cipher_b.shift(RIGHT * 3.1 + DOWN * 0.7)
        arrows = VGroup(
            Arrow(secret.get_right(), mixer.get_left(), buff=0.1, color=GREEN_C),
            Arrow(random.get_right(), mixer.get_left(), buff=0.1, color=BLUE_C),
            Arrow(error.get_right(), mixer.get_left(), buff=0.1, color=GREY_B),
        )
        self.play(FadeIn(secret), FadeIn(random), FadeIn(error), run_time=step)
        self.play(LaggedStart(*(GrowArrow(arrow) for arrow in arrows), lag_ratio=0.15), run_time=step)
        self.play(FadeIn(mixer), Rotate(mixer, angle=PI), run_time=step)
        self.play(Rotate(mixer, angle=PI), run_time=step)
        self.play(TransformFromCopy(mixer, cipher_a), run_time=step)
        self.play(TransformFromCopy(mixer, cipher_b), run_time=step)
        self.play(Indicate(error, color=GREY_B), Circumscribe(VGroup(cipher_a, cipher_b), color=RED_C), run_time=step)
        return VGroup(secret, random, error, mixer, cipher_a, cipher_b, arrows)

    def demo_ring_4(self, accent, duration):
        step = self.motion_step(duration, 6)
        bars = VGroup(
            self.resource_bar("modulus", 0.92, RED_C),
            self.resource_bar("levels", 0.82, YELLOW_D),
            self.resource_bar("precision", 0.88, GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).shift(LEFT * 2)
        token = self.lock_icon(RED_C).scale(0.55).shift(RIGHT * 3.8)
        halo = Circle(radius=0.62, color=GREY_B, stroke_opacity=0.4).move_to(token)
        multiply = Text("x", font_size=40, color=YELLOW_D).next_to(token, UP, buff=0.4)
        self.play(LaggedStart(*(FadeIn(bar) for bar in bars), lag_ratio=0.15), FadeIn(token), run_time=step)
        self.play(FadeIn(multiply), FadeIn(halo), run_time=step)
        self.play(
            bars[0][1][1].animate.scale(0.82, about_edge=LEFT),
            bars[1][1][1].animate.scale(0.75, about_edge=LEFT),
            bars[2][1][1].animate.scale(0.88, about_edge=LEFT),
            halo.animate.scale(1.2),
            run_time=step,
        )
        self.play(
            bars[0][1][1].animate.scale(0.82, about_edge=LEFT),
            bars[1][1][1].animate.scale(0.66, about_edge=LEFT),
            bars[2][1][1].animate.scale(0.86, about_edge=LEFT),
            halo.animate.scale(1.2),
            run_time=step,
        )
        threshold = DashedLine(UP * 1.4, DOWN * 1.4, color=RED_C).shift(RIGHT * 5.0)
        self.play(Create(threshold), token.animate.shift(RIGHT * 0.75), run_time=step)
        self.play(Indicate(bars, color=YELLOW_D), Flash(threshold, color=RED_C), run_time=step)
        return VGroup(bars, token, halo, multiply, threshold)

    def demo_ring_5(self, accent, duration):
        step = self.motion_step(duration, 8)
        vector = VGroup(*[Dot(radius=0.1, color=BLUE_C) for _ in range(6)]).arrange(RIGHT, buff=0.18).shift(LEFT * 5.3)
        slots = VGroup(*[Square(side_length=0.34, color=BLUE_C, fill_opacity=0.15) for _ in range(6)])
        slots.arrange(RIGHT, buff=0.06).shift(LEFT * 2.8)
        polynomial = ParametricFunction(
            lambda t: np.array([t, 0.55 * np.sin(2.2 * t), 0]),
            t_range=[-1.2, 1.2],
            color=PURPLE_C,
        )
        cipher = VGroup(
            Circle(radius=0.62, color=RED_C),
            Circle(radius=0.62, color=RED_A),
        ).arrange(DOWN, buff=0.2).shift(RIGHT * 2.4)
        evaluate = VGroup(
            Circle(radius=0.66, color=YELLOW_D),
            Text("f", font_size=34, color=YELLOW_D),
        ).shift(RIGHT * 4.8)
        evaluate[1].move_to(evaluate[0])
        arrows = VGroup(
            Arrow(vector.get_right(), slots.get_left(), buff=0.12, color=BLUE_C),
            Arrow(slots.get_right(), polynomial.get_left(), buff=0.12, color=PURPLE_C),
            Arrow(polynomial.get_right(), cipher.get_left(), buff=0.12, color=RED_C),
            Arrow(cipher.get_right(), evaluate.get_left(), buff=0.12, color=YELLOW_D),
        )
        self.play(FadeIn(vector), run_time=step)
        self.play(GrowArrow(arrows[0]), TransformFromCopy(vector, slots), run_time=step)
        self.play(GrowArrow(arrows[1]), Create(polynomial), run_time=step)
        self.play(Indicate(polynomial, color=PURPLE_C), run_time=step)
        self.play(GrowArrow(arrows[2]), TransformFromCopy(polynomial, cipher), run_time=step)
        self.play(GrowArrow(arrows[3]), FadeIn(evaluate), run_time=step)
        self.play(Rotate(evaluate[0], angle=PI), Rotate(cipher, angle=PI / 5), run_time=step)
        self.play(Indicate(VGroup(vector, slots, polynomial, cipher, evaluate), color=accent), run_time=step)
        return VGroup(vector, slots, polynomial, cipher, evaluate, arrows)

    def open_lesson(self, lesson_title, audio_path):
        self.camera.background_color = "#101214"
        self.add_optional_sound(audio_path)
        act = Text("ACT 1 | MATHEMATICS AND CRYPTOGRAPHY", font_size=25, color=COLOR_ENCRYPTION)
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
            title.animate.scale(0.58).to_edge(UP, buff=0.18),
            run_time=1,
        )
        self.lesson_title = title
        return title

    def show_chapter_plate(self, title, image_path, summary, accent):
        subtitle = Text("Visual roadmap", font_size=25, color=GREY_B).next_to(title, DOWN, buff=0.2)
        stages = VGroup(
            self.card("PLAIN\nVALUES", COLOR_PLAINTEXT, 2.3, 1.25, 23),
            self.card("CRYPTO\nTRANSFORM", COLOR_ENCRYPTION, 2.3, 1.25, 23),
            self.card("ENCRYPTED\nOBJECTS", COLOR_CIPHERTEXT, 2.3, 1.25, 23),
        ).arrange(RIGHT, buff=0.9)
        arrows = VGroup(
            self.arrow_between(stages[0], stages[1], accent),
            self.arrow_between(stages[1], stages[2], accent),
        )
        summary_text = Text(summary, font_size=26, color=GREY_B)
        self.fit_text(summary_text, 10.8)
        summary_text.next_to(stages, DOWN, buff=0.55)
        self.play(FadeIn(subtitle), FadeIn(stages[0]))
        self.play(GrowArrow(arrows[0]), FadeIn(stages[1]))
        self.play(GrowArrow(arrows[1]), FadeIn(stages[2]))
        self.play(Write(summary_text), Indicate(stages[1], color=accent))
        self.play(FadeOut(VGroup(subtitle, stages, arrows, summary_text)))

    def show_trust_boundary(self, title):
        subtitle = Text("Protect data while the cloud is computing", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.2)
        row_y = -0.25
        client = self.card("TRUSTED\nCLIENT", COLOR_PLAINTEXT, 2.05, 1.25, 23)
        client.move_to([-5.35, row_y, 0])
        encrypted_input = CiphertextBlock("Enc(x)").scale(0.45)
        encrypted_input.move_to([-3.05, row_y, 0])
        evaluator = self.card("Evaluate f", COLOR_ENCRYPTION, 1.75, 0.82, 21)
        evaluator.move_to([-0.25, row_y, 0])
        encrypted_output = CiphertextBlock("Enc(f(x))").scale(0.43)
        encrypted_output.move_to([2.45, row_y, 0])
        cloud = self.card("UNTRUSTED\nCLOUD", PURPLE_C, 2.05, 1.25, 23)
        cloud.move_to([5.25, row_y, 0])

        boundary = DashedLine(
            [-1.65, 1.45, 0],
            [-1.65, -2.35, 0],
            color=GREY_B,
        )
        boundary_label = Text("trust boundary", font_size=20, color=GREY_B).next_to(boundary, UP, buff=0.1)
        secret = self.card("SecretKey", GREEN_C, 1.9, 0.72, 21).next_to(client, DOWN, buff=0.55)
        arrows = VGroup(
            Arrow(client.get_right(), encrypted_input.get_left(), buff=0.12, color=COLOR_CIPHERTEXT),
            Arrow(encrypted_input.get_right(), evaluator.get_left(), buff=0.12, color=COLOR_CIPHERTEXT),
            Arrow(evaluator.get_right(), encrypted_output.get_left(), buff=0.12, color=COLOR_CIPHERTEXT),
            Arrow(encrypted_output.get_right(), cloud.get_left(), buff=0.12, color=COLOR_CIPHERTEXT),
        )
        self.play(FadeIn(subtitle), FadeIn(client), FadeIn(cloud))
        self.play(Create(boundary), FadeIn(boundary_label), FadeIn(secret))
        self.play(GrowArrow(arrows[0]), FadeIn(encrypted_input))
        self.play(GrowArrow(arrows[1]), FadeIn(evaluator))
        self.play(GrowArrow(arrows[2]), FadeIn(encrypted_output))
        self.play(GrowArrow(arrows[3]), Indicate(cloud, color=PURPLE_C))
        self.play(Indicate(secret, color=GREEN_C), Flash(boundary, color=COLOR_ENCRYPTION))
        self.play(
            FadeOut(
                VGroup(
                    subtitle, client, cloud, boundary, boundary_label, secret,
                    encrypted_input, evaluator, encrypted_output, arrows,
                )
            )
        )

    def show_data_in_use_problem(self, title):
        subtitle = Text("Encryption protects three different data states", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.2)
        states = VGroup(
            self.card("DATA AT REST\nEncrypted disk", COLOR_PLAINTEXT, 3.2, 1.15, 21),
            self.card("DATA IN TRANSIT\nTLS channel", COLOR_ENCRYPTION, 3.2, 1.15, 21),
            self.card("DATA IN USE\nServer memory", RED_C, 3.2, 1.15, 21),
        ).arrange(RIGHT, buff=0.45).shift(UP * 0.8)

        pipeline_y = -1.15
        plain = PlaintextBlock("medical image").scale(0.48)
        plain.move_to([-5.0, pipeline_y, 0])
        tls = self.card("TLS", COLOR_ENCRYPTION, 1.35, 0.72, 22)
        tls.move_to([-2.15, pipeline_y, 0])
        cloud = self.card("CLOUD\nCOMPUTE", PURPLE_C, 2.0, 1.0, 21)
        cloud.move_to([0.65, pipeline_y, 0])
        exposed = self.card("PLAINTEXT\nmedical image", RED_C, 2.25, 1.0, 20)
        exposed.move_to([4.55, pipeline_y, 0])
        route = VGroup(
            Arrow(plain.get_right(), tls.get_left(), buff=0.12, color=COLOR_ENCRYPTION),
            Arrow(tls.get_right(), cloud.get_left(), buff=0.12, color=COLOR_ENCRYPTION),
            Arrow(cloud.get_right(), exposed.get_left(), buff=0.12, color=RED_C),
        )
        warning = Text("Plaintext exposed during computation", font_size=24, color=RED_A)
        self.fit_text(warning, 10.8)
        warning.to_edge(DOWN, buff=0.48)
        packet = Dot(route[0].get_start(), radius=0.09, color=WHITE)

        self.play(FadeIn(subtitle), LaggedStart(*(FadeIn(state) for state in states), lag_ratio=0.18))
        self.play(FadeIn(plain), FadeIn(tls), FadeIn(cloud))
        self.play(GrowArrow(route[0]), FadeIn(packet))
        self.play(MoveAlongPath(packet, route[0]), run_time=0.7)
        self.play(GrowArrow(route[1]))
        self.play(MoveAlongPath(packet, route[1]), run_time=0.7)
        self.play(GrowArrow(route[2]), FadeIn(exposed, shift=LEFT * 0.15))
        self.play(
            MoveAlongPath(packet, route[2]),
            cloud.animate.set_color(RED_C),
            Write(warning),
            run_time=1.0,
        )
        self.play(Flash(exposed, color=RED_C), FadeOut(packet))
        self.play(FadeOut(VGroup(subtitle, states, plain, tls, cloud, exposed, route, warning)))

    def construct(self):
        # ==================================================
        # PHAN DOAN 1.1: DATA IN USE VA TRUST BOUNDARY
        # ==================================================
        first_start = scene_time(self)
        title = self.open_lesson(
            "Act 1.1 - Why Homomorphic Encryption?",
            "assets/audio/01_math_crypto/scene_01_he_foundations.mp3",
        )
        self.show_chapter_plate(
            title,
            "assets/image/01_math_crypto/scene_01_trust_boundary.png",
            "Private data crosses the boundary only as ciphertext",
            COLOR_ENCRYPTION,
        )
        self.show_data_in_use_problem(title)
        self.show_trust_boundary(title)
        self.play_section_beats(
            first_start,
            300,
            "00:00 - 05:00 | Privacy boundary",
            self.privacy_beats(),
            COLOR_PLAINTEXT,
        )

        # ==================================================
        # PHAN DOAN 1.2: HOMOMORPHIC CORRECTNESS
        # ==================================================
        second_start = scene_time(self)
        self.show_homomorphic_equation(title)
        self.show_scheme_and_depth(title)
        self.play_section_beats(
            second_start,
            300,
            "05:00 - 10:00 | Computing while encrypted",
            self.homomorphism_beats(),
            COLOR_ENCRYPTION,
        )

        # ==================================================
        # PHAN DOAN 1.3: POLYNOMIAL RINGS VA RLWE
        # ==================================================
        third_start = scene_time(self)
        self.show_ring_picture(title)
        self.play_section_beats(
            third_start,
            300,
            "10:00 - 15:00 | Ring and RLWE intuition",
            self.ring_beats(),
            COLOR_CIPHERTEXT,
        )

    def show_homomorphic_equation(self, title):
        subtitle = Text("The cloud transforms ciphertext, not plaintext", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.2)
        plain = self.card("x", COLOR_PLAINTEXT, 1.3, 1.0, 34).shift(LEFT * 5)
        encrypt = self.card("Encrypt", COLOR_ENCRYPTION, 1.9, 1.0, 23).shift(LEFT * 2.7)
        cipher = self.card("Enc(x)", COLOR_CIPHERTEXT, 1.8, 1.0, 28)
        evaluate = self.card("Evaluate f", PURPLE_C, 2.1, 1.0, 23).shift(RIGHT * 2.65)
        output = self.card("Enc(f(x))", COLOR_CIPHERTEXT, 2.15, 1.0, 25).shift(RIGHT * 5.15)
        items = [plain, encrypt, cipher, evaluate, output]
        arrows = VGroup(*[self.arrow_between(items[i], items[i + 1]) for i in range(4)])
        invariant = Text("Decrypt(Enc(f(x))) is approximately f(x)", font_size=27, color=GREEN_C)
        invariant.next_to(cipher, DOWN, buff=0.85)
        unsupported = VGroup(
            self.card("branch", RED_C, 1.5, 0.68, 20),
            self.card("compare", RED_C, 1.7, 0.68, 20),
            self.card("max", RED_C, 1.3, 0.68, 20),
        ).arrange(RIGHT, buff=0.18)
        unsupported.next_to(invariant, DOWN, buff=0.42)
        cross = Text("not native CKKS operations", font_size=21, color=RED_A)
        cross.next_to(unsupported, DOWN, buff=0.18)

        self.play(FadeIn(subtitle), FadeIn(plain))
        for item, arrow in zip(items[1:], arrows):
            self.play(GrowArrow(arrow), FadeIn(item), run_time=0.7)
        self.play(Write(invariant), Indicate(output, color=COLOR_ENCRYPTION))
        self.play(LaggedStart(*(FadeIn(item) for item in unsupported), lag_ratio=0.12))
        self.play(Write(cross), Indicate(unsupported, color=RED_C))
        self.play(FadeOut(VGroup(subtitle, *items, arrows, invariant, unsupported, cross)))

    def show_scheme_and_depth(self, title):
        subtitle = Text("Choose a scheme for the value type", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.2)
        schemes = VGroup(
            self.card("BFV\nexact integers", BLUE_D, 2.45, 1.15, 22),
            self.card("BGV\nexact integers", BLUE_D, 2.45, 1.15, 22),
            self.card("CKKS\napproximate values", COLOR_ENCRYPTION, 2.65, 1.15, 22),
        ).arrange(RIGHT, buff=0.55).shift(UP * 0.55)
        real_vector = Text("[0.25, -1.40, 3.12, ...]", font_size=25, color=COLOR_PLAINTEXT)
        real_vector.next_to(schemes[2], DOWN, buff=0.38)

        depth_subtitle = Text("Then budget the multiplication depth", font_size=27, color=GREY_B)
        depth_subtitle.move_to(subtitle)
        levels = VGroup(
            *[
                RoundedRectangle(
                    width=4.6 - i * 0.55,
                    height=0.42,
                    corner_radius=0.05,
                    color=interpolate_color(GREEN_C, RED_C, i / 3),
                    fill_opacity=0.16,
                )
                for i in range(4)
            ]
        ).arrange(DOWN, buff=0.24)
        levels.move_to([-2.2, -0.25, 0])
        token = self.lock_icon(RED_C).scale(0.48).move_to(levels[0])
        multiply = Text("x", font_size=34, color=YELLOW_D)
        multiply.next_to(levels, LEFT, buff=0.35)
        add_note = Text("+ does not spend a level", font_size=21, color=GREEN_C)
        add_note.next_to(levels, DOWN, buff=0.28)
        bootstrap = BootstrappingGate("BOOTSTRAP").scale(0.5)
        bootstrap.move_to([3.65, -0.2, 0])
        expensive = Text("powerful, but expensive", font_size=20, color=RED_A)
        expensive.next_to(bootstrap, DOWN, buff=0.2)
        refresh_arrow = CurvedArrow(
            bootstrap.get_top(),
            levels[0].get_right(),
            angle=-TAU / 5,
            color=COLOR_ENCRYPTION,
        )

        self.play(FadeIn(subtitle), LaggedStart(*(FadeIn(scheme) for scheme in schemes), lag_ratio=0.18))
        self.play(Indicate(schemes[2], color=COLOR_ENCRYPTION), Write(real_vector))
        self.play(
            FadeOut(schemes),
            FadeOut(real_vector),
            Transform(subtitle, depth_subtitle),
            run_time=0.75,
        )
        self.play(
            LaggedStart(*(FadeIn(level) for level in levels), lag_ratio=0.12),
            FadeIn(token),
            FadeIn(multiply),
        )
        self.play(token.animate.move_to(levels[1]), Indicate(multiply), run_time=0.65)
        self.play(token.animate.move_to(levels[2]), Indicate(multiply), run_time=0.65)
        self.play(Write(add_note), run_time=0.55)
        self.play(
            FadeIn(bootstrap),
            Write(expensive),
            token.animate.move_to(bootstrap),
            run_time=0.8,
        )
        self.play(
            Create(refresh_arrow),
            token.animate.move_to(levels[0]),
            Flash(bootstrap, color=COLOR_ENCRYPTION),
            run_time=0.9,
        )
        self.play(
            FadeOut(
                VGroup(
                    subtitle,
                    levels,
                    token,
                    multiply,
                    add_note,
                    bootstrap,
                    expensive,
                    refresh_arrow,
                )
            )
        )

    def show_ring_picture(self, title):
        subtitle = Text("A vector is encoded before it becomes ciphertext", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.2)
        pipeline = VGroup(
            self.card("real vector", COLOR_PLAINTEXT, 1.8, 0.78, 20),
            self.card("encode", COLOR_ENCRYPTION, 1.5, 0.78, 20),
            self.card("ring polynomial", PURPLE_C, 2.1, 0.78, 20),
            self.card("+ small error", GREY_B, 1.8, 0.78, 19),
            self.card("ciphertext", COLOR_CIPHERTEXT, 1.8, 0.78, 20),
        ).arrange(RIGHT, buff=0.5).shift(DOWN * 0.1)
        pipeline_arrows = VGroup(
            *[self.arrow_between(pipeline[i], pipeline[i + 1]) for i in range(4)]
        )

        ring_subtitle = Text("The quotient keeps polynomial degree bounded", font_size=27, color=GREY_B)
        ring_subtitle.move_to(subtitle)
        ring = Circle(radius=1.45, color=COLOR_ENCRYPTION, fill_opacity=0.06)
        ring.move_to([-2.55, -0.35, 0])
        ring_formula = Text("R_q = Z_q[X] / (X^N + 1)", font_size=24, color=WHITE)
        ring_formula.next_to(ring, UP, buff=0.25)
        marker = Dot(ring.get_right(), radius=0.11, color=COLOR_PLAINTEXT)
        reduction = VGroup(
            self.card("X^(N+2)", COLOR_PLAINTEXT, 1.75, 0.68, 21),
            Text("wraps to", font_size=20, color=GREY_B),
            self.card("-X^2", COLOR_ENCRYPTION, 1.55, 0.68, 21),
        ).arrange(RIGHT, buff=0.16)
        reduction.move_to([2.55, 0.65, 0])
        operations = VGroup(
            self.card("polynomial +", COLOR_PLAINTEXT, 2.2, 0.7, 20),
            self.card("negacyclic x", COLOR_ENCRYPTION, 2.2, 0.7, 20),
        ).arrange(DOWN, buff=0.28)
        operations.move_to([2.55, -0.75, 0])
        budgets = VGroup(
            self.resource_bar("modulus", 0.86, COLOR_CIPHERTEXT),
            self.resource_bar("levels", 0.68, COLOR_ENCRYPTION),
            self.resource_bar("precision", 0.78, GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        budgets.scale(0.58).move_to([2.55, -2.0, 0])

        self.play(FadeIn(subtitle), FadeIn(pipeline[0]))
        for item, arrow in zip(pipeline[1:], pipeline_arrows):
            self.play(GrowArrow(arrow), FadeIn(item), run_time=0.55)
        self.play(Indicate(pipeline[2], color=PURPLE_C), Indicate(pipeline[4], color=COLOR_CIPHERTEXT))
        self.play(
            FadeOut(VGroup(pipeline, pipeline_arrows)),
            Transform(subtitle, ring_subtitle),
            run_time=0.75,
        )
        self.play(Create(ring), Write(ring_formula), FadeIn(marker))
        self.play(MoveAlongPath(marker, ring), run_time=1.1, rate_func=linear)
        self.play(FadeIn(reduction), marker.animate.set_color(COLOR_ENCRYPTION))
        self.play(FadeIn(operations), Indicate(operations, color=COLOR_ENCRYPTION))
        self.play(LaggedStart(*(FadeIn(bar) for bar in budgets), lag_ratio=0.15))
        for bar in budgets:
            self.play(bar[1][1].animate.scale(0.72, about_edge=LEFT), run_time=0.45)
        self.play(
            FadeOut(
                VGroup(
                    subtitle,
                    ring,
                    ring_formula,
                    marker,
                    reduction,
                    operations,
                    budgets,
                )
            )
        )

    @staticmethod
    def resource_bar(label, level, color):
        label_mob = Text(label, font_size=20, color=GREY_B)
        track = Rectangle(width=3.2, height=0.2, color=GREY_D, fill_opacity=0.15)
        fill = Rectangle(
            width=3.2 * level,
            height=0.2,
            color=color,
            fill_color=color,
            fill_opacity=0.72,
            stroke_width=0,
        )
        fill.align_to(track, LEFT)
        return VGroup(label_mob, VGroup(track, fill)).arrange(RIGHT, buff=0.2)

    @staticmethod
    def privacy_beats():
        return [
            ("The outsourced-compute dilemma", ["Cloud hardware is useful but may not be trusted.", "Ordinary encryption protects storage and transport.", "Computation normally requires exposing plaintext."], "HE targets the missing state: data in use."),
            ("Define the actors", ["The client owns private inputs and the secret key.", "The server receives ciphertext and an evaluation program.", "Only the client is allowed to reveal the result."], "Security begins with a precise trust boundary."),
            ("What transport encryption cannot solve", ["TLS protects bytes while they cross the network.", "The server endpoint still sees decrypted values.", "A compromised service can inspect inputs and intermediates."], "A secure channel is not encrypted computation."),
            ("The privacy promise", ["The server manipulates opaque algebraic objects.", "Intermediate activations remain encrypted.", "The response returns as another ciphertext."], "The secret key never needs to reach the cloud."),
            ("The price of stronger privacy", ["Ciphertexts are much larger than plaintext values.", "Supported operations are algebraically constrained.", "Parameter choices control precision, security, and speed."], "FHE is a systems tradeoff, not free encryption."),
        ]

    @staticmethod
    def homomorphism_beats():
        return [
            ("Correctness is the central invariant", ["Encrypt x before outsourcing the computation.", "Evaluate f directly over the ciphertext.", "Decrypt to recover f(x), within scheme error."], "The encrypted path must agree with the clear path."),
            ("Partial, somewhat, and fully homomorphic", ["Early schemes supported one operation family.", "Leveled HE supports circuits up to a planned depth.", "Bootstrapping can refresh a ciphertext for longer work."], "The circuit budget determines what can be evaluated."),
            ("Circuits replace ordinary programs", ["Addition and multiplication form arithmetic circuits.", "Comparisons and branches are not native CKKS operations.", "Algorithms must be rewritten into compatible algebra."], "Program design moves from control flow to polynomials."),
            ("Public models, private data", ["Model weights may remain plaintext on the server.", "Ciphertext-plaintext products are often cheaper.", "Inputs and outputs stay encrypted for the client."], "This is the common private-inference setting."),
            ("Why Act 1 focuses on CKKS", ["Computer vision uses real-valued tensors.", "Approximate arithmetic tolerates controlled numeric error.", "SIMD packing amortizes work across many values."], "CKKS matches numerical workloads better than exact schemes."),
        ]

    @staticmethod
    def ring_beats():
        return [
            ("Why polynomials appear", ["SEAL stores messages and ciphertexts in quotient rings.", "Polynomial addition and multiplication are efficient.", "The modulus makes coefficients finite machine objects."], "Ring arithmetic is the language of the scheme."),
            ("The cyclotomic quotient", ["A common ring is Z_q[X] modulo X^N plus 1.", "The polynomial degree N is a power of two.", "Negacyclic multiplication wraps high powers with a sign."], "The quotient keeps every result at bounded degree."),
            ("RLWE intuition", ["A secret polynomial is sampled with small coefficients.", "Encryption mixes the secret with random public data.", "A small error term hides exact algebraic relationships."], "Recovering the secret resembles a hard noisy lattice problem."),
            ("Security error and numerical budget", ["Fresh ciphertext needs randomness and error for RLWE security.", "CKKS also tracks scale, levels, and approximation error.", "Correct decoding requires all resources to remain controlled."], "CKKS capacity is a combined modulus, level, and precision budget."),
            ("Bridge to CKKS", ["CKKS adds an approximate encoder above ring arithmetic.", "Vectors are mapped into polynomial coefficients indirectly.", "Scale tracks meaningful fractional precision."], "The next scene follows values into CKKS slots."),
        ]
