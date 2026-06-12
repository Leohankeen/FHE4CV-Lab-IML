import os
import sys
from manim import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from library.constants import *
from library.ehe_primitives import ResNetBlock, PlaintextBlock, CiphertextBlock
from library.storyboard import StoryboardScene

class CryptoFace(StoryboardScene):
    def create_database(self):
        top = Ellipse(width=1.1, height=0.25, fill_color=GREY_B, fill_opacity=1, color=BLACK)
        middle = Rectangle(width=1.1, height=0.8, fill_color=GREY_B, fill_opacity=1, color=BLACK)
        bottom = Ellipse(width=1.1, height=0.25, fill_color=GREY_B, fill_opacity=1, color=BLACK)
        bottom.next_to(middle, DOWN, buff=0)
        top.next_to(middle, UP, buff=0)
        return VGroup(bottom, middle, top)

    def get_face_image(self, file_path, scale_height=1.5):
        if os.path.exists(file_path):
            img = ImageMobject(file_path)
            img.scale_to_fit_height(scale_height) 
            return img
        else:
            fallback = Square(side_length=scale_height, fill_color=WHITE, fill_opacity=1, color=BLACK)
            warning = Text("MISSING\nIMAGE FILE", font_size=14, color=RED).move_to(fallback)
            return VGroup(fallback, warning)

    def construct(self):
        # ==================================================
        # 📍 PHÂN ĐOẠN 1: ĐẶT VẤN ĐỀ & KHÁI NIỆM CỐT LÕI
        # ==================================================
    
        # Tiêu đề Act 3
        self.add_sound("./assets/audio/03_demos/01_01_1_1.mp3")
        title_act3 = Text("Act 3: Practical FHE Applications\nCryptoFace System", font_size=36, color=WHITE, line_spacing=0.8)
        self.play(Write(title_act3))
        self.wait(22)
        self.add_sound("./assets/audio/03_demos/01_01_1_2.mp3")
        self.wait(47)
        self.play(FadeOut(title_act3))
        self.add_sound("./assets/audio/03_demos/01_01_2_1.mp3")
        # Minh họa rủi ro đám mây truyền thống
        user_node = Circle(radius=0.6, fill_color=BLUE_D, fill_opacity=0.8, color=WHITE).move_to(LEFT * 4)
        user_lbl = Text("User Device", font_size=18).next_to(user_node, DOWN)
        cloud_node = Rectangle(width=2, height=1.2, fill_color=GREY_B, fill_opacity=0.5, color=WHITE).move_to(RIGHT * 4)
        cloud_lbl = Text("Cloud Server", font_size=18).next_to(cloud_node, DOWN)
        
        self.play(FadeIn(user_node, user_lbl, cloud_node, cloud_lbl))
        self.wait(20)
        # Gửi ảnh rõ lên đám mây và bị tấn công
        plain_data = PlaintextBlock(label_text="Plaintext Face").scale(0.5).move_to(user_node)
        self.play(plain_data.animate.move_to(cloud_node.get_center()), run_time=2)
        self.wait(31)
        self.add_sound("./assets/audio/03_demos/01_01_2_2.mp3")

        hacker_lbl = Text("⚠️ HACKER EXPLOIT (Data Leaked)", font_size=20, color=RED).move_to(UP * 2)
        self.play(Write(hacker_lbl), cloud_node.animate.set_color(RED))
        self.wait(50)
        
        # Chuyển giao sang giải pháp FHE (Mã hóa đầu cuối)
        self.add_sound("./assets/audio/03_demos/01_01_3_1.mp3")
        self.play(FadeOut(plain_data), FadeOut(hacker_lbl), cloud_node.animate.set_color(WHITE))
        self.wait(15)

        lock_box = CiphertextBlock(label_text="🔒 Ciphertext").scale(0.5).move_to(user_node)
        self.play(FadeIn(lock_box))
        self.play(lock_box.animate.move_to(cloud_node.get_center()), run_time=2)
        self.wait(17)
        self.add_sound("./assets/audio/03_demos/01_01_3_2.mp3")
        fhe_eval_lbl = Text("Direct Computation on Ciphertext\n(No Decryption Needed)", font_size=20, color=GREEN).move_to(UP * 2)
        self.play(Write(fhe_eval_lbl))
        self.wait(48)
        
        # Xóa phân cảnh 1 để sang phân cảnh 2
        self.play(FadeOut(user_node), FadeOut(user_lbl), FadeOut(cloud_node), FadeOut(cloud_lbl), FadeOut(lock_box), FadeOut(fhe_eval_lbl))

        # ==================================================
        # 📍 PHÂN ĐOẠN 2: KIẾN TRÚC CRYPTOFACENET & TỐI ƯU CKKS
        # ==================================================
        
        depth_title = Text("Challenge: Multiplicative Depth", font_size=24, color=RED).move_to(UP * 3)
        self.play(Write(depth_title))
        self.add_sound("./assets/audio/03_demos/01_02_1_1.mp3")
        # Vẽ mạng CNN quá sâu gây nhiễu sụp đổ
        deep_cnn = VGroup(*[ResNetBlock(label_text="").scale(0.5) for _ in range(4)]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.5)
        self.wait(25)
        self.play(FadeIn(deep_cnn))
        self.wait(30)
        self.add_sound("./assets/audio/03_demos/01_02_1_2.mp3")
        noise_text = Text("❌ Noise Accumulation -> CKKS Data Collapse", font_size=18, color=RED).next_to(deep_cnn, DOWN, buff=0.4)
        self.play(Write(noise_text))
        self.wait(45)
        self.play(FadeOut(deep_cnn), FadeOut(noise_text), FadeOut(depth_title))
        self.add_sound("./assets/audio/03_demos/01_02_2.mp3")
        # Giải pháp: Patch-based CNN (Chia nhỏ ảnh)
        patch_title = Text("CryptoFaceNet Solution: Patch-based Processing", font_size=24, color=GREEN).move_to(UP * 3)
        self.play(Write(patch_title))
        self.wait(17)
        # Vẽ lưới 8x8 ma trận các mảnh nhỏ (patches) đại diện cho phân tách ảnh
        grid_patches = VGroup()
        for i in range(4):
            for j in range(4):
                rect = Square(side_length=0.4, stroke_color=WHITE, fill_color=BLUE_E, fill_opacity=0.6)
                rect.move_to(LEFT * 3 + np.array([j * 0.45, i * 0.45, 0]))
                grid_patches.add(rect)
        
        grid_lbl = Text("Face divided into discrete patches", font_size=16).next_to(grid_patches, DOWN)
        self.play(FadeIn(grid_patches), Write(grid_lbl))
        self.wait(40)
        self.add_sound("./assets/audio/03_demos/01_02_3.mp3")
        # Các mảnh nhỏ xử lý song song bởi nhiều PCNN nông
        pcnns = VGroup(*[ResNetBlock(label_text="PCNN").scale(0.4) for _ in range(3)]).arrange(DOWN, buff=0.2).move_to(RIGHT * 3)
        self.wait(15)
        self.play(FadeIn(pcnns))
        
        # Tạo hiệu ứng các mũi tên song song bứt phá sang các PCNN
        arrows = VGroup(*[Arrow(grid_patches.get_right(), pcnns[i].get_left(), color=WHITE, stroke_width=2) for i in range(3)])
        self.wait(15)
        self.play(Create(arrows))
        self.wait(31)
        
        # Xóa phân cảnh 2 chuẩn bị bước vào Layout hệ thống tổng thể 2x2
        self.play(FadeOut(grid_patches), FadeOut(grid_lbl), FadeOut(pcnns), FadeOut(arrows), FadeOut(patch_title))
        self.add_sound("./assets/audio/03_demos/01_02_4.mp3")

        # ==================================================
        # PHÂN BỔ MÔI TRƯỜNG CHO HỆ THỐNG TỔNG THỂ DƯỚI DẠNG 2X2 LAYOUT
        # ==================================================
        client_color = "#D9E5F2"
        server_color = "#FFF2CC"

        tl = Rectangle(width=7, height=4, fill_color=client_color, fill_opacity=1, color=BLACK).move_to(LEFT * 3.5 + UP * 2)
        tr = Rectangle(width=7, height=4, fill_color=server_color, fill_opacity=1, color=BLACK).move_to(RIGHT * 3.5 + UP * 2)
        bl = Rectangle(width=7, height=4, fill_color=client_color, fill_opacity=1, color=BLACK).move_to(LEFT * 3.5 + DOWN * 2)
        br = Rectangle(width=7, height=4, fill_color=server_color, fill_opacity=1, color=BLACK).move_to(RIGHT * 3.5 + DOWN * 2)

        divider_v = Line(UP * 4, DOWN * 4, color=BLACK, stroke_width=8)
        divider_h = Line(LEFT * 7, RIGHT * 7, color=BLACK, stroke_width=8)
        self.add(tl, tr, bl, br, divider_v, divider_h)

        client_txt = Text("Client", color=COLOR_PLAINTEXT, font_size=32).move_to(LEFT * 5.8 + UP * 3.5)
        server_txt = Text("Server", color=COLOR_ENCRYPTION, font_size=32).move_to(RIGHT * 5.8 + UP * 3.5)
        self.play(Write(client_txt), Write(server_txt))
        self.wait(48)
        # ==================================================
        # 📍 PHÂN ĐOẠN 3: LUỒNG ĐĂNG KÝ - ENROLLMENT
        # ==================================================
        self.add_sound("./assets/audio/03_demos/01_03_1.mp3")
        self.wait(10)
        # 1. Khởi tạo ảnh và ID tại Client
        ref_face = self.get_face_image("./assets/reference_face.jpg", scale_height=1.4).move_to(LEFT * 5.5 + UP * 2.3)
        ref_label = Text("reference face", font_size=18, color=BLACK).next_to(ref_face, DOWN, buff=0.1)
        id_block = PlaintextBlock(label_text="identity ID").scale(0.5).next_to(ref_label, DOWN, buff=0.1)
        self.play(FadeIn(ref_face), Write(ref_label), FadeIn(id_block))
        self.wait(46)
        self.add_sound("./assets/audio/03_demos/01_03_2.mp3")
        # 2. Thực hiện cấu trúc mã hóa tại chỗ
        enc_box = RoundedRectangle(corner_radius=0.1, width=1.6, height=0.7, fill_color=COLOR_ENCRYPTION, fill_opacity=1, color=BLACK).move_to(LEFT * 2.8 + UP * 2.3)
        enc_text = Text("Encrypt", font_size=20, color=BLACK).move_to(enc_box)
        pubkey = Text("🔑 Public Key", font_size=16, color=GREEN_E).next_to(enc_box, UP, buff=0.1)
        
        self.play(FadeIn(enc_box), Write(enc_text), Write(pubkey))
        self.wait(20)
        self.play(GrowArrow(Arrow(ref_face.get_right(), enc_box.get_left(), buff=0.1, color=BLACK)))

        enc_face = ref_face.copy().move_to(LEFT * 0.8 + UP * 2.3)
        lock1 = Text("🔒", font_size=24).move_to(enc_face.get_corner(DR) + LEFT*0.1 + UP*0.1)
        self.play(GrowArrow(Arrow(enc_box.get_right(), enc_face.get_left(), buff=0.1, color=BLACK)), FadeIn(enc_face), FadeIn(lock1))
        self.wait(40)
        self.add_sound("./assets/audio/03_demos/01_03_3.mp3")
        # 3. Đẩy Ciphertext sang kiến trúc Server thông qua mạng nơ-ron PCNN nông
        nn1 = ResNetBlock(label_text="").scale(0.8).move_to(RIGHT * 1.8 + UP * 2.3)
        self.play(GrowArrow(Arrow(enc_face.get_right(), nn1.get_left(), buff=0.1, color=BLACK)), FadeIn(nn1))
        self.wait(27)
        ref_vec = Rectangle(width=0.25, height=1.3, fill_color=COLOR_CIPHERTEXT, fill_opacity=0.8, color=BLACK).move_to(RIGHT * 3.8 + UP * 2.3)
        self.play(GrowArrow(Arrow(nn1.get_right(), ref_vec.get_left(), buff=0.1, color=BLACK)), FadeIn(ref_vec))
        self.wait(30)
        # 4. Lưu trữ thông tin kết cấu đặc trưng vào Database đám mây
        self.add_sound("./assets/audio/03_demos/01_03_4.mp3")
        db = self.create_database().move_to(RIGHT * 5.8 + UP * 2.3)
        db_label = Text("database", font_size=18, color=BLACK).next_to(db, DOWN, buff=0.1)
        self.play(FadeIn(db), Write(db_label))
        self.wait(13)
        self.play(GrowArrow(Arrow(ref_vec.get_right(), db.get_left(), buff=0.1, color=BLACK)))
        self.play(GrowArrow(Arrow(id_block.get_right(), db.get_bottom() + DOWN*0.2, path_arc=0.2, color=BLACK)))
        self.wait(35)

        # ==================================================
        # 📍 PHÂN ĐOẠN 4: LUỒNG XÁC THỰC - VERIFICATION
        # ==================================================
        self.add_sound("./assets/audio/03_demos/01_04_1.mp3")
        # 1. Khởi tạo dữ liệu kiểm tra đầu vào tại Client góc dưới
        claimed_block = PlaintextBlock(label_text="claimed ID").scale(0.5).move_to(LEFT * 5.5 + DOWN * 0.3)
        probe_face = self.get_face_image("./assets/probe_face.jpg", scale_height=1.4).move_to(LEFT * 5.5 + DOWN * 1.8)
        probe_label = Text("probe face", font_size=18, color=BLACK).next_to(probe_face, DOWN, buff=0.1)
        self.wait(10)
        self.play(FadeIn(claimed_block), FadeIn(probe_face), Write(probe_label))
        self.wait(17)

        # 2. Thiết lập quy trình mã hóa Probe Face bảo vệ luồng truyền
        enc2 = enc_box.copy().move_to(LEFT * 2.8 + DOWN * 1.8)
        enc2_text = Text("Encrypt", font_size=20, color=BLACK).move_to(enc2)
        pubkey2 = pubkey.copy().next_to(enc2, UP, buff=0.1)
        self.play(FadeIn(enc2), Write(enc2_text), Write(pubkey2))
        self.play(GrowArrow(Arrow(probe_face.get_right(), enc2.get_left(), buff=0.1, color=BLACK)))

        enc_probe = probe_face.copy().move_to(LEFT * 0.8 + DOWN * 1.8)
        lock2 = Text("🔒", font_size=24).move_to(enc_probe.get_corner(DR) + LEFT*0.1 + UP*0.1)
        self.play(GrowArrow(Arrow(enc2.get_right(), enc_probe.get_left(), buff=0.1, color=BLACK)), FadeIn(enc_probe), FadeIn(lock2))
        self.wait(34)

        # 3. Client thực hiện gửi song song Claimed ID kích hoạt Database xử lý
        self.add_sound("./assets/audio/03_demos/01_04_2.mp3")
        db2 = db.copy().move_to(RIGHT * 5.8 + DOWN * 1.8)
        self.play(FadeIn(db2))
        cid_arrow = Arrow(claimed_block.get_right(), db2.get_top() + UP*0.2, path_arc=-0.2, color=ORANGE, stroke_width=4)
        self.play(GrowArrow(cid_arrow))
        self.wait(15)
        # 4. Ảnh mã hóa truyền qua mạng trích xuất vector mới
        nn2 = ResNetBlock(label_text="").scale(0.8).move_to(RIGHT * 1.8 + DOWN * 1.8)
        self.play(GrowArrow(Arrow(enc_probe.get_right(), nn2.get_left(), buff=0.1, color=BLACK)), FadeIn(nn2))
        self.wait(20)
        probe_vec = Rectangle(width=0.25, height=1.3, fill_color=COLOR_CIPHERTEXT, fill_opacity=0.8, color=BLACK).move_to(RIGHT * 3.5 + DOWN * 1.8)
        self.play(GrowArrow(Arrow(nn2.get_right(), probe_vec.get_left(), buff=0.1, color=BLACK)), FadeIn(probe_vec))
        # 5. Rút trích dữ liệu cũ đối chuẩn (Reference Vector) trong database
        ref_vec_db = ref_vec.copy().move_to(RIGHT * 4.2 + DOWN * 1.8)
        self.play(GrowArrow(Arrow(db2.get_left(), ref_vec_db.get_right(), buff=0.1, color=ORANGE)), FadeIn(ref_vec_db))
        self.wait(21)
        self.add_sound("./assets/audio/03_demos/01_04_3.mp3")
        # 6. Đưa song song 2 vector tính toán sai biệt khoảng cách ra hộp Score mã hóa
        score_box = Rectangle(width=1.2, height=0.4, color=BLACK).move_to(RIGHT * 3.85 + DOWN * 2.8)
        score_text = Text("score", font_size=16, color=BLACK).move_to(score_box)
        vec_center = (probe_vec.get_bottom() + ref_vec_db.get_bottom()) / 2
        arr_to_score = Arrow(vec_center, score_box.get_top(), buff=0.1, color=BLACK)
        self.play(FadeIn(score_box), Write(score_text), GrowArrow(arr_to_score))
        self.wait(25)
        # 7. Sai biệt tích hợp ngưỡng an toàn bảo mật: result = score - threshold
        result_box = Rectangle(width=3.2, height=0.5, color=BLACK).move_to(RIGHT * 2.5 + DOWN * 3.4)
        result_text = Text("result = score - threshold", font_size=16, color=BLACK).move_to(result_box)
        lock3 = Text("🔒", font_size=18).move_to(result_box.get_corner(DR) + LEFT*0.1)
        self.play(GrowArrow(Arrow(score_box.get_bottom(), result_box.get_top(), buff=0.1, color=BLACK)))
        self.play(FadeIn(result_box), Write(result_text), FadeIn(lock3))
        self.wait(35)

        # 8. Trả hộp kết quả bảo mật về phía Client để thực thi giải mã
        self.add_sound("./assets/audio/03_demos/01_04_4.mp3")
        dec_box = RoundedRectangle(corner_radius=0.1, width=1.6, height=0.7, fill_color=GREEN_C, fill_opacity=1, color=BLACK).move_to(LEFT * 2.5 + DOWN * 3.4)
        dec_text = Text("Decrypt", font_size=20, color=BLACK).move_to(dec_box)
        secret_key = Text("🗝️ Secret Key", font_size=16, color=RED_C).next_to(dec_box, UP, buff=0.1)
        self.wait(7)
        self.play(GrowArrow(Arrow(result_box.get_left(), dec_box.get_right(), buff=0.1, color=BLACK)))
        self.play(FadeIn(dec_box), Write(dec_text), Write(secret_key))
        self.wait(22)
        # 9. Trả kết quả Plaintext cuối cùng, hiển thị trạng thái Access Granted
        result_client = Text("result", font_size=20, color=BLACK).move_to(LEFT * 4.8 + DOWN * 3.4)
        self.play(GrowArrow(Arrow(dec_box.get_left(), result_client.get_right(), buff=0.1, color=BLACK)), Write(result_client))
        
        access_granted = Text("✅ Access Granted", font_size=18, color=GREEN_E).next_to(result_client, DOWN, buff=0.2)
        self.play(FadeIn(access_granted))
        self.wait(31)