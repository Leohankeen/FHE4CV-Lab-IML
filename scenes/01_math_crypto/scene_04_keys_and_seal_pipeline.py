import os
import sys

import numpy as np
from manim import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene, scene_time


class KeysAndSEALPipeline(StoryboardScene):
    """15-minute visual lesson on SEAL keys, objects, and deployment."""

    MOTION_TIME = 1.15
    CONTENT_TOP = 2.15
    CONTENT_BOTTOM = -2.6
    KEY_DURATIONS = (56.75, 60.09, 58.71, 59.17, 61.48)
    OBJECT_DURATIONS = (56.95, 61.57, 59.72, 60.65, 61.11)
    LIFECYCLE_DURATIONS = (59.72, 59.26, 57.88, 61.57, 61.57)

    @staticmethod
    def fit_text(text, max_width, max_height=None):
        if text.width > max_width:
            text.scale_to_fit_width(max_width)
        if max_height is not None and text.height > max_height:
            text.scale_to_fit_height(max_height)
        return text

    @classmethod
    def motion_step(cls, duration, actions):
        return min(cls.MOTION_TIME, max(0.82, duration / max(1, actions * 10)))

    def card(self, label, color, width=2.0, height=0.74, font_size=21):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.09,
            color=color,
            fill_color=color,
            fill_opacity=0.13,
        )
        text = Text(label, font_size=font_size, color=WHITE, line_spacing=0.8)
        self.fit_text(text, width - 0.22, height - 0.18)
        text.move_to(box)
        return VGroup(box, text)

    def slot_row(self, values, color=BLUE_C, cell_size=0.64):
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

    def lock_icon(self, color=GREEN_C, scale=1.0):
        body = RoundedRectangle(
            width=0.62,
            height=0.42,
            corner_radius=0.07,
            color=color,
            fill_color=color,
            fill_opacity=0.08,
            stroke_width=4,
        ).shift(DOWN * 0.15)
        shackle = ParametricFunction(
            lambda t: np.array([0.22 * np.cos(t), 0.22 * np.sin(t) + 0.08, 0]),
            t_range=[0, PI],
            color=color,
            stroke_width=4,
        )
        legs = VGroup(
            Line(LEFT * 0.22 + UP * 0.08, LEFT * 0.22 + DOWN * 0.02, color=color, stroke_width=4),
            Line(RIGHT * 0.22 + UP * 0.08, RIGHT * 0.22 + DOWN * 0.02, color=color, stroke_width=4),
        )
        return VGroup(body, shackle, legs).scale(scale)

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
            "keys"
            if "Key Capabilities" in section_label
            else "objects"
            if "SEAL Objects" in section_label
            else "lifecycle"
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
        title = Text("Scene 04 - Keys and the SEAL Workflow", font_size=40, color=WHITE)
        subtitle = Text("Provision capabilities, run the circuit, verify the result", font_size=22, color=GREY_B)
        group = VGroup(act, title, subtitle).arrange(DOWN, buff=0.3)
        self.fit_text(group, 11.4)
        self.play(FadeIn(act, shift=DOWN * 0.12), Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(group), run_time=1.0)

    # ------------------------------------------------------------------
    # 4.1 Key capabilities
    # ------------------------------------------------------------------

    def demo_keys_1(self, accent, duration):
        step = self.motion_step(duration, 9)
        generator = Circle(radius=0.82, color=YELLOW_D, fill_color=YELLOW_D, fill_opacity=0.08).move_to(LEFT * 4.25)
        generator_label = Text("KeyGenerator", font_size=20, color=YELLOW_D)
        self.fit_text(generator_label, 1.35, 0.42)
        generator_label.move_to(generator)
        samples = VGroup(*[Dot(radius=0.05, color=GREY_B) for _ in range(9)]).arrange(RIGHT, buff=0.11)
        samples.next_to(generator, UP, buff=0.28)
        secret = self.card("SecretKey s(X)", GREEN_C, 1.85, 0.66, 18).move_to(LEFT * 1.45 + UP * 0.75)
        arrow = Arrow(generator.get_right(), secret.get_left(), buff=0.16, color=GREEN_C)
        vault = RoundedRectangle(
            width=3.15,
            height=1.5,
            corner_radius=0.15,
            color=GREEN_C,
            fill_color=GREEN_C,
            fill_opacity=0.05,
        ).move_to(RIGHT * 2.55 + DOWN * 0.95)
        vault_label = Text("trusted client", font_size=19, color=GREEN_C).next_to(vault, DOWN, buff=0.15)
        secret_target = vault.get_center() + LEFT * 0.48
        lock = self.lock_icon(GREEN_C, 0.82).move_to(vault.get_center() + RIGHT * 0.92)
        ciphertext = self.card("ciphertext", RED_C, 1.55, 0.62, 18).move_to(LEFT * 1.25 + DOWN * 0.95)
        decrypt_arrow = Arrow(ciphertext.get_right(), vault.get_left(), buff=0.16, color=GREEN_C)
        plaintext = self.card("plaintext", BLUE_C, 1.55, 0.62, 18).move_to(RIGHT * 5.05 + DOWN * 0.95)
        output_arrow = Arrow(vault.get_right(), plaintext.get_left(), buff=0.16, color=BLUE_C)

        self.play(FadeIn(generator), FadeIn(generator_label), run_time=step)
        self.play(LaggedStart(*(FadeIn(dot) for dot in samples), lag_ratio=0.08), run_time=step)
        self.play(GrowArrow(arrow), FadeIn(secret, shift=LEFT * 0.12), run_time=step)
        self.play(FadeIn(vault), FadeIn(vault_label), FadeIn(lock), run_time=step)
        self.play(FadeOut(arrow), secret.animate.move_to(secret_target), run_time=step)
        self.play(FadeIn(ciphertext), GrowArrow(decrypt_arrow), run_time=step)
        self.play(GrowArrow(output_arrow), FadeIn(plaintext, shift=LEFT * 0.1), run_time=step)
        self.play(Indicate(lock, color=GREEN_C), run_time=step)
        self.play(Circumscribe(plaintext, color=BLUE_C), run_time=step)
        return VGroup(
            generator,
            generator_label,
            samples,
            secret,
            arrow,
            vault,
            vault_label,
            lock,
            ciphertext,
            decrypt_arrow,
            plaintext,
            output_arrow,
        )

    def demo_keys_2(self, accent, duration):
        step = self.motion_step(duration, 9)
        client = RoundedRectangle(width=2.8, height=2.5, corner_radius=0.15, color=GREEN_C, fill_opacity=0.04).move_to(LEFT * 4.5)
        producer = RoundedRectangle(width=4.7, height=2.5, corner_radius=0.15, color=BLUE_C, fill_opacity=0.04).move_to(RIGHT * 3.35)
        client_label = Text("key owner", font_size=20, color=GREEN_C).next_to(client, UP, buff=0.18)
        producer_label = Text("data producer", font_size=20, color=BLUE_C).next_to(producer, UP, buff=0.18)
        public = self.card("PublicKey", YELLOW_D, 1.7, 0.64, 19).move_to(client)
        share_arrow = Arrow(client.get_right(), producer.get_left(), buff=0.2, color=YELLOW_D)
        shared = public.copy().scale(0.86).move_to(producer.get_top() + DOWN * 0.48)
        plain = self.card("vector", BLUE_C, 1.15, 0.54, 17).move_to(RIGHT * 1.8 + DOWN * 0.55)
        encrypt = Circle(radius=0.38, color=YELLOW_D, fill_opacity=0.08).move_to(RIGHT * 3.2 + DOWN * 0.55)
        encrypt_label = Text("Enc", font_size=22, color=YELLOW_D).move_to(encrypt)
        ct1 = self.card("ciphertext A", RED_C, 1.35, 0.5, 14).move_to(RIGHT * 4.95 + DOWN * 0.2)
        ct2 = self.card("ciphertext B", RED_C, 1.35, 0.5, 14).move_to(RIGHT * 4.95 + DOWN * 0.92)
        path1 = Arrow(plain.get_right(), encrypt.get_left(), buff=0.1, color=BLUE_C)
        path2 = Arrow(encrypt.get_right(), ct1.get_left(), buff=0.1, color=RED_C)

        self.play(FadeIn(client), FadeIn(producer), FadeIn(client_label), FadeIn(producer_label), run_time=step)
        self.play(FadeIn(public), GrowArrow(share_arrow), run_time=step)
        self.play(TransformFromCopy(public, shared), run_time=step)
        self.play(FadeIn(plain), FadeIn(encrypt), FadeIn(encrypt_label), GrowArrow(path1), run_time=step)
        self.play(GrowArrow(path2), FadeIn(ct1), run_time=step)
        self.play(TransformFromCopy(ct1, ct2), run_time=step)
        self.play(Indicate(VGroup(ct1, ct2), color=RED_C), run_time=step)
        self.play(Indicate(shared, color=YELLOW_D), run_time=step)
        self.play(Circumscribe(plain, color=BLUE_C), run_time=step)
        return VGroup(
            client,
            producer,
            client_label,
            producer_label,
            public,
            share_arrow,
            shared,
            plain,
            encrypt,
            encrypt_label,
            ct1,
            ct2,
            path1,
            path2,
        )

    def demo_keys_3(self, accent, duration):
        step = self.motion_step(duration, 8)
        enlarged = VGroup(
            self.card("e0", RED_C, 1.1, 0.65, 21),
            self.card("e1", RED_C, 1.1, 0.65, 21),
            self.card("e2", RED_C, 1.1, 0.65, 21),
        ).arrange(RIGHT, buff=0.16).move_to(LEFT * 4.0 + UP * 0.45)
        switch = self.card("key switch", YELLOW_D, 2.0, 1.0, 21).move_to(ORIGIN + UP * 0.45)
        relin = self.card("RelinKeys", GREEN_C, 1.9, 0.68, 20).move_to(DOWN * 1.25)
        reduced = VGroup(
            self.card("r0", BLUE_C, 1.2, 0.68, 21),
            self.card("r1", BLUE_C, 1.2, 0.68, 21),
        ).arrange(RIGHT, buff=0.18).move_to(RIGHT * 3.8 + UP * 0.45)
        arrows = VGroup(
            Arrow(enlarged.get_right(), switch.get_left(), buff=0.15, color=RED_C),
            Arrow(relin.get_top(), switch.get_bottom(), buff=0.15, color=GREEN_C),
            Arrow(switch.get_right(), reduced.get_left(), buff=0.15, color=BLUE_C),
        )
        lock = self.lock_icon(GREEN_C, 0.85).move_to(RIGHT * 3.0 + DOWN * 1.15)
        note = Text("no plaintext revealed", font_size=18, color=GREEN_C).next_to(lock, RIGHT, buff=0.2)

        self.play(FadeIn(enlarged), run_time=step)
        self.play(FadeIn(switch), GrowArrow(arrows[0]), run_time=step)
        self.play(FadeIn(relin), GrowArrow(arrows[1]), run_time=step)
        self.play(enlarged[2].animate.move_to(switch), run_time=step)
        self.play(FadeOut(enlarged[2]), Flash(switch, color=GREEN_C), run_time=step)
        self.play(GrowArrow(arrows[2]), FadeIn(reduced), run_time=step)
        self.play(FadeIn(lock), FadeIn(note), run_time=step)
        self.play(Circumscribe(reduced, color=BLUE_C), run_time=step)
        return VGroup(enlarged, switch, relin, reduced, arrows, lock, note)

    def demo_keys_4(self, accent, duration):
        step = self.motion_step(duration, 9)
        source = self.slot_row([1, 2, 3, 4], RED_C, 0.68).move_to(LEFT * 4.0 + UP * 0.65)
        rotate_one = self.slot_row([4, 1, 2, 3], BLUE_C, 0.68).move_to(RIGHT * 3.9 + UP * 0.85)
        rotate_two = self.slot_row([3, 4, 1, 2], PURPLE_C, 0.68).move_to(RIGHT * 3.9 + DOWN * 0.85)
        arc_one = CurvedArrow(source.get_right(), rotate_one.get_left(), angle=-PI / 3, color=BLUE_C)
        arc_two = CurvedArrow(source.get_bottom(), rotate_two.get_left(), angle=PI / 3, color=PURPLE_C)
        keys = VGroup(
            self.card("Galois key +1", BLUE_C, 1.9, 0.58, 17).move_to(LEFT * 0.4 + UP * 0.25),
            self.card("Galois key +2", PURPLE_C, 1.9, 0.58, 17).move_to(LEFT * 1.0 + DOWN * 1.55),
        )

        self.play(FadeIn(source), run_time=step)
        self.play(FadeIn(keys[0]), Create(arc_one), run_time=step)
        self.play(TransformFromCopy(source, rotate_one), run_time=step)
        self.play(FadeIn(keys[1]), Create(arc_two), run_time=step)
        self.play(TransformFromCopy(source, rotate_two), run_time=step)
        self.play(Indicate(rotate_one, color=BLUE_C), run_time=step)
        self.play(Indicate(rotate_two, color=PURPLE_C), run_time=step)
        self.play(Circumscribe(keys, color=GREEN_C), run_time=step)
        self.play(Indicate(source, color=RED_C), run_time=step)
        return VGroup(source, rotate_one, rotate_two, arc_one, arc_two, keys)

    def demo_keys_5(self, accent, duration):
        step = self.motion_step(duration, 9)
        boundary = DashedLine(UP * 2.0, DOWN * 1.15, color=GREY_D)
        client_label = Text("client", font_size=21, color=GREEN_C).move_to(LEFT * 5.0 + UP * 1.82)
        server_label = Text("server", font_size=21, color=BLUE_C).move_to(RIGHT * 4.5 + UP * 1.75)
        secret_home = LEFT * 3.8 + UP * 1.5
        secret = self.card("SecretKey", GREEN_C, 1.7, 0.58, 18).move_to(secret_home)
        public = self.card("PublicKey", YELLOW_D, 1.7, 0.58, 18)
        relin = self.card("RelinKeys", RED_C, 1.7, 0.58, 18)
        galois = self.card("Galois +1,+2", PURPLE_C, 1.7, 0.58, 17)
        source_keys = VGroup(public, relin, galois).arrange(DOWN, buff=0.16).move_to(LEFT * 3.8 + DOWN * 0.1)
        allowed = source_keys.copy().move_to(RIGHT * 3.8)
        arrows = VGroup(
            Arrow(public.get_right(), allowed[0].get_left(), buff=0.18, color=YELLOW_D),
            Arrow(relin.get_right(), allowed[1].get_left(), buff=0.18, color=RED_C),
            Arrow(galois.get_right(), allowed[2].get_left(), buff=0.18, color=PURPLE_C),
        )
        blocked = Cross(secret.copy(), stroke_color=RED_C, stroke_width=5).move_to(UP * 1.5)
        all_bar = Rectangle(width=3.4, height=0.18, color=RED_C, fill_color=RED_C, fill_opacity=0.65)
        needed_bar = Rectangle(width=1.45, height=0.18, color=GREEN_C, fill_color=GREEN_C, fill_opacity=0.75)
        bars = VGroup(
            VGroup(Text("all rotations", font_size=17, color=GREY_B), all_bar).arrange(RIGHT, buff=0.2),
            VGroup(Text("required only", font_size=17, color=GREY_B), needed_bar).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 1.72)

        self.play(FadeIn(boundary), FadeIn(client_label), FadeIn(server_label), run_time=step)
        self.play(FadeIn(secret), FadeIn(source_keys), run_time=step)
        self.play(secret.animate.move_to(UP * 1.5), FadeIn(blocked), run_time=step)
        self.play(secret.animate.move_to(secret_home), run_time=step)
        self.play(GrowArrow(arrows[0]), TransformFromCopy(public, allowed[0]), run_time=step)
        self.play(GrowArrow(arrows[1]), TransformFromCopy(relin, allowed[1]), run_time=step)
        self.play(GrowArrow(arrows[2]), TransformFromCopy(galois, allowed[2]), run_time=step)
        self.play(FadeIn(bars[0]), run_time=step)
        self.play(FadeIn(bars[1]), run_time=step)
        self.play(Indicate(bars[1], color=GREEN_C), run_time=step)
        return VGroup(
            boundary,
            client_label,
            server_label,
            secret,
            source_keys,
            allowed,
            arrows,
            blocked,
            bars,
        )

    # ------------------------------------------------------------------
    # 4.2 Core SEAL objects
    # ------------------------------------------------------------------

    def demo_objects_1(self, accent, duration):
        step = self.motion_step(duration, 9)
        scheme = self.card("scheme: CKKS", YELLOW_D, 2.1, 0.68, 19).move_to(LEFT * 4.4 + UP * 0.95)
        degree = self.card("N = 8192", BLUE_C, 2.1, 0.68, 19).move_to(LEFT * 4.4)
        chain = VGroup(*[self.card(bits, PURPLE_C, 0.72, 0.5, 16) for bits in ("60", "40", "40", "60")]).arrange(RIGHT, buff=0.08)
        chain.move_to(LEFT * 4.4 + DOWN * 0.95)
        params = RoundedRectangle(width=3.1, height=3.0, corner_radius=0.15, color=YELLOW_D, fill_opacity=0.04).move_to(LEFT * 4.4)
        params_label = Text("EncryptionParameters", font_size=19, color=YELLOW_D).next_to(params, UP, buff=0.17)
        context = Circle(radius=1.15, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.06).move_to(ORIGIN)
        context_label = Text("SEALContext", font_size=21, color=BLUE_C).move_to(context)
        arrow = Arrow(params.get_right(), context.get_left(), buff=0.18, color=accent)
        checks = VGroup(
            Text("scheme valid", font_size=18, color=GREEN_C),
            Text("security valid", font_size=18, color=GREEN_C),
            Text("chain valid", font_size=18, color=GREEN_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 3.65)
        marks = VGroup(*[Text("PASS", font_size=18, color=GREEN_C) for _ in range(3)])
        for mark, check in zip(marks, checks):
            mark.next_to(check, RIGHT, buff=0.35)

        self.play(FadeIn(params), FadeIn(params_label), run_time=step)
        self.play(FadeIn(scheme), FadeIn(degree), FadeIn(chain), run_time=step)
        self.play(GrowArrow(arrow), FadeIn(context), FadeIn(context_label), run_time=step)
        for check, mark in zip(checks, marks):
            self.play(FadeIn(check, shift=LEFT * 0.1), FadeIn(mark), run_time=step)
        self.play(Circumscribe(context, color=BLUE_C), run_time=step)
        self.play(Indicate(marks, color=GREEN_C), run_time=step)
        return VGroup(params, params_label, scheme, degree, chain, context, context_label, arrow, checks, marks)

    def demo_objects_2(self, accent, duration):
        step = self.motion_step(duration, 8)
        context = self.card("SEALContext", BLUE_C, 2.2, 0.72, 20).move_to(LEFT * 4.6 + UP * 0.85)
        levels = VGroup()
        colors = (BLUE_C, PURPLE_C, YELLOW_D, GREEN_C)
        for index, color in enumerate(colors):
            blocks = VGroup(
                *[
                    Rectangle(width=0.58, height=0.28, color=color, fill_color=color, fill_opacity=0.45)
                    for _ in range(4 - index)
                ]
            ).arrange(RIGHT, buff=0.08)
            label = Text(f"level {3-index}", font_size=17, color=GREY_B)
            row = VGroup(label, blocks).arrange(RIGHT, buff=0.28)
            levels.add(row)
        levels.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(LEFT * 1.2 + DOWN * 0.2)
        arrow = Arrow(context.get_right(), levels.get_left(), buff=0.2, color=accent)
        ids = VGroup(
            *[self.card(f"parms ID {index}", colors[index], 1.8, 0.52, 16) for index in range(4)]
        ).arrange(DOWN, buff=0.27).move_to(RIGHT * 3.85 + DOWN * 0.2)
        id_arrows = VGroup(
            *[
                Arrow(level.get_right(), identity.get_left(), buff=0.18, color=colors[index])
                for index, (level, identity) in enumerate(zip(levels, ids))
            ]
        )
        token = Dot(levels[0].get_center(), color=WHITE, radius=0.08)

        self.play(FadeIn(context), GrowArrow(arrow), run_time=step)
        self.play(LaggedStart(*(FadeIn(level, shift=DOWN * 0.08) for level in levels), lag_ratio=0.12), run_time=step)
        self.play(FadeIn(token), run_time=step)
        for index, (level, identity, id_arrow) in enumerate(zip(levels, ids, id_arrows)):
            self.play(token.animate.move_to(level.get_center()), GrowArrow(id_arrow), FadeIn(identity), run_time=step)
        self.play(Indicate(ids, color=accent), run_time=step)
        self.play(Circumscribe(levels, color=BLUE_C), run_time=step)
        return VGroup(context, levels, arrow, ids, id_arrows, token)

    def demo_objects_3(self, accent, duration):
        step = self.motion_step(duration, 9)
        generator = Circle(radius=0.8, color=YELLOW_D, fill_opacity=0.08).move_to(LEFT * 4.6)
        generator_label = Text("KeyGenerator", font_size=18, color=YELLOW_D)
        self.fit_text(generator_label, 1.22, 0.34)
        generator_label.move_to(generator)
        secret = self.card("SecretKey", GREEN_C, 1.7, 0.62, 19).move_to(LEFT * 1.7 + UP * 1.25)
        public = self.card("PublicKey", BLUE_C, 1.7, 0.62, 19).move_to(LEFT * 1.7 + UP * 0.25)
        relin = self.card("RelinKeys", RED_C, 1.7, 0.62, 19).move_to(LEFT * 1.7 + DOWN * 0.75)
        requested = VGroup(
            self.card("rotate +1", PURPLE_C, 1.5, 0.56, 17),
            self.card("rotate +2", PURPLE_C, 1.5, 0.56, 17),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.9 + DOWN * 0.3)
        galois = self.card("GaloisKeys", PURPLE_C, 1.9, 0.68, 19).move_to(RIGHT * 0.75 + DOWN * 0.3)
        branches = VGroup(
            Arrow(generator.get_right(), secret.get_left(), buff=0.15, color=GREEN_C),
            Arrow(generator.get_right(), public.get_left(), buff=0.15, color=BLUE_C),
            Arrow(generator.get_right(), relin.get_left(), buff=0.15, color=RED_C),
            Arrow(generator.get_right(), galois.get_left(), buff=0.15, color=PURPLE_C),
        )
        request_arrow = Arrow(galois.get_right(), requested.get_left(), buff=0.15, color=PURPLE_C)

        self.play(FadeIn(generator), FadeIn(generator_label), run_time=step)
        for arrow, key in zip(branches[:3], (secret, public, relin)):
            self.play(GrowArrow(arrow), FadeIn(key), run_time=step)
        self.play(GrowArrow(branches[3]), FadeIn(galois), run_time=step)
        self.play(GrowArrow(request_arrow), run_time=step)
        self.play(LaggedStart(*(FadeIn(item, shift=LEFT * 0.1) for item in requested), lag_ratio=0.18), run_time=step)
        self.play(Indicate(requested, color=PURPLE_C), run_time=step)
        self.play(Circumscribe(secret, color=GREEN_C), run_time=step)
        self.play(Indicate(VGroup(public, relin, galois), color=accent), run_time=step)
        return VGroup(generator, generator_label, secret, public, relin, galois, requested, branches, request_arrow)

    def demo_objects_4(self, accent, duration):
        step = self.motion_step(duration, 9)
        divider = DashedLine(UP * 2.0, DOWN * 2.0, color=GREY_D).shift(RIGHT * 2.45)
        client_label = Text("trusted client", font_size=20, color=GREEN_C).move_to(LEFT * 4.7 + UP * 1.75)
        cloud_label = Text("cloud", font_size=20, color=PURPLE_C).move_to(RIGHT * 4.6 + UP * 1.75)
        vector = self.slot_row(["x0", "x1", "x2", "x3"], BLUE_C, 0.52).move_to(LEFT * 5.45 + UP * 0.45)
        encoder = self.card("CKKSEncoder", YELLOW_D, 1.9, 0.68, 18).move_to(LEFT * 2.9 + UP * 0.45)
        plain = self.card("Plaintext", BLUE_C, 1.55, 0.68, 19).move_to(LEFT * 0.8 + UP * 0.45)
        encryptor = self.card("Encryptor", YELLOW_D, 1.55, 0.68, 19).move_to(LEFT * 0.8 + DOWN * 0.85)
        cipher = self.card("Ciphertext", RED_C, 1.65, 0.68, 19).move_to(RIGHT * 1.25 + DOWN * 0.85)
        evaluator = self.card("Evaluator", PURPLE_C, 1.8, 0.78, 20).move_to(RIGHT * 4.2 + UP * 0.3)
        secret = self.card("SecretKey", GREEN_C, 1.65, 0.62, 18).move_to(LEFT * 5.0 + DOWN * 1.45)
        paths = VGroup(
            Arrow(vector.get_right(), encoder.get_left(), buff=0.08, color=BLUE_C),
            Arrow(encoder.get_right(), plain.get_left(), buff=0.12, color=YELLOW_D),
            Arrow(plain.get_bottom(), encryptor.get_top(), buff=0.12, color=YELLOW_D),
            Arrow(encryptor.get_right(), cipher.get_left(), buff=0.12, color=RED_C),
            Arrow(cipher.get_right(), evaluator.get_left(), buff=0.18, color=PURPLE_C),
        )
        operations = VGroup(
            *[self.card(op, PURPLE_C, 1.0, 0.48, 15) for op in ("add", "multiply", "rotate")]
        ).arrange(RIGHT, buff=0.12).next_to(evaluator, DOWN, buff=0.35)

        self.play(FadeIn(divider), FadeIn(client_label), FadeIn(cloud_label), FadeIn(secret), run_time=step)
        self.play(FadeIn(vector), GrowArrow(paths[0]), FadeIn(encoder), run_time=step)
        self.play(GrowArrow(paths[1]), FadeIn(plain), run_time=step)
        self.play(GrowArrow(paths[2]), FadeIn(encryptor), run_time=step)
        self.play(GrowArrow(paths[3]), FadeIn(cipher), run_time=step)
        self.play(GrowArrow(paths[4]), FadeIn(evaluator), run_time=step)
        self.play(LaggedStart(*(FadeIn(op) for op in operations), lag_ratio=0.14), run_time=step)
        self.play(Indicate(secret, color=GREEN_C), run_time=step)
        self.play(Circumscribe(VGroup(evaluator, operations), color=PURPLE_C), run_time=step)
        return VGroup(
            divider,
            client_label,
            cloud_label,
            vector,
            encoder,
            plain,
            encryptor,
            cipher,
            evaluator,
            secret,
            paths,
            operations,
        )

    def demo_objects_5(self, accent, duration):
        step = self.motion_step(duration, 9)
        cloud = RoundedRectangle(width=6.25, height=3.0, corner_radius=0.2, color=PURPLE_C, fill_opacity=0.04).move_to(LEFT * 2.65)
        cloud_label = Text("untrusted server", font_size=20, color=PURPLE_C).next_to(cloud, UP, buff=0.17)
        evaluator = self.card("Evaluator", PURPLE_C, 1.8, 0.72, 20).move_to(cloud.get_top() + DOWN * 0.55)
        input_ct = self.card("ciphertext", RED_C, 1.25, 0.56, 15).move_to(LEFT * 5.0)
        ops = VGroup(
            *[Circle(radius=0.31, color=YELLOW_D, fill_opacity=0.08) for _ in range(3)]
        ).arrange(RIGHT, buff=0.55).move_to(LEFT * 2.55)
        op_labels = VGroup(*[Text(op, font_size=15, color=YELLOW_D).move_to(node) for op, node in zip(("x", "R", "+"), ops)])
        output_ct = self.card("result", RED_C, 1.15, 0.56, 16).move_to(LEFT * 0.3)
        paths = VGroup(
            Arrow(input_ct.get_right(), ops[0].get_left(), buff=0.1, color=RED_C),
            Arrow(ops[0].get_right(), ops[1].get_left(), buff=0.1, color=GREY_C),
            Arrow(ops[1].get_right(), ops[2].get_left(), buff=0.1, color=GREY_C),
            Arrow(ops[2].get_right(), output_ct.get_left(), buff=0.1, color=RED_C),
        )
        keys = VGroup(
            self.card("RelinKeys", GREEN_C, 1.55, 0.58, 17),
            self.card("GaloisKeys", BLUE_C, 1.55, 0.58, 17),
        ).arrange(RIGHT, buff=0.34).move_to(cloud.get_bottom() + UP * 0.52)
        client = RoundedRectangle(width=2.8, height=2.2, corner_radius=0.16, color=GREEN_C, fill_opacity=0.04).move_to(RIGHT * 4.65)
        client_label = Text("trusted client", font_size=20, color=GREEN_C).next_to(client, UP, buff=0.17)
        secret = self.card("SecretKey", GREEN_C, 1.65, 0.62, 18).move_to(client.get_center() + UP * 0.22)
        blocked = DashedLine(UP * 1.35, DOWN * 1.35, color=GREY_D).shift(RIGHT * 1.45)
        no_secret = Text("never exported", font_size=16, color=GREEN_C).next_to(secret, DOWN, buff=0.22)

        self.play(FadeIn(cloud), FadeIn(cloud_label), FadeIn(client), FadeIn(client_label), run_time=step)
        self.play(FadeIn(evaluator), FadeIn(input_ct), FadeIn(secret), run_time=step)
        self.play(FadeIn(keys), run_time=step)
        for path, node, label in zip(paths[:3], ops, op_labels):
            self.play(GrowArrow(path), FadeIn(node), FadeIn(label), run_time=step)
        self.play(GrowArrow(paths[3]), FadeIn(output_ct), run_time=step)
        self.play(Create(blocked), FadeIn(no_secret), run_time=step)
        self.play(Indicate(secret, color=GREEN_C), run_time=step)
        self.play(Circumscribe(output_ct, color=RED_C), run_time=step)
        return VGroup(
            cloud,
            cloud_label,
            evaluator,
            input_ct,
            ops,
            op_labels,
            output_ct,
            paths,
            keys,
            client,
            client_label,
            secret,
            blocked,
            no_secret,
        )

    # ------------------------------------------------------------------
    # 4.3 End-to-end lifecycle
    # ------------------------------------------------------------------

    def demo_lifecycle_1(self, accent, duration):
        step = self.motion_step(duration, 9)
        input_node = self.card("packed input", BLUE_C, 1.7, 0.62, 18).move_to(LEFT * 5.0 + UP * 0.55)
        multiplications = VGroup(
            *[Circle(radius=0.38, color=RED_C, fill_opacity=0.08) for _ in range(3)]
        ).arrange(RIGHT, buff=1.15).move_to(LEFT * 0.7 + UP * 0.55)
        labels = VGroup(*[Text("x", font_size=24, color=RED_C).move_to(node) for node in multiplications])
        output = self.card("output", GREEN_C, 1.45, 0.62, 18).move_to(RIGHT * 5.0 + UP * 0.55)
        nodes = VGroup(input_node, *multiplications, output)
        arrows = VGroup(
            *[
                Arrow(nodes[index].get_right(), nodes[index + 1].get_left(), buff=0.12, color=GREY_C)
                for index in range(len(nodes) - 1)
            ]
        )
        rotation = CurvedArrow(
            multiplications[1].get_bottom() + DOWN * 0.55,
            multiplications[2].get_bottom() + DOWN * 0.55,
            angle=PI / 2,
            color=PURPLE_C,
        )
        rotation_label = Text("rotate +1, +2", font_size=16, color=PURPLE_C).next_to(rotation, DOWN, buff=0.1)
        counts = VGroup(
            self.card("depth = 3", RED_C, 1.65, 0.56, 17),
            self.card("rotations = 2", PURPLE_C, 1.9, 0.56, 17),
            self.card("slots = 4096", BLUE_C, 1.85, 0.56, 17),
        ).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.55)

        self.play(FadeIn(input_node), run_time=step)
        for arrow, node, label in zip(arrows[:3], multiplications, labels):
            self.play(GrowArrow(arrow), FadeIn(node), FadeIn(label), run_time=step)
        self.play(GrowArrow(arrows[-1]), FadeIn(output), run_time=step)
        self.play(Create(rotation), FadeIn(rotation_label), run_time=step)
        self.play(LaggedStart(*(FadeIn(count, shift=UP * 0.08) for count in counts), lag_ratio=0.14), run_time=step)
        self.play(Indicate(counts[0], color=RED_C), run_time=step)
        self.play(Indicate(counts[1], color=PURPLE_C), run_time=step)
        self.play(Circumscribe(VGroup(nodes, arrows), color=accent), run_time=step)
        return VGroup(input_node, multiplications, labels, output, arrows, rotation, rotation_label, counts)

    def demo_lifecycle_2(self, accent, duration):
        step = self.motion_step(duration, 9)
        requirements = VGroup(
            self.card("depth 3", RED_C, 1.55, 0.58, 17),
            self.card("4096 slots", BLUE_C, 1.7, 0.58, 17),
            self.card("precision 40 bits", YELLOW_D, 2.0, 0.58, 17),
        ).arrange(DOWN, buff=0.24).move_to(LEFT * 4.2)
        config = VGroup(
            self.card("N = 8192", BLUE_C, 2.1, 0.62, 18),
            VGroup(*[self.card(bits, PURPLE_C, 0.68, 0.48, 15) for bits in ("60", "40", "40", "60")]).arrange(RIGHT, buff=0.08),
            self.card("scale = 2^40", YELLOW_D, 2.1, 0.62, 18),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 0.95)
        arrow = Arrow(requirements.get_right(), config[0].get_left(), buff=0.22, color=accent)
        context = Circle(radius=1.0, color=GREEN_C, fill_opacity=0.06).move_to(RIGHT * 4.45)
        context_label = Text("SEALContext", font_size=19, color=GREEN_C).move_to(context)
        valid = Text("VALID", font_size=23, color=GREEN_C).next_to(context, DOWN, buff=0.28)
        config_arrow = Arrow(config.get_right(), context.get_left(), buff=0.18, color=GREEN_C)

        self.play(FadeIn(requirements), run_time=step)
        self.play(GrowArrow(arrow), FadeIn(config[0]), run_time=step)
        self.play(FadeIn(config[1]), run_time=step)
        self.play(FadeIn(config[2]), run_time=step)
        self.play(GrowArrow(config_arrow), FadeIn(context), FadeIn(context_label), run_time=step)
        self.play(FadeIn(valid, scale=0.8), run_time=step)
        self.play(Circumscribe(config, color=GREEN_C), run_time=step)
        self.play(Indicate(valid, color=GREEN_C), run_time=step)
        self.play(Indicate(requirements, color=accent), run_time=step)
        return VGroup(requirements, arrow, config, context, context_label, valid, config_arrow)

    def demo_lifecycle_3(self, accent, duration):
        step = self.motion_step(duration, 9)
        divider = DashedLine(UP * 2.0, DOWN * 2.0, color=GREY_D)
        client_label = Text("trusted client", font_size=20, color=GREEN_C).move_to(LEFT * 4.5 + UP * 1.75)
        server_label = Text("server", font_size=20, color=BLUE_C).move_to(RIGHT * 4.5 + UP * 1.75)
        keygen = self.card("KeyGenerator", YELLOW_D, 2.0, 0.68, 19).move_to(LEFT * 4.2 + UP * 0.55)
        secret = self.card("SecretKey", GREEN_C, 1.7, 0.62, 18).move_to(LEFT * 4.2 + DOWN * 0.65)
        exported = VGroup(
            self.card("PublicKey", BLUE_C, 1.7, 0.58, 17),
            self.card("RelinKeys", RED_C, 1.7, 0.58, 17),
            self.card("Galois +1,+2", PURPLE_C, 1.7, 0.58, 16),
        ).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.9)
        source_keys = exported.copy().move_to(LEFT * 1.75)
        arrows = VGroup(
            *[
                Arrow(source.get_right(), target.get_left(), buff=0.18, color=color)
                for source, target, color in zip(source_keys, exported, (BLUE_C, RED_C, PURPLE_C))
            ]
        )
        stay = Arrow(keygen.get_bottom(), secret.get_top(), buff=0.12, color=GREEN_C)

        self.play(FadeIn(divider), FadeIn(client_label), FadeIn(server_label), run_time=step)
        self.play(FadeIn(keygen), GrowArrow(stay), FadeIn(secret), run_time=step)
        self.play(LaggedStart(*(FadeIn(key) for key in source_keys), lag_ratio=0.14), run_time=step)
        for arrow, source, target in zip(arrows, source_keys, exported):
            self.play(GrowArrow(arrow), TransformFromCopy(source, target), run_time=step)
        self.play(Indicate(secret, color=GREEN_C), run_time=step)
        self.play(Circumscribe(exported, color=accent), run_time=step)
        self.play(Indicate(exported[-1], color=PURPLE_C), run_time=step)
        return VGroup(divider, client_label, server_label, keygen, secret, source_keys, exported, arrows, stay)

    def demo_lifecycle_4(self, accent, duration):
        step = self.motion_step(duration, 10)
        divider = DashedLine(UP * 2.0, DOWN * 2.0, color=GREY_D).shift(RIGHT * 0.2)
        client_label = Text("client", font_size=20, color=GREEN_C).move_to(LEFT * 5.0 + UP * 1.75)
        server_label = Text("server", font_size=20, color=PURPLE_C).move_to(RIGHT * 4.8 + UP * 1.75)
        vector = self.slot_row([0.2, -1.1, 3.4, 0.8], BLUE_C, 0.5).move_to(LEFT * 5.1 + UP * 0.55)
        encode = self.card("encode", YELLOW_D, 1.35, 0.62, 18).move_to(LEFT * 2.9 + UP * 0.55)
        encrypt = self.card("encrypt", YELLOW_D, 1.35, 0.62, 18).move_to(LEFT * 1.0 + UP * 0.55)
        ciphertext = self.card("ciphertext", RED_C, 1.55, 0.62, 18).move_to(RIGHT * 1.45 + UP * 0.55)
        operations = VGroup(
            *[Circle(radius=0.32, color=PURPLE_C, fill_opacity=0.08) for _ in range(3)]
        ).arrange(RIGHT, buff=0.42).move_to(RIGHT * 4.0 + UP * 0.55)
        operation_labels = VGroup(*[Text(op, font_size=15, color=PURPLE_C).move_to(node) for op, node in zip(("x", "R", "+"), operations)])
        result = self.card("encrypted result", RED_C, 1.8, 0.62, 17).move_to(RIGHT * 4.0 + DOWN * 1.0)
        nodes = VGroup(vector, encode, encrypt, ciphertext, *operations)
        arrows = VGroup(
            *[
                Arrow(nodes[index].get_right(), nodes[index + 1].get_left(), buff=0.1, color=GREY_C)
                for index in range(len(nodes) - 1)
            ]
        )
        result_arrow = Arrow(operations[-1].get_bottom(), result.get_top(), buff=0.15, color=RED_C)

        self.play(FadeIn(divider), FadeIn(client_label), FadeIn(server_label), run_time=step)
        self.play(FadeIn(vector), GrowArrow(arrows[0]), FadeIn(encode), run_time=step)
        self.play(GrowArrow(arrows[1]), FadeIn(encrypt), run_time=step)
        self.play(GrowArrow(arrows[2]), FadeIn(ciphertext), run_time=step)
        for arrow, node, label in zip(arrows[3:], operations, operation_labels):
            self.play(GrowArrow(arrow), FadeIn(node), FadeIn(label), run_time=step)
        self.play(GrowArrow(result_arrow), FadeIn(result), run_time=step)
        self.play(Circumscribe(operations, color=PURPLE_C), run_time=step)
        self.play(Indicate(result, color=RED_C), run_time=step)
        self.play(Indicate(vector, color=BLUE_C), run_time=step)
        return VGroup(
            divider,
            client_label,
            server_label,
            vector,
            encode,
            encrypt,
            ciphertext,
            operations,
            operation_labels,
            result,
            arrows,
            result_arrow,
        )

    def demo_lifecycle_5(self, accent, duration):
        step = self.motion_step(duration, 10)
        encrypted = self.card("encrypted result", RED_C, 1.9, 0.66, 18).move_to(LEFT * 5.0 + UP * 0.75)
        decrypt = self.card("decrypt", GREEN_C, 1.4, 0.62, 18).move_to(LEFT * 2.9 + UP * 0.75)
        decode = self.card("decode", YELLOW_D, 1.4, 0.62, 18).move_to(LEFT * 1.0 + UP * 0.75)
        fhe = Dot(LEFT * 0.25 + DOWN * 0.35, color=RED_C, radius=0.1)
        plain = Dot(RIGHT * 0.15 + DOWN * 0.35, color=BLUE_C, radius=0.1)
        number_line = NumberLine(x_range=[0.84, 0.90, 0.01], length=5.5, include_numbers=False, color=GREY_C).move_to(RIGHT * 3.4 + DOWN * 0.35)
        fhe.move_to(number_line.n2p(0.871))
        plain.move_to(number_line.n2p(0.872))
        tolerance = Line(number_line.n2p(0.868), number_line.n2p(0.875), color=GREEN_C, stroke_width=10).shift(UP * 0.5)
        tolerance_label = Text("accepted tolerance", font_size=17, color=GREEN_C).next_to(tolerance, UP, buff=0.1)
        result = Text("PASS", font_size=24, color=GREEN_C).next_to(number_line, DOWN, buff=0.45)
        paths = VGroup(
            Arrow(encrypted.get_right(), decrypt.get_left(), buff=0.12, color=GREEN_C),
            Arrow(decrypt.get_right(), decode.get_left(), buff=0.12, color=YELLOW_D),
            Arrow(decode.get_right(), number_line.get_left(), buff=0.18, color=BLUE_C),
        )
        metrics = VGroup(
            *[self.card(metric, color, 1.55, 0.5, 15) for metric, color in (
                ("security", GREEN_C),
                ("accuracy", BLUE_C),
                ("latency", YELLOW_D),
                ("memory", PURPLE_C),
            )]
        ).arrange(RIGHT, buff=0.18).move_to(DOWN * 1.75)

        self.play(FadeIn(encrypted), GrowArrow(paths[0]), FadeIn(decrypt), run_time=step)
        self.play(GrowArrow(paths[1]), FadeIn(decode), run_time=step)
        self.play(GrowArrow(paths[2]), Create(number_line), run_time=step)
        self.play(FadeIn(plain), FadeIn(tolerance), FadeIn(tolerance_label), run_time=step)
        self.play(TransformFromCopy(plain, fhe), run_time=step)
        self.play(FadeIn(result, scale=0.8), run_time=step)
        self.play(LaggedStart(*(FadeIn(metric, shift=UP * 0.08) for metric in metrics), lag_ratio=0.12), run_time=step)
        self.play(Indicate(VGroup(plain, fhe), color=GREEN_C), run_time=step)
        self.play(Circumscribe(metrics, color=accent), run_time=step)
        self.play(Indicate(result, color=GREEN_C), run_time=step)
        return VGroup(
            encrypted,
            decrypt,
            decode,
            number_line,
            fhe,
            plain,
            tolerance,
            tolerance_label,
            result,
            paths,
            metrics,
        )

    @staticmethod
    def key_beats():
        return [
            ("SecretKey grants decryption", [], "The secret polynomial remains inside the trusted client."),
            ("PublicKey grants encryption", [], "Approved producers can encrypt without learning the SecretKey."),
            ("RelinKeys maintain ciphertext size", [], "Key switching removes the extra component without revealing plaintext."),
            ("GaloisKeys grant selected rotations", [], "Each generated key authorizes a specific packed-slot movement."),
            ("Provision only required capabilities", [], "Least privilege applies to cryptographic evaluation material."),
        ]

    @staticmethod
    def object_beats():
        return [
            ("Parameters define the SEAL universe", [], "Scheme, degree, and modulus chain must form a valid context."),
            ("SEALContext builds compatible levels", [], "Every chain level receives a distinct parameter identity."),
            ("KeyGenerator follows the circuit plan", [], "Generate only the keys required by the scheduled operations."),
            ("Encoding and encryption are separate", [], "CKKSEncoder prepares numbers; Encryptor protects the plaintext."),
            ("Evaluator is the cloud workbench", [], "Encrypted arithmetic uses evaluation keys, never the SecretKey."),
        ]

    @staticmethod
    def lifecycle_beats():
        return [
            ("Design the arithmetic circuit", [], "Packing, depth, and rotations are counted before setup."),
            ("Fit parameters to requirements", [], "The chosen degree, chain, and scale must validate together."),
            ("Provision client and server keys", [], "The client retains decryption authority and exports selected capabilities."),
            ("Encode, encrypt, and evaluate", [], "The server follows the planned circuit without opening ciphertexts."),
            ("Decrypt, decode, and verify", [], "A useful result must satisfy security, accuracy, and system budgets."),
        ]

    def construct(self):
        first_start = scene_time(self)
        self.open_lesson("assets/audio/01_math_crypto/scene_04_keys_and_seal_pipeline.mp3")
        self.play_timed_section(
            first_start,
            300,
            "00:00 - 05:00 | Key Capabilities",
            self.key_beats(),
            GREEN_C,
            self.KEY_DURATIONS,
        )

        second_start = scene_time(self)
        self.play_timed_section(
            second_start,
            300,
            "05:00 - 10:00 | Core SEAL Objects",
            self.object_beats(),
            YELLOW_D,
            self.OBJECT_DURATIONS,
        )

        third_start = scene_time(self)
        self.play_timed_section(
            third_start,
            300,
            "10:00 - 15:00 | End-to-End Lifecycle",
            self.lifecycle_beats(),
            BLUE_C,
            self.LIFECYCLE_DURATIONS,
        )
