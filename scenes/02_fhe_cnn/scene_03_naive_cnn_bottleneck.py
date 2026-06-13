import sys
import os
import numpy as np
sys.path.append(".")

from manim import *
from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene

class NaiveCNNBottleneck(StoryboardScene):
    """Scene 3: The Naive CNN Bottleneck - 3B1B Mathematical Deep Dive
    Total duration strictly managed to 600 seconds (10 Minutes). Background Navy Blue."""

    def construct(self):
        self.camera.background_color = "#001A33"

        # [00:00 - 00:15] Tiêu đề Intro (Chính xác 15 giây)
        self.title_main = Tex(r"\textbf{The Naive CNN Bottleneck}", font_size=50, color=WHITE)
        self.title_main.set_color_by_gradient(RED_B, ORANGE)
        self.play(Write(self.title_main), run_time=5)
        self.play(self.title_main.animate.to_edge(UP).scale(0.8), run_time=5)
        self.wait(5)
        # Tổng: 15s

        self.slot_waste()             # Chính xác 292 giây
        self.bootstrapping_queue()    # Chính xác 293 giây
        # TỔNG CỘNG: 15 + 292 + 293 = 600 giây (10 phút)

    def safe_play_audio(self, filename):
        full_path = os.path.abspath(filename)
        if os.path.exists(full_path):
            try:
                self.add_sound(full_path)
                print(f"[AUDIO] Kích hoạt: {filename}")
            except Exception as e:
                print(f"[ERROR] Audio issue: {e}")
        else:
            print(f"[WARNING] Thiếu file: {full_path}")

    def slot_waste(self):
        """Phần 3.1: Sự lãng phí Slot (292 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_03_01.mp3")

        subtitle = Tex(r"3.1 Massive Slot Underutilization", font_size=36, color=GREY_B).next_to(self.title_main, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        # Mô phỏng Image Grid & Rút trích 1 Pixel
        img_grid = VGroup(*[Square(side_length=0.5, stroke_color=GREY_D) for _ in range(16)]).arrange_in_grid(rows=4, cols=4, buff=0).shift(LEFT*4 + UP*0.5)
        img_lbl = Tex(r"Image Tensor", font_size=28).next_to(img_grid, UP)
        
        self.play(Create(img_grid), Write(img_lbl), run_time=3)
        
        target_pixel = img_grid[5]
        self.play(target_pixel.animate.set_fill(BLUE_C, opacity=1), run_time=1)
        self.play(target_pixel.animate.shift(RIGHT*1), run_time=2)

        # Mô phỏng Ciphertext Vector với 8192 Slots
        vector_frame = Rectangle(width=6.0, height=0.8, color=COLOR_CIPHERTEXT).shift(RIGHT*2 + UP*0.5)
        slots = VGroup(*[Square(side_length=0.4, stroke_color=GREY_D) for _ in range(12)]).arrange(RIGHT, buff=0.05).move_to(vector_frame)
        vector_lbl = Tex(r"CKKS Ciphertext ($N = 8192$ slots)", font_size=28, color=COLOR_CIPHERTEXT).next_to(vector_frame, UP)
        
        self.play(Create(vector_frame), FadeIn(slots), Write(vector_lbl), run_time=3)

        # Nạp pixel vào Slot 0
        self.play(target_pixel.animate.move_to(slots[0]).scale(0.8), run_time=2)
        
        # Đổ màu Đỏ (Lãng phí) vào các Slot còn lại
        wasted_slots = VGroup(*[slots[i] for i in range(1, len(slots))])
        self.play(wasted_slots.animate.set_fill(RED_E, opacity=0.6), run_time=3)

        # Công thức giải thích sự lãng phí toán học
        cost_eq = MathTex(
            r"\text{Efficiency } = \frac{1}{8192} \approx 0.012\%", 
            font_size=36, color=YELLOW_C
        ).next_to(vector_frame, DOWN, buff=1)
        
        comp_eq = MathTex(
            r"\text{Computation Cost } \propto \mathcal{O}(N \log N) \text{ regardless of utilized slots.}",
            font_size=32, color=RED_C
        ).next_to(cost_eq, DOWN, buff=0.5)

        self.play(Write(cost_eq), run_time=3)
        self.play(Write(comp_eq), run_time=2)
        self.wait(10)
        # Subtotal: 4 + 3 + 1 + 2 + 3 + 2 + 3 + 3 + 2 + 10 = 33s (Audio ~ 40s)

        # Padding (249s): Hoạt ảnh quét qua các slot trống
        scan_tracker = ValueTracker(slots[1].get_left()[0])
        scan_line = Line(UP*0.5, DOWN*0.5, color=YELLOW_C).move_to(np.array([scan_tracker.get_value(), slots.get_center()[1], 0]))
        
        empty_lbl = Tex(r"Computing on Zeros...", font_size=24, color=RED_B)
        empty_lbl.add_updater(lambda m: m.next_to(scan_line, DOWN))
        
        self.play(FadeIn(scan_line), FadeIn(empty_lbl), run_time=2)

        def scan_updater(m):
            m.move_to(np.array([scan_tracker.get_value(), slots.get_center()[1], 0]))
            
        scan_line.add_updater(scan_updater)

        # Quét đi quét lại chậm rãi
        self.play(scan_tracker.animate.set_value(slots[-1].get_right()[0]), run_time=123, rate_func=there_and_back)
        self.play(scan_tracker.animate.set_value(slots[-1].get_right()[0]), run_time=124, rate_func=there_and_back)
        
        scan_line.remove_updater(scan_updater)
        empty_lbl.clear_updaters()

        # Dọn dẹp sạch sẽ để nhường chỗ cho Part 2
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 1: 33 + 2 + 123 + 124 + 10 = 292s

    def bootstrapping_queue(self):
        """Phần 3.2: Kẹt xe Bootstrapping (293 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_03_02.mp3")

        # Tái tạo lại Title vì đã bị xóa ở hàm trên
        self.title_main = Tex(r"\textbf{The Naive CNN Bottleneck}", font_size=50, color=WHITE).to_edge(UP).scale(0.8)
        self.title_main.set_color_by_gradient(RED_B, ORANGE)
        self.add(self.title_main)

        subtitle = Tex(r"3.2 The Bootstrapping Traffic Jam", font_size=36, color=GREY_B).next_to(self.title_main, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        # Mô phỏng quá trình cạn kiệt Depth
        eq_depth = MathTex(
            r"10^6 \text{ Pixels} \implies 10^6 \text{ Ciphertexts}",
            font_size=40, color=YELLOW_C
        ).shift(UP*1.5)
        self.play(Write(eq_depth), run_time=3)

        depth_bar = Rectangle(width=4, height=0.4, color=WHITE).shift(LEFT*3.5 + DOWN*0.5)
        depth_fill = Rectangle(width=4, height=0.4, color=GREEN_D, fill_opacity=0.8).align_to(depth_bar, LEFT)
        depth_lbl = Tex(r"Multiplicative Depth", font_size=28).next_to(depth_bar, UP)

        self.play(Create(depth_bar), FadeIn(depth_fill), Write(depth_lbl), run_time=3)

        # Cạn kiệt
        self.play(depth_fill.animate.stretch_to_fit_width(0.01).align_to(depth_bar, LEFT).set_color(RED_C), run_time=3)
        self.play(Flash(depth_bar, color=RED), run_time=2)

        # Trạm Bootstrapping Gate
        gate_box = RoundedRectangle(width=2, height=3, corner_radius=0.2, color=GREEN_C, fill_opacity=0.2).shift(RIGHT * 3.5 + DOWN * 1)
        gate_txt = Tex(r"\textbf{Bootstrap} \\ \textbf{Gate}", font_size=28, color=WHITE).move_to(gate_box)
        gate = VGroup(gate_box, gate_txt)
        
        belt = Line(LEFT * 6.5, RIGHT * 2.5, color=GREY_C, stroke_width=6).shift(DOWN * 2)
        self.play(FadeIn(gate), Create(belt), run_time=3)

        jam_txt = MathTex(r"\text{Latency} \approx \sum_{i=1}^{10^6} T_{\text{boot}} \rightarrow \text{Days!}", font_size=36, color=RED_A).next_to(gate, UP, buff=0.5)
        self.play(Write(jam_txt), run_time=4)
        self.wait(15)
        # Subtotal: 4+3+3+3+2+3+4+15 = 37s (Audio ~ 45s)

        # Padding (246s): Mô phỏng hàng đợi kẹt xe (Traffic Jam)
        queue_tracker = ValueTracker(0)
        
        conveyor_items = always_redraw(
            lambda: self.draw_traffic_jam(queue_tracker.get_value())
        )
        self.add(conveyor_items)

        # Chạy hoạt ảnh trong 246 giây, càng về sau khối đỏ càng chất đống
        self.play(queue_tracker.animate.set_value(100), run_time=246, rate_func=linear)
        
        conveyor_items.clear_updaters()

        # Dọn dẹp sạch sẽ Scene 3
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 2: 37 + 246 + 10 = 293s

    def draw_traffic_jam(self, t):
        """Hàm phụ trợ vẽ hàng đợi kẹt xe: 
        Khối đỏ tràn vào từ trái, dồn ứ lại ở cổng Gate bên phải."""
        items = VGroup()
        queue_size = int(t * 1.5) 
        
        # Giới hạn số khối hiển thị là 70 để Manim render mượt mà trong 10 phút
        for i in range(min(queue_size, 70)): 
            # x_pos lùi dần về phía trái của cổng (cổng ở x=2.5)
            x_pos = 2.0 - (i * 0.2)
            y_pos = -1.7
            
            # Nếu hàng đợi tràn ra khỏi băng chuyền (vượt x = -6.0)
            # Thì xếp chồng lên hàng thứ 2, thứ 3...
            if x_pos < -6.0:
                row = (i // 40)
                x_pos = 2.0 - ((i % 40) * 0.2)
                y_pos = -1.7 + (row * 0.45)

            # Tạo hiệu ứng rung lắc kẹt xe
            y_pos += np.sin(t * 5 + i) * 0.03

            ct = Rectangle(width=0.15, height=0.35, color=RED_C, fill_opacity=0.8)
            ct.move_to(np.array([x_pos, y_pos, 0]))
            items.add(ct)
            
        return items