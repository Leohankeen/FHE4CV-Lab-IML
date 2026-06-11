from pathlib import Path

from manim import *


class CiphertextOperations(Scene):
    AUDIO = Path("assets/audio/01_math_crypto/scene_03_ciphertext_operations.mp3")
    TOTAL_SECONDS = 900

    def construct(self):
        if self.AUDIO.exists():
            self.add_sound(str(self.AUDIO))
        self.show_opening("ACT 1", "Ciphertext Structure and Operations", "Components, metadata, and planned arithmetic")
        self.run_chapter("3.1  CIPHERTEXT ANATOMY", self.anatomy_beats(), RED_C, "components", 296)
        self.run_chapter("3.2  ADD, MULTIPLY, RELINEARIZE", self.arithmetic_beats(), YELLOW_D, "pipeline", 296)
        self.run_chapter("3.3  LEVELS, ROTATIONS, REDUCTIONS", self.advanced_beats(), BLUE_C, "rotation", 296)

    def show_opening(self, eyebrow, title, subtitle):
        group = VGroup(
            Text(eyebrow, font_size=22, color=YELLOW_D, weight=BOLD),
            Text(title, font_size=44, color=WHITE, weight=BOLD),
            Text(subtitle, font_size=25, color=GREY_B),
        ).arrange(DOWN, buff=0.24)
        self.play(FadeIn(group[0], shift=UP * 0.2), Write(group[1]), run_time=2)
        self.play(FadeIn(group[2]), run_time=1)
        self.play(group.animate.scale(0.96), run_time=7, rate_func=smooth)
        self.play(FadeOut(group), run_time=2)

    def run_chapter(self, chapter, beats, accent, visual_kind, duration):
        for index, beat in enumerate(beats):
            self.show_beat(chapter, beat, accent, visual_kind, index, duration / len(beats))

    def show_beat(self, chapter, beat, accent, visual_kind, index, duration):
        heading, labels, takeaway = beat
        chapter_text = Text(chapter, font_size=20, color=accent, weight=BOLD).to_corner(UL).shift(DOWN * 0.25)
        heading_text = Text(heading, font_size=34, color=WHITE, weight=BOLD)
        heading_text.next_to(chapter_text, DOWN, aligned_edge=LEFT, buff=0.2)
        visual = self.make_visual(visual_kind, index, labels, accent).move_to(DOWN * 0.05)
        footer = Text(takeaway, font_size=22, color=GREY_B).to_edge(DOWN, buff=0.55)
        track = Line(LEFT * 5.6, RIGHT * 5.6, color=GREY_D, stroke_width=3).to_edge(DOWN, buff=0.25)
        cursor = Dot(track.get_start(), radius=0.06, color=accent)
        self.play(FadeIn(chapter_text), Write(heading_text), run_time=1.2)
        for part in visual:
            self.play(FadeIn(part, shift=UP * 0.12), run_time=3.8 / max(1, len(visual)))
        self.play(FadeIn(footer), Create(track), FadeIn(cursor), run_time=1)
        self.play(
            cursor.animate.move_to(track.get_end()),
            visual.animate.scale(1.015),
            run_time=max(1, duration - 7.2),
            rate_func=linear,
        )
        self.play(FadeOut(VGroup(chapter_text, heading_text, visual, footer, track, cursor)), run_time=1.2)

    def make_visual(self, kind, index, labels, accent):
        if kind == "components":
            return self.make_component_visual(index, labels, accent)
        if kind == "pipeline":
            return self.make_pipeline_visual(index, labels, accent)
        return self.make_rotation_visual(index, labels, accent)

    def card(self, text, color, width=2.0):
        box = RoundedRectangle(width=width, height=1.05, corner_radius=0.1, color=color, fill_opacity=0.13)
        return VGroup(box, Text(text, font_size=19, color=WHITE).move_to(box))

    def make_component_visual(self, index, labels, accent):
        outer = RoundedRectangle(width=6.8, height=2.6, corner_radius=0.16, color=RED_C, fill_opacity=0.06)
        cards = VGroup(*[self.card(label, accent, 1.8) for label in labels]).arrange(RIGHT, buff=0.38)
        cards.move_to(outer)
        badges = VGroup(
            Text("size = 2", font_size=16, color=GREY_B),
            Text("scale", font_size=16, color=GREY_B),
            Text("parms_id", font_size=16, color=GREY_B),
        ).arrange(RIGHT, buff=0.75).next_to(outer, DOWN, buff=0.28)
        if index == 1:
            secret = Text("s(X)", font_size=26, color=GREEN_C).next_to(outer, UP, buff=0.3)
            return VGroup(outer, cards, secret, badges)
        if index == 3:
            warning = Text("MISMATCH", font_size=19, color=RED_C, weight=BOLD).next_to(outer, UP, buff=0.3)
            return VGroup(outer, cards, warning, badges)
        return VGroup(outer, cards, badges)

    def make_pipeline_visual(self, index, labels, accent):
        cards = VGroup(*[self.card(label, accent, 2.05) for label in labels]).arrange(RIGHT, buff=0.68)
        arrows = VGroup(
            Arrow(cards[0].get_right(), cards[1].get_left(), buff=0.1, color=GREY_B),
            Arrow(cards[1].get_right(), cards[2].get_left(), buff=0.1, color=GREY_B),
        )
        if index == 2:
            components = VGroup(*[Circle(radius=0.18, color=RED_C, fill_opacity=0.35) for _ in range(3)])
            components.arrange(RIGHT, buff=0.16).next_to(cards[1], UP, buff=0.35)
            return VGroup(cards, arrows, components)
        if index == 3:
            key = Text("RelinKeys", font_size=19, color=GREEN_C).next_to(cards[1], UP, buff=0.35)
            return VGroup(cards, arrows, key)
        return VGroup(cards, arrows)

    def make_rotation_visual(self, index, labels, accent):
        cells = VGroup(
            *[
                VGroup(
                    Square(side_length=0.82, color=accent, fill_opacity=0.12),
                    Text(str(value), font_size=20),
                )
                for value in (1, 2, 3, 4)
            ]
        )
        for cell in cells:
            cell[1].move_to(cell[0])
        cells.arrange(RIGHT, buff=0.12)
        labels_group = VGroup(*[Text(label, font_size=18) for label in labels]).arrange(RIGHT, buff=0.75)
        labels_group.next_to(cells, DOWN, buff=0.55)
        if index in (2, 3):
            arc = CurvedArrow(cells.get_right() + UP * 0.2, cells.get_left() + UP * 0.2, angle=TAU / 4, color=YELLOW_D)
            key = Text("GaloisKeys", font_size=18, color=GREEN_C).next_to(cells, UP, buff=0.45)
            return VGroup(cells, arc, key, labels_group)
        if index == 0:
            levels = VGroup(*[Line(LEFT * (2.5 - i * 0.35), RIGHT * (2.5 - i * 0.35), color=accent) for i in range(3)])
            levels.arrange(DOWN, buff=0.32).next_to(cells, UP, buff=0.42)
            return VGroup(levels, cells, labels_group)
        return VGroup(cells, labels_group)

    def anatomy_beats(self):
        return [
            ("Two ring-polynomial components", ("c0(X)", "RNS LIMBS", "c1(X)"), "A fresh public-key ciphertext commonly has size two."),
            ("Decryption intuition", ("c0", "+ c1 TIMES s", "MESSAGE + ERROR"), "Only the client combines components with the secret key."),
            ("Metadata is operational state", ("SIZE", "SCALE", "PARMS ID"), "Legal arithmetic depends on metadata compatibility."),
            ("Compatibility before addition", ("LEVEL A", "ALIGN STATE", "LEVEL A"), "Numerically related operands can still be incompatible."),
            ("Serialization is not authority", ("BYTE STREAM", "SEAL CONTEXT", "NO SECRET KEY"), "Transported ciphertext remains separate from decryption power."),
        ]

    def arithmetic_beats(self):
        return [
            ("Homomorphic addition", ("SIZE TWO", "ADD COMPONENTS", "SIZE TWO"), "Addition is cheap and normally preserves the level."),
            ("Plaintext or ciphertext weight", ("CT x PT", "VERSUS", "CT x CT"), "Protecting both operands costs more."),
            ("Multiplication grows state", ("SIZE TWO", "MULTIPLY", "SIZE THREE"), "Ciphertext multiplication grows size and scale."),
            ("Relinearization changes size", ("SIZE THREE", "RELIN KEYS", "SIZE TWO"), "Key switching reduces components without decrypting."),
            ("Maintenance has an order", ("MULTIPLY", "RELINEARIZE", "RESCALE"), "Each step solves a different state problem."),
        ]

    def advanced_beats(self):
        return [
            ("Meet at one level", ("HIGH LEVEL", "MOD SWITCH", "LOW LEVEL"), "Operands generally align before combination."),
            ("Mod switch versus rescale", ("DROP PRIME", "UPDATE SCALE", "NEXT LEVEL"), "Only rescale also normalizes CKKS scale."),
            ("Rotate packed slots", ("[1 2 3 4]", "ROTATE", "[4 1 2 3]"), "Galois automorphisms move data between slots."),
            ("Packed dot product", ("SLOT MULTIPLY", "ROTATE + ADD", "SUM"), "Logarithmic reductions combine packed products."),
            ("Plan before evaluation", ("DEPTH", "SCALE + LEVEL", "ROTATIONS"), "The evaluator executes a circuit designed in advance."),
        ]

