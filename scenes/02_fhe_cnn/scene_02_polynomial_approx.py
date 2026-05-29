import sys
sys.path.append('.')

from manim import *
from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, PlaintextBlock

class PolynomialApproximation(Scene):
    def construct(self):
        # Thiết lập trục tọa độ
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 3, 1],
            axis_config={"color": GREY_C}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        self.play(Create(axes), FadeIn(axes_labels))
        
        # Đồ thị ReLU gốc (Đường gãy khúc)
        relu_graph = axes.plot(lambda x: max(0, x), color=RED_C, use_smoothing=False)
        relu_label = MathTex(r"f(x) = \max(0, x)", color=RED_C).to_corner(UL)
        
        self.play(Create(relu_graph), Write(relu_label))
        self.wait(2) # Khớp với lời thoại giải thích rào cản
        
        # Đồ thị Đa thức xấp xỉ (Đường cong) - Ví dụ: y = 0.1x^2 + 0.5x + 0.4
        poly_graph = axes.plot(lambda x: 0.125 * x**2 + 0.5 * x + 0.25, color=COLOR_ENCRYPTION)
        poly_label = MathTex(r"P(x) = ax^2 + bx + c", color=COLOR_ENCRYPTION).to_corner(UL)
        
        # Hiệu ứng "Bẻ cong": Biến đổi đồ thị và công thức
        self.play(
            ReplacementTransform(relu_graph, poly_graph),
            ReplacementTransform(relu_label, poly_label),
            run_time=3
        )
        self.wait(2)