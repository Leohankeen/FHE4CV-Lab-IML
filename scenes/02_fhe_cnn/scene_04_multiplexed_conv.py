import sys
import os
import numpy as np
sys.path.append(".")

from manim import *
from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene

class MultiplexedPacking(StoryboardScene):
    """25-minute lesson: Multiplexed packing and parallel convolutions.
    Total duration strictly managed to 1500 seconds (25 minutes)."""

    def construct(self):
        self.camera.background_color = "#101214"

        # Tiêu đề với hiệu ứng mượt mà (15 giây)
        title = Tex(r"\textbf{Multiplexed Parallel Convolutions}", font_size=42, color=WHITE)
        self.play(Write(title), run_time=5)
        self.play(title.animate.to_edge(UP).scale(0.8), run_time=5)
        self.wait(5)

        # 3 Phân đoạn chính, mỗi phân đoạn chính xác 495 giây
        self.multiplexed_packing(title)
        self.rotation_reduction(title)
        self.deep_resnet_flow(title)

    def play_audio(self, filename):
        full_path = os.path.abspath(filename)
        if os.path.exists(full_path):
            try:
                self.add_sound(full_path)
                print(f"\n[SUCCESS] Loaded Audio: {full_path}\n")
            except Exception as e:
                print(f"\n[ERROR] Audio issue: {e}\n")
        else:
            print(f"\n[CRITICAL] MISSING AUDIO: {full_path}\n")

    def multiplexed_packing(self, title):
        """Phần 4.1: Đóng gói dồn kênh (495 giây)"""
        self.play_audio("assets/audio/02_fhe_cnn/02_04_01.mp3")

        subtitle = Tex(r"4.1 Convert loose feature maps into a dense slot layout", font_size=28, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=5)

        # Hiển thị 4 Feature Maps
        colors = [RED_C, GREEN_C, BLUE_C, YELLOW_C]
        feature_maps = VGroup()
        for index, color in enumerate(colors):
            grid = VGroup(*[
                Square(side_length=0.24, stroke_color=color, stroke_width=1).set_fill(color, opacity=0.3 + 0.1 * ((i + index) % 3))
                for i in range(16)
            ]).arrange_in_grid(rows=4, cols=4, buff=0.05)
            frame = SurroundingRectangle(grid, color=color, buff=0.05)
            # FIX: Tách ghép chuỗi để tránh f-string nuốt ký tự
            label = Tex("Channel " + str(index + 1), font_size=20, color=color).next_to(frame, DOWN, buff=0.1)
            feature_maps.add(VGroup(frame, grid, label))
            
        feature_maps.arrange(RIGHT, buff=0.5).shift(UP * 1.5)
        self.play(LaggedStart(*(FadeIn(fm, shift=UP) for fm in feature_maps), lag_ratio=0.2), run_time=5)

        # Chuyển thành dải vector đan xen (Interleaving)
        strip = VGroup(*[
            Square(side_length=0.25, stroke_color=colors[i % 4], stroke_width=1).set_fill(colors[i % 4], opacity=0.8)
            for i in range(32)
        ]).arrange(RIGHT, buff=0.02).shift(DOWN * 0.5)
        
        strip_label = Tex(r"Interleaved Spatial \& Channel Segments", font_size=28, color=COLOR_MATH).next_to(strip, DOWN, buff=0.2)

        self.play(ReplacementTransform(feature_maps.copy(), strip), FadeIn(strip_label), run_time=5)

        # Dense Utilization
        utilization = Tex(r"\textbf{Dense Slot Utilization: } $\approx 100\%$", font_size=36, color=GREEN_C).shift(DOWN * 2.5)
        self.play(Write(utilization), Flash(strip, color=GREEN_C), run_time=5)

        # Mô phỏng dòng chảy dữ liệu
        ambient_title = Tex(r"Continuous Multiplexed Data Stream", font_size=24, color=GREY_A).to_edge(DOWN)
        self.play(FadeIn(ambient_title), run_time=5)

        stream_tracker = ValueTracker(0)
        dots = VGroup(*[Dot(radius=0.08) for _ in range(40)])
        self.add(dots)

        def stream_updater(m):
            t = stream_tracker.get_value()
            for i, dot in enumerate(m):
                channel = i % 4
                dot.set_color(colors[channel])
                start_x = -3 + channel * 2
                start_y = 3
                progress = (t * 2 + i * 0.1) % 5
                
                if progress < 2:
                    y_val = start_y - progress
                    x_val = start_x
                else:
                    x_val = start_x + (progress - 2) * 3
                    y_val = 1 - (progress - 2) * 0.5
                    
                dot.move_to(np.array([x_val, y_val, 0]))

        dots.add_updater(stream_updater)
        
        self.play(stream_tracker.animate.set_value(230), run_time=460, rate_func=linear)
        dots.remove_updater(stream_updater)

        self.play(FadeOut(VGroup(subtitle, feature_maps, strip, strip_label, utilization, ambient_title, dots)), run_time=5)

    def rotation_reduction(self, title):
        """Phần 4.2: Giảm thiểu phép xoay Rotation (495 giây)"""
        self.play_audio("assets/audio/02_fhe_cnn/02_04_02.mp3")

        subtitle = Tex(r"4.2 Make one rotation align several channels together", font_size=28, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=5)

        naive_box = Rectangle(width=3, height=1, color=RED_A, fill_opacity=0.2).shift(LEFT * 4 + UP * 1.5)
        naive_txt = Tex(r"Naive Layout \\ $N$ Rotations", font_size=24, color=RED_A).move_to(naive_box)
        
        packed_box = Rectangle(width=3, height=1, color=GREEN_C, fill_opacity=0.2).shift(LEFT * 4 + DOWN * 1.5)
        packed_txt = Tex(r"MPCNN Packed \\ $1$ Shared Rotation", font_size=24, color=GREEN_C).move_to(packed_box)

        self.play(FadeIn(VGroup(naive_box, naive_txt)), run_time=5)
        self.play(FadeIn(VGroup(packed_box, packed_txt)), run_time=5)

        chart_origin = RIGHT * 2 + DOWN * 2
        chart_axes = VGroup(
            Line(chart_origin, chart_origin + UP * 4, color=GREY_C),
            Line(chart_origin, chart_origin + RIGHT * 4, color=GREY_C)
        )
        naive_bar = Rectangle(width=1, height=3.5, color=RED_A, fill_opacity=0.8).move_to(chart_origin + RIGHT*1 + UP*1.75)
        mpcnn_bar = Rectangle(width=1, height=1.33, color=GREEN_C, fill_opacity=0.8).move_to(chart_origin + RIGHT*3 + UP*0.66)
        
        result_txt = Tex(r"\textbf{Rotations: 38\% of Naive}", font_size=28, color=GREEN_C).next_to(chart_axes, UP)

        self.play(Create(chart_axes), run_time=2)
        self.play(GrowFromEdge(naive_bar, DOWN), GrowFromEdge(mpcnn_bar, DOWN), run_time=3)
        self.play(Write(result_txt), run_time=5)

        gear_tracker = ValueTracker(0)
        
        def draw_gears(t):
            gears = VGroup()
            for i in range(4):
                gear = RegularPolygon(n=8, radius=0.4, color=RED_B, stroke_width=4).shift(LEFT*1 + UP*(2.5 - i*1.2))
                gear.rotate(t * (1 + i*0.2))
                gears.add(gear)
            
            big_gear = RegularPolygon(n=12, radius=1.5, color=GREEN_C, stroke_width=6).shift(LEFT*4 + DOWN*1.5)
            big_gear.rotate(t)
            gears.add(big_gear)
            return gears

        dynamic_gears = always_redraw(lambda: draw_gears(gear_tracker.get_value()))
        self.add(dynamic_gears)

        ambient_title = Tex(r"Algorithmic Synchronization of Ciphertext Rotations", font_size=24, color=GREY_A).to_edge(DOWN)
        self.play(FadeIn(ambient_title), run_time=5)

        self.play(gear_tracker.animate.set_value(200), run_time=455, rate_func=linear)
        self.play(FadeOut(VGroup(subtitle, naive_box, naive_txt, packed_box, packed_txt, chart_axes, naive_bar, mpcnn_bar, result_txt, ambient_title, dynamic_gears)), run_time=5)

    def deep_resnet_flow(self, title):
        """Phần 4.3: Luồng ResNet sâu (495 giây)"""
        self.play_audio("assets/audio/02_fhe_cnn/02_04_03.mp3")

        subtitle = Tex(r"4.3 Coordinate packing, levels and refresh across ResNet", font_size=28, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=5)

        blocks = VGroup(*[
            RoundedRectangle(width=1.5, height=1.5, corner_radius=0.2, color=BLUE_D, fill_opacity=0.3)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.5).shift(UP * 0.5)
        
        # FIX TRỌNG TÂM: Khắc phục lỗi LaTeX '\1' bằng cách dùng ghép chuỗi thông thường
        block_labels = VGroup(*[
            Tex(r"ResBlock \\ " + str(i+1), font_size=20, color=WHITE).move_to(blocks[i])
            for i in range(5)
        ])

        arrows = VGroup(*[
            Arrow(blocks[i].get_right(), blocks[i+1].get_left(), buff=0.1, color=GREY_B)
            for i in range(4)
        ])

        self.play(FadeIn(blocks), FadeIn(block_labels), LaggedStart(*(GrowArrow(a) for a in arrows), lag_ratio=0.2), run_time=5)

        badges = VGroup(
            Tex(r"\textbf{ResNet-20 \& ResNet-110}", font_size=32, color=BLUE_C),
            Tex(r"128-bit Security Target", font_size=28, color=GREEN_C),
            Tex(r"\textbf{Reported Speedup: 4.67x}", font_size=32, color=YELLOW_C),
        ).arrange(DOWN, buff=0.3).shift(DOWN * 2)

        self.play(LaggedStart(*(FadeIn(b, shift=UP*0.2) for b in badges), lag_ratio=0.3), run_time=5)

        packet_tracker = ValueTracker(0)
        packet = RoundedRectangle(width=0.6, height=0.6, corner_radius=0.1, color=GREEN_A, fill_opacity=1)
        self.add(packet)

        def packet_updater(m):
            t = packet_tracker.get_value()
            x_pos = -6 + (t % 12)
            y_pos = 0.5
            m.move_to(np.array([x_pos, y_pos, 0]))
            
            noise_level = (x_pos % 2) / 2.0  
            interpolated_color = interpolate_color(GREEN_A, RED_C, noise_level)
            m.set_color(interpolated_color)

        packet.add_updater(packet_updater)

        ambient_title = Tex(r"Imaginary-Removing Bootstrapping refreshing Cryptographic Noise", font_size=24, color=GREY_A).to_edge(DOWN)
        self.play(FadeIn(ambient_title), run_time=5)

        self.play(packet_tracker.animate.set_value(200), run_time=460, rate_func=linear)
        packet.remove_updater(packet_updater)

        objects_to_remove = [m for m in self.mobjects]
        self.play(FadeOut(Group(*objects_to_remove)), run_time=10)