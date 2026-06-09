import sys
from manim import *

from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, ResNetBlock, SlotGrid
from scenes.library.storyboard import StoryboardScene, scene_time


class MultiplexedPacking(StoryboardScene):
    """25-minute lesson: multiplexed packing and parallel convolutions."""

    def construct(self):
        self.camera.background_color = "#101214"
        self.add_optional_sound("assets/audio/act2_scene04_mpcnn_speedup.mp3")

        first_section_start = scene_time(self)
        title = Text("Multiplexed parallel convolutions", font_size=42, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.multiplexed_packing(title, first_section_start)
        self.rotation_reduction(title)
        self.deep_resnet_flow(title)

    def multiplexed_packing(self, title, section_start):
        subtitle = Text("4.1  Convert loose feature maps into a dense slot layout", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        colors = [RED_C, GREEN_C, BLUE_C, TEAL_C]
        feature_maps = VGroup()
        for index, color in enumerate(colors):
            grid = VGroup(*[
                Square(side_length=0.24, stroke_color=color, stroke_width=1).set_fill(
                    color,
                    opacity=0.28 + 0.08 * ((cell_index + index) % 3),
                )
                for cell_index in range(16)
            ]).arrange_in_grid(rows=4, cols=4, buff=0.025)
            frame = SurroundingRectangle(grid, color=color, buff=0.04)
            label = Text(f"channel {index + 1}", font_size=17, color=color).next_to(frame, DOWN, buff=0.08)
            feature_maps.add(VGroup(frame, grid, label))
        feature_maps.arrange(RIGHT, buff=0.28).shift(UP * 1.25)

        strip = VGroup(*[
            Square(side_length=0.22, stroke_color=colors[index // 8], stroke_width=1).set_fill(
                colors[index // 8],
                opacity=0.58,
            )
            for index in range(32)
        ]).arrange(RIGHT, buff=0.015).shift(DOWN * 0.35)
        strip_label = Text("interleaved channel and spatial segments", font_size=23, color=COLOR_MATH)
        strip_label.next_to(strip, DOWN, buff=0.14)

        slots = SlotGrid(rows=2, cols=16, filled_indices=range(32), cell_size=0.25).shift(DOWN * 1.65)
        packed_label = Text("one dense CKKS ciphertext", font_size=24, color=COLOR_CIPHERTEXT)
        packed_label.next_to(slots, DOWN, buff=0.15)
        utilization = Text("dense slot utilization", font_size=34, color=COLOR_ENCRYPTION)
        utilization.shift(RIGHT * 3.85 + DOWN * 0.2)

        self.play(FadeIn(subtitle), LaggedStart(*(FadeIn(fm, shift=UP) for fm in feature_maps), lag_ratio=0.12))
        self.play(ReplacementTransform(feature_maps.copy(), strip), FadeIn(strip_label), run_time=2.0)
        self.play(ReplacementTransform(strip.copy(), slots), FadeIn(packed_label), run_time=2.0)
        self.play(Write(utilization), Flash(slots, color=COLOR_ENCRYPTION))
        self.play(FadeOut(VGroup(subtitle, feature_maps, strip, strip_label, slots, packed_label, utilization)))

        self.play_section_beats(
            section_start,
            480,
            "01:45:00 - 01:53:00 | Multiplexed packing",
            self.packing_beats(),
            COLOR_ENCRYPTION,
        )

    def rotation_reduction(self, title):
        section_start = scene_time(self)
        subtitle = Text("4.2  Make one rotation align several channels together", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        naive = CiphertextBlock("naive layout").scale(0.68).shift(LEFT * 4.35 + UP * 1.0)
        rotations = VGroup(*[
            Text(f"rot {index + 1}", font_size=20, color=RED_A)
            for index in range(8)
        ]).arrange_in_grid(rows=2, cols=4, buff=0.2).next_to(naive, RIGHT, buff=0.48)

        packed = CiphertextBlock("MPCNN packed").scale(0.68).shift(LEFT * 4.35 + DOWN * 1.3)
        one_rotation = Text("one shared rotation", font_size=27, color=COLOR_ENCRYPTION)
        one_rotation.next_to(packed, RIGHT, buff=0.75)
        wave = Arrow(one_rotation.get_right(), one_rotation.get_right() + RIGHT * 1.55, color=COLOR_ENCRYPTION)

        chart_origin = RIGHT * 3.2 + DOWN * 1.65
        chart = VGroup(
            Line(chart_origin, chart_origin + UP * 2.55, color=GREY_C),
            Line(chart_origin, chart_origin + RIGHT * 2.65, color=GREY_C),
        )
        naive_bar = Rectangle(width=0.7, height=2.25, color=RED_A, fill_opacity=0.72)
        mpcnn_bar = Rectangle(width=0.7, height=0.86, color=COLOR_ENCRYPTION, fill_opacity=0.78)
        bars = VGroup(naive_bar, mpcnn_bar).arrange(RIGHT, aligned_edge=DOWN, buff=0.48)
        bars.move_to(chart_origin + RIGHT * 1.25 + UP * 1.12)
        result = Text("reported rotations: 38% of naive", font_size=24, color=COLOR_ENCRYPTION)
        result.next_to(chart, UP, buff=0.18)

        self.play(FadeIn(subtitle), FadeIn(naive))
        self.play(LaggedStart(*(FadeIn(item) for item in rotations), lag_ratio=0.07))
        self.play(FadeIn(packed), FadeIn(one_rotation), GrowArrow(wave))
        self.play(Create(chart), GrowFromEdge(naive_bar, DOWN), GrowFromEdge(mpcnn_bar, DOWN))
        self.play(Write(result))
        self.play(FadeOut(VGroup(subtitle, naive, rotations, packed, one_rotation, wave, chart, bars, result)))

        self.play_section_beats(
            section_start,
            480,
            "01:53:00 - 02:01:00 | Rotation reduction",
            self.rotation_beats(),
            TEAL_C,
        )

    def deep_resnet_flow(self, title):
        section_start = scene_time(self)
        subtitle = Text("4.3  Coordinate packing, levels and refresh across ResNet", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        blocks = VGroup(*[
            ResNetBlock(f"residual\nblock {index + 1}").scale(0.86)
            for index in range(5)
        ]).arrange(RIGHT, buff=0.3).shift(UP * 0.25)
        arrows = VGroup(*[
            Arrow(left.get_right(), right.get_left(), buff=0.08, color=GREY_B)
            for left, right in zip(blocks[:-1], blocks[1:], strict=True)
        ])
        packet = CiphertextBlock("packed ct").scale(0.42).move_to(blocks[0].get_left() + LEFT * 0.6)
        badges = VGroup(
            Text("ResNet-20", font_size=29, color=COLOR_PLAINTEXT),
            Text("ResNet-110", font_size=29, color=COLOR_ENCRYPTION),
            Text("128-bit security target", font_size=27, color=GREEN_C),
            Text("reported speedup: 4.67x", font_size=29, color=YELLOW_C),
        ).arrange(DOWN, buff=0.2).shift(DOWN * 1.55)

        self.play(FadeIn(subtitle), FadeIn(blocks), LaggedStart(*(GrowArrow(arrow) for arrow in arrows), lag_ratio=0.12))
        self.play(FadeIn(packet))
        for block in blocks:
            self.play(packet.animate.move_to(block), Flash(block, color=COLOR_ENCRYPTION), run_time=0.65)
        self.play(packet.animate.move_to(blocks[-1].get_right() + RIGHT * 0.7), run_time=0.7)
        self.play(LaggedStart(*(FadeIn(badge, shift=UP * 0.1) for badge in badges), lag_ratio=0.16))
        self.play(FadeOut(VGroup(subtitle, blocks, arrows, packet, badges)))

        self.play_section_beats(
            section_start,
            540,
            "02:01:00 - 02:10:00 | Deep encrypted ResNet",
            self.resnet_beats(),
            GREEN_C,
        )

    @staticmethod
    def packing_beats():
        return [
            (
                "Start from a three-dimensional tensor",
                [
                    "A CNN feature tensor has channel, height and width dimensions.",
                    "Nearby spatial values participate in the same convolution windows.",
                    "Channels must also be combined into each output channel.",
                ],
                "The slot layout must preserve both spatial and channel structure.",
            ),
            (
                "Flattening order is part of the algorithm",
                [
                    "Row-major flattening keeps neighboring columns close.",
                    "Channel-major blocks make channel boundaries predictable.",
                    "Segment offsets determine which rotation aligns each neighbor.",
                ],
                "A ciphertext is a programmable memory layout.",
            ),
            (
                "Multiplex several channels together",
                [
                    "Spatial segments from multiple channels occupy one slot vector.",
                    "The same slot offset means the same spatial relationship.",
                    "One encrypted instruction now touches several channels.",
                ],
                "Packing converts channel parallelism into SIMD parallelism.",
            ),
            (
                "Masks protect segment boundaries",
                [
                    "A rotation can wrap values from one segment into another.",
                    "Plaintext masks remove wrapped or invalid positions.",
                    "Padding slots preserve the intended convolution geometry.",
                ],
                "Dense packing still requires carefully designed boundary handling.",
            ),
            (
                "Weights are encoded to match the layout",
                [
                    "Kernel coefficients are repeated across corresponding slot groups.",
                    "Ciphertext-plaintext products apply weights in parallel.",
                    "Rotated weighted vectors are accumulated into output slots.",
                ],
                "Model weights and slot layout are compiled together.",
            ),
            (
                "Output channels can remain multiplexed",
                [
                    "The convolution result is arranged for the next encrypted layer.",
                    "Avoiding repacking saves rotations and temporary ciphertexts.",
                    "Layer interfaces become layout contracts.",
                ],
                "The best representation supports an entire sequence of layers.",
            ),
            (
                "Packing changes the resource equation",
                [
                    "More useful values share each multiplication and refresh.",
                    "Ciphertext count and memory traffic decrease.",
                    "The remaining optimization target is rotation count.",
                ],
                "Dense utilization prepares the path for parallel convolution.",
            ),
        ]

    @staticmethod
    def rotation_beats():
        return [
            (
                "What a ciphertext rotation does",
                [
                    "A rotation cyclically shifts every CKKS slot by an offset.",
                    "Convolution uses shifts to align neighboring pixels.",
                    "Each kernel position normally requires a corresponding alignment.",
                ],
                "Rotations are encrypted data movement operations.",
            ),
            (
                "Why rotations are expensive",
                [
                    "Rotation invokes an automorphism on the ciphertext polynomial.",
                    "Key switching returns the result to the active secret-key form.",
                    "Large evaluation keys and polynomial products are involved.",
                ],
                "A rotation is much heavier than changing an array index.",
            ),
            (
                "Naive channel processing repeats work",
                [
                    "Each channel is shifted independently for the same kernel offset.",
                    "The operation count grows with input and output channels.",
                    "Repeated key switching dominates convolution latency.",
                ],
                "The same spatial movement is paid for many times.",
            ),
            (
                "Interlocking layouts share offsets",
                [
                    "Matching spatial positions occupy matching channel segments.",
                    "One cyclic shift moves every multiplexed channel together.",
                    "All channels become aligned for the same kernel position.",
                ],
                "Layout converts redundant rotations into one SIMD rotation.",
            ),
            (
                "Masks and accumulation finish the convolution",
                [
                    "Plaintext masks select valid values after each shared shift.",
                    "Kernel weights are multiplied into the aligned slots.",
                    "Partial products are accumulated into packed outputs.",
                ],
                "Rotation reduction must preserve exact convolution semantics.",
            ),
            (
                "Count operations before benchmarking",
                [
                    "A layout can be analyzed by rotations per kernel position.",
                    "Ciphertext multiplications and additions are counted separately.",
                    "Memory and evaluation-key traffic should also be measured.",
                ],
                "Operation count explains where a measured speedup originates.",
            ),
            (
                "Reported reduction",
                [
                    "The MPCNN layout removes many redundant channel rotations.",
                    "The storyboard reference reports a 62 percent reduction.",
                    "Only 38 percent of the naive rotation count remains.",
                ],
                "Fewer rotations improve both latency and key-switch workload.",
            ),
        ]

    @staticmethod
    def resnet_beats():
        return [
            (
                "Residual blocks preserve trainability",
                [
                    "A residual path learns a transformation of the input.",
                    "A skip path carries the input toward the block output.",
                    "The two paths are added before the next activation.",
                ],
                "Addition is FHE-friendly, making residual structure attractive.",
            ),
            (
                "Every block has a level budget",
                [
                    "Convolution products consume scale and modulus levels.",
                    "Polynomial activations consume several additional levels.",
                    "Skip paths must reach additions with compatible scales.",
                ],
                "Encrypted residual execution requires explicit level planning.",
            ),
            (
                "Bootstrapping becomes scheduled infrastructure",
                [
                    "Refresh points are selected before levels are exhausted.",
                    "Dense packed ciphertexts maximize useful work per refresh.",
                    "Refresh placement must respect residual dependencies.",
                ],
                "Bootstrapping is part of the network execution graph.",
            ),
            (
                "Imaginary removal protects repeated refresh",
                [
                    "Deep models may cross several bootstrapping boundaries.",
                    "Complex leakage must not accumulate between residual stages.",
                    "Real-subspace projection keeps later activations stable.",
                ],
                "Stable refresh enables depth, not only one isolated layer.",
            ),
            (
                "ResNet-20 is the first scaling target",
                [
                    "The model contains enough blocks to expose scheduling issues.",
                    "Packing reuse and bootstrap placement can be measured end to end.",
                    "Accuracy validates the polynomial activation strategy.",
                ],
                "A complete encrypted model is more meaningful than a layer microbenchmark.",
            ),
            (
                "ResNet-110 stresses the complete design",
                [
                    "Many more residual blocks amplify small inefficiencies.",
                    "Repeated activations test approximation stability.",
                    "Multiple refreshes test noise and imaginary-error control.",
                ],
                "Deep encrypted inference requires every optimization to cooperate.",
            ),
            (
                "Security parameters constrain performance",
                [
                    "Polynomial degree and modulus sizes determine security and capacity.",
                    "Rotation and bootstrap keys increase memory requirements.",
                    "The parameter set targets standard 128-bit security.",
                ],
                "Reported speed must be interpreted together with its security level.",
            ),
            (
                "Combined system result",
                [
                    "Multiplexing improves slot utilization and rotation sharing.",
                    "Level planning and stable bootstrap support deeper execution.",
                    "The reference reports more than a 4.6 times latency improvement.",
                ],
                "The breakthrough is a coordinated encrypted-CNN system design.",
            ),
        ]


class MultiplexedParallelConvolutions(MultiplexedPacking):
    """Alias with the full storyboard name."""
