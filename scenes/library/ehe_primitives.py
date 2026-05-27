from manim import *
from .constants import *

class CiphertextBlock(VGroup):
    """
    Khối hình hộp đại diện cho một Ciphertext.
    Hiệu ứng đặc trưng: Có viền đỏ và lớp nhiễu (noise) bên trong.
    """
    def __init__(self, label_text="Encrypted", **kwargs):
        super().__init__(**kwargs)
        
        # Hình hộp bên ngoài
        self.box = Rectangle(
            width=3.0, height=1.5, 
            color=COLOR_CIPHERTEXT, 
            fill_opacity=0.2,
            stroke_width=DEFAULT_STROKE_WIDTH
        )
        
        # Text nhãn
        self.label = Text(label_text, font_size=DEFAULT_FONT_SIZE, color=COLOR_MATH)
        self.label.move_to(self.box.get_center())
        
        self.add(self.box, self.label)

class PlaintextBlock(VGroup):
    """
    Khối đại diện cho dữ liệu chưa mã hóa.
    """
    def __init__(self, label_text="Data", **kwargs):
        super().__init__(**kwargs)
        
        self.box = Rectangle(
            width=2.5, height=1.2, 
            color=COLOR_PLAINTEXT, 
            fill_opacity=0.5,
            stroke_width=DEFAULT_STROKE_WIDTH
        )
        self.label = Text(label_text, font_size=DEFAULT_FONT_SIZE, color=COLOR_MATH)
        self.label.move_to(self.box.get_center())
        
        self.add(self.box, self.label)