import sys
sys.path.append('.')

from manim import *
from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, PlaintextBlock

class ReLuBarrier(Scene):
    def construct(self):
        # 1. Đồng bộ Audio (Ghi chú: Thay tên file thực tế của bạn)
        # self.add_sound("assets/audio/act2_scene01_relu_barrier.mp3")
        
        # 2. Tạo Node ReLU
        relu_node = Circle(radius=1.5, color=COLOR_PLAINTEXT).set_fill(COLOR_PLAINTEXT, opacity=0.2)
        relu_label = MathTex(r"\max(0, x)", font_size=48, color=COLOR_MATH)
        node_group = VGroup(relu_node, relu_label).shift(RIGHT * 3)
        
        self.play(DrawBorderThenFill(relu_node), Write(relu_label))
        self.wait(1)

        # 3. CiphertextBlock tiến vào Node
        ctx_block = CiphertextBlock(label_text="FHE Data").shift(LEFT * 4)
        self.play(FadeIn(ctx_block))
        
        # Di chuyển khối mã hóa đến hàm ReLU
        self.play(ctx_block.animate.next_to(node_group, LEFT, buff=0.5), run_time=2)
        
        # 4. Báo lỗi: Đổi màu Node sang Đỏ và thêm dấu X
        error_cross = Cross(node_group, stroke_color=RED_C, stroke_width=8)
        self.play(
            relu_node.animate.set_color(RED_C).set_fill(RED_C, opacity=0.4),
            Create(error_cross)
        )
        self.wait(2)

sys.path.append(".")

from manim import *

from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, MatrixGrid
from scenes.library.storyboard import StoryboardScene, scene_time


