import sys
import os
import numpy as np
sys.path.append(".")

from manim import *
from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene

class PolynomialApproximation(StoryboardScene):
    """20-minute lesson: Polynomial activations and stable bootstrapping (3B1B Style)."""

    def construct(self):
        self.camera.background_color = "#101214"

        title = Tex(r"\textbf{Bending the Curve: Polynomial Approximation}", font_size=42, color=WHITE)
        self.play(Write(title), run_time=5)
        self.play(title.animate.to_edge(UP).scale(0.8), run_time=5)

        self.polynomial_replacement(title)
        self.degree_tradeoff(title)
        self.imaginary_removing_bootstrap(title)

    def play_audio(self, filename):
        """Cơ chế bắt lỗi Audio và lấy đường dẫn tuyệt đối"""
        full_path = os.path.abspath(filename)
        if os.path.exists(full_path):
            try:
                self.add_sound(full_path)
                print(f"\n[SUCCESS] Đã chèn Audio thành công: {full_path}\n")
            except Exception as e:
                print(f"\n[ERROR] Lỗi khi chèn Audio Manim: {e}\n")
        else:
            print(f"\n[CRITICAL WARNING] KHÔNG TÌM THẤY FILE AUDIO: {full_path}")
            print(f"-> Vui lòng chạy lại scripts/generate_audio.py\n")

    def polynomial_replacement(self, title):
        # Gọi Audio phân đoạn 1
        self.play_audio("assets/audio/02_fhe_cnn/02_02_01.mp3")

        subtitle = Tex(r"2.1 Replace comparison with arithmetic approximation", font_size=32, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        axes = Axes(x_range=[-3, 3, 1], y_range=[-1, 3, 1], x_length=6.5, y_length=4, axis_config={"color": GREY_C}).shift(DOWN * 0.5)
        relu_graph = axes.plot(lambda x: max(0, x), color=RED_C, use_smoothing=False)
        relu_label = MathTex(r"\max(0, x)", color=RED_C).next_to(relu_graph, UP)
        
        self.play(Create(axes), run_time=3)
        self.play(Create(relu_graph), Write(relu_label), run_time=3)

        poly_formula = MathTex(r"P(x) = c_0 + c_1 x + c_2 x^2 + \dots + c_n x^n", font_size=36, color=COLOR_ENCRYPTION).to_corner(UR).shift(DOWN * 1)
        self.play(Write(poly_formula), run_time=3)

        poly_graph = axes.plot(lambda x: 0.125 * x**2 + 0.5 * x + 0.25, color=COLOR_ENCRYPTION)
        poly_label = MathTex(r"P(x)", color=COLOR_ENCRYPTION).next_to(poly_graph, UP)

        self.play(ReplacementTransform(relu_graph, poly_graph), ReplacementTransform(relu_label, poly_label), run_time=4)

        # Hoạt ảnh Search (Padding thời gian)
        tracker = ValueTracker(0)
        dynamic_poly = always_redraw(
            lambda: axes.plot(
                lambda x: (0.125 + 0.05 * np.sin(tracker.get_value())) * x**2 + 0.5 * x + (0.25 + 0.1 * np.cos(tracker.get_value())),
                color=YELLOW_C
            )
        )
        self.add(dynamic_poly)
        self.remove(poly_graph)

        ambient_text = Tex(r"Continuous search for optimal coefficients $c_i$", font_size=28, color=GREY_A).next_to(axes, DOWN)
        self.play(FadeIn(ambient_text), run_time=3)
        self.play(tracker.animate.set_value(100), run_time=387, rate_func=linear)

        self.play(FadeOut(VGroup(subtitle, axes, dynamic_poly, poly_label, poly_formula, ambient_text)), run_time=3)

    def degree_tradeoff(self, title):
        # Gọi Audio phân đoạn 2
        self.play_audio("assets/audio/02_fhe_cnn/02_02_02.mp3")

        subtitle = Tex(r"2.2 AutoFHE: Balancing Accuracy and Multiplicative Depth", font_size=32, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=3)

        axes = Axes(x_range=[-3, 3, 1], y_range=[-1, 3, 1], x_length=5, y_length=3.5, axis_config={"color": GREY_C}).shift(LEFT * 2.5 + DOWN * 0.5)
        relu_ref = axes.plot(lambda x: max(0, x), color=GREY_C, stroke_opacity=0.5, use_smoothing=False)
        self.play(Create(axes), FadeIn(relu_ref), run_time=3)

        def create_meter(label, fill_ratio, color):
            g = VGroup()
            text = Tex(label, font_size=24, color=WHITE)
            track = Rectangle(width=3.5, height=0.2, color=GREY_C, fill_opacity=0.2)
            fill = Rectangle(width=3.5 * fill_ratio, height=0.2, color=color, fill_opacity=0.8, stroke_width=0).align_to(track, LEFT)
            bar = VGroup(track, fill)
            g.add(text, bar)
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            return g

        meter2 = create_meter("Degree 2 (Low Depth)", 0.3, BLUE_C)
        meter4 = create_meter("Degree 4 (Medium Depth)", 0.6, GREEN_C)
        meter6 = create_meter("Degree 6 (High Depth!)", 0.9, RED_C)
        meters = VGroup(meter2, meter4, meter6).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(RIGHT * 3.5 + DOWN * 0.5)

        p2 = axes.plot(lambda x: 0.13 * x**2 + 0.5 * x + 0.22, color=BLUE_C)
        self.play(Create(p2), FadeIn(meter2), run_time=3)

        p4 = axes.plot(lambda x: -0.012 * x**4 + 0.14 * x**2 + 0.52 * x + 0.20, color=GREEN_C)
        self.play(ReplacementTransform(p2, p4), FadeIn(meter4), run_time=3)

        p6 = axes.plot(lambda x: 0.002 * x**6 - 0.018 * x**4 + 0.13 * x**2 + 0.5 * x + 0.18, color=RED_C)
        self.play(ReplacementTransform(p4, p6), FadeIn(meter6), run_time=3)
        self.play(Flash(meter6[1][1], color=RED), run_time=3)

        ambient_title = Tex(r"AutoFHE navigating the Loss Landscape", font_size=28, color=GREY_A).next_to(axes, DOWN)
        self.play(FadeIn(ambient_title), run_time=3)

        loss_axes = Axes(x_range=[0, 10], y_range=[0, 10], x_length=4, y_length=2, axis_config={"color": GREY_E}).move_to(p6.get_center())
        loss_curve = loss_axes.plot(lambda x: 8 * np.exp(-0.2*x) + 1.5 * np.sin(2*x) + 2, color=YELLOW_E)
        loss_dot = Dot(color=WHITE)
        
        self.play(FadeIn(loss_axes), FadeIn(loss_curve), run_time=3)

        loss_tracker = ValueTracker(0)
        loss_dot.add_updater(lambda m: m.move_to(loss_axes.c2p(loss_tracker.get_value(), 8 * np.exp(-0.2*loss_tracker.get_value()) + 1.5 * np.sin(2*loss_tracker.get_value()) + 2)))
        self.add(loss_dot)

        self.play(loss_tracker.animate.set_value(10), run_time=388, rate_func=there_and_back)
        loss_dot.clear_updaters()

        self.play(FadeOut(VGroup(subtitle, axes, relu_ref, p6, meters, ambient_title, loss_axes, loss_curve, loss_dot)), run_time=5)

    def imaginary_removing_bootstrap(self, title):
        # Gọi Audio phân đoạn 3
        self.play_audio("assets/audio/02_fhe_cnn/02_02_03.mp3")

        subtitle = Tex(r"2.3 Imaginary-Removing Bootstrapping", font_size=32, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=3)

        complex_plane = Axes(x_range=[-5, 5], y_range=[-3, 3], x_length=8, y_length=5, 
                             axis_config={"color": GREY_C}, 
                             x_axis_config={"include_ticks": False},
                             y_axis_config={"include_ticks": False}).shift(DOWN*0.5)
        
        real_label = Tex(r"Real Subspace (Data)", font_size=24, color=BLUE_C).next_to(complex_plane.x_axis.get_end(), UP)
        imag_label = Tex(r"Imaginary (Noise)", font_size=24, color=RED_C).next_to(complex_plane.y_axis.get_end(), RIGHT)
        
        self.play(Create(complex_plane), Write(real_label), Write(imag_label), run_time=4)

        laser_gate = Line(complex_plane.c2p(2, 3), complex_plane.c2p(2, -3), color=GREEN_C, stroke_width=6)
        gate_lbl = Tex(r"Bootstrapping \\ Projection", font_size=24, color=GREEN_C).next_to(laser_gate, UP)
        self.play(Create(laser_gate), Write(gate_lbl), run_time=3)

        num_particles = 40
        particles = VGroup(*[Dot(radius=0.06, color=BLUE_C) for _ in range(num_particles)])
        self.add(particles)

        time_tracker = ValueTracker(0)
        def particle_flow_updater(m):
            t = time_tracker.get_value()
            for i, dot in enumerate(m):
                x_val = -5 + ((t * 1.5 + i * 0.4) % 10)
                if x_val < 2:
                    noise_amp = max(0, x_val + 5) * 0.3
                    y_val = np.sin(t * 3 + i) * noise_amp
                    dot.set_color(RED_B) 
                else:
                    y_val = 0
                    dot.set_color(BLUE_C) 
                dot.move_to(complex_plane.c2p(x_val, y_val))

        particles.add_updater(particle_flow_updater)

        self.play(time_tracker.animate.set_value(200), run_time=340, rate_func=linear)
        particles.remove_updater(particle_flow_updater)
        
        objects_to_remove = [m for m in self.mobjects]
        self.play(FadeOut(Group(*objects_to_remove)), run_time=10)