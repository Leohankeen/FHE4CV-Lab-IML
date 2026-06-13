import sys
import os
import numpy as np
sys.path.append(".")

from manim import *
from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene

class PolynomialApproximation(StoryboardScene):
<<<<<<< HEAD
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
=======
    """Scene 2: Polynomial Approximation - Ultimate 3B1B Edition
    Thời lượng: 1200 giây (Chính xác 20 phút). Background Navy Blue."""

    def construct(self):
        # Background Navy Blue chuẩn giáo dục
        self.camera.background_color = "#001A33"

        # [00:00 - 00:15] Tiêu đề Intro (Chính xác 15 giây)
        self.title_main = Tex(r"\textbf{Bending the Curve: Polynomial Approximation}", font_size=48, color=WHITE)
        self.title_main.set_color_by_gradient(YELLOW_C, TEAL_C)
        self.play(Write(self.title_main), run_time=5)
        self.play(self.title_main.animate.to_edge(UP).scale(0.8), run_time=5)
        self.wait(5)
        # Tổng: 15s

        self.minimax_approximation()         # 300 giây (5 phút)
        self.multiplicative_depth_cost()     # 300 giây (5 phút)
        self.orthogonal_bases_autofhe()      # 300 giây (5 phút)
        self.imaginary_removing_bootstrap()  # 285 giây (4m 45s)
        # TỔNG CỘNG: 15 + 300 + 300 + 300 + 285 = 1200 giây (20 phút)

    def safe_play_audio(self, filename):
        full_path = os.path.abspath(filename)
        if os.path.exists(full_path):
            try:
                self.add_sound(full_path)
                print(f"[AUDIO] Kích hoạt: {filename}")
            except Exception as e:
                print(f"[ERROR] Lỗi audio: {e}")
        else:
            print(f"[WARNING] Thiếu file: {full_path}")

    def minimax_approximation(self):
        """Phần 1: Sự thất bại của Taylor & Minimax Appx (300 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_02_01.mp3")

        subtitle = Tex(r"2.1 Taylor Series vs Minimax Approximation", font_size=36, color=GREY_B).next_to(self.title_main, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        axes = Axes(x_range=[-3, 3, 1], y_range=[-1, 3, 1], x_length=6, y_length=4, axis_config={"color": GREY_C}).shift(DOWN * 0.5 + LEFT * 2.5)
        relu_graph = axes.plot(lambda x: max(0, x), color=WHITE, stroke_width=5, use_smoothing=False)
        relu_label = MathTex(r"\text{ReLU}(x)", color=WHITE).next_to(relu_graph, UP)
        
        self.play(Create(axes), Create(relu_graph), Write(relu_label), run_time=6)

        # Mô phỏng Taylor Series phân kỳ ở xa gốc tọa độ
        taylor_eq = MathTex(r"T(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(0)}{n!} x^n", font_size=36, color=RED_C).next_to(axes, RIGHT, buff=1).shift(UP*1)
        taylor_lbl = Tex(r"Taylor diverges outside $|x| < 1$", font_size=28, color=RED_B).next_to(taylor_eq, DOWN)
        taylor_graph = axes.plot(lambda x: 0.5*x + 0.25*x**2 - 0.05*x**4, color=RED_C, stroke_width=4)
        
        self.play(Write(taylor_eq), Write(taylor_lbl), Create(taylor_graph), run_time=5)
        self.wait(10) # 4 + 6 + 5 + 10 = 25s

        # Chuyển sang Minimax Approximation
        minimax_eq = MathTex(r"\min_{P \in \mathbb{P}_n} \max_{x \in [a,b]} |f(x) - P(x)|", font_size=36, color=GREEN_C).move_to(taylor_eq)
        minimax_lbl = Tex(r"Minimax minimizes worst-case error", font_size=28, color=GREEN_B).next_to(minimax_eq, DOWN)
        minimax_graph = axes.plot(lambda x: 0.125 * x**2 + 0.5 * x + 0.25, color=GREEN_C, stroke_width=4)

        self.play(
            ReplacementTransform(taylor_eq, minimax_eq),
            ReplacementTransform(taylor_lbl, minimax_lbl),
            ReplacementTransform(taylor_graph, minimax_graph),
            run_time=5
        )
        self.wait(10) # 25 + 15 = 40s (Đã hết Audio 1)

        # Padding (250s): Đồ thị Minimax uốn lượn tối ưu hóa
        tracker = ValueTracker(0)
        dynamic_poly = always_redraw(
            lambda: axes.plot(
                lambda x: (0.125 + 0.05 * np.sin(tracker.get_value())) * x**2 + 0.5 * x + (0.25 + 0.1 * np.cos(tracker.get_value())),
                color=YELLOW_D, stroke_width=3
            )
        )
        self.add(dynamic_poly)
        
        self.play(tracker.animate.set_value(15 * np.pi), run_time=250, rate_func=smooth)

        # Dọn dẹp
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 1: 40 + 250 + 10 = 300s

    def multiplicative_depth_cost(self):
        """Phần 2: Tính toán Multiplicative Depth (300 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_02_02.mp3")

        subtitle = Tex(r"2.2 Multiplicative Depth Cost", font_size=36, color=GREY_B).to_edge(UP, buff=1.0)
        self.play(FadeIn(subtitle), run_time=4)

        # Mô phỏng sự sai lệch giữa Degree và Cost
        cost_eq = MathTex(r"\text{Cost}(x^d) \neq d - 1", font_size=50, color=YELLOW_C).shift(UP*1.5)
        self.play(Write(cost_eq), run_time=4)
        self.wait(7) # 4 + 4 + 7 = 15s

        # Phương pháp tuần tự
        naive = MathTex(r"x^4 = x \otimes x \otimes x \otimes x", r"\Rightarrow \text{Depth: 3}", font_size=40, color=RED_C).shift(DOWN*0.5 + LEFT*2.5)
        optimal = MathTex(r"x^4 = (x \otimes x) \otimes (x \otimes x)", r"\Rightarrow \text{Depth: 2}", font_size=40, color=GREEN_C).shift(DOWN*0.5 + RIGHT*2.5)
        
        self.play(Write(naive), run_time=5)
        self.play(Write(optimal), run_time=5)
        self.wait(15) # 15 + 25 = 40s (Khớp Audio 2)

        # Padding (250s): Mô phỏng Modulus Chain (Thanh máu) cạn kiệt
        budget_box = Rectangle(width=6, height=0.5, color=WHITE).shift(DOWN*3)
        budget_fill = Rectangle(width=6, height=0.5, color=BLUE_D, fill_opacity=0.8).align_to(budget_box, LEFT)
        budget_lbl = Tex(r"Ciphertext Modulus Budget $q_L$", font_size=28, color=WHITE).next_to(budget_box, UP)
        
        self.play(Create(budget_box), FadeIn(budget_fill), Write(budget_lbl), run_time=5)

        budget_tracker = ValueTracker(6)
        budget_fill.add_updater(lambda m: m.become(
            Rectangle(width=max(0.01, budget_tracker.get_value()), height=0.5, color=BLUE_D, fill_opacity=0.8).align_to(budget_box, LEFT)
        ))

        # Hiệu ứng tiêu hao
        self.play(budget_tracker.animate.set_value(0.5), run_time=240, rate_func=linear)
        self.play(Flash(budget_box, color=RED, line_length=2), run_time=5)
        
        budget_fill.clear_updaters()
        
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 2: 40 + 5 + 240 + 5 + 10 = 300s

    def orthogonal_bases_autofhe(self):
        """Phần 3: Chebyshev Bases & AutoFHE (300 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_02_03.mp3")

        subtitle = Tex(r"2.3 Orthogonal Bases \& AutoFHE", font_size=36, color=GREY_B).to_edge(UP, buff=1.0)
        self.play(FadeIn(subtitle), run_time=4)

        # Công thức đệ quy của Chebyshev Polynomials
        cheb_def = MathTex(
            r"T_0(x) = 1 \\ T_1(x) = x \\ T_{n+1}(x) = 2x T_n(x) - T_{n-1}(x)", 
            font_size=36, color=BLUE_C
        ).shift(LEFT*3.5 + UP*1)
        self.play(Write(cheb_def), run_time=6)

        # Vẽ đồ thị Chebyshev
        axes = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5], x_length=5, y_length=4, axis_config={"color": GREY_C}).shift(RIGHT*3 + DOWN*0.5)
        self.play(Create(axes), run_time=5)
        
        t1 = axes.plot(lambda x: x, color=GREY_B)
        t2 = axes.plot(lambda x: 2*x**2 - 1, color=YELLOW_C)
        t3 = axes.plot(lambda x: 4*x**3 - 3*x, color=RED_C)
        t4 = axes.plot(lambda x: 8*x**4 - 8*x**2 + 1, color=GREEN_C)

        self.play(Create(t1), run_time=3)
        self.play(Create(t2), run_time=4)
        self.play(Create(t3), run_time=4)
        self.play(Create(t4), run_time=4)
        self.wait(10) # 4+6+5+3+4+4+4+10 = 40s (Khớp Audio 3)

        # Mô phỏng quá trình AutoFHE (250s)
        autofhe_lbl = Tex(r"AutoFHE: Layer-wise Degree Search", font_size=32, color=PURPLE_C).next_to(cheb_def, DOWN, buff=1.5)
        self.play(Write(autofhe_lbl), run_time=5)

        layer_boxes = VGroup(*[Rectangle(width=0.8, height=0.8, color=WHITE) for _ in range(5)]).arrange(RIGHT, buff=0.2).next_to(autofhe_lbl, DOWN)
        degrees = VGroup(*[MathTex(str(d), font_size=28) for d in [2, 6, 4, 8, 2]])
        for box, deg in zip(layer_boxes, degrees):
            deg.move_to(box)
        
        self.play(FadeIn(layer_boxes), run_time=5)

        # Chạy thay đổi degree liên tục
        pulse_tracker = ValueTracker(0)
        def layer_updater(m):
            t = pulse_tracker.get_value()
            for i, box in enumerate(m):
                # Thay đổi màu và hiển thị ngẫu nhiên độ sâu
                box.set_color(interpolate_color(BLUE_C, RED_C, (np.sin(t*2 + i)+1)/2))

        layer_boxes.add_updater(layer_updater)
        self.play(FadeIn(degrees), run_time=5)
        
        # Padding time
        self.play(pulse_tracker.animate.set_value(50), run_time=225, rate_func=linear)
        layer_boxes.remove_updater(layer_updater)

        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 3: 40 + 5 + 5 + 5 + 225 + 10 = 290s + 10s wait = 300s
        self.wait(10)

    def imaginary_removing_bootstrap(self):
        """Phần 4: Imaginary-Removing Bootstrapping (285 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_02_04.mp3")

        subtitle = Tex(r"2.4 Imaginary-Removing Bootstrapping", font_size=36, color=GREY_B).to_edge(UP, buff=1.0)
        self.play(FadeIn(subtitle), run_time=4)

        # Vẽ Complex Plane (Trục thực và ảo)
        complex_plane = Axes(
            x_range=[-6, 6], y_range=[-3, 3], x_length=9, y_length=4.5, 
            axis_config={"color": GREY_D}, 
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False}
        ).shift(DOWN*0.5)
        
        real_label = Tex(r"Real Subspace (Data)", font_size=28, color=BLUE_C).next_to(complex_plane.x_axis.get_end(), UP, buff=0.1)
        imag_label = Tex(r"Imaginary (Noise)", font_size=28, color=RED_C).next_to(complex_plane.y_axis.get_end(), RIGHT, buff=0.1)
        
        self.play(Create(complex_plane), Write(real_label), Write(imag_label), run_time=6)

        # Phương trình Cleansing
        cleanse_eq = MathTex(r"\text{Re}(c) = \frac{c + \bar{c}}{2}", font_size=40, color=GREEN_C).to_corner(UR).shift(DOWN*1)
        self.play(Write(cleanse_eq), run_time=5)
        self.wait(25) # 4 + 6 + 5 + 25 = 40s (Khớp Audio 4)

        # Cổng chiếu Laser (Projection Gate)
        laser_gate = Line(complex_plane.c2p(2, 3), complex_plane.c2p(2, -3), color=GREEN_C, stroke_width=8)
        gate_lbl = Tex(r"Projection Gate", font_size=28, color=GREEN_C).next_to(laser_gate, UP)
        self.play(Create(laser_gate), Write(gate_lbl), run_time=5)

        # Hạt dữ liệu bị nhiễu (230s padding)
        num_particles = 60
        particles = VGroup(*[Dot(radius=0.08, color=BLUE_C) for _ in range(num_particles)])
        self.add(particles)

        time_tracker = ValueTracker(0)
        def particle_flow_updater(m):
            t = time_tracker.get_value()
            for i, dot in enumerate(m):
                # Data đi từ trái sang phải
                x_val = -6 + ((t * 1.5 + i * 0.4) % 12)
                
                if x_val < 2:
                    # Trước gate: Nhiễu ảo tăng dần (Trôi lên trục Y)
                    noise_amp = max(0, x_val + 6) * 0.35
                    y_val = np.sin(t * 4 + i) * noise_amp
                    dot.set_color(interpolate_color(BLUE_C, RED_C, min(1, noise_amp/2))) 
                else:
                    # Sau gate: Phép chiếu ép chặt về trục hoành (Data sạch)
                    y_val = 0
                    dot.set_color(BLUE_C) 
                    
                dot.move_to(complex_plane.c2p(x_val, y_val))

        particles.add_updater(particle_flow_updater)

        # Chạy hạt flow cực dài để đủ thời lượng 285s
        self.play(time_tracker.animate.set_value(150), run_time=230, rate_func=linear)
        particles.remove_updater(particle_flow_updater)
        
        # FadeOut kết thúc Scene
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
>>>>>>> feature/act2-fhe-cnn
