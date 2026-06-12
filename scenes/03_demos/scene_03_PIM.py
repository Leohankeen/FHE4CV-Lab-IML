import os
import sys
from manim import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from library.constants import *
from library.ehe_primitives import ResNetBlock, PlaintextBlock, CiphertextBlock
from library.storyboard import StoryboardScene

class PrivateImageMatching(StoryboardScene):
    def construct(self):
        # ==================================================
        # 📍 PHÂN ĐOẠN 3.1: ĐẶT VẤN ĐỀ & BỐI CẢNH TRUY VẤN
        # ==================================================
        self.add_sound("./assets/audio/03_demos/03_01_1.mp3")


        title = Text("Private Image Matching: Secure Database Retrieval", font_size=30, color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP, buff=0.2).scale(0.8))

        # Khởi tạo layout Client và Central Database
        client_area = Rectangle(width=4.5, height=6.5, fill_color="#D9E5F2", fill_opacity=0.1, color=BLUE).move_to(LEFT * 4.5 + DOWN * 0.2)
        client_label = Text("Client / Investigator", color=BLUE_C, font_size=24).next_to(client_area, UP, buff=0.1)
        
        server_area = Rectangle(width=4.5, height=6.5, fill_color="#E8DAEF", fill_opacity=0.1, color=PURPLE).move_to(RIGHT * 4.5 + DOWN * 0.2)
        server_label = Text("Central Database", color=PURPLE_C, font_size=24).next_to(server_area, UP, buff=0.1)
        
        self.play(
            FadeIn(client_area), Write(client_label),
            FadeIn(server_area), Write(server_label)
        )
        self.wait(22)

        self.add_sound("./assets/audio/03_demos/03_01_2.mp3")

        # Mô phỏng Query Leakage
        query_img_mock = Rectangle(width=1.0, height=1.0, fill_color=BLUE_E, fill_opacity=0.8).move_to(client_area.get_center() + UP * 1.5)
        query_text = Text("Query Image", font_size=14).move_to(query_img_mock)
        query_group = VGroup(query_img_mock, query_text)
        
        self.play(FadeIn(query_group))
        self.wait(35) 
        self.add_sound("./assets/audio/03_demos/03_01_3.mp3")
        moving_query = query_group.copy()
        self.play(moving_query.animate.move_to(server_area.get_center() + UP * 1.5), run_time=2)
        
        # Cảnh báo đặt gọn trong hộp Server
        leak_warning = Text("⚠️ Query Leakage\n(Intent Revealed)", font_size=16, color=RED).next_to(moving_query, DOWN, buff=0.3)
        self.play(Indicate(server_area, color=RED), FadeIn(leak_warning))
        self.wait(52) 
        self.add_sound("./assets/audio/03_demos/03_01_4.mp3")

        # Đổi sang FHE - Chữ đã được hạ thấp xuống UP * 2.5 để không đè viền
        self.play(FadeOut(moving_query), FadeOut(leak_warning))
        zk_text = Text("Zero-Knowledge Query (FHE)", font_size=18, color=GREEN).move_to(LEFT * 4.5 + UP * 2.5)
        self.play(FadeIn(zk_text))
        self.wait(41)

        # ==================================================
        # 📍 PHÂN ĐOẠN 3.2: TIỀN XỬ LÝ & ĐÓNG GÓI ĐẶC TRƯNG
        # ==================================================
        self.add_sound("./assets/audio/03_demos/03_02_1.mp3")


        local_cnn = ResNetBlock(label_text="Local Extractor\nCNN").scale(0.6).move_to(LEFT * 4.5 + UP * 0.5)
        self.play(FadeIn(local_cnn))
        self.play(query_group.animate.next_to(local_cnn, UP))
        self.wait(54) 
        self.add_sound("./assets/audio/03_demos/03_02_2.mp3")
        vector_1d = MathTex(r"\begin{bmatrix} 0.15 \\ -0.82 \\ 0.44 \\ \vdots \end{bmatrix}", font_size=24).next_to(local_cnn, DOWN)
        self.play(ReplacementTransform(query_group.copy(), vector_1d))
        self.wait(47) 
        self.add_sound("./assets/audio/03_demos/03_02_3.mp3")

        plain_block = PlaintextBlock(label_text="SIMD: 4096 slots").scale(0.6).move_to(LEFT * 4.5 + DOWN * 2.2)
        self.play(FadeIn(plain_block))
        
        self.play(
            vector_1d.animate.rotate(-PI/2).scale(0.5).move_to(plain_block.get_center()),
            run_time=2
        )
        self.play(FadeOut(vector_1d))
        self.wait(63)
        self.add_sound("./assets/audio/03_demos/03_02_4.mp3")

        pub_key = Text("🔑 Public Key", font_size=16, color=ORANGE).move_to(LEFT * 2.5 + DOWN * 2.2)
        self.play(FadeIn(pub_key))
        
        enc_query = CiphertextBlock(label_text="Encrypted\nQuery Vector").scale(0.6).move_to(LEFT * 4.5 + DOWN * 2.2)
        lock_icon = Text("🔒", font_size=20).next_to(enc_query, UP, buff=0.1)
        enc_group = VGroup(enc_query, lock_icon)
        
        self.play(
            pub_key.animate.move_to(plain_block.get_center()).set_opacity(0),
            ReplacementTransform(plain_block, enc_group)
        )
        
        self.play(FadeOut(query_group), FadeOut(local_cnn))
        
        # Di chuyển vào đúng trọng tâm Server (RIGHT * 4.5)
        self.play(enc_group.animate.move_to(RIGHT * 4.5 + UP * 1.5), run_time=3, path_arc=-0.2)
        self.wait(51)

        # ==================================================
        # 📍 PHÂN ĐOẠN 3.3: TÍNH TOÁN KHOẢNG CÁCH 1-to-N
        # ==================================================
        self.add_sound("./assets/audio/03_demos/03_03_1.mp3")

        # Database Grid - Đặt căn giữa RIGHT * 4.5
        db_vectors = VGroup(*[
            PlaintextBlock(label_text=f"DB\n{i+1}").scale(0.4) for i in range(4)
        ]).arrange(RIGHT, buff=0.3).move_to(RIGHT * 4.5 + DOWN * 0.5)
        
        db_label = Text("Database Reference Vectors", font_size=14, color=PURPLE_C).next_to(db_vectors, DOWN, buff=0.2)
        self.play(FadeIn(db_vectors), Write(db_label))

        # Công thức đặt an toàn bên trong viền (UP * 2.6)
        formula = MathTex("D^2 = \sum (Q_i - V_i)^2", font_size=28, color=GREEN_C).move_to(RIGHT * 4.5 + UP * 2.6)
        self.play(Write(formula))
        self.wait(67) 
        self.add_sound("./assets/audio/03_demos/03_03_2.mp3")

        # Broadcast Query tới toàn bộ DB
        query_copies = VGroup(*[enc_group.copy().scale(0.6).next_to(db_vectors[i], UP, buff=0.8) for i in range(4)])
        self.play(ReplacementTransform(enc_group, query_copies))
        self.wait(20)
        minus_signs = VGroup(*[MathTex("-", font_size=30).next_to(db_vectors[i], UP, buff=0.3) for i in range(4)])
        self.play(FadeIn(minus_signs))
        
        # Homomorphic Subtraction hàng loạt
        diff_blocks = VGroup(*[
            CiphertextBlock(label_text="Diff").scale(0.4).move_to(db_vectors[i].get_center() + UP*0.5)
            for i in range(4)
        ])
        
        self.play(
            ReplacementTransform(query_copies, diff_blocks),
            ReplacementTransform(db_vectors, diff_blocks),
            FadeOut(minus_signs), FadeOut(db_label)
        )
        self.wait(41)
        self.add_sound("./assets/audio/03_demos/03_03_3.mp3")

        # Homomorphic Squaring hàng loạt & Noise Bar đặt nép phải (RIGHT * 6.2)
        square_signs = VGroup(*[MathTex("^2", font_size=24, color=YELLOW).next_to(diff_blocks[i], RIGHT, buff=0.05) for i in range(4)])
        self.play(FadeIn(square_signs))
        
        noise_bar = Rectangle(width=0.3, height=1.5, fill_color=GREEN, fill_opacity=0.8).move_to(RIGHT * 6.2 + DOWN * 0.2)
        noise_label = Text("Noise", font_size=12).next_to(noise_bar, UP)
        self.play(FadeIn(noise_bar), FadeIn(noise_label))
        self.wait(31)
        self.play(
            *[Wiggle(diff_blocks[i], run_time=2) for i in range(4)],
            noise_bar.animate.stretch_to_fit_height(0.6, about_edge=DOWN).set_fill(YELLOW)
        )
        self.play(FadeOut(square_signs))
        self.wait(33)
        # Biến thành mảng Encrypted Distances
        self.add_sound("./assets/audio/03_demos/03_03_4.mp3")
        dist_array = VGroup(*[
            RoundedRectangle(corner_radius=0.1, width=0.6, height=0.6, fill_color=RED_D, fill_opacity=0.8)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.1).move_to(RIGHT * 4.5 + DOWN * 1.5)
        
        for i in range(4):
            lock = Text("🔒", font_size=12).move_to(dist_array[i])
            dist_array[i].add(lock)
            
        dist_label = Text("Encrypted Distances", font_size=16).next_to(dist_array, DOWN)
        dist_group = VGroup(dist_array, dist_label)
        
        self.play(ReplacementTransform(diff_blocks, dist_array), FadeIn(dist_label))
        self.wait(54)

        # ==================================================
        # 📍 PHÂN ĐOẠN 3.4: GIẢI MÃ & ARGMIN
        # ==================================================
        self.add_sound("./assets/audio/03_demos/03_04_1.mp3")

        self.play(
            FadeOut(formula), FadeOut(noise_bar), FadeOut(noise_label)
        )
        # Bay về khu vực Client
        self.play(dist_group.animate.move_to(LEFT * 4.5 + UP * 1.0), run_time=3, path_arc=0.3)
        self.wait(61)
        self.add_sound("./assets/audio/03_demos/03_04_2.mp3")
        dec_box = RoundedRectangle(corner_radius=0.1, width=2.0, height=0.8, fill_color="#34495E", fill_opacity=0.9).move_to(LEFT * 4.5 + DOWN * 0.5)
        dec_text = Text("Decryption", font_size=18, color=WHITE).move_to(dec_box)
        sec_key = Text("🗝️ Secret Key", font_size=18, color=RED_C).move_to(LEFT * 2.5 + DOWN * 0.5)
        self.wait(30)
        self.play(FadeIn(dec_box), Write(dec_text), FadeIn(sec_key))
        
        self.play(
            dist_group.animate.move_to(dec_box.get_center()).set_opacity(0),
            sec_key.animate.move_to(dec_box.get_center()).set_opacity(0),
            run_time=1.5
        )
        self.wait(23)
        self.add_sound("./assets/audio/03_demos/03_04_3.mp3")

        scores = VGroup(
            Text("5.22", font_size=20), 
            Text("9.81", font_size=20), 
            Text("0.04", font_size=20, color=GREEN), 
            Text("6.15", font_size=20)
        ).arrange(RIGHT, buff=0.5).move_to(LEFT * 4.5 + DOWN * 1.5)
        
        self.play(FadeIn(scores))
        self.wait(10)

        # HOẠT ẢNH ARGMIN: Khung trượt
        box = SurroundingRectangle(scores[0], color=YELLOW, buff=0.1)
        self.play(Create(box))
        
        self.play(box.animate.move_to(scores[1]), run_time=0.5)
        self.play(box.animate.move_to(scores[2]), run_time=0.5)
        self.play(box.animate.move_to(scores[3]), run_time=0.5)
        self.play(box.animate.move_to(scores[2]), run_time=0.5) 
        
        self.play(
            Indicate(scores[2], color=GREEN, scale_factor=1.5), 
            box.animate.set_color(GREEN),
            run_time=1.5
        )
        self.wait(42)

        self.add_sound("./assets/audio/03_demos/03_04_4.mp3")
        final_result = Text("✅ EXACT MATCH RETRIEVED", font_size=20, color=GREEN).next_to(scores, DOWN, buff=0.5)
        self.play(Write(final_result))
        
        self.wait(63) 
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)