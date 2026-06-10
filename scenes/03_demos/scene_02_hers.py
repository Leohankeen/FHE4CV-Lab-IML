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
        # KHỞI TẠO BỐ CỤC: PATIENT - NETWORK - CLOUD HOSPITAL
        # Căn chỉnh lại kích thước để không bị tràn viền
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_01_1.mp3")

        title = Text("HERS: Privacy-Preserving Health Record System", font_size=32, color=WHITE)
        self.play(Write(title))
        self.wait(15)
        self.play(title.animate.to_edge(UP, buff=0.2).scale(0.8))

        # Thu hẹp vùng Area lại một chút (width 4.5 thay vì 5) để có khoảng trống ở giữa
        client_area = Rectangle(width=4.5, height=6.5, fill_color="#D9E5F2", fill_opacity=0.1, color=BLUE).move_to(LEFT * 4.5 + DOWN * 0.2)
        client_label = Text("Patient / Local Clinic", color=BLUE_C, font_size=24).next_to(client_area, UP, buff=0.1)
        
        server_area = Rectangle(width=4.5, height=6.5, fill_color="#FFF2CC", fill_opacity=0.1, color=YELLOW).move_to(RIGHT * 4.5 + DOWN * 0.2)
        server_label = Text("Cloud Hospital AI", color=YELLOW_C, font_size=24).next_to(server_area, UP, buff=0.1)
        
        network_node = Ellipse(width=2, height=1, fill_color=GREY_B, fill_opacity=0.4, color=WHITE).move_to(DOWN * 0.2)
        network_label = Text("Network", color=WHITE, font_size=18).move_to(network_node)
        self.add_sound("./assets/audio/03_demos/02_01_2.mp3")
        self.play(
            FadeIn(client_area), Write(client_label),
            FadeIn(server_area), Write(server_label),
            FadeIn(network_node), Write(network_label)
        )
        self.wait(51)

        # ==================================================
        # BƯỚC 1: CLIENT - MÃ HÓA HỒ SƠ Y TẾ
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_02_1.mp3")
        # Đổi tên Data thành EHR (Electronic Health Record)
        plain_data = PlaintextBlock(label_text="Health Record\n(ECG/EHR)").scale(0.6).move_to(LEFT * 5.5 + UP * 1.8)
        pub_key = Text("🔑 Public Key", font_size=18, color=ORANGE).move_to(LEFT * 3.2 + UP * 2.5)
        
        self.play(FadeIn(plain_data), FadeIn(pub_key))
        self.wait(21)
        self.add_sound("./assets/audio/03_demos/02_02_2.mp3")

        enc_box = RoundedRectangle(corner_radius=0.1, width=1.8, height=0.8, fill_color=ORANGE, fill_opacity=0.8, color=BLACK).move_to(LEFT * 4.5 + UP * 0.5)
        enc_text = Text("Encryption", font_size=18, color=BLACK).move_to(enc_box)
        
        self.play(FadeIn(enc_box), Write(enc_text))
        self.play(
            GrowArrow(Arrow(plain_data.get_bottom(), enc_box.get_top(), buff=0.1, color=WHITE)),
            GrowArrow(Arrow(pub_key.get_bottom(), enc_box.get_top(), buff=0.1, color=WHITE))
        )

        # Kết quả mã hóa: Encrypted Medical Data
        cipher_data = CiphertextBlock(label_text="Encrypted\nHealth Data").scale(0.6).move_to(LEFT * 4.5 + DOWN * 1.2)
        lock_icon2 = Text("🔒", font_size=20).next_to(cipher_data, UP, buff=0.1)
        cipher_group = VGroup(cipher_data, lock_icon2)
        
        self.play(GrowArrow(Arrow(enc_box.get_bottom(), cipher_group.get_top(), buff=0.1, color=WHITE)))
        self.play(FadeIn(cipher_group))
        self.wait(36)

        # ==================================================
        #  BƯỚC 2: TRUYỀN DỮ LIỆU Y TẾ & CHẨN ĐOÁN TRÊN CLOUD
        # ==================================================
        
        # Mô phỏng gói dữ liệu bay qua Network sang Server
        self.add_sound("./assets/audio/03_demos/02_03_1.mp3")

        moving_cipher = cipher_group.copy()
        self.play(moving_cipher.animate.move_to(RIGHT * 4.5 + UP * 1.8), run_time=2, path_arc=-0.5)
        self.wait(1)

        # Khối Model chẩn đoán bệnh
        model_box = RoundedRectangle(corner_radius=0.2, width=2.8, height=1.2, fill_color=BLUE_D, fill_opacity=0.8, color=BLACK).move_to(RIGHT * 4.5 + UP * 0.2)
        model_text = Text("Medical Diagnostic\nCNN Model", font_size=20, color=WHITE).move_to(model_box)
        self.play(FadeIn(model_box), Write(model_text))
        self.wait(18)
        self.play(GrowArrow(Arrow(moving_cipher.get_bottom(), model_box.get_top(), buff=0.1, color=WHITE)))
        self.add_sound("./assets/audio/03_demos/02_03_2.mp3")
        # Kết quả chẩn đoán mã hóa
        result_cipher = CiphertextBlock(label_text="Encrypted\nDiagnosis").scale(0.6).move_to(RIGHT * 4.5 + DOWN * 1.8)
        lock_icon3 = Text("🔒", font_size=20).next_to(result_cipher, UP, buff=0.1)
        result_group = VGroup(result_cipher, lock_icon3)

        self.play(GrowArrow(Arrow(model_box.get_bottom(), result_group.get_top(), buff=0.1, color=WHITE)))
        self.play(FadeIn(result_group))
        self.wait(41)

        # ==================================================
        # BƯỚC 3: TRẢ KẾT QUẢ VỀ BỆNH NHÂN & GIẢI MÃ
        # ==================================================
        self.add_sound("./assets/audio/03_demos/02_04_1.mp3")
        # Mô phỏng kết quả bay về qua Network
        moving_result = result_group.copy()
        self.play(moving_result.animate.move_to(LEFT * 2.5 + DOWN * 1.5), run_time=2, path_arc=0.5)
        self.wait(1)

        # Đẩy hộp Decryption lên cao hơn (Y = -2.6) để không bị cắt chữ
        dec_box = RoundedRectangle(corner_radius=0.1, width=1.8, height=0.8, fill_color="#34495E", fill_opacity=0.9, color=BLACK).move_to(LEFT * 4.5 + DOWN * 2.6)
        dec_text = Text("Decryption", font_size=18, color=WHITE).move_to(dec_box)
        
        sec_key = Text("🗝️ Secret Key", font_size=18, color=RED_C).move_to(LEFT * 2.5 + DOWN * 2.6)
        
        self.play(FadeIn(dec_box), Write(dec_text), FadeIn(sec_key))
        self.wait(13)
        self.add_sound("./assets/audio/03_demos/02_04_2.mp3")

        self.play(
            GrowArrow(Arrow(moving_result.get_bottom(), dec_box.get_top(), buff=0.1, color=WHITE)),
            GrowArrow(Arrow(sec_key.get_left(), dec_box.get_right(), buff=0.1, color=WHITE))
        )
        self.wait(1)

        # Kết quả chẩn đoán an toàn cuối cùng
        final_result = PlaintextBlock(label_text="Final Diagnosis\n(e.g., Healthy)").scale(0.6).move_to(LEFT * 6.8 + DOWN * 2.6)
        self.play(GrowArrow(Arrow(dec_box.get_left(), final_result.get_right(), buff=0.1, color=WHITE)))
        self.play(FadeIn(final_result))
        
        self.wait(39)
        self.play(*[FadeOut(mob) for mob in self.mobjects])