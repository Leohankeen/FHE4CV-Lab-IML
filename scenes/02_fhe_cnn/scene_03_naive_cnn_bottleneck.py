import sys
sys.path.append('.')

from manim import *
from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, PlaintextBlock

class NaiveCNNBottleneck(Scene):
    def construct(self):
        # 1. Đồng bộ Audio
        # self.add_sound("assets/audio/act2_scene03_naive_bottleneck.mp3")
        
        # --- Phân đoạn 3.1: Sự lãng phí không gian Slot ---
        # Tạo lưới đại diện cho 1 Ciphertext với hàng ngàn slots (rút gọn thành 10 ô trực quan)
        slots = VGroup(*[
            Rectangle(width=0.8, height=1.2, stroke_color=COLOR_MATH)
            for _ in range(10)
        ]).arrange(RIGHT, buff=0)
        
        # Chỉ có slot đầu tiên chứa dữ liệu pixel (màu xanh)
        slots[0].set_fill(COLOR_PLAINTEXT, opacity=0.8)
        pixel_label = Text("1 Pixel", font_size=16, color=WHITE).move_to(slots[0])
        
        # 99% slots còn lại trống (màu xám nhiễu)
        for i in range(1, 10):
            slots[i].set_fill(COLOR_NOISE, opacity=0.4)
            
        grid_group = VGroup(slots, pixel_label)
        main_label = Text("CKKS Ciphertext (16384 Slots)", font_size=28).next_to(grid_group, UP)
        
        self.play(FadeIn(main_label), Create(slots), Write(pixel_label))
        self.wait(1)
        
        # Cảnh báo lãng phí
        waste_alert = Text("> 99% Empty Slots!", color=RED_C, font_size=36).next_to(grid_group, DOWN)
        self.play(Write(waste_alert))
        self.wait(2)
        
        # Dọn dẹp màn hình để chuyển cảnh
        self.play(FadeOut(grid_group), FadeOut(main_label), FadeOut(waste_alert))
        
        # --- Phân đoạn 3.2: Nghẽn cổ chai Bootstrapping ---
        # Tạo Trạm Bootstrapping (Rất nặng nề)
        gate = Rectangle(width=2, height=4, color=COLOR_ENCRYPTION, fill_opacity=0.3)
        gate_text = Text("Bootstrapping\nGate\n(Heavy)", font_size=24, color=YELLOW).move_to(gate)
        gate_group = VGroup(gate, gate_text).shift(RIGHT * 3)
        self.play(FadeIn(gate_group))
        
        # Tạo một đoàn tàu các CiphertextBlock thưa thớt
        queue = VGroup(*[
            Rectangle(width=1.5, height=1, color=COLOR_CIPHERTEXT, fill_opacity=0.5)
            for _ in range(6)
        ]).arrange(RIGHT, buff=0.3).shift(LEFT * 7)
        
        # Di chuyển đoàn dữ liệu đâm sầm vào Trạm Bootstrapping và bị kẹt
        self.play(queue.animate.next_to(gate_group, LEFT, buff=0.1), run_time=3, rate_func=linear)
        
        # Báo động đỏ và Đồng hồ đếm thời gian
        bottleneck_text = Text("Latency Explosion!", color=RED_A, font_size=40).next_to(gate_group, UP)
        
        # SỬA LỖI TẠI ĐÂY: Dùng ValueTracker thay cho CountInFrom
        # 1. Khởi tạo một biến theo dõi giá trị bắt đầu từ 0
        tracker = ValueTracker(0)
        
        # 2. Khởi tạo số hiển thị
        timer = DecimalNumber(0, num_decimal_places=0, font_size=60).to_corner(UR).shift(LEFT*2)
        
        # 3. Liên kết số hiển thị với biến tracker (mỗi khi tracker đổi, số sẽ tự cập nhật)
        timer.add_updater(lambda d: d.set_value(tracker.get_value()))
        
        timer_label = Text("Hours", font_size=36).next_to(timer, RIGHT)
        timer_group = VGroup(timer, timer_label)
        
        self.play(Write(bottleneck_text), FadeIn(timer_group))
        
        # 4. Animate biến tracker chạy từ 0 lên 150 trong 3 giây
        self.play(tracker.animate.set_value(150), run_time=3)
        
        self.wait(2)