import sys

sys.path.append(".")

from manim import *

from scenes.library.constants import *
from scenes.library.ehe_primitives import BootstrappingGate, DepthMeter, SlotGrid
from scenes.library.storyboard import StoryboardScene, scene_time


class PolynomialApproximation(StoryboardScene):
    """20-minute lesson: polynomial activations and stable bootstrapping."""

    def construct(self):
        self.camera.background_color = "#101214"
        self.add_optional_sound("assets/audio/act2_scene02_poly_approx.mp3")

        first_section_start = scene_time(self)
        title = Text("Bending the curve", font_size=42, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.polynomial_replacement(title, first_section_start)
        self.degree_tradeoff(title)
        self.imaginary_removing_bootstrap(title)

    def make_axes(self, x_length=6.2, y_length=3.8):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.8, 3, 1],
            x_length=x_length,
            y_length=y_length,
            tips=False,
            axis_config={"color": GREY_C, "stroke_width": 2},
        )
        labels = VGroup(
            Text("x", font_size=22, color=GREY_C).next_to(axes.x_axis.get_end(), RIGHT, buff=0.1),
            Text("y", font_size=22, color=GREY_C).next_to(axes.y_axis.get_end(), UP, buff=0.1),
        )
        return axes, labels

    def polynomial_replacement(self, title, section_start):
        subtitle = Text("2.1  Replace comparison with arithmetic approximation", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)
        axes, labels = self.make_axes()
        axes.shift(DOWN * 0.2)
        labels.shift(DOWN * 0.2)
        relu = axes.plot(lambda x: max(0, x), color=RED_C, use_smoothing=False)
        quadratic = axes.plot(lambda x: 0.125 * x**2 + 0.5 * x + 0.25, color=COLOR_ENCRYPTION)
        formula = Text("P(x) = c0 + c1*x + c2*x^2 + ...", font_size=27, color=COLOR_MATH)
        formula.to_corner(UR).shift(DOWN * 0.85)

        samples = VGroup(*[
            Dot(axes.c2p(x, max(0, x)), radius=0.05, color=COLOR_PLAINTEXT)
            for x in [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
        ])

        self.play(FadeIn(subtitle), Create(axes), FadeIn(labels))
        self.play(Create(relu), LaggedStart(*(FadeIn(dot) for dot in samples), lag_ratio=0.12))
        self.play(Write(formula))
        self.play(ReplacementTransform(relu, quadratic), run_time=2.6)
        self.play(LaggedStart(*(Flash(dot, color=COLOR_ENCRYPTION) for dot in samples), lag_ratio=0.1))
        self.play(FadeOut(VGroup(subtitle, axes, labels, quadratic, formula, samples)))

        self.play_section_beats(
            section_start,
            420,
            "01:15:00 - 01:22:00 | Polynomial approximation",
            self.approximation_beats(),
            COLOR_ENCRYPTION,
        )

    def degree_tradeoff(self, title):
        section_start = scene_time(self)
        subtitle = Text("2.2  AutoFHE searches for the useful accuracy-depth balance", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        axes, labels = self.make_axes(x_length=5.5, y_length=3.5)
        axes.shift(LEFT * 2.65 + DOWN * 0.2)
        labels.shift(LEFT * 2.65 + DOWN * 0.2)
        relu = axes.plot(lambda x: max(0, x), color=GREY_B, use_smoothing=False)
        p2 = axes.plot(lambda x: 0.13 * x**2 + 0.5 * x + 0.22, color=BLUE_C)
        p4 = axes.plot(lambda x: -0.012 * x**4 + 0.14 * x**2 + 0.52 * x + 0.20, color=GREEN_C)
        p6 = axes.plot(
            lambda x: 0.002 * x**6 - 0.018 * x**4 + 0.13 * x**2 + 0.5 * x + 0.18,
            color=COLOR_ENCRYPTION,
        )
        meters = VGroup(
            DepthMeter("degree 2", 0.32),
            DepthMeter("degree 4", 0.58),
            DepthMeter("degree 6", 0.84),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).scale(0.82).shift(RIGHT * 3.55 + DOWN * 0.15)
        error = Text("approximation error", font_size=25, color=RED_A).next_to(axes, DOWN, buff=0.22)

        self.play(FadeIn(subtitle), Create(axes), FadeIn(labels), Create(relu))
        self.play(Create(p2), FadeIn(meters[0]), FadeIn(error))
        self.play(Create(p4), FadeIn(meters[1]), p2.animate.set_opacity(0.3))
        self.play(Create(p6), FadeIn(meters[2]), p4.animate.set_opacity(0.35), error.animate.set_color(GREEN_C))
        self.play(LaggedStart(*(Indicate(meter, color=COLOR_ENCRYPTION) for meter in meters), lag_ratio=0.2))
        self.play(FadeOut(VGroup(subtitle, axes, labels, relu, p2, p4, p6, meters, error)))

        self.play_section_beats(
            section_start,
            420,
            "01:22:00 - 01:29:00 | AutoFHE optimization",
            self.autofhe_beats(),
            GREEN_C,
        )

    def imaginary_removing_bootstrap(self, title):
        section_start = scene_time(self)
        subtitle = Text("2.3  Remove imaginary leakage during ciphertext refresh", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        slots = SlotGrid(rows=3, cols=12, filled_indices=range(36), cell_size=0.29).shift(LEFT * 3.65)
        noise = VGroup(*[
            Dot(radius=0.04, color=COLOR_NOISE).move_to(
                slots.get_center() + RIGHT * (-1.25 + 0.34 * i) + UP * (0.72 - 0.2 * (i % 5))
            )
            for i in range(9)
        ])
        zoom = RoundedRectangle(
            width=2.35,
            height=1.45,
            corner_radius=0.08,
            color=COLOR_MATH,
            fill_opacity=0.08,
        ).shift(RIGHT * 0.3 + UP * 0.6)
        real = Line(zoom.get_left() + RIGHT * 0.3, zoom.get_right() + LEFT * 0.3, color=COLOR_PLAINTEXT, stroke_width=6)
        imaginary = Line(
            zoom.get_left() + RIGHT * 0.3 + DOWN * 0.35,
            zoom.get_right() + LEFT * 0.3 + DOWN * 0.35,
            color=RED_A,
            stroke_width=5,
        ).set_opacity(0.5)
        gate = BootstrappingGate("Imaginary-removing\nbootstrap").scale(0.82).shift(RIGHT * 3.85 + DOWN * 0.15)
        sweep = Rectangle(width=0.16, height=1.62, color=COLOR_ENCRYPTION, fill_opacity=0.55)
        sweep.move_to(zoom.get_left() + RIGHT * 0.12)
        clean = Text("real component preserved", font_size=24, color=GREEN_C).next_to(gate, DOWN, buff=0.28)

        self.play(FadeIn(subtitle), FadeIn(slots), FadeIn(noise))
        self.play(FadeIn(zoom), Create(real), Create(imaginary))
        self.play(FadeIn(sweep))
        self.play(
            sweep.animate.move_to(zoom.get_right() + LEFT * 0.12),
            imaginary.animate.set_opacity(0),
            run_time=2.2,
        )
        self.play(FadeIn(gate), FadeIn(clean), noise.animate.set_opacity(0.1))
        self.play(FadeOut(VGroup(subtitle, slots, noise, zoom, real, imaginary, gate, sweep, clean)))

        self.play_section_beats(
            section_start,
            360,
            "01:29:00 - 01:35:00 | Imaginary-removing bootstrap",
            self.bootstrap_beats(),
            TEAL_C,
        )

    @staticmethod
    def approximation_beats():
        return [
            (
                "Why a polynomial is compatible",
                [
                    "Every polynomial is a finite graph of additions and multiplications.",
                    "CKKS evaluates that graph without inspecting encrypted values.",
                    "No comparison or data-dependent branch is required.",
                ],
                "Compatibility is obtained by changing the activation function.",
            ),
            (
                "Approximation is always local",
                [
                    "The polynomial is fitted over a chosen input interval.",
                    "Accuracy inside the interval can be high.",
                    "Values outside the interval may diverge rapidly.",
                ],
                "Activation ranges must be measured or controlled during training.",
            ),
            (
                "Coefficients determine the curve",
                [
                    "The constant term sets the vertical offset.",
                    "Odd terms control slope and sign-sensitive behavior.",
                    "Even terms smooth the sharp corner near zero.",
                ],
                "Coefficient selection is an optimization problem, not guesswork.",
            ),
            (
                "Evaluation order changes the cost",
                [
                    "A naive power expansion computes many repeated products.",
                    "Horner-style evaluation reuses intermediate values.",
                    "Balanced multiplication trees can reduce circuit depth.",
                ],
                "The same polynomial may have several encrypted circuits.",
            ),
            (
                "Error enters every activation layer",
                [
                    "A small local mismatch changes the next layer input.",
                    "Errors can amplify as depth increases.",
                    "Network accuracy depends on cumulative, not isolated, error.",
                ],
                "Layer-level curve quality is only one part of model quality.",
            ),
            (
                "Training must adapt to the replacement",
                [
                    "Polynomial-aware fine-tuning exposes the model to the new curve.",
                    "Weights learn to keep activations in the valid interval.",
                    "Accuracy is recovered before encrypted deployment.",
                ],
                "FHE inference begins with an FHE-aware training pipeline.",
            ),
        ]

    @staticmethod
    def autofhe_beats():
        return [
            (
                "A Taylor polynomial is not enough",
                [
                    "Taylor expansion is strongest near its expansion point.",
                    "CNN activations may occupy a much wider interval.",
                    "Tail behavior can dominate classification error.",
                ],
                "The optimization target must reflect real activation statistics.",
            ),
            (
                "Degree two is cheap but coarse",
                [
                    "A quadratic uses a shallow multiplication circuit.",
                    "It rounds the ReLU corner aggressively.",
                    "Low depth preserves levels but may reduce accuracy.",
                ],
                "Cheap activation does not automatically mean cheap total inference.",
            ),
            (
                "Higher degree improves shape flexibility",
                [
                    "Degree four and six can track more of the target interval.",
                    "Additional terms reduce approximation error in selected regions.",
                    "Every added dependency can consume levels and increase noise.",
                ],
                "Curve fidelity and cryptographic cost pull in opposite directions.",
            ),
            (
                "AutoFHE searches layer by layer",
                [
                    "Early and late layers do not need identical polynomials.",
                    "The search allocates degree where accuracy benefits most.",
                    "Less sensitive layers receive cheaper approximations.",
                ],
                "A mixed activation policy can beat one global polynomial.",
            ),
            (
                "The objective is network-level accuracy",
                [
                    "Candidate coefficients are evaluated through the full model.",
                    "The search measures end-to-end classification behavior.",
                    "Depth and bootstrap placement are included in the trade-off.",
                ],
                "The best local fit may not be the best encrypted network.",
            ),
            (
                "The output is an execution plan",
                [
                    "Each activation receives a degree and coefficient set.",
                    "The plan predicts level consumption across residual blocks.",
                    "Bootstrapping is inserted before the budget is exhausted.",
                ],
                "Optimization connects model design to cryptographic scheduling.",
            ),
        ]

    @staticmethod
    def bootstrap_beats():
        return [
            (
                "Why ciphertexts need refresh",
                [
                    "Multiplication grows approximation error and consumes modulus.",
                    "Rescaling removes low-order bits from the modulus chain.",
                    "A deep network eventually reaches an unusable level.",
                ],
                "Bootstrapping restores computation capacity without decryption.",
            ),
            (
                "Refresh changes representation internally",
                [
                    "Slots are transformed into coefficient representation.",
                    "A modular reduction approximation is evaluated homomorphically.",
                    "The refreshed value is transformed back into slots.",
                ],
                "These transformations are among the heaviest FHE operations.",
            ),
            (
                "CKKS slots are complex-valued",
                [
                    "Real model values are embedded into complex arithmetic.",
                    "Numerical transforms may introduce a small imaginary residue.",
                    "Repeated refreshes can make that residue accumulate.",
                ],
                "An error that begins invisible can destabilize a deep network.",
            ),
            (
                "Imaginary leakage breaks convergence",
                [
                    "Unexpected complex components alter later polynomial inputs.",
                    "High-degree terms can amplify the unwanted component.",
                    "Residual connections may propagate it across many blocks.",
                ],
                "Stable bootstrapping must preserve the intended real subspace.",
            ),
            (
                "Imaginary-removing projection",
                [
                    "Conjugate symmetry separates real and imaginary components.",
                    "The unwanted component is canceled during refresh.",
                    "The real signal continues with a renewed level budget.",
                ],
                "The refresh performs both level recovery and error cleanup.",
            ),
            (
                "Why this matters for ResNet",
                [
                    "Deep residual models require multiple refresh points.",
                    "Each refresh must avoid injecting systematic drift.",
                    "Stable repeated bootstrapping enables much deeper encrypted paths.",
                ],
                "Polynomial activations become practical only with stable refresh.",
            ),
        ]
