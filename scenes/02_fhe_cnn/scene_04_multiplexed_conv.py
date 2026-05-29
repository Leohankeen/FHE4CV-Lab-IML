import sys
sys.path.append('.')

from manim import *
from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, PlaintextBlock

class MultiplexedPacking(Scene):
    def construct(self):
        # 1. Tạo các kênh dữ liệu thô (Feature maps)
        channels = VGroup(*[
            PlaintextBlock(label_text=f"Ch {i}") for i in range(4)
        ])
        # Xếp các kênh thành hàng ngang
        channels.arrange(RIGHT, buff=0.2).shift(UP * 2)
        
        self.play(LaggedStart(*[FadeIn(ch) for ch in channels], lag_ratio=0.2))
        self.wait(1)
        
        # 2. Tạo một khối CiphertextBlock trống khổng lồ
        packed_box = Rectangle(
            width=8.0, height=2.0, 
            color=COLOR_CIPHERTEXT, 
            fill_opacity=0.2, 
            stroke_width=DEFAULT_STROKE_WIDTH
        ).shift(DOWN * 1)
        packed_label = Text("Single CKKS Ciphertext (16384 slots)", font_size=24).next_to(packed_box, DOWN)
        
        self.play(Create(packed_box), Write(packed_label))
        self.wait(1)
        
        # 3. Hiệu ứng Packing: Thu nhỏ và hút các kênh vào trong hộp
        # Tạo bản sao thu nhỏ của các kênh để đặt vào trong hộp
        packed_channels = channels.copy().scale(0.6).move_to(packed_box.get_center())
        
        self.play(
            ReplacementTransform(channels, packed_channels),
            run_time=2,
            path_arc=0.5 # Tạo đường cong đẹp mắt khi di chuyển
        )
        
        # Bật sáng màu vàng thể hiện "Đã đóng gói thành công"
        success_glow = SurroundingRectangle(packed_channels, color=COLOR_ENCRYPTION, buff=0.1)
        self.play(Create(success_glow))
        self.wait(2)