import sys
from manim import *

from scenes.library.constants import *
from scenes.library.ehe_primitives import BootstrappingGate, CiphertextBlock, SlotGrid
from scenes.library.storyboard import StoryboardScene, scene_time


class NaiveCNNBottleneck(StoryboardScene):
    """10-minute lesson: why naive ciphertext-per-pixel CNNs are inefficient."""

    def construct(self):
        self.camera.background_color = "#101214"
        self.add_optional_sound("assets/audio/act2_scene03_naive_bottleneck.mp3")

        first_section_start = scene_time(self)
        title = Text("The naive CNN bottleneck", font_size=42, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.slot_waste(title, first_section_start)
        self.bootstrapping_queue(title)

    def slot_waste(self, title, section_start):
        subtitle = Text("3.1  A vector processor carrying one useful value", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        frame = RoundedRectangle(
            width=9.0,
            height=3.35,
            corner_radius=0.08,
            color=COLOR_CIPHERTEXT,
            fill_opacity=0.08,
        ).shift(DOWN * 0.12)
        grid = SlotGrid(rows=4, cols=18, filled_indices=[0], cell_size=0.25).move_to(frame)
        pixel = Text("pixel", font_size=17, color=WHITE).move_to(grid.cells[0])
        empty_label = Text("71 empty visual slots", font_size=28, color=RED_A).next_to(frame, DOWN, buff=0.26)
        ratio = Text("visual utilization: 1 / 72", font_size=31, color=COLOR_ENCRYPTION).next_to(frame, UP, buff=0.22)

        self.play(FadeIn(subtitle), FadeIn(frame), FadeIn(grid), Write(pixel))
        self.play(Write(ratio))
        self.play(
            LaggedStart(
                *(Indicate(cell, color=COLOR_NOISE, scale_factor=0.92) for cell in grid.cells[1::8]),
                lag_ratio=0.16,
            )
        )
        self.play(Write(empty_label), Flash(grid.cells[0], color=COLOR_PLAINTEXT))
        self.play(FadeOut(VGroup(subtitle, frame, grid, pixel, empty_label, ratio)))

        self.play_section_beats(
            section_start,
            300,
            "01:35:00 - 01:40:00 | Slot underutilization",
            self.slot_beats(),
            COLOR_CIPHERTEXT,
        )

    def bootstrapping_queue(self, title):
        section_start = scene_time(self)
        subtitle = Text("3.2  Sparse ciphertexts create a refresh traffic jam", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        gate = BootstrappingGate("Bootstrapping\nGate").shift(RIGHT * 3.0 + DOWN * 0.15)
        belt = Line(LEFT * 6.0 + DOWN * 1.5, RIGHT * 5.7 + DOWN * 1.5, color=GREY_C, stroke_width=5)
        queue = VGroup(*[
            CiphertextBlock(f"ct{i + 1}").scale(0.36)
            for i in range(9)
        ]).arrange(RIGHT, buff=0.12).move_to(LEFT * 4.2 + DOWN * 1.0)
        levels = VGroup(*[
            Rectangle(
                width=0.3,
                height=max(0.12, 1.2 - i * 0.18),
                color=COLOR_ENCRYPTION,
                fill_opacity=0.72,
            )
            for i in range(6)
        ]).arrange(RIGHT, aligned_edge=DOWN, buff=0.1).shift(LEFT * 3.5 + UP * 0.85)
        level_text = Text("levels consumed by repeated products", font_size=23, color=COLOR_MATH)
        level_text.next_to(levels, UP, buff=0.16)
        latency = Text("queue length grows faster than throughput", font_size=30, color=RED_A)
        latency.next_to(gate, UP, buff=0.36)

        self.play(FadeIn(subtitle), Create(belt), FadeIn(gate))
        self.play(FadeIn(queue), FadeIn(levels), FadeIn(level_text))
        for index in range(3):
            self.play(queue.animate.shift(RIGHT * 0.42), run_time=0.8)
            self.play(Flash(queue[-1 - index], color=RED_A), run_time=0.45)
        self.play(Write(latency), gate.animate.set_fill(RED_C, opacity=0.18))
        self.play(FadeOut(VGroup(subtitle, gate, belt, queue, levels, level_text, latency)))

        self.play_section_beats(
            section_start,
            300,
            "01:40:00 - 01:45:00 | Bootstrapping bottleneck",
            self.bootstrap_beats(),
            RED_A,
        )

    @staticmethod
    def slot_beats():
        return [
            (
                "CKKS was designed for SIMD",
                [
                    "A ciphertext can hold thousands of independent slot values.",
                    "One addition or multiplication processes every slot together.",
                    "The expensive cryptographic instruction should do useful work in parallel.",
                ],
                "Slot occupancy determines how much work each operation accomplishes.",
            ),
            (
                "The scalar translation wastes capacity",
                [
                    "One pixel or channel is placed into one ciphertext.",
                    "Almost every remaining slot contains padding or zero.",
                    "The cloud still pays the full polynomial arithmetic cost.",
                ],
                "A mostly empty ciphertext is not proportionally cheaper.",
            ),
            (
                "Ciphertext count grows with the tensor",
                [
                    "An image has width, height and channel dimensions.",
                    "A separate ciphertext for each value multiplies memory demand.",
                    "Intermediate feature maps can be larger than the original input.",
                ],
                "Naive representation turns tensor size into ciphertext count.",
            ),
            (
                "Memory traffic becomes part of latency",
                [
                    "Large ciphertexts must be allocated, copied and serialized.",
                    "Evaluation keys and temporary products increase working memory.",
                    "Cache misses and bandwidth costs appear before bootstrapping.",
                ],
                "Cryptographic arithmetic is only one part of system cost.",
            ),
            (
                "Utilization is an architectural decision",
                [
                    "Packing layout decides which tensor values share one ciphertext.",
                    "A good layout preserves locality needed by convolution.",
                    "It also minimizes the number of rotations and masks.",
                ],
                "Efficient FHE-CNN design starts with data layout.",
            ),
        ]

    @staticmethod
    def bootstrap_beats():
        return [
            (
                "Convolution consumes the level budget",
                [
                    "Each weighted product introduces multiplication and rescaling.",
                    "Activation polynomials add several more multiplication stages.",
                    "Residual networks repeat this pattern across many blocks.",
                ],
                "The modulus chain eventually reaches its final usable level.",
            ),
            (
                "Bootstrapping is a heavy service station",
                [
                    "The refresh runs transforms and a modular reduction approximation.",
                    "It is far more expensive than one addition or rotation.",
                    "Throughput is limited by how many ciphertexts require refresh.",
                ],
                "Bootstrapping cost is paid per ciphertext, not per useful slot.",
            ),
            (
                "Sparse ciphertexts multiply refresh work",
                [
                    "Thousands of underfilled ciphertexts arrive at the same gate.",
                    "Each carries very little useful feature data.",
                    "The queue spends most of its time refreshing empty capacity.",
                ],
                "Poor packing converts a depth problem into a throughput disaster.",
            ),
            (
                "Latency compounds across the network",
                [
                    "A slow refresh delays every dependent layer.",
                    "Multiple refresh points repeat the same queueing penalty.",
                    "End-to-end inference can expand from minutes toward hours.",
                ],
                "Layer latency cannot be evaluated independently of the schedule.",
            ),
            (
                "The bottleneck suggests the remedy",
                [
                    "Increase useful slot occupancy before encrypted computation.",
                    "Make one rotation serve several channels at once.",
                    "Refresh dense ciphertexts instead of thousands of sparse ones.",
                ],
                "Multiplexed packing attacks utilization and rotation cost together.",
            ),
        ]
