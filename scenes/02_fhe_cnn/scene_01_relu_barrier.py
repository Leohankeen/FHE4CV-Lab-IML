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