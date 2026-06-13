import os
import sys
from manim import *
import numpy as np

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

# Giả định các import từ thư viện dùng chung của nhóm bạn
from library.constants import *
from library.ehe_primitives import ResNetBlock, PlaintextBlock, CiphertextBlock
from library.storyboard import StoryboardScene

class XRayTriage(StoryboardScene):
    def get_xray_image(self, file_path, scale_height=2.0):
        if os.path.exists(file_path):
            img = ImageMobject(file_path)
            img.scale_to_fit_height(scale_height)
            return img
        else:
            # Fallback nếu không tìm thấy ảnh X-quang gốc
            fallback = Rectangle(width=1.5, height=2.0, fill_color=BLACK, fill_opacity=1, color=WHITE)
            warning = Text("X-RAY\nIMAGE", font_size=18, color=WHITE).move_to(fallback)
            return VGroup(fallback, warning)

    def construct(self):
        # ==================================================
        # 📍 PHÂN ĐOẠN 2.1: BỐI CẢNH Y TẾ & TRÍCH XUẤT EDGE
        # ==================================================
        self.add_sound("./assets/audio/03_demos/04_01_1.mp3")
        title = Text("Medical FHE: X-Ray Priority Triage (TenSEAL)", font_size=30, color=WHITE)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP, buff=0.2).scale(0.8))

        # Khởi tạo hai vùng Hospital và Cloud (Tâm là 3.6)
        hospital_area = Rectangle(width=6.0, height=6.0, fill_color="#E0F7FA", fill_opacity=0.1, color=TEAL).move_to(LEFT * 3.6 + DOWN * 0.5)
        hospital_label = Text("Secure Hospital Client", color=TEAL_C, font_size=24).next_to(hospital_area, UP, buff=0.2)
        
        cloud_area = Rectangle(width=6.0, height=6.0, fill_color="#ECEFF1", fill_opacity=0.1, color=GREY).move_to(RIGHT * 3.6 + DOWN * 0.5)
        cloud_label = Text("Untrusted Server", color=GREY_B, font_size=24).next_to(cloud_area, UP, buff=0.2)
        self.play(
            FadeIn(hospital_area), Write(hospital_label),
            FadeIn(cloud_area), Write(cloud_label)
        )
        self.wait(51)
        self.add_sound("./assets/audio/03_demos/04_01_2.mp3")
        # 1. Tải ảnh X-quang (Căn theo tâm 3.6)
        xray_img = self.get_xray_image("./assets/X-quang.jpg").move_to(LEFT * 3.6 + UP * 1.2)
        self.play(FadeIn(xray_img))
        self.wait(25)

        # 2. Rút trích đặc trưng (Edge Computing)
        edge_extractor = RoundedRectangle(corner_radius=0.1, width=2.5, height=0.6, fill_color=BLUE_E, fill_opacity=0.8).move_to(LEFT * 3.6 + DOWN * 0.3)
        extractor_text = Text("Edge Feature Extractor", font_size=16).move_to(edge_extractor)
        self.play(FadeIn(edge_extractor), Write(extractor_text))
        self.wait(14)
        self.play(xray_img.animate.next_to(edge_extractor, UP, buff=0.2))
        self.add_sound("./assets/audio/03_demos/04_01_3.mp3")

        # 3. Tạo Vector đặc trưng 1D (10 phần tử)
        features_vec = MathTex(r"\begin{bmatrix} 0.45 \\ 1.12 \\ \vdots \\ 0.88 \end{bmatrix}_{10}", font_size=24, color=BLUE_C).next_to(edge_extractor, DOWN, buff=0.3)
        features_label = Text("1D Feature Vector", font_size=14).next_to(features_vec, RIGHT)
        img_copy = xray_img.copy()

        # Visual trick cho hoạt ảnh trích xuất
        self.play(img_copy.animate.move_to(features_vec.get_center()).scale(0.5), run_time=0.8)
        self.play(
            FadeOut(img_copy), 
            FadeIn(features_vec), 
            FadeIn(features_label),
            run_time=0.8
        )
        self.wait(42)

        # ==================================================
        # 📍 PHÂN ĐOẠN 2.2: ĐÓNG GÓI TENSEAL & MÃ HÓA CKKS
        # ==================================================
        self.add_sound("./assets/audio/03_demos/04_02_1.mp3")
        self.play(FadeOut(xray_img), FadeOut(edge_extractor), FadeOut(extractor_text))
        
        # 4. Giới thiệu TenSEAL Context
        tenseal_logo = Text("TenSEAL Framework", font_size=20, color=ORANGE).move_to(LEFT * 3.6 + UP * 2.0)
        ts_context = Text("ts.context(CKKS,\npoly_modulus_degree=8192)", font="Consolas", font_size=14).next_to(tenseal_logo, DOWN)        
        self.play(Write(tenseal_logo), FadeIn(ts_context))
        self.wait(53)
        self.add_sound("./assets/audio/03_demos/04_02_2.mp3")
        # 5. Khóa Vector thành CKKS_Vector
        pub_key = Text("🔑 Public Key", font_size=16, color=GREEN_C).move_to(LEFT * 1.2 + DOWN * 1.5)
        self.play(FadeIn(pub_key))
        
        ckks_block = CiphertextBlock(label_text="CKKS_Vector\n(Encrypted Features)").scale(0.6).move_to(features_vec.get_center())
        lock_icon = Text("🔒", font_size=20).next_to(ckks_block, UP, buff=0.1)
        ckks_group = VGroup(ckks_block, lock_icon)
        
        self.play(
            pub_key.animate.move_to(features_vec.get_center()).set_opacity(0),
            ReplacementTransform(features_vec, ckks_group),
            FadeOut(features_label)
        )
        self.wait(57)
        self.add_sound("./assets/audio/03_demos/04_02_3.mp3")

        # 6. Truyền tải sang Cloud (Đích đến là RIGHT * 3.6)
        self.play(FadeOut(tenseal_logo), FadeOut(ts_context))
        self.play(ckks_group.animate.move_to(RIGHT * 3.6 + UP * 2.0), run_time=4, path_arc=-0.2)
        self.wait(36)

        # ==================================================
        # 📍 PHÂN ĐOẠN 2.3: TÍNH TOÁN DOT PRODUCT ĐỒNG HÌNH
        # ==================================================

        # 7. Hiển thị Model Weights & Bias tại Cloud (Căn chỉnh gọn gàng bên trong hộp 6.0)
        self.add_sound("./assets/audio/03_demos/04_03_1.mp3")

        weights_block = PlaintextBlock(label_text="Model Weights (W)").scale(0.5).move_to(RIGHT * 1.8 + UP * 0.5)
        bias_block = PlaintextBlock(label_text="Bias (b)").scale(0.5).move_to(RIGHT * 5.4 + UP * 0.5)
        self.play(FadeIn(weights_block), FadeIn(bias_block))
        
        # Công thức
        formula = MathTex(r"\text{EncLogit} = \text{Enc}(X) \cdot W + b", font_size=28, color=YELLOW).move_to(RIGHT * 3.6 + DOWN * 0.5)
        self.play(Write(formula))
        self.wait(40)
        self.add_sound("./assets/audio/03_demos/04_03_2.mp3")

        # 8. Mô phỏng Phép toán và Noise (Kéo Noise bar thụt vào trong hộp)
        noise_bar = Rectangle(width=0.3, height=1.5, fill_color=GREEN, fill_opacity=0.8).move_to(RIGHT * 6.0 + DOWN * 2.0)
        noise_label = Text("Noise", font_size=12).next_to(noise_bar, UP)
        self.play(FadeIn(noise_bar), FadeIn(noise_label))

        # Hội tụ 3 khối lại để tính Logit
        enc_logit = CiphertextBlock(label_text="Encrypted\nLogit").scale(0.6).move_to(RIGHT * 3.6 + DOWN * 2.0)
        lock2 = Text("🔒", font_size=20).next_to(enc_logit, UP, buff=0.1)
        logit_group = VGroup(enc_logit, lock2)
        
        self.play(
            ReplacementTransform(ckks_group, logit_group),
            ReplacementTransform(weights_block, logit_group),
            ReplacementTransform(bias_block, logit_group),
            run_time=3
        )
        
        # Sụt nhiễu RẤT ÍT
        self.play(
            Wiggle(logit_group),
            noise_bar.animate.stretch_to_fit_height(1.2, about_edge=DOWN).set_fill(GREEN_B)
        )
        self.wait(60)

        # ==================================================
        # 📍 PHÂN ĐOẠN 2.4: GIẢI MÃ & SIGMOID PHI TUYẾN
        # ==================================================
        self.add_sound("./assets/audio/03_demos/04_04_1.mp3")

        self.play(FadeOut(formula), FadeOut(noise_bar), FadeOut(noise_label))
        
        # 9. Trả Encrypted Logit về Hospital
        self.play(logit_group.animate.move_to(LEFT * 3.6 + UP * 1.8), run_time=4, path_arc=0.3)
        self.wait(43)
        self.add_sound("./assets/audio/03_demos/04_04_2.mp3")

        # 10. Giải mã cục bộ
        dec_box = RoundedRectangle(corner_radius=0.1, width=2.0, height=0.6, fill_color="#34495E", fill_opacity=0.9).move_to(LEFT * 3.6 + UP * 1.8)
        dec_text = Text("Decryption", font_size=16, color=WHITE).move_to(dec_box)
        sec_key = Text("🗝️ Secret Key", font_size=16, color=RED_C).next_to(dec_box, UP, buff=0.1)
        
        self.play(FadeIn(dec_box), Write(dec_text), FadeIn(sec_key))
        
        self.play(
            logit_group.animate.move_to(dec_box.get_center()).set_opacity(0),
            sec_key.animate.move_to(dec_box.get_center()).set_opacity(0),
            run_time=2.0
        )
        
        # Xuất ra Plaintext Logit
        plain_logit = Text("Logit (x) = 2.45", font_size=20, color=BLUE_B).next_to(dec_box, DOWN, buff=0.3)
        self.play(FadeIn(plain_logit))

        sigmoid_form = MathTex(r"P = \frac{1}{1 + e^{-x}}", font_size=24, color=WHITE).next_to(plain_logit, RIGHT, buff=0.4)
        self.play(Write(sigmoid_form))
        self.wait(20)
        
        # Khởi tạo trục tọa độ (Axes) vừa vặn trong hộp Hospital
        ax = Axes(
            x_range=[-5, 5, 2],
            y_range=[0, 1.2, 0.5],
            x_length=4.0,
            y_length=2.0,
            axis_config={"color": WHITE, "include_numbers": False}
        ).move_to(LEFT * 3.6 + DOWN * 1.0)
        
        # Vẽ đường cong Sigmoid
        sigmoid_curve = ax.plot(lambda x: 1 / (1 + np.exp(-x)), color=BLUE_C, stroke_width=4)
        graph_label = Text("Sigmoid Activation", font_size=14, color=GRAY_B).next_to(ax, UP, buff=0.1)
        
        self.play(Create(ax), Write(graph_label))
        self.play(Create(sigmoid_curve), run_time=2)
        self.wait(21)
        self.add_sound("./assets/audio/03_demos/04_04_3.mp3")

        # Ánh xạ Logit = 2.45 lên đồ thị
        x_val = 2.45
        y_val = 1 / (1 + np.exp(-x_val)) # ~0.91
        
        point_on_curve = Dot(ax.c2p(x_val, y_val), color=YELLOW, radius=0.08)
        
        # Vẽ các đường gióng (Dashed lines)
        v_line = ax.get_vertical_line(ax.c2p(x_val, y_val), color=BLUE_B, line_func=DashedLine)
        h_line = ax.get_horizontal_line(ax.c2p(x_val, y_val), color=GREEN_C, line_func=DashedLine)
        
        x_label = MathTex("2.45", font_size=16, color=BLUE_B).next_to(v_line, DOWN, buff=0.1)
        y_label = MathTex("0.91", font_size=16, color=GREEN_C).next_to(h_line, LEFT, buff=0.1)
        
        # Hoạt ảnh ánh xạ: Trượt từ X lên hàm, rồi bắn sang Y
        self.play(Create(v_line), FadeIn(x_label), run_time=1.5)
        self.play(FadeIn(point_on_curve))
        self.play(Create(h_line), FadeIn(y_label), run_time=1.5)
        self.wait(27)
        self.add_sound("./assets/audio/03_demos/04_04_4.mp3")

        # 12. Áp dụng Threshold & Cảnh báo Triage
        threshold_line = ax.get_horizontal_line(ax.c2p(5, 0.5), color=RED_C, line_func=DashedLine)
        threshold_lbl = Text("Threshold (0.5)", font_size=12, color=RED_C).next_to(threshold_line, RIGHT, buff=0.1)
        
        self.play(Create(threshold_line), Write(threshold_lbl))
        self.wait(15)
        
        # Rung lắc điểm ảnh vì nó nằm trên Threshold
        self.play(Wiggle(point_on_curve, run_time=2, scale_value=1.5))

        # Hiện chữ Cảnh báo ở đáy màn hình
        alert = Text("🚨 TRIAGE FLAG: TRUE (URGENT)", font_size=20, color=RED, weight=BOLD).next_to(ax, DOWN, buff=0.4)
        alert_box = SurroundingRectangle(alert, color=RED, buff=0.2)
        
        self.play(FadeIn(alert), Create(alert_box))
        
        # Hiệu ứng chớp nháy cảnh báo đỏ rực
        self.play(
            Flash(alert_box, line_length=0.2, num_lines=12, color=RED, flash_radius=2.0, time_width=0.3),
            run_time=2
        )
        
        self.wait(26)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=2)