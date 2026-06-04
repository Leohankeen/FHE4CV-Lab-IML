from manim import *

from scenes.library.constants import (
    COLOR_CIPHERTEXT,
    COLOR_ENCRYPTION,
    COLOR_MATH,
    COLOR_PLAINTEXT,
)
from scenes.library.ehe_primitives import CiphertextBlock, PlaintextBlock


class FHE4CVFullExplainer(Scene):
    """Long-form Manim explainer for the FHE4CV medical image demo."""

    def construct(self):
        self.camera.background_color = "#101214"
        self.privacy_problem()
        self.he_concept()
        self.ckks_pipeline()
        self.results_and_limits()

    def privacy_problem(self):
        title = Text("Medical AI privacy problem", font_size=42, color=WHITE)
        title.to_edge(UP)

        patient = PlaintextBlock("X-ray image").scale(0.86).shift(LEFT * 4)
        cloud = RoundedRectangle(
            width=3.0,
            height=1.7,
            corner_radius=0.08,
            color=GREY_B,
            fill_opacity=0.14,
        ).shift(RIGHT * 3.7)
        cloud_text = Text("Cloud AI\nserver", font_size=28, color=WHITE).move_to(cloud)
        arrow = Arrow(patient.get_right(), cloud.get_left(), buff=0.25, color=RED_C)
        risk = Text(
            "Plaintext upload exposes sensitive patient data",
            font_size=27,
            color=RED_C,
        ).next_to(arrow, DOWN, buff=0.35)

        self.play(Write(title))
        self.play(FadeIn(patient, shift=RIGHT), FadeIn(VGroup(cloud, cloud_text), shift=LEFT))
        self.play(GrowArrow(arrow), FadeIn(risk))
        self.wait(1.2)
        self.play(FadeOut(VGroup(title, patient, cloud, cloud_text, arrow, risk)))

    def he_concept(self):
        title = Text("Homomorphic Encryption idea", font_size=42, color=WHITE).to_edge(UP)

        plain = PlaintextBlock("x").scale(0.8).shift(LEFT * 4)
        enc = CiphertextBlock("Enc(x)").scale(0.8).shift(LEFT * 1.25)
        compute = RoundedRectangle(
            width=2.45,
            height=1.35,
            corner_radius=0.08,
            color=COLOR_MATH,
            fill_opacity=0.10,
        ).shift(RIGHT * 1.35)
        compute_text = Text("compute\non ciphertext", font_size=23, color=WHITE).move_to(compute)
        result = CiphertextBlock("Enc(score)").scale(0.74).shift(RIGHT * 4.4)

        arrows = VGroup(
            Arrow(plain.get_right(), enc.get_left(), buff=0.18, color=COLOR_ENCRYPTION),
            Arrow(enc.get_right(), compute.get_left(), buff=0.18, color=COLOR_CIPHERTEXT),
            Arrow(compute.get_right(), result.get_left(), buff=0.18, color=COLOR_CIPHERTEXT),
        )

        labels = VGroup(
            Text("encrypt", font_size=22, color=COLOR_ENCRYPTION).next_to(arrows[0], DOWN),
            Text("add / multiply", font_size=22, color=COLOR_MATH).next_to(arrows[1], DOWN),
            Text("still encrypted", font_size=22, color=COLOR_CIPHERTEXT).next_to(arrows[2], DOWN),
        )

        self.play(Write(title))
        self.play(FadeIn(plain), GrowArrow(arrows[0]), FadeIn(enc))
        self.play(GrowArrow(arrows[1]), FadeIn(VGroup(compute, compute_text)))
        self.play(GrowArrow(arrows[2]), FadeIn(result), FadeIn(labels))
        self.wait(1.2)
        self.play(FadeOut(Group(title, plain, enc, compute, compute_text, result, arrows, labels)))

    def ckks_pipeline(self):
        title = Text("TenSEAL / CKKS medical image pipeline", font_size=39, color=WHITE)
        title.to_edge(UP)

        steps = VGroup(
            self.step_box("1", "Client\nextracts features", COLOR_PLAINTEXT),
            self.step_box("2", "CKKS\nencryption", COLOR_ENCRYPTION),
            self.step_box("3", "Cloud computes\nEnc(x) dot w + b", COLOR_CIPHERTEXT),
            self.step_box("4", "Client decrypts\ntriage score", COLOR_PLAINTEXT),
        ).arrange(RIGHT, buff=0.35)
        steps.scale(0.84).move_to(ORIGIN)

        arrows = VGroup()
        for left, right in zip(steps[:-1], steps[1:], strict=True):
            arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.12, color=GREY_B))

        bottom = Text(
            "The server never receives the raw image, plaintext features, or secret key",
            font_size=25,
            color=GREY_B,
        ).to_edge(DOWN)

        self.play(Write(title))
        self.play(LaggedStart(*(FadeIn(step, shift=UP) for step in steps), lag_ratio=0.18))
        self.play(LaggedStart(*(GrowArrow(arrow) for arrow in arrows), lag_ratio=0.18))
        self.play(FadeIn(bottom))
        self.wait(1.4)
        self.play(FadeOut(Group(title, steps, arrows, bottom)))

    def results_and_limits(self):
        title = Text("What this project proves", font_size=42, color=WHITE).to_edge(UP)

        left_title = Text("Working demo", font_size=30, color=COLOR_PLAINTEXT)
        right_title = Text("Current limits", font_size=30, color=COLOR_ENCRYPTION)

        left_items = VGroup(
            Text("8 local X-ray samples", font_size=25),
            Text("TenSEAL CKKS encrypted dot product", font_size=25),
            Text("Encrypted-vs-plaintext error around 1e-6", font_size=25),
            Text("Renderable Manim explainer", font_size=25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.23)

        right_items = VGroup(
            Text("Not a clinical diagnostic model", font_size=25),
            Text("Feature extraction stays client-side", font_size=25),
            Text("CNN layers need FHE-friendly redesign", font_size=25),
            Text("Production keys and audit are future work", font_size=25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.23)

        left = VGroup(left_title, left_items).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(right_title, right_items).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.1).move_to(ORIGIN + DOWN * 0.15)

        footer = Text(
            "Next: train with real labels, benchmark parameters, and test FHE-friendly models",
            font_size=24,
            color=GREY_B,
        ).to_edge(DOWN)

        self.play(Write(title))
        self.play(FadeIn(left, shift=RIGHT), FadeIn(right, shift=LEFT))
        self.play(FadeIn(footer))
        self.wait(2.0)

    def step_box(self, number: str, label: str, color):
        number_text = Text(number, font_size=32, color=color)
        label_text = Text(label, font_size=23, color=WHITE, line_spacing=0.85)
        content = VGroup(number_text, label_text).arrange(DOWN, buff=0.14)
        box = RoundedRectangle(
            width=2.55,
            height=1.85,
            corner_radius=0.08,
            color=color,
            fill_opacity=0.11,
        )
        content.move_to(box)
        return VGroup(box, content)
