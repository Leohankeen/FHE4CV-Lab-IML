import sys
import os
import random
import numpy as np
sys.path.append(".")

from manim import *
from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene

class ReLuBarrier(StoryboardScene):
    """Scene 1: The Non-Linearity Wall - 3Blue1Brown Style
    Đảm bảo thời lượng chuẩn 15 phút (900 giây) không đè âm thanh."""

    def construct(self):
        self.camera.background_color = "#101214"
        
        # Tiêu đề với hiệu ứng mượt mà (10 giây)
        title = Tex(r"\textbf{The Non-Linearity Wall}", font_size=48, color=WHITE)
        self.play(Write(title), run_time=5)
        self.play(title.animate.to_edge(UP).scale(0.8), run_time=5)
        
        # 3 Phân đoạn chính: Mỗi phân đoạn chiếm chính xác 296 giây
        # Tổng thời gian: 10 + (296 * 3) = 898 giây (~15 phút)
        self.linear_collapse_and_relu(title)
        self.fhe_polynomial_ring(title)
        self.the_blind_server_barrier(title)

    def play_audio(self, filename):
        """Hàm an toàn để thêm âm thanh, tránh crash nếu file chưa được generate."""
        if os.path.exists(filename):
            self.add_sound(filename)
        else:
            print(f"[WARNING] Thiếu file audio: {filename}. Hãy chạy scripts/generate_audio.py")

    def linear_collapse_and_relu(self, title):
        """Phần 1: Sự sụp đổ tuyến tính & ReLU (296 giây)"""
        
        # --- AUDIO 1: Khái niệm Convolution (Cấp phát 30 giây) ---
        self.play_audio("assets/audio/02_fhe_cnn/02_01_01.mp3")

        matrix_data = [["X_{11}", "X_{12}"], ["X_{21}", "X_{22}"]]
        matrix = Matrix(matrix_data, left_bracket="[", right_bracket="]").shift(LEFT*3.5 + UP*0.5)
        matrix.set_color(BLUE_C)
        matrix_label = Tex(r"Image Patch", font_size=24, color=BLUE_B).next_to(matrix, DOWN)
        
        weights_data = [["W_{11}", "W_{12}"], ["W_{21}", "W_{22}"]]
        weights = Matrix(weights_data, left_bracket="[", right_bracket="]").shift(RIGHT*3.5 + UP*0.5)
        weights.set_color(YELLOW_C)
        weights_label = Tex(r"Kernel Weights", font_size=24, color=YELLOW_B).next_to(weights, DOWN)
        op_star = MathTex(r"\star", font_size=40).move_to(ORIGIN + UP*0.5)
        
        self.play(FadeIn(matrix), Write(matrix_label), run_time=5)
        self.play(Write(op_star), run_time=2)
        self.play(FadeIn(weights), Write(weights_label), run_time=5)
        
        eq_transform = MathTex(r"=", r"X_{11}W_{11}", r"+", r"X_{12}W_{12}", r"+", r"\dots", r"+", r"b", font_size=36)
        eq_transform.shift(DOWN*2).set_color_by_tex("X", BLUE_C).set_color_by_tex("W", YELLOW_C)
        self.play(TransformFromCopy(VGroup(matrix, op_star, weights), eq_transform), run_time=8)
        
        linear_eq = MathTex(r"y = \mathbf{W}^T \mathbf{x} + b", font_size=48).move_to(eq_transform)
        linear_eq[0][2].set_color(YELLOW_C)  # W
        linear_eq[0][4].set_color(BLUE_C)    # x
        self.play(TransformMatchingShapes(eq_transform, linear_eq), run_time=5)
        self.wait(5) # Đủ 30 giây
        
        # --- AUDIO 2: Sự sụp đổ tuyến tính (Cấp phát 30 giây) ---
        self.play_audio("assets/audio/02_fhe_cnn/02_01_02.mp3")
        self.play(FadeOut(VGroup(matrix, matrix_label, weights, weights_label, op_star)), linear_eq.animate.to_corner(UR).scale(0.8), run_time=4)
        
        axes = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=6, y_length=5, axis_config={"color": GREY_B}).shift(LEFT*1.5 + DOWN*0.5)
        self.play(Create(axes), run_time=4)

        line1 = axes.plot(lambda x: 0.5*x + 0.5, color=BLUE)
        line2 = axes.plot(lambda x: -0.8*(0.5*x + 0.5) + 1, color=TEAL)
        line3 = axes.plot(lambda x: 1.2*(-0.8*(0.5*x + 0.5) + 1) - 0.5, color=YELLOW)
        
        label_l1 = MathTex(r"Layer_1", font_size=24, color=BLUE).next_to(line1, UP, buff=0.1)
        self.play(Create(line1), Write(label_l1), run_time=6)
        self.play(Transform(line1, line2), Transform(label_l1, MathTex(r"Layer_2", font_size=24, color=TEAL).next_to(line2, UP, buff=0.1)), run_time=6)
        self.play(Transform(line1, line3), Transform(label_l1, MathTex(r"Deep \ Layer", font_size=24, color=YELLOW).next_to(line3, UP, buff=0.1)), run_time=6)
        
        collapse_text = Tex(r"Remains a single line!", font_size=32, color=RED_C).next_to(axes, RIGHT)
        self.play(Write(collapse_text), run_time=4)
        
        # --- AUDIO 3: Giới thiệu ReLU (Cấp phát 36 giây) ---
        self.play_audio("assets/audio/02_fhe_cnn/02_01_03.mp3")
        self.play(FadeOut(collapse_text), FadeOut(label_l1), run_time=3)
        
        relu_graph = axes.plot(lambda x: max(0, x), color=RED_C, stroke_width=5)
        relu_formula = MathTex(r"\text{ReLU}(x) = \max(0, x)", color=RED_C).next_to(axes, RIGHT).shift(UP)
        self.play(ReplacementTransform(line1, relu_graph), Write(relu_formula), run_time=5)
        
        dot = Dot(color=WHITE)
        self.play(MoveAlongPath(dot, relu_graph), run_time=8, rate_func=there_and_back)
        self.play(FadeOut(VGroup(axes, relu_graph, relu_formula, dot, linear_eq)), run_time=5)
        self.wait(15) # Đủ 36 giây

        # --- ĐỈNH CAO 3B1B: HOẠT ẢNH BẺ CONG KHÔNG GIAN (200 giây) ---
        # Lấp đầy 200 giây bằng đồ thị không gian động để người xem chiêm nghiệm
        ambient_title = Tex(r"Geometric Intuition of Non-Linearity", color=GREY_A).to_edge(DOWN)
        self.play(FadeIn(ambient_title), run_time=5)

        plane_tracker = ValueTracker(0)
        # Sử dụng always_redraw để bẻ gập mặt phẳng tọa độ (Space Folding)
        space_plane = always_redraw(
            lambda: NumberPlane(
                x_range=[-6, 6, 1], y_range=[-4, 4, 1],
                background_line_style={"stroke_opacity": 0.4, "stroke_color": BLUE_E}
            ).apply_function(
                lambda p: np.array([p[0], p[1] * (1 - plane_tracker.get_value()) if p[1] < 0 else p[1], 0])
            )
        )
        self.add(space_plane)
        
        # Animation từ từ bẻ cong không gian trong 185 giây
        self.play(plane_tracker.animate.set_value(1), run_time=185, rate_func=there_and_back)
        
        self.play(FadeOut(space_plane), FadeOut(ambient_title), run_time=10)
        # ----------------------------------------------------

    def fhe_polynomial_ring(self, title):
        """Phần 2: Miền FHE vành đa thức (296 giây)"""
        
        # --- AUDIO 4: Scalar -> FHE (Cấp phát 25 giây) ---
        self.play_audio("assets/audio/02_fhe_cnn/02_01_04.mp3")
        scalar_x = MathTex(r"x = 0.75", font_size=50, color=BLUE_C).shift(LEFT*4)
        scalar_lbl = Tex(r"Plaintext Scalar", font_size=24, color=BLUE_B).next_to(scalar_x, DOWN)
        self.play(FadeIn(scalar_x), Write(scalar_lbl), run_time=5)
        self.wait(20)

        # --- AUDIO 5: Đặc tính đa thức (Cấp phát 40 giây) ---
        self.play_audio("assets/audio/02_fhe_cnn/02_01_05.mp3")
        arrow = Arrow(LEFT*2, RIGHT*0, color=YELLOW)
        enc_lbl = Tex(r"CKKS Encode \& Encrypt", font_size=24, color=YELLOW).next_to(arrow, UP)
        self.play(GrowArrow(arrow), Write(enc_lbl), run_time=5)

        poly_ring = MathTex(r"c_0(X) = a_0 + a_1 X + a_2 X^2 + \dots + a_{N-1} X^{N-1}", font_size=36, color=RED_C)
        poly_ring2 = MathTex(r"c_1(X) = b_0 + b_1 X + b_2 X^2 + \dots + b_{N-1} X^{N-1}", font_size=36, color=RED_C)
        cipher_group = VGroup(poly_ring, poly_ring2).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT*2.5)
        ring_def = MathTex(r"c_0, c_1 \in \mathcal{R}_q = \mathbb{Z}_q[X]/(X^N+1)", font_size=32, color=GREY_A).next_to(cipher_group, DOWN, buff=0.5)
        
        self.play(TransformFromCopy(scalar_x, poly_ring), run_time=6)
        self.play(FadeIn(poly_ring2), Write(ring_def), run_time=6)
        
        self.play(FadeOut(scalar_x), FadeOut(scalar_lbl), FadeOut(arrow), FadeOut(enc_lbl), run_time=4)
        self.play(cipher_group.animate.shift(LEFT*3).scale(0.8), ring_def.animate.shift(LEFT*3).scale(0.8), run_time=4)

        add_box = VGroup(
            RoundedRectangle(width=3, height=1.5, color=GREEN, fill_opacity=0.1),
            MathTex(r"\oplus", font_size=50, color=GREEN).shift(UP*0.2),
            Tex(r"Addition", font_size=24, color=WHITE).shift(DOWN*0.3)
        ).shift(RIGHT*3 + UP*1.5)

        mul_box = VGroup(
            RoundedRectangle(width=3, height=1.5, color=PURPLE, fill_opacity=0.1),
            MathTex(r"\otimes", font_size=50, color=PURPLE).shift(UP*0.2),
            Tex(r"Multiplication", font_size=24, color=WHITE).shift(DOWN*0.3)
        ).shift(RIGHT*3 + DOWN*1.5)

        self.play(Create(add_box), Create(mul_box), run_time=6)
        only_text = Tex(r"ONLY Arithmetic Operations!", font_size=32, color=YELLOW).next_to(mul_box, DOWN)
        self.play(Write(only_text), run_time=4)
        self.play(Wiggle(add_box), Wiggle(mul_box), run_time=5)
        
        # Xóa bớt để nhường chỗ cho ambient
        self.play(FadeOut(VGroup(add_box, mul_box, only_text, cipher_group, ring_def)), run_time=5)

        # --- ĐỈNH CAO 3B1B: HOẠT ẢNH ĐA THỨC SÓNG (226 giây) ---
        ambient_title_2 = Tex(r"Polynomial Evaluation under Encryption", color=GREY_A).to_edge(DOWN)
        self.play(FadeIn(ambient_title_2), run_time=5)

        wave_axes = Axes(x_range=[-5, 5], y_range=[-3, 3], x_length=10, y_length=6, axis_config={"color": GREY_C})
        self.play(Create(wave_axes), run_time=6)

        wave_tracker = ValueTracker(0)
        # Vẽ một đa thức chuyển động không ngừng tựa như Cryptographic Noise
        poly_wave = always_redraw(
            lambda: wave_axes.plot(
                lambda x: np.sin(2 * x + wave_tracker.get_value()) * (0.1 * x**2 + 0.5) * np.cos(wave_tracker.get_value() * 0.5),
                color=YELLOW_C
            )
        )
        self.add(poly_wave)
        
        # Chạy mượt mà trong 205 giây
        self.play(wave_tracker.animate.set_value(50), run_time=205, rate_func=linear)
        
        self.play(FadeOut(wave_axes), FadeOut(poly_wave), FadeOut(ambient_title_2), run_time=10)

    def the_blind_server_barrier(self, title):
        """Phần 3: Bức tường mù lòa của Server (296 giây)"""
        
        # --- AUDIO 6: Rào cản (Cấp phát 30 giây) ---
        self.play_audio("assets/audio/02_fhe_cnn/02_01_06.mp3")
        relu_eq = MathTex(r"\max(0, ", r"x", r")", font_size=60)
        self.play(Write(relu_eq), run_time=5)

        ct_noise = MathTex(r"Enc(x)", font_size=50, color=RED_C).move_to(relu_eq[1])
        self.play(ReplacementTransform(relu_eq[1], ct_noise), run_time=5)

        top_group = VGroup(relu_eq[0], ct_noise, relu_eq[2])
        self.play(top_group.animate.shift(UP*2.5), run_time=5)
        self.wait(15)

        # --- AUDIO 7: Mù lòa (Cấp phát 36 giây) ---
        self.play_audio("assets/audio/02_fhe_cnn/02_01_07.mp3")
        question = MathTex(r"Enc(x)", r">", r"0", r"?", font_size=56).shift(UP*0.5)
        question[0].set_color(RED_C)
        self.play(Write(question), run_time=5)

        noise_tracker = ValueTracker(0)
        def noise_updater(m):
            val = int(noise_tracker.get_value())
            m.set_opacity(0.5 + 0.5 * np.sin(val))
        
        question[0].add_updater(noise_updater)
        self.play(noise_tracker.animate.set_value(50), run_time=10)
        question[0].remove_updater(noise_updater)

        wall = Rectangle(width=10, height=0.2, color=RED_E, fill_opacity=0.9).shift(DOWN*1)
        wall_lbl = Tex(r"\textbf{NON-LINEARITY WALL}", font_size=40, color=WHITE).move_to(wall)
        wall_group = VGroup(wall, wall_lbl)

        self.play(FadeIn(wall_group, shift=UP), run_time=4)
        self.play(wall_group.animate.scale(1.5), run_time=3)
        
        cross = Cross(question, stroke_color=RED, stroke_width=6)
        self.play(Create(cross), run_time=4)

        warning = Tex(r"Requires Secret Key to Decrypt!", font_size=36, color=YELLOW).next_to(wall_group, DOWN, buff=1)
        self.play(Write(warning), Flash(wall_group, color=RED, line_length=1.5), run_time=5)
        self.wait(5)

        # --- ĐỈNH CAO 3B1B: HOẠT ẢNH NHIỄU BỨC TƯỜNG (230 giây) ---
        # Hàng trăm hạt nhỏ (đại diện data) rơi xuống và vỡ vụn khi đụng Bức tường
        particles = VGroup(*[Dot(radius=0.05, color=GREY_C).shift(UP*4 + RIGHT*random.uniform(-4, 4)) for _ in range(30)])
        self.add(particles)

        particle_tracker = ValueTracker(0)
        def particle_updater(m):
            t = particle_tracker.get_value()
            for i, dot in enumerate(m):
                # Các hạt chuyển động đi xuống, reset khi chạm tường
                new_y = 4 - ((t * (0.5 + 0.1*(i%5))) % 5)
                dot.move_to(np.array([dot.get_center()[0], new_y, 0]))
                if new_y <= wall.get_center()[1] + 0.2:
                    dot.set_color(RED_E)
                else:
                    dot.set_color(GREY_C)
                    
        particles.add_updater(particle_updater)
        self.play(particle_tracker.animate.set_value(150), run_time=215, rate_func=linear)
        particles.remove_updater(particle_updater)
        
        self.play(FadeOut(particles), run_time=5)
        
        # Xóa gọn màn hình ở phân cảnh cuối cùng
        objects_to_remove = [m for m in self.mobjects]
        self.play(FadeOut(Group(*objects_to_remove)), run_time=10)