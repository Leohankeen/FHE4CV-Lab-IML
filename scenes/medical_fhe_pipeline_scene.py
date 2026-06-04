from pathlib import Path

from manim import *

from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, PlaintextBlock


class MedicalFHEPipeline(Scene):
    """Manim explainer for Computer Vision over encrypted X-ray features."""

    def construct(self):
        self.camera.background_color = "#101214"

        title = Text(
            "Computer Vision over Homomorphically Encrypted Data",
            font_size=36,
            color=WHITE,
        ).to_edge(UP)
        subtitle = Text(
            "Case: xử lý ảnh X-ray y tế bảo mật bằng TenSEAL / CKKS",
            font_size=24,
            color=GREY_B,
        ).next_to(title, DOWN, buff=0.18)

        self.play(Write(title), FadeIn(subtitle, shift=DOWN))
        self.wait(0.5)

        image_panel = self._make_xray_panel().scale(0.9).to_edge(LEFT, buff=0.55)
        encrypted = CiphertextBlock("CKKS vector").scale(0.85).move_to(ORIGIN + LEFT * 0.2)
        cloud = self._server_panel().to_edge(RIGHT, buff=0.55)

        arrow_1 = Arrow(
            image_panel.get_right(),
            encrypted.get_left(),
            buff=0.25,
            color=COLOR_ENCRYPTION,
        )
        arrow_2 = Arrow(
            encrypted.get_right(),
            cloud.get_left(),
            buff=0.25,
            color=COLOR_ENCRYPTION,
        )

        self.play(FadeIn(image_panel, shift=RIGHT))
        self.play(GrowArrow(arrow_1), FadeIn(encrypted, shift=RIGHT))
        self.play(GrowArrow(arrow_2), FadeIn(cloud, shift=LEFT))

        equation = Text(
            "Enc(x) dot w + b = Enc(score)",
            font_size=30,
            color=COLOR_MATH,
        ).next_to(encrypted, DOWN, buff=0.85)
        note = Text(
            "Server không thấy ảnh gốc, feature vector, hoặc score plaintext",
            font_size=24,
            color=GREY_B,
        ).next_to(equation, DOWN, buff=0.2)

        self.play(Write(equation), FadeIn(note))
        self.wait(0.8)

        encrypted_score = CiphertextBlock("Enc(score)").scale(0.8)
        encrypted_score.move_to(cloud.get_bottom() + DOWN * 0.95)
        return_arrow = Arrow(
            cloud.get_bottom(),
            encrypted_score.get_top(),
            buff=0.16,
            color=COLOR_CIPHERTEXT,
        )
        self.play(GrowArrow(return_arrow), FadeIn(encrypted_score, shift=DOWN))

        doctor = PlaintextBlock("Doctor: score").scale(0.85)
        doctor.move_to(image_panel.get_bottom() + DOWN * 1.05)
        decrypt_arrow = Arrow(
            encrypted_score.get_left(),
            doctor.get_right(),
            buff=0.22,
            color=COLOR_PLAINTEXT,
        )
        decrypt_label = Text("decrypt client-side", font_size=20, color=COLOR_PLAINTEXT)
        decrypt_label.next_to(decrypt_arrow, DOWN, buff=0.08)

        self.play(GrowArrow(decrypt_arrow), FadeIn(decrypt_label))
        self.play(FadeIn(doctor, shift=UP))

        footer = Text(
            "Prototype: linear triage score over encrypted features; not a clinical diagnostic model",
            font_size=22,
            color=GREY_C,
        ).to_edge(DOWN)
        self.play(FadeIn(footer))
        self.wait(2)

    def _make_xray_panel(self):
        data_image = Path("data/chestxray_sample/000001-1.png")
        box = RoundedRectangle(
            corner_radius=0.08,
            width=3.3,
            height=3.45,
            color=COLOR_PLAINTEXT,
            fill_opacity=0.10,
        )
        label = Text("Hospital / Client", font_size=24, color=WHITE)
        label.next_to(box, UP, buff=0.15)
        caption = Text("X-ray -> features", font_size=22, color=GREY_B)
        caption.next_to(box, DOWN, buff=0.14)

        if data_image.exists():
            image = ImageMobject(str(data_image)).set_height(2.55)
            image.move_to(box.get_center())
            content = image
        else:
            content = Text("X-ray", font_size=36, color=COLOR_PLAINTEXT).move_to(
                box.get_center()
            )

        return Group(label, box, caption, content)

    def _server_panel(self):
        box = RoundedRectangle(
            corner_radius=0.08,
            width=3.45,
            height=2.55,
            color=GREY_B,
            fill_opacity=0.12,
        )
        title = Text("HE Cloud Server", font_size=25, color=WHITE)
        title.move_to(box.get_top() + DOWN * 0.35)

        rows = VGroup(
            Text("linear score", font_size=23, color=COLOR_MATH),
            Text("add / multiply", font_size=23, color=COLOR_MATH),
            Text("no secret key", font_size=23, color=COLOR_CIPHERTEXT),
        ).arrange(DOWN, buff=0.18)
        rows.move_to(box.get_center() + DOWN * 0.2)

        return VGroup(box, title, rows)
