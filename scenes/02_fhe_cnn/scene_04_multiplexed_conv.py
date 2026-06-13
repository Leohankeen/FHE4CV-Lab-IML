import sys
import os
import numpy as np
sys.path.append(".")

from manim import *
from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene

class MultiplexedPacking(StoryboardScene):
    """Scene 4: Multiplexed Parallel Convolutions - Ultimate 3B1B Edition
    Total duration strictly managed to 1500 seconds (25 minutes). Navy Blue Background."""

    def construct(self):
        self.camera.background_color = "#001A33"

        # [00:00 - 00:15] Tiêu đề Intro (Chính xác 15 giây)
        self.title_main = Tex(r"\textbf{Multiplexed Parallel Convolutions}", font_size=50, color=WHITE)
        self.title_main.set_color_by_gradient(GREEN_C, TEAL_C)
        self.play(Write(self.title_main), run_time=5)
        self.play(self.title_main.animate.to_edge(UP).scale(0.8), run_time=5)
        self.wait(5)
        # Tổng: 15s

        # 3 Phân đoạn chính, mỗi phân đoạn chính xác 495 giây
        self.multiplexed_packing()      # 495 giây
        self.rotation_reduction()       # 495 giây
        self.deep_resnet_flow()         # 495 giây
        # TỔNG CỘNG: 15 + 495 + 495 + 495 = 1500 giây (25 phút)

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

    def multiplexed_packing(self):
        """Phần 4.1: Đóng gói dồn kênh (495 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_04_01.mp3")

        subtitle = Tex(r"4.1 SIMD Packing: Interleaving Spatial \& Channel Segments", font_size=36, color=GREY_B).next_to(self.title_main, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        # Trực quan hóa 4 loose feature maps
        colors = [RED_C, GREEN_C, BLUE_C, YELLOW_C]
        feature_maps = VGroup()
        for index, color in enumerate(colors):
            grid = VGroup(*[
                Square(side_length=0.25, stroke_color=color, stroke_width=1).set_fill(color, opacity=0.4 + 0.1 * ((i + index) % 3))
                for i in range(16)
            ]).arrange_in_grid(rows=4, cols=4, buff=0.05)
            frame = SurroundingRectangle(grid, color=color, buff=0.05)
            label = Tex("Ch " + str(index + 1), font_size=24, color=color).next_to(frame, DOWN, buff=0.1)
            feature_maps.add(VGroup(frame, grid, label))
            
        feature_maps.arrange(RIGHT, buff=0.8).shift(UP * 1)
        self.play(LaggedStart(*(FadeIn(fm, shift=UP) for fm in feature_maps), lag_ratio=0.2), run_time=6)

        # Biểu diễn phương trình SIMD
        math_eq = MathTex(
            r"c = \text{Enc}\left( [p_{1}^{ch1}, p_{1}^{ch2}, p_{1}^{ch3}, p_{1}^{ch4}, \dots, p_{N}^{ch4}] \right)", 
            font_size=40, color=YELLOW_C
        ).shift(DOWN * 1.0)

        # Chuyển đổi thành 1 dải Dense Ciphertext
        strip = VGroup(*[
            Square(side_length=0.3, stroke_color=colors[i % 4], stroke_width=2).set_fill(colors[i % 4], opacity=0.8)
            for i in range(32)
        ]).arrange(RIGHT, buff=0.02).next_to(math_eq, DOWN, buff=0.5)

        self.play(Write(math_eq), run_time=5)
        self.play(ReplacementTransform(feature_maps.copy(), strip), run_time=5)

        utilization = Tex(r"\textbf{Utilization: } $\approx 100\%$ (Zero Waste)", font_size=36, color=GREEN_C).next_to(strip, DOWN, buff=0.5)
        self.play(Write(utilization), Flash(strip, color=GREEN_C), run_time=5)
        # Subtotal: 4 + 6 + 5 + 5 + 5 = 25s

        # Padding (460s): Dòng chảy dữ liệu SIMD khổng lồ liên tục xử lý
        stream_tracker = ValueTracker(0)
        dots = VGroup(*[Dot(radius=0.08) for _ in range(60)])
        self.add(dots)

        def stream_updater(m):
            t = stream_tracker.get_value()
            for i, dot in enumerate(m):
                channel = i % 4
                dot.set_color(colors[channel])
                # Tạo sóng lượn vòng từ trái sang phải
                x_val = -7 + ((t * 2 + i * 0.3) % 14)
                y_val = 2.5 + np.sin(x_val * 1.5 + t) * 0.5
                dot.move_to(np.array([x_val, y_val, 0]))

        dots.add_updater(stream_updater)
        
        self.play(stream_tracker.animate.set_value(230), run_time=460, rate_func=linear)
        dots.remove_updater(stream_updater)

        # Clear toàn bộ màn hình
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 1: 25 + 460 + 10 = 495s

    def rotation_reduction(self):
        """Phần 4.2: Giảm thiểu phép xoay Rotation (495 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_04_02.mp3")

        # Khôi phục Tiêu đề
        self.title_main = Tex(r"\textbf{Multiplexed Parallel Convolutions}", font_size=50, color=WHITE).to_edge(UP).scale(0.8)
        self.title_main.set_color_by_gradient(GREEN_C, TEAL_C)
        self.add(self.title_main)

        subtitle = Tex(r"4.2 Algorithmic Alignment for Rotation Reduction", font_size=36, color=GREY_B).next_to(self.title_main, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        # Khối so sánh: Naive vs MPCNN
        naive_box = Rectangle(width=4.5, height=1.5, color=RED_A, fill_opacity=0.2).shift(LEFT * 3.5 + UP * 1.2)
        naive_txt = Tex(r"Naive Layout \\ $\mathcal{O}(C_{in} \cdot C_{out})$ Rotations", font_size=32, color=RED_A).move_to(naive_box)
        
        packed_box = Rectangle(width=4.5, height=1.5, color=GREEN_C, fill_opacity=0.2).shift(LEFT * 3.5 + DOWN * 1.2)
        packed_txt = Tex(r"MPCNN Packed \\ $\mathcal{O}(1)$ Shared Rotation", font_size=32, color=GREEN_C).move_to(packed_box)

        self.play(FadeIn(VGroup(naive_box, naive_txt)), run_time=4)
        self.play(FadeIn(VGroup(packed_box, packed_txt)), run_time=4)

        # Biểu đồ tiết kiệm
        chart_origin = RIGHT * 1.5 + DOWN * 2
        chart_axes = VGroup(
            Line(chart_origin, chart_origin + UP * 4.5, color=GREY_C),
            Line(chart_origin, chart_origin + RIGHT * 4.5, color=GREY_C)
        )
        naive_bar = Rectangle(width=1.2, height=4.0, color=RED_A, fill_opacity=0.8).move_to(chart_origin + RIGHT*1.2 + UP*2.0)
        mpcnn_bar = Rectangle(width=1.2, height=1.52, color=GREEN_C, fill_opacity=0.8).move_to(chart_origin + RIGHT*3.3 + UP*0.76)
        
        result_txt = Tex(r"\textbf{Rotations: 38\% of Naive}", font_size=36, color=GREEN_C).next_to(chart_axes, UP, buff=0.5)

        self.play(Create(chart_axes), run_time=3)
        self.play(GrowFromEdge(naive_bar, DOWN), GrowFromEdge(mpcnn_bar, DOWN), run_time=5)
        self.play(Write(result_txt), Flash(result_txt, color=GREEN), run_time=5)
        # Subtotal: 4+4+4+3+5+5 = 25s

        # Padding (460s): Mô phỏng phép dịch chuyển xoay vòng vector (Homomorphic Rotation)
        rot_tracker = ValueTracker(0)
        
        def draw_rotations(t):
            # Tạo 1 dải vector đang xoay vòng một cách đồng bộ
            group = VGroup()
            for i in range(10):
                box = Square(side_length=0.4, color=BLUE_C, fill_opacity=0.5)
                # Dịch chuyển xoay vòng từ trái sang phải
                x_pos = -6 + ((i * 0.5 + t * 2) % 5)
                box.move_to(np.array([x_pos, -3, 0]))
                
                label = MathTex(str(i), font_size=20).move_to(box)
                group.add(VGroup(box, label))
            
            arr = Arrow(np.array([-6, -2.2, 0]), np.array([-1, -2.2, 0]), color=YELLOW_C)
            rot_lbl = MathTex(r"\text{Shared } \circlearrowleft", font_size=28, color=YELLOW_C).next_to(arr, UP, buff=0.1)
            group.add(arr, rot_lbl)
            return group

        dynamic_rotations = always_redraw(lambda: draw_rotations(rot_tracker.get_value()))
        self.add(dynamic_rotations)

        self.play(rot_tracker.animate.set_value(230), run_time=460, rate_func=linear)

        # Clear toàn bộ
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 2: 25 + 460 + 10 = 495s

    def deep_resnet_flow(self):
        """Phần 4.3: Luồng ResNet sâu (495 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_04_03.mp3")

        # Khôi phục Tiêu đề
        self.title_main = Tex(r"\textbf{Multiplexed Parallel Convolutions}", font_size=50, color=WHITE).to_edge(UP).scale(0.8)
        self.title_main.set_color_by_gradient(GREEN_C, TEAL_C)
        self.add(self.title_main)

        subtitle = Tex(r"4.3 End-to-End ResNet over FHE", font_size=36, color=GREY_B).next_to(self.title_main, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        # Xây dựng ResNet Pipeline trực quan
        blocks = VGroup(*[
            RoundedRectangle(width=1.6, height=1.6, corner_radius=0.2, color=BLUE_D, fill_opacity=0.3)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.6).shift(UP * 0.8)
        
        block_labels = VGroup(*[
            Tex("ResBlock\\\\" + str(i+1), font_size=24, color=WHITE).move_to(blocks[i])
            for i in range(5)
        ])

        arrows = VGroup(*[
            Arrow(blocks[i].get_right(), blocks[i+1].get_left(), buff=0.1, color=GREY_B)
            for i in range(4)
        ])

        self.play(FadeIn(blocks), FadeIn(block_labels), run_time=5)
        self.play(LaggedStart(*(GrowArrow(a) for a in arrows), lag_ratio=0.2), run_time=4)

        # Danh hiệu / Thành tựu
        badges = VGroup(
            Tex(r"\textbf{Supported: ResNet-20 \& ResNet-110}", font_size=36, color=BLUE_B),
            Tex(r"Strict 128-bit Security Target", font_size=32, color=GREEN_C),
            Tex(r"\textbf{Inference Speedup: 4.67x}", font_size=40, color=YELLOW_C),
        ).arrange(DOWN, buff=0.4).shift(DOWN * 2)

        self.play(LaggedStart(*(FadeIn(b, shift=UP*0.2) for b in badges), lag_ratio=0.3), run_time=7)
        # Subtotal: 4+5+4+7 = 20s

        # Padding (465s): Gói dữ liệu mã hóa di chuyển xuyên suốt mạng
        packet_tracker = ValueTracker(0)
        packet = RoundedRectangle(width=0.7, height=0.7, corner_radius=0.1, color=GREEN_A, fill_opacity=1)
        self.add(packet)

        def packet_updater(m):
            t = packet_tracker.get_value()
            # Loop vị trí từ block đầu đến block cuối
            x_pos = blocks[0].get_center()[0] - 1 + ((t % 10) / 10.0) * (blocks[-1].get_center()[0] - blocks[0].get_center()[0] + 2)
            y_pos = 0.8
            m.move_to(np.array([x_pos, y_pos, 0]))
            
            # Mô phỏng nhiễu gia tăng và được làm sạch (Bootstrapping) mỗi khi qua block
            noise_level = (x_pos % 2) / 2.0  
            interpolated_color = interpolate_color(GREEN_A, RED_C, noise_level)
            m.set_color(interpolated_color)

        packet.add_updater(packet_updater)

        ambient_title = Tex(r"Data safely shielded by cryptographic noise through ResNet", font_size=28, color=GREY_A).to_edge(DOWN)
        self.play(FadeIn(ambient_title), run_time=5)

        self.play(packet_tracker.animate.set_value(230), run_time=460, rate_func=linear)
        packet.remove_updater(packet_updater)

        # FadeOut kết thúc Act 2
        objects_to_remove = [m for m in self.mobjects]
        self.play(FadeOut(Group(*objects_to_remove)), run_time=10)
        # Tổng Part 3: 20 + 5 + 460 + 10 = 495s
