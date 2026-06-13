import sys
import os
import numpy as np
sys.path.append(".")

from manim import *
from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene

class ReLuBarrier(StoryboardScene):
    """Scene 1: The Non-Linearity Wall - Aligned with Wei Ao's Tutorial
    Thời lượng cam kết: 900 giây (Chính xác 15 phút). Nền Navy Blue."""

    def construct(self):
        # Nền Navy Blue theo chuẩn giáo dục
        self.camera.background_color = "#001A33"
        
        # [00:00 - 00:15] Tiêu đề Intro (Chính xác 15 giây)
        self.title_main = Tex(r"\textbf{The Non-Linearity Wall: Polynomial Approximation}", font_size=48, color=WHITE)
        self.title_main.set_color_by_gradient(BLUE_B, TEAL_C)
        self.play(Write(self.title_main), run_time=5)
        self.play(self.title_main.animate.to_edge(UP).scale(0.8), run_time=5)
        self.wait(5)
        # Tổng thời gian đã qua: 15 giây
        
        self.cnn_to_fhe_transition()         # Chính xác 225 giây
        self.precision_vs_depth_tradeoff()   # Chính xác 250 giây
        self.polynomial_bases_and_cost()     # Chính xác 200 giây
        self.training_instability_and_norm() # Chính xác 210 giây
        # TỔNG CỘNG: 15 + 225 + 250 + 200 + 210 = 900 giây (15 phút)

    def safe_play_audio(self, filename):
        full_path = os.path.abspath(filename)
        if os.path.exists(full_path):
            self.add_sound(full_path)
            print(f"[AUDIO] Kích hoạt: {filename}")
        else:
            print(f"[WARNING] Thiếu file: {full_path}")

    def cnn_to_fhe_transition(self):
        """Phần 1: Thay thế ReLU bằng Đa thức (225 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_01_01.mp3") 
        
        # Mô phỏng Standard CNN Pipeline
        box_conv = Rectangle(width=2.5, height=1.5, color=BLUE_C).shift(LEFT*3.5)
        txt_conv = Tex("Conv", font_size=40).move_to(box_conv)
        box_bn = Rectangle(width=2.5, height=1.5, color=TEAL_C)
        txt_bn = Tex("BN", font_size=40).move_to(box_bn)
        box_relu = Rectangle(width=2.5, height=1.5, color=RED_C).shift(RIGHT*3.5)
        txt_relu = Tex("ReLU", font_size=40).move_to(box_relu)
        
        arr1 = Arrow(box_conv.get_right(), box_bn.get_left(), buff=0.1, color=WHITE)
        arr2 = Arrow(box_bn.get_right(), box_relu.get_left(), buff=0.1, color=WHITE)
        
        cnn_group = VGroup(box_conv, txt_conv, box_bn, txt_bn, box_relu, txt_relu, arr1, arr2)
        self.play(FadeIn(cnn_group, shift=UP), run_time=5)
        
        fhe_tools = MathTex(r"\text{FHE Operations: } \oplus \text{ (Add)}, \otimes \text{ (Mult)}, \circlearrowleft \text{ (Rot)}", font_size=40, color=YELLOW_C).shift(DOWN*2)
        self.play(Write(fhe_tools), run_time=5)
        self.wait(10)
        
        cross_relu = Cross(box_relu, stroke_color=RED, stroke_width=8)
        max_eq = MathTex(r"\max(0, x) \notin \mathbb{P}[x]", font_size=36, color=RED_B).next_to(box_relu, DOWN)
        self.play(Create(cross_relu), Write(max_eq), run_time=5)
        self.wait(5) 
        # (Subtotal: 30s - Đã khớp Audio 1)
        
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_01_02.mp3")
        
        # Chuyển đổi sang Polynomial Appx
        box_poly = Rectangle(width=2.5, height=1.5, color=GREEN_C).move_to(box_relu)
        txt_poly = Tex("Poly Appx", font_size=36).move_to(box_poly)
        
        self.play(
            FadeOut(VGroup(box_relu, txt_relu, cross_relu, max_eq)),
            FadeIn(VGroup(box_poly, txt_poly)),
            run_time=5
        )
        
        tradeoff = MathTex(r"\text{Trade-off: Multiplicative Depth } \leftrightarrow \text{ Precision}", font_size=45, color=YELLOW_C).shift(DOWN*2)
        self.play(TransformMatchingTex(fhe_tools, tradeoff), run_time=5)
        self.wait(20) 
        # (Subtotal: 30s - Đã khớp Audio 2)
        
        # Padding time bằng hạt dữ liệu chạy qua Pipeline (155 giây)
        tracker = ValueTracker(-5.5)
        data_packet = always_redraw(lambda: Rectangle(width=0.5, height=0.5, color=YELLOW, fill_opacity=0.8).move_to(
            [tracker.get_value(), 0, 0]
        ))
        self.add(data_packet)
        
        self.play(tracker.animate.set_value(5.5), run_time=77, rate_func=linear)
        self.play(tracker.animate.set_value(-5.5), run_time=78, rate_func=linear)
        
        # Lệnh dọn dẹp sạch sẽ màn hình để KHÔNG BỊ ĐÈ CHỮ (10s)
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 1: 30 + 30 + 77 + 78 + 10 = 225s

    def precision_vs_depth_tradeoff(self):
        """Phần 2: Trade-off Depth vs Precision (250 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_01_03.mp3") 
        
        axes = Axes(x_range=[-4, 4, 1], y_range=[-1, 4, 1], x_length=8, y_length=5, axis_config={"color": GREY_C})
        relu_graph = axes.plot(lambda x: max(0, x), color=WHITE, stroke_width=6)
        relu_lbl = Tex("ReLU", color=WHITE, font_size=36).next_to(relu_graph.get_end(), UP)
        
        self.play(Create(axes), Create(relu_graph), Write(relu_lbl), run_time=6)
        self.wait(14)
        
        # Low degree appx (Fast, Inaccurate)
        low_deg_graph = axes.plot(lambda x: 0.2*x**2 + 0.5*x + 0.3, color=RED_C, stroke_width=4)
        low_lbl = Tex("Low-Degree (Fast, Inaccurate)", color=RED_C, font_size=32).next_to(low_deg_graph.get_end(), DOWN).shift(LEFT*2.5)
        
        self.play(Create(low_deg_graph), Write(low_lbl), run_time=5)
        self.wait(5)
        
        # High degree appx (Slow, Accurate)
        high_deg_graph = axes.plot(lambda x: max(0, x) - 0.1*np.sin(x*10)*np.exp(-x**2), color=GREEN_C, stroke_width=4)
        high_lbl = Tex("High-Degree (Slow, Accurate)", color=GREEN_C, font_size=32).next_to(high_deg_graph.get_end(), LEFT).shift(UP*1.5)
        
        self.play(Create(high_deg_graph), Write(high_lbl), run_time=5)
        self.wait(5) 
        # (Subtotal: 40s - Khớp Audio 3)
        
        warning = Tex(r"\textbf{High Degree $\rightarrow$ Frequent Bootstrapping $\rightarrow$ High Latency}", color=YELLOW_C, font_size=36).to_edge(DOWN)
        self.play(Write(warning), run_time=5)
        
        # Padding time dao động quá trình Search Optimization (195s)
        var_tracker = ValueTracker(0)
        dynamic_appx = always_redraw(lambda: axes.plot(
            lambda x: max(0, x) - (0.5 * np.cos(var_tracker.get_value()) * np.exp(-0.5*x**2)),
            color=PURPLE_C, stroke_width=3
        ))
        self.add(dynamic_appx)
        
        self.play(var_tracker.animate.set_value(10 * np.pi), run_time=195, rate_func=smooth)
        
        # Dọn dẹp
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 2: 40 + 5 + 195 + 10 = 250s

    def polynomial_bases_and_cost(self):
        """Phần 3: Chọn Basis & Tính Toán Depth x^4 (200 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_01_04.mp3") 
        
        bases_title = Tex(r"Polynomial Bases", font_size=45, color=WHITE).to_edge(UP, buff=1.0)
        self.play(Write(bases_title), run_time=3)
        
        eq_power = MathTex(r"\text{Power: } \{1, x, x^2, x^3, \dots\}", font_size=40, color=GREY_A).shift(UP*1.2)
        eq_cheb = MathTex(r"\text{Chebyshev: } T_{n+1}(x) = 2x T_n(x) - T_{n-1}(x)", font_size=40, color=BLUE_C)
        eq_herm = MathTex(r"\text{Hermite: } H_{n+1}(x) = 2x H_n(x) - 2n H_{n-1}(x)", font_size=40, color=TEAL_C).shift(DOWN*1.2)
        
        self.play(FadeIn(eq_power), run_time=3)
        self.play(FadeIn(eq_cheb), run_time=3)
        self.play(FadeIn(eq_herm), run_time=3)
        self.wait(18) 
        # (Subtotal: 30s)
        
        self.play(FadeOut(VGroup(bases_title, eq_power, eq_cheb, eq_herm)), run_time=5)
        
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_01_05.mp3") 
        
        cost_title = Tex(r"Evaluation Cost $\neq$ Degree", font_size=45, color=YELLOW_C).shift(UP*2.5)
        self.play(Write(cost_title), run_time=4)
        
        naive = MathTex(r"x^4 = x \otimes x \otimes x \otimes x", r"\Rightarrow \text{Depth: 3}", font_size=45, color=RED_C).shift(UP*1)
        optimal = MathTex(r"x^4 = (x \otimes x) \otimes (x \otimes x)", r"\Rightarrow \text{Depth: 2}", font_size=45, color=GREEN_C).shift(DOWN*0.5)
        
        self.play(Write(naive[0]), run_time=3)
        self.play(Write(naive[1]), run_time=3)
        self.wait(2)
        
        self.play(Write(optimal[0]), run_time=4)
        self.play(Write(optimal[1]), Flash(optimal[1], color=GREEN), run_time=4)
        self.wait(10) 
        # (Subtotal: 30s)
        
        # Vẽ Computation Tree - Đã thu nhỏ và chỉnh tọa độ để KHÔNG BỊ CẮT RÌA (120s)
        node_x = Circle(radius=0.4, color=WHITE).shift(UP*1.5)
        txt_x = MathTex("x").move_to(node_x)
        node_x2 = Circle(radius=0.4, color=BLUE_C).shift(DOWN*0.5)
        txt_x2 = MathTex("x^2").move_to(node_x2)
        node_x4 = Circle(radius=0.4, color=GREEN_C).shift(DOWN*2.5)
        txt_x4 = MathTex("x^4").move_to(node_x4)
        
        arr1 = Arrow(node_x.get_bottom(), node_x2.get_top(), color=WHITE)
        arr2 = Arrow(node_x2.get_bottom(), node_x4.get_top(), color=WHITE)
        
        tree_group = VGroup(node_x, txt_x, node_x2, txt_x2, node_x4, txt_x4, arr1, arr2)
        
        # Shift phương trình sang trái, thu nhỏ cây và đặt ở bên phải một cách an toàn
        self.play(
            FadeIn(tree_group.scale(0.8).shift(RIGHT*3)), 
            naive.animate.shift(LEFT*3.5).scale(0.8), 
            optimal.animate.shift(LEFT*3.5).scale(0.8), 
            run_time=5
        )
        
        pulse_tracker = ValueTracker(0)
        def tree_updater(m):
            t = pulse_tracker.get_value()
            m.set_stroke(width=4 + 3*np.sin(t*5))
            m.set_color(interpolate_color(BLUE_C, GREEN_C, (np.sin(t*3)+1)/2))
            
        node_x4.add_updater(tree_updater)
        self.play(pulse_tracker.animate.set_value(50), run_time=120, rate_func=linear)
        node_x4.remove_updater(tree_updater)
        
        # Dọn dẹp màn hình
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)
        # Tổng Part 3: 30 + 5 + 30 + 5 + 120 + 10 = 200s

    def training_instability_and_norm(self):
        """Phần 4: Gradient Explosion & Basis-wise Normalization (210 giây)"""
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_01_06.mp3") 
        
        title = Tex(r"Training Low-Degree Polynomials", font_size=45, color=WHITE).to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=4)
        
        # Dịch chuyển đồ thị sang TRÁI để nhường chỗ an toàn cho công thức bên phải
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 100, 20], x_length=6, y_length=4.5, axis_config={"color": GREY_C}).shift(DOWN*0.5 + LEFT*2.5)
        self.play(Create(axes), run_time=4)
        
        grad_lbl = Tex(r"Gradients Explode", font_size=36, color=RED_C).next_to(axes, UP)
        self.play(Write(grad_lbl), run_time=3)
        
        grad_curve = axes.plot(lambda x: 1.5**x, color=RED_C, stroke_width=5)
        self.play(Create(grad_curve), run_time=6)
        self.wait(10) 
        # (Subtotal: 27s - Khớp Audio 6)
        
        self.safe_play_audio("assets/audio/02_fhe_cnn/02_01_07.mp3") 
        
        sol_title = Tex(r"Solution: Basis-wise Normalization", font_size=40, color=GREEN_C).next_to(title, DOWN)
        self.play(Write(sol_title), run_time=4)
        
        # Công thức đặt bên phải axes, kích thước chữ thu nhỏ để không bị cắt lề
        norm_eq = MathTex(
            r"f(x) = \sum_{i=1}^d w_i \cdot \text{Norm}(B_i(x))",
            font_size=36, color=YELLOW_C
        ).next_to(axes, RIGHT, buff=0.8)
        
        self.play(Write(norm_eq), run_time=6)
        self.wait(15) 
        # (Subtotal: 25s - Khớp Audio 7)
        
        stable_curve = axes.plot(lambda x: 10 * np.log(x+1) + 20, color=GREEN_C, stroke_width=5)
        stable_lbl = Tex(r"Stable Forward Prop", font_size=36, color=GREEN_C).move_to(grad_lbl)
        
        self.play(
            Transform(grad_curve, stable_curve),
            Transform(grad_lbl, stable_lbl),
            run_time=8
        )
        
        # Padding flow (140s)
        dots = VGroup(*[Dot(axes.c2p(0, 20), color=WHITE, radius=0.08) for _ in range(15)])
        self.add(dots)
        
        tracker = ValueTracker(0)
        def flow_updater(m):
            t = tracker.get_value()
            for i, dot in enumerate(m):
                x_val = (t * 2 - i * 0.5) % 10
                if x_val < 0: x_val = 0
                y_val = 10 * np.log(x_val + 1) + 20
                dot.move_to(axes.c2p(x_val, y_val))
                dot.set_opacity(min(1, x_val / 2))
                
        dots.add_updater(flow_updater)
        
        self.play(tracker.animate.set_value(50), run_time=140, rate_func=linear)
        dots.remove_updater(flow_updater)
        
        # Dọn dẹp lần cuối
        self.play(FadeOut(Group(*self.mobjects)), run_time=10)