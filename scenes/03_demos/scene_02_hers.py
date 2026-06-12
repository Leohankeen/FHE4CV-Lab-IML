import os
import sys
from manim import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from library.constants import *
from library.ehe_primitives import ResNetBlock, PlaintextBlock, CiphertextBlock
from library.storyboard import StoryboardScene

class HERS_System(StoryboardScene):
    def construct(self):
        # ==================================================
        # 📍 PHÂN ĐOẠN 2.1: BỐI CẢNH & MÔ HÌNH ĐE DỌA
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_01_1.mp3")
        title = Text("HERS: Advanced Privacy-Preserving Health Record", font_size=32, color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP, buff=0.2).scale(0.8))
        self.wait(11)
        # Khởi tạo layout 2 bên

        self.add_sound("./assets/audio/03_demos/02_01_2.mp3")
        client_area = Rectangle(width=4.5, height=6.5, fill_color="#D9E5F2", fill_opacity=0.1, color=BLUE).move_to(LEFT * 4.5 + DOWN * 0.2)
        client_label = Text("Patient / Local Clinic", color=BLUE_C, font_size=24).next_to(client_area, UP, buff=0.1)
        
        server_area = Rectangle(width=4.5, height=6.5, fill_color="#FFF2CC", fill_opacity=0.1, color=YELLOW).move_to(RIGHT * 4.5 + DOWN * 0.2)
        server_label = Text("Cloud Hospital AI", color=YELLOW_C, font_size=24).next_to(server_area, UP, buff=0.1)
        
        network_node = Ellipse(width=2, height=1, fill_color=GREY_B, fill_opacity=0.4, color=WHITE).move_to(DOWN * 0.2)
        network_label = Text("Network", color=WHITE, font_size=18).move_to(network_node)

        self.play(
            FadeIn(client_area), Write(client_label),
            FadeIn(server_area), Write(server_label),
            FadeIn(network_node), Write(network_label)
        )
        self.wait(31)
        self.add_sound("./assets/audio/03_demos/02_01_3.mp3")
        self.wait(31)
        self.add_sound("./assets/audio/03_demos/02_01_4.mp3")
        warning_text = Text("⚠️ Threat: Honest-but-Curious Cloud", font_size=18, color=RED).move_to(RIGHT * 4.5 + UP * 2.5)
        self.play(FadeIn(warning_text, shift=UP*0.5))
        self.play(warning_text.animate.set_color(YELLOW), run_time=2)
        self.wait(28)

        self.add_sound("./assets/audio/03_demos/02_01_5.mp3")
        self.wait(16)
        self.add_sound("./assets/audio/03_demos/02_01_6.mp3")
        shield_text = Text("🛡️ FHE Protection Enabled", font_size=18, color=GREEN).move_to(LEFT * 4.5 + UP * 2.5)
        self.play(FadeIn(shield_text, shift=DOWN*0.5))
        
        self.wait(30) 

        # XÓA CẢNH BÁO ĐỂ LẤY CHỖ TRỐNG CHO MODEL
        self.play(FadeOut(warning_text))

        # ==================================================
        # 📍 PHÂN ĐOẠN 2.2: TIỀN XỬ LÝ & ĐÓNG GÓI SIMD
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_02_1.mp3")
        ecg_signal = Text("📈 Continuous ECG Signal", font_size=20, color=GREEN_C).move_to(LEFT * 4.5 + UP * 1.5)
        self.play(FadeIn(ecg_signal))
        self.wait(33)

        # Tránh dùng MathTex nếu không cài LaTeX, dùng Text cho mảng số
        self.add_sound("./assets/audio/03_demos/02_02_2.mp3")
        array_text = Text("[0.85, 1.20, -0.45, 2.10, ...]", font_size=24, color=WHITE).move_to(LEFT * 4.5 + UP * 0.5)
        self.play(ReplacementTransform(ecg_signal, array_text))
        self.wait(38)
        self.add_sound("./assets/audio/03_demos/02_02_3.mp3")
        plain_data = PlaintextBlock(label_text="SIMD Batching:\n4096 slots").scale(0.7).move_to(LEFT * 4.5 + DOWN * 1.0)
        self.wait(16)
        self.add_sound("./assets/audio/03_demos/02_02_4.mp3")
        self.play(array_text.animate.scale(0.5).move_to(plain_data.get_center()), FadeIn(plain_data))
        self.play(FadeOut(array_text)) # Ẩn mảng số sau khi đã chui vào PlaintextBlock
        
        self.wait(26) 

        # ==================================================
        # 📍 PHÂN ĐOẠN 2.3: MÃ HÓA FHE & TRUYỀN TẢI
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_03_1.mp3")

        pub_key = Text("🔑 Public Key", font_size=18, color=ORANGE).move_to(LEFT * 2.5 + DOWN * 1.0)
        enc_box = RoundedRectangle(corner_radius=0.1, width=1.8, height=0.8, fill_color=ORANGE, fill_opacity=0.8).move_to(LEFT * 4.5 + UP * 0.5)
        enc_text = Text("Encryption", font_size=18, color=BLACK).move_to(enc_box)
        
        self.play(FadeIn(pub_key), FadeIn(enc_box), Write(enc_text))
        self.wait(39)
        # Plaintext và Key di chuyển vào hộp mã hóa
        self.add_sound("./assets/audio/03_demos/02_03_2.mp3")
        self.play(
            plain_data.animate.move_to(enc_box.get_center()).set_opacity(0),
            pub_key.animate.move_to(enc_box.get_center()).set_opacity(0),
            run_time=1.5
        )
        self.wait(42)
        self.add_sound("./assets/audio/03_demos/02_03_3.mp3")
        cipher_data = CiphertextBlock(label_text="Encrypted\nHealth Data").scale(0.6).move_to(LEFT * 4.5 + DOWN * 1.5)
        lock_icon = Text("🔒", font_size=20).next_to(cipher_data, UP, buff=0.1)
        cipher_group = VGroup(cipher_data, lock_icon)
        enc_arrow = Arrow(enc_box.get_bottom(), cipher_group.get_top(), buff=0.1, color=WHITE)
        self.play(GrowArrow(enc_arrow))
        self.play(FadeIn(cipher_group))

        # DỌN DẸP KHU VỰC PATIENT ĐỂ CHUẨN BỊ CHO BƯỚC GIẢI MÃ
        self.play(FadeOut(enc_box), FadeOut(enc_text), FadeOut(plain_data), FadeOut(pub_key), FadeOut(lock_icon), FadeOut(enc_arrow))
        self.wait(31)
        self.add_sound("./assets/audio/03_demos/02_03_4.mp3")        
        moving_cipher = cipher_group.copy()
        self.play(FadeOut(cipher_group)) # Xóa bản gốc để bản copy di chuyển
        self.play(moving_cipher.animate.move_to(RIGHT * 4.5 + UP * 2.5), run_time=4, path_arc=-0.3)
        
        self.wait(36)

        # ==================================================
        # 📍 PHÂN ĐOẠN 2.4: CNN MÙ & XẤP XỈ ĐA THỨC
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_04_1.mp3")

        ax = Axes(x_range=[-2, 2, 1], y_range=[-1, 3, 1], x_length=2.5, y_length=2.5, axis_config={"color": GREY_C}).move_to(RIGHT * 4.5 + UP * 0.2)
        
        relu_graph = ax.plot(lambda x: x if x > 0 else 0, color=RED, stroke_width=4)
        relu_label = Text("❌ ReLU (Incompatible)", font_size=14, color=RED).next_to(ax, DOWN)
        
        poly_graph = ax.plot(lambda x: x**2, color=GREEN, stroke_width=4)
        poly_label = Text("✅ Polynomial Appx (y = x²)", font_size=14, color=GREEN).next_to(ax, DOWN)

        self.play(Create(ax))
        self.play(Create(relu_graph), Write(relu_label))
        self.wait(46) 
        self.add_sound("./assets/audio/03_demos/02_04_2.mp3")

        self.play(ReplacementTransform(relu_graph, poly_graph), ReplacementTransform(relu_label, poly_label))
        self.wait(46)
        self.add_sound("./assets/audio/03_demos/02_04_3.mp3")
        self.wait(37)
        # DỌN DẸP ĐỒ THỊ ĐỂ LẤY CHỖ CHO MẠNG CNN
        self.play(FadeOut(ax), FadeOut(poly_graph), FadeOut(poly_label))

        # ==================================================
        # 📍 PHÂN ĐOẠN 2.5: ĐỘ SÂU & NOISE BUDGET
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_05_1.mp3")
        noise_title = Text("Noise Budget", font_size=14, color=WHITE).move_to(RIGHT * 6.2 + UP * 1.5)
        # Sửa lỗi thanh nhiễu: Đặt tọa độ chuẩn
        noise_bar = Rectangle(width=0.4, height=2.0, fill_color=GREEN, fill_opacity=0.8, color=WHITE).next_to(noise_title, DOWN, buff=0.2)
        self.play(FadeIn(noise_title, noise_bar))

        cnn_layers = VGroup(*[ResNetBlock(label_text=f"Conv {i+1}").scale(0.5) for i in range(3)]).arrange(DOWN, buff=0.3).move_to(RIGHT * 4.5 + DOWN * 0.2)
        self.play(FadeIn(cnn_layers))
        self.wait(42) 
        self.add_sound("./assets/audio/03_demos/02_05_2.mp3")
        self.play(moving_cipher.animate.scale(0.8).next_to(cnn_layers[0], UP, buff=0.2))
        
        for i in range(3):
            self.play(moving_cipher.animate.move_to(cnn_layers[i].get_center()), run_time=1.0)
            # Sụt giảm thanh Noise (Neo tại cạnh dưới about_edge=DOWN)
            new_height = max(0.2, 2.0 - (i+1)*0.6)
            color_shift = YELLOW if i == 1 else RED
            self.play(noise_bar.animate.stretch_to_fit_height(new_height, about_edge=DOWN).set_fill(color_shift), run_time=0.5)
            self.wait(5)
        self.wait(38)

        self.add_sound("./assets/audio/03_demos/02_05_3.mp3")
        result_cipher = CiphertextBlock(label_text="Encrypted\nDiagnosis").scale(0.6).move_to(RIGHT * 4.5 + DOWN * 2.5)
        lock_icon3 = Text("🔒", font_size=20).next_to(result_cipher, UP, buff=0.1)
        result_group = VGroup(result_cipher, lock_icon3)

        self.play(ReplacementTransform(moving_cipher, result_group))
        
        # DỌN DẸP CLOUD BOX
        self.play(FadeOut(cnn_layers), FadeOut(noise_bar), FadeOut(noise_title))
        self.wait(43)

        # ==================================================
        # 📍 PHÂN ĐOẠN 2.6: GIẢI MÃ CỤC BỘ & TƯƠNG LAI
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_06_1.mp3")
        moving_result = result_group.copy()
        self.play(FadeOut(result_group))
        self.play(moving_result.animate.move_to(LEFT * 4.5 + UP * 0.5), run_time=3, path_arc=0.4)
        self.wait(45)
        self.add_sound("./assets/audio/03_demos/02_06_2.mp3")

        dec_box = RoundedRectangle(corner_radius=0.1, width=1.8, height=0.8, fill_color="#34495E", fill_opacity=0.9).move_to(LEFT * 4.5 + DOWN * 1.0)
        dec_text = Text("Decryption", font_size=18, color=WHITE).move_to(dec_box)
        sec_key = Text("🗝️ Secret Key", font_size=18, color=RED_C).move_to(LEFT * 2.5 + DOWN * 1.0)
        
        self.play(FadeIn(dec_box), Write(dec_text), FadeIn(sec_key))
        self.wait(55) 
        self.add_sound("./assets/audio/03_demos/02_06_3.mp3")

        self.play(
            moving_result.animate.move_to(dec_box.get_center()).set_opacity(0),
            sec_key.animate.move_to(dec_box.get_center()).set_opacity(0),
            run_time=1.5
        )
        self.wait(10)
        final_result = PlaintextBlock(label_text="Final Diagnosis:\n✅ HEALTHY").scale(0.7).move_to(LEFT * 4.5 + DOWN * 2.5)
        self.play(GrowArrow(Arrow(dec_box.get_bottom(), final_result.get_top(), buff=0.1, color=WHITE)))
        self.play(FadeIn(final_result))
        self.wait(28)
        self.add_sound("./assets/audio/03_demos/02_06_4.mp3")
        self.wait(53)
        self.play(*[FadeOut(mob) for mob in self.mobjects])