class ReLuBarrier(StoryboardScene):
    """15-minute lesson: why ReLU is a hard wall for encrypted CNNs."""

    def construct(self):
        self.camera.background_color = "#101214"
        self.add_optional_sound("assets/audio/act2_scene01_relu_barrier.mp3")

        first_section_start = scene_time(self)
        title = Text("The non-linearity wall", font_size=42, color=WHITE).to_edge(UP)
        self.play(Write(title))
        self.standard_cnn_path(title, first_section_start)
        self.fhe_arithmetic_path(title)
        self.relu_failure(title)

    def standard_cnn_path(self, title, section_start):
        subtitle = Text("1.1  How a conventional CNN builds visual features", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        image = MatrixGrid(rows=5, cols=5).scale(0.95).shift(LEFT * 4.6 + DOWN * 0.25)
        image_label = Text("input pixels", font_size=23, color=COLOR_PLAINTEXT).next_to(image, DOWN)
        kernel = Square(side_length=1.12, color=COLOR_ENCRYPTION, stroke_width=4)
        kernel.move_to(image.get_center() + LEFT * 0.37 + UP * 0.37)
        conv = self.node("linear convolution", COLOR_PLAINTEXT).shift(LEFT * 1.25)
        relu = self.node("ReLU", RED_C).shift(RIGHT * 1.55)
        output = MatrixGrid(rows=4, cols=4, cell_size=0.31, color=GREEN_C).shift(RIGHT * 4.45 + DOWN * 0.25)
        output_label = Text("feature map", font_size=23, color=GREEN_C).next_to(output, DOWN)
        arrows = VGroup(
            Arrow(image.get_right(), conv.get_left(), buff=0.2, color=GREY_B),
            Arrow(conv.get_right(), relu.get_left(), buff=0.2, color=GREY_B),
            Arrow(relu.get_right(), output.get_left(), buff=0.2, color=GREY_B),
        )

        self.play(FadeIn(subtitle), FadeIn(image), FadeIn(image_label))
        self.play(Create(kernel))
        for direction in [RIGHT, DOWN, LEFT, DOWN, RIGHT]:
            self.play(kernel.animate.shift(direction * 0.36), run_time=0.65)
        self.play(FadeIn(conv), GrowArrow(arrows[0]))
        self.play(FadeIn(relu), GrowArrow(arrows[1]))
        self.play(FadeIn(output), FadeIn(output_label), GrowArrow(arrows[2]))
        self.play(LaggedStart(*(Flash(cell, color=GREEN_C) for cell in output.cells[::3]), lag_ratio=0.16))
        self.play(FadeOut(VGroup(subtitle, image, image_label, kernel, conv, relu, output, output_label, arrows)))

        self.play_section_beats(
            section_start,
            300,
            "01:00:00 - 01:05:00 | Conventional CNN",
            self.cnn_beats(),
            COLOR_PLAINTEXT,
        )

    def fhe_arithmetic_path(self, title):
        section_start = scene_time(self)
        subtitle = Text("1.2  What RNS-CKKS can evaluate directly", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        cipher = CiphertextBlock("Enc(x)").scale(0.82).shift(LEFT * 4.4)
        add_box = self.operation_box("+", "homomorphic add").shift(LEFT * 1.1)
        mul_box = self.operation_box("x", "homomorphic multiply").shift(RIGHT * 1.75)
        output = CiphertextBlock("Enc(y)").scale(0.82).shift(RIGHT * 4.65)
        arrows = VGroup(
            Arrow(cipher.get_right(), add_box.get_left(), buff=0.16, color=COLOR_CIPHERTEXT),
            Arrow(add_box.get_right(), mul_box.get_left(), buff=0.16, color=COLOR_CIPHERTEXT),
            Arrow(mul_box.get_right(), output.get_left(), buff=0.16, color=COLOR_CIPHERTEXT),
        )
        ring = Text("ciphertext polynomial ring", font_size=25, color=COLOR_MATH)
        ring.next_to(VGroup(add_box, mul_box), DOWN, buff=0.65)

        self.play(FadeIn(subtitle), FadeIn(cipher))
        self.play(FadeIn(add_box), GrowArrow(arrows[0]))
        self.play(FadeIn(mul_box), GrowArrow(arrows[1]))
        self.play(FadeIn(output), GrowArrow(arrows[2]), Write(ring))
        self.play(Indicate(add_box, color=COLOR_ENCRYPTION), Indicate(mul_box, color=COLOR_ENCRYPTION))
        self.play(FadeOut(VGroup(subtitle, cipher, add_box, mul_box, output, arrows, ring)))

        self.play_section_beats(
            section_start,
            300,
            "01:05:00 - 01:10:00 | RNS-CKKS arithmetic",
            self.ckks_beats(),
            COLOR_ENCRYPTION,
        )

    def relu_failure(self, title):
        section_start = scene_time(self)
        subtitle = Text("1.3  Why max cannot be applied to a hidden value", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.18)

        cipher = CiphertextBlock("encrypted\nfeature").scale(0.78).shift(LEFT * 4.25)
        relu_node = Circle(radius=1.05, color=RED_C, fill_opacity=0.18).shift(LEFT * 0.75)
        relu_formula = Text("max(0, x)", font_size=31, color=RED_C).move_to(relu_node)
        relu = VGroup(relu_node, relu_formula)
        compare = Text("is x greater than zero?", font_size=25, color=RED_A).next_to(relu, DOWN, buff=0.35)
        wall = Rectangle(width=0.34, height=4.45, color=RED_C, fill_opacity=0.42).shift(RIGHT * 1.45)
        wall_label = Text("NON-LINEARITY WALL", font_size=28, color=RED_A).next_to(wall, RIGHT, buff=0.38)
        lock = VGroup(
            RoundedRectangle(width=0.78, height=0.58, corner_radius=0.06, color=GREY_B, fill_opacity=0.45),
            Arc(radius=0.28, start_angle=0, angle=PI, color=GREY_B).shift(UP * 0.27),
        ).move_to(relu_node.get_center() + UP * 0.08)

        self.play(FadeIn(subtitle), FadeIn(cipher), FadeIn(relu))
        self.play(cipher.animate.next_to(relu, LEFT, buff=0.38), run_time=1.4)
        self.play(FadeIn(compare))
        self.play(Create(lock), relu_node.animate.set_fill(RED_C, opacity=0.34))
        self.play(FadeIn(wall, shift=LEFT), FadeIn(wall_label), cipher.animate.shift(LEFT * 0.35))
        self.play(Flash(relu_node, color=RED_C), Flash(wall, color=RED_C))
        self.play(FadeOut(VGroup(subtitle, cipher, relu, compare, wall, wall_label, lock)))

        self.play_section_beats(
            section_start,
            300,
            "01:10:00 - 01:15:00 | ReLU failure",
            self.relu_beats(),
            RED_C,
        )

    @staticmethod
    def cnn_beats():
        return [
            (
                "A CNN alternates two different jobs",
                [
                    "Convolution mixes nearby pixels with learned weights.",
                    "Bias shifts the response before an activation is applied.",
                    "The activation decides which responses continue forward.",
                ],
                "Linear mixing extracts evidence; non-linearity selects it.",
            ),
            (
                "A small convolution example",
                [
                    "A 3 by 3 kernel multiplies nine neighboring pixel values.",
                    "The products are summed into one output position.",
                    "Sliding the same kernel creates an entire feature map.",
                ],
                "Weight sharing is why convolution is efficient on plaintext.",
            ),
            (
                "What the linear layer can learn",
                [
                    "Edge filters respond to horizontal or vertical contrast.",
                    "Later filters combine edges into textures and shapes.",
                    "Without an activation, stacked layers collapse to one linear map.",
                ],
                "Depth alone does not create expressive decision boundaries.",
            ),
            (
                "ReLU introduces the essential bend",
                [
                    "Negative evidence is mapped to zero.",
                    "Positive evidence passes through without changing scale.",
                    "The corner at zero divides the input space into regions.",
                ],
                "ReLU(x) = max(0, x).",
            ),
            (
                "Why repeated bends matter",
                [
                    "Each activation creates a new piecewise-linear partition.",
                    "Many layers compose simple regions into complex visual rules.",
                    "Classification power needs both linear and non-linear stages.",
                ],
                "This plaintext recipe becomes the FHE compatibility problem.",
            ),
        ]

    @staticmethod
    def ckks_beats():
        return [
            (
                "Encryption changes the data representation",
                [
                    "A pixel value is encoded into a polynomial-based ciphertext.",
                    "The cloud receives coefficients unrelated to the visible pixel.",
                    "Only the secret key can recover the approximate numeric value.",
                ],
                "Privacy hides values while preserving selected algebra.",
            ),
            (
                "CKKS packs many approximate numbers",
                [
                    "One ciphertext contains a vector of complex-valued slots.",
                    "The same operation is applied to all slots in SIMD fashion.",
                    "Packing is the main source of encrypted parallelism.",
                ],
                "A ciphertext should be treated as a vector, not one scalar.",
            ),
            (
                "Homomorphic addition is straightforward",
                [
                    "Enc(a) plus Enc(b) encrypts the value a plus b.",
                    "Ciphertext-plaintext addition supports public model biases.",
                    "Addition consumes little depth compared with multiplication.",
                ],
                "Linear accumulation maps naturally to encrypted execution.",
            ),
            (
                "Multiplication has a cryptographic cost",
                [
                    "Encrypted multiplication increases approximation noise.",
                    "Rescaling keeps CKKS scales aligned after multiplication.",
                    "Each multiplication consumes part of the modulus chain.",
                ],
                "Multiplicative depth is a finite computation budget.",
            ),
            (
                "The supported instruction set is narrow",
                [
                    "Polynomials use only additions and multiplications.",
                    "Branches, equality tests and ordering are not native.",
                    "An FHE-friendly network must stay inside this language.",
                ],
                "The cloud computes algebraically without seeing conditions.",
            ),
        ]

    @staticmethod
    def relu_beats():
        return [
            (
                "Maximum hides a comparison",
                [
                    "max(0, x) must determine whether x is positive.",
                    "That decision is equivalent to evaluating the sign of x.",
                    "Sign and ordering are discontinuous decision operations.",
                ],
                "The simple ReLU formula contains hidden control flow.",
            ),
            (
                "The server cannot inspect the sign",
                [
                    "Ciphertext coefficients do not reveal whether x is positive.",
                    "Decrypting each activation would expose private features.",
                    "Client round trips after every layer destroy latency.",
                ],
                "A secure cloud must remain blind throughout the network.",
            ),
            (
                "Branching is incompatible with blind execution",
                [
                    "Plain code chooses one branch for x below zero.",
                    "It chooses another branch for x above zero.",
                    "Encrypted execution cannot select from a hidden condition.",
                ],
                "Normal control flow depends on information the cloud cannot see.",
            ),
            (
                "Secure comparison is possible but expensive",
                [
                    "Interactive protocols add communication and synchronization.",
                    "Boolean FHE comparison requires deep logic circuits.",
                    "Both are heavier than approximate CKKS arithmetic.",
                ],
                "The goal is usable inference, not only theoretical possibility.",
            ),
            (
                "The design consequence",
                [
                    "Replace ReLU with an arithmetic approximation.",
                    "Control polynomial degree to protect the depth budget.",
                    "Coordinate activation, packing and refresh strategy.",
                ],
                "The next scene replaces the wall with a polynomial curve.",
            ),
        ]

    @staticmethod
    def node(label_text, color):
        box = RoundedRectangle(
            width=2.05,
            height=1.05,
            corner_radius=0.08,
            color=color,
            fill_opacity=0.14,
        )
        label = Text(label_text, font_size=22, color=WHITE).move_to(box)
        return VGroup(box, label)

    @staticmethod
    def operation_box(symbol, label_text):
        symbol_mob = Text(symbol, font_size=45, color=COLOR_ENCRYPTION)
        label = Text(label_text, font_size=18, color=WHITE)
        content = VGroup(symbol_mob, label).arrange(DOWN, buff=0.05)
        box = RoundedRectangle(
            width=2.25,
            height=1.28,
            corner_radius=0.08,
            color=COLOR_ENCRYPTION,
            fill_opacity=0.12,
        )
        content.move_to(box)
        return VGroup(box, content)
