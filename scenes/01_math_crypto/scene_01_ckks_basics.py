import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from manim import *
from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, PlaintextBlock, SlotGrid

class CKKSBasicsScene(Scene):
    def construct(self):
        # Thiết lập nền đen chuyên nghiệp theo phong cách 3b1b
        self.camera.background_color = "#141414"

        # Hàm kiểm tra an toàn: Báo lỗi nếu thiếu file mp3
        def safe_add_sound(audio_path):
            if os.path.exists(audio_path):
                self.add_sound(audio_path)
            else:
                print(f"\n[CẢNH BÁO LỚN] Không tìm thấy file âm thanh: {audio_path}")
                print("Vui lòng đảm bảo bạn đã chạy file scripts/generate_audio.py!\n")

        # =======================================================
        # --- Phân đoạn 1.1: Vector Dữ liệu & Đóng gói ---
        # =======================================================
        title = Text("1. Data Packing & Encoding", font_size=DEFAULT_FONT_SIZE, color=COLOR_MATH).to_edge(UP)
        self.play(Write(title))
        
        # Bắt đầu phát âm thanh đoạn 1
        safe_add_sound("assets/audio/01_math_crypto/01_01.mp3")
        
        # Hiển thị dữ liệu dạng Plaintext
        plaintext = PlaintextBlock(label_text="Real Numbers Vector").shift(UP * 1.5)
        self.play(FadeIn(plaintext, shift=DOWN))
        self.wait(1)

        # Trực quan hóa Data Packing vào các Slots
        slot_grid = SlotGrid(rows=1, cols=8, filled_indices=[0, 1, 2, 3]).next_to(plaintext, DOWN, buff=1.2)
        arrow_encode = Arrow(plaintext.get_bottom(), slot_grid.get_top(), color=COLOR_MATH)
        encode_label = Text("Encode", font_size=24, color=COLOR_MATH).next_to(arrow_encode, RIGHT)

        self.play(GrowArrow(arrow_encode), FadeIn(encode_label))
        self.play(FadeIn(slot_grid, shift=UP))
        
        # Đợi 10 giây để giọng đọc AI bắt kịp hình ảnh trước khi qua cảnh
        self.wait(10)

        # =======================================================
        # --- Phân đoạn 1.2: Phép Mã Hóa (Encryption) ---
        # =======================================================
        # Bắt đầu phát âm thanh đoạn 2
        safe_add_sound("assets/audio/01_math_crypto/01_02.mp3")

        self.play(
            FadeOut(plaintext), 
            FadeOut(arrow_encode), 
            FadeOut(encode_label),
            slot_grid.animate.shift(UP * 2.5)
        )

        title_enc = Text("2. Encryption (Adding Noise)", font_size=DEFAULT_FONT_SIZE, color=COLOR_MATH).to_edge(UP)
        self.play(Transform(title, title_enc))

        # Chuyển Plaintext slots thành Ciphertext đỏ
        ciphertext = CiphertextBlock(label_text="Ciphertext Polynomial").next_to(slot_grid, DOWN, buff=1.2)
        arrow_encrypt = Arrow(slot_grid.get_bottom(), ciphertext.get_top(), color=COLOR_ENCRYPTION)
        encrypt_label = Text("Encrypt (pk)", font_size=24, color=COLOR_ENCRYPTION).next_to(arrow_encrypt, RIGHT)

        self.play(GrowArrow(arrow_encrypt), FadeIn(encrypt_label))
        self.play(FadeIn(ciphertext, shift=UP))
        
        # Đợi 8 giây cho AI đọc xong
        self.wait(8)

        # =======================================================
        # --- Phân đoạn 1.3: Tính toán Đồng cấu ---
        # =======================================================
        # Bắt đầu phát âm thanh đoạn 3
        safe_add_sound("assets/audio/01_math_crypto/01_03.mp3")

        self.play(
            FadeOut(slot_grid),
            FadeOut(arrow_encrypt),
            FadeOut(encrypt_label),
            ciphertext.animate.move_to(LEFT * 3)
        )

        title_homo = Text("3. Homomorphic Evaluation", font_size=DEFAULT_FONT_SIZE, color=COLOR_MATH).to_edge(UP)
        self.play(Transform(title, title_homo))

        # Xuất hiện Ciphertext thứ 2 để thực hiện phép toán
        ct2 = CiphertextBlock(label_text="Ciphertext 2").move_to(RIGHT * 3)
        self.play(FadeIn(ct2, shift=LEFT))

        # Dấu cộng đồng cấu
        op_plus = MathTex(r"\oplus", font_size=60, color=COLOR_ENCRYPTION).move_to(ORIGIN)
        self.play(Write(op_plus))
        self.wait(1)

        # Kết quả
        ct_result = CiphertextBlock(label_text="Result Ciphertext").move_to(DOWN * 2.5)
        arrow_res = Arrow(op_plus.get_bottom(), ct_result.get_top(), color=COLOR_MATH)
        
        self.play(GrowArrow(arrow_res))
        self.play(FadeIn(ct_result, shift=DOWN))
        
        # Đợi 10 giây cho câu thoại cuối kết thúc
        self.wait(10)