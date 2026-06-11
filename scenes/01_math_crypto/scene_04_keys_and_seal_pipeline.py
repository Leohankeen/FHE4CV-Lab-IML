import os
import sys
from manim import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from scenes.library.constants import *
from scenes.library.ehe_primitives import CiphertextBlock, PlaintextBlock, SlotGrid
from scenes.library.storyboard import StoryboardScene, scene_time


class KeysAndSEALPipeline(StoryboardScene):
    """15-minute lesson on SEAL keys, objects, and deployment lifecycle."""

    @staticmethod
    def fit_text(text, max_width):
        if text.width > max_width:
            text.scale_to_fit_width(max_width)
        return text

    def card(self, label, color, width=2.5, height=1.0, font_size=25):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            color=color,
            fill_color=color,
            fill_opacity=0.16,
        )
        text = Text(label, font_size=font_size, color=COLOR_MATH, line_spacing=0.8)
        self.fit_text(text, width - 0.25)
        text.move_to(box)
        return VGroup(box, text)

    @staticmethod
    def arrow_between(left, right, color=COLOR_ENCRYPTION):
        return Arrow(left.get_right(), right.get_left(), buff=0.12, color=color)

    def open_lesson(self, lesson_title, audio_path):
        self.camera.background_color = "#101214"
        self.add_optional_sound(audio_path)
        act = Text("ACT 1 | MATHEMATICS AND CRYPTOGRAPHY", font_size=25, color=COLOR_ENCRYPTION)
        title = Text(lesson_title, font_size=42, color=WHITE)
        self.fit_text(title, 11.4)
        rule = Line(LEFT * 5.5, RIGHT * 5.5, color=GREY_D)
        self.play(FadeIn(act), Write(title), Create(rule), run_time=2)
        self.wait(0.8)
        self.play(
            FadeOut(act),
            FadeOut(rule),
            title.animate.scale(0.58).to_edge(UP, buff=0.18),
            run_time=1,
        )
        return title

    def show_chapter_plate(self, title, image_path, summary, accent):
        subtitle = Text("Visual roadmap", font_size=25, color=GREY_B).next_to(title, DOWN, buff=0.2)
        stages = VGroup(
            self.card("KEYS", GREEN_C, 2.2, 1.1, 23),
            self.card("SEAL\nOBJECTS", COLOR_ENCRYPTION, 2.2, 1.1, 23),
            self.card("DEPLOYMENT", COLOR_CIPHERTEXT, 2.2, 1.1, 23),
        ).arrange(RIGHT, buff=0.9)
        summary_text = Text(summary, font_size=26, color=GREY_B)
        self.fit_text(summary_text, 10.8)
        summary_text.next_to(stages, DOWN, buff=0.55)
        self.play(FadeIn(subtitle), LaggedStart(*(FadeIn(stage) for stage in stages), lag_ratio=0.18))
        self.play(Write(summary_text), Indicate(stages[0], color=accent))
        self.play(FadeOut(VGroup(subtitle, stages, summary_text)))

    def show_key_roles(self, title):
        subtitle = Text("Each key grants one specific capability", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.2)
        keys = VGroup(
            self.card("SecretKey\nDECRYPT", GREEN_C, 3.0, 1.2, 22),
            self.card("PublicKey\nENCRYPT", COLOR_PLAINTEXT, 3.0, 1.2, 22),
            self.card("RelinKeys\nREDUCE SIZE", COLOR_ENCRYPTION, 3.0, 1.2, 22),
            self.card("GaloisKeys\nROTATE SLOTS", PURPLE_C, 3.0, 1.2, 22),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.55, 0.42))
        client_only = Text("CLIENT ONLY", font_size=20, color=GREEN_C).next_to(keys[0], LEFT, buff=0.3)
        note = Text("Evaluation keys maintain ciphertexts; they do not decrypt.", font_size=24, color=GREY_B)
        note.next_to(keys, DOWN, buff=0.4)
        self.play(FadeIn(subtitle))
        self.play(LaggedStart(*(FadeIn(key, shift=UP * 0.15) for key in keys), lag_ratio=0.16))
        self.play(Write(client_only), Indicate(keys[0], color=GREEN_C))
        self.play(Write(note), Indicate(VGroup(keys[2], keys[3]), color=COLOR_ENCRYPTION))

        boundary = DashedLine(UP * 1.2, DOWN * 2.8, color=GREY_B).shift(RIGHT * 4.2)
        cloud = Text("CLOUD", font_size=20, color=PURPLE_C).next_to(boundary, RIGHT, buff=0.3)
        blocked = Text("BLOCKED", font_size=20, color=RED_A).next_to(boundary, LEFT, buff=0.2)
        secret_attempt = keys[0].copy()
        self.play(Create(boundary), FadeIn(cloud))
        self.play(secret_attempt.animate.next_to(boundary, LEFT, buff=0.2), Write(blocked), Flash(boundary, color=RED_C))

        plain = PlaintextBlock("vector").scale(0.45).shift(LEFT * 4.7 + DOWN * 2.3)
        cipher = CiphertextBlock("Enc(vector)").scale(0.4).shift(LEFT * 1.8 + DOWN * 2.3)
        encrypt_arrow = Arrow(plain.get_right(), cipher.get_left(), buff=0.12, color=COLOR_ENCRYPTION)
        self.play(FadeIn(plain), GrowArrow(encrypt_arrow), FadeIn(cipher), Indicate(keys[1], color=COLOR_PLAINTEXT))

        expanded = self.card("(c0,c1,c2)", RED_C, 1.9, 0.7, 19).shift(RIGHT * 0.9 + DOWN * 2.3)
        compact = self.card("(r0,r1)", COLOR_CIPHERTEXT, 1.7, 0.7, 19).shift(RIGHT * 3.2 + DOWN * 2.3)
        slots = SlotGrid(rows=1, cols=4, filled_indices=range(4), cell_size=0.28).scale(0.75)
        slots.shift(RIGHT * 5.3 + DOWN * 2.3)
        self.play(FadeIn(expanded), TransformFromCopy(expanded, compact), Indicate(keys[2], color=COLOR_ENCRYPTION))
        self.play(FadeIn(slots), slots.animate.shift(RIGHT * 0.25), Indicate(keys[3], color=PURPLE_C))

        bars = VGroup(
            Rectangle(width=3.5, height=0.28, color=RED_C, fill_opacity=0.6),
            Rectangle(width=1.5, height=0.28, color=GREEN_C, fill_opacity=0.6),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(RIGHT * 2.6 + UP * 2.0)
        labels = VGroup(
            Text("all rotations", font_size=18, color=RED_A),
            Text("required rotations", font_size=18, color=GREEN_C),
        )
        labels[0].next_to(bars[0], LEFT, buff=0.2)
        labels[1].next_to(bars[1], LEFT, buff=0.2)
        least = Text("Least privilege for cryptographic capabilities", font_size=21, color=GREEN_C)
        least.next_to(bars, DOWN, buff=0.25)
        self.play(FadeIn(bars), FadeIn(labels), Write(least))
        self.play(FadeOut(VGroup(subtitle, keys, client_only, note, boundary, cloud, blocked, secret_attempt, plain, cipher, encrypt_arrow, expanded, compact, slots, bars, labels, least)))

    def show_seal_objects(self, title):
        subtitle = Text("Microsoft SEAL separates setup, data and evaluation", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.2)
        labels = (
            ("Encryption\nParameters", COLOR_ENCRYPTION),
            ("SEAL\nContext", COLOR_ENCRYPTION),
            ("Key\nGenerator", GREEN_C),
            ("CKKS\nEncoder", COLOR_PLAINTEXT),
            ("Encryptor", COLOR_CIPHERTEXT),
            ("Evaluator", PURPLE_C),
            ("Decryptor", GREEN_C),
        )
        objects = VGroup(*[self.card(label, color, 1.58, 1.0, 18) for label, color in labels]).arrange(RIGHT, buff=0.12).scale(0.82)
        arrows = VGroup(*[self.arrow_between(objects[index], objects[index + 1]) for index in range(6)])
        cloud_frame = SurroundingRectangle(objects[5], color=PURPLE_C, buff=0.18)
        cloud_label = Text("cloud-side workbench", font_size=21, color=PURPLE_C).next_to(cloud_frame, DOWN, buff=0.25)
        self.play(FadeIn(subtitle), FadeIn(objects[0]))
        for item, arrow in zip(objects[1:], arrows):
            self.play(GrowArrow(arrow), FadeIn(item), run_time=0.42)
        self.play(Create(cloud_frame), Write(cloud_label))

        key_branch = VGroup(
            self.card("SecretKey", GREEN_C, 1.45, 0.58, 17),
            self.card("PublicKey", COLOR_PLAINTEXT, 1.45, 0.58, 17),
            self.card("RelinKeys", COLOR_ENCRYPTION, 1.45, 0.58, 17),
            self.card("GaloisKeys", PURPLE_C, 1.45, 0.58, 17),
        ).arrange(RIGHT, buff=0.12).next_to(objects[2], DOWN, buff=0.55)
        branch_arrows = VGroup(*[
            Arrow(objects[2].get_bottom(), key.get_top(), buff=0.08, color=key[0].get_color(), stroke_width=2)
            for key in key_branch
        ])
        self.play(FadeIn(key_branch), Create(branch_arrows))

        pipeline = VGroup(
            self.card("vector", COLOR_PLAINTEXT, 1.2, 0.58, 17),
            self.card("encode", COLOR_ENCRYPTION, 1.3, 0.58, 17),
            self.card("Plaintext", COLOR_PLAINTEXT, 1.5, 0.58, 17),
            self.card("encrypt", COLOR_ENCRYPTION, 1.3, 0.58, 17),
            self.card("Ciphertext", COLOR_CIPHERTEXT, 1.6, 0.58, 17),
        ).arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(pipeline[0]))
        for item in pipeline[1:]:
            self.play(FadeIn(item), run_time=0.3)

        table = VGroup(
            Text("Object", font_size=18, color=WHITE),
            Text("Responsibility", font_size=18, color=WHITE),
            Text("Required key", font_size=18, color=WHITE),
            Text("Evaluator", font_size=17, color=PURPLE_C),
            Text("encrypted arithmetic", font_size=17, color=GREY_B),
            Text("Relin / Galois", font_size=17, color=COLOR_ENCRYPTION),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.22))
        table.move_to(RIGHT * 3.7 + DOWN * 1.5)
        self.play(FadeIn(table))
        self.play(FadeOut(VGroup(subtitle, objects, arrows, cloud_frame, cloud_label, key_branch, branch_arrows, pipeline, table)))

    def construct(self):
        # ==================================================
        # PHAN DOAN 4.1: KEY CAPABILITIES
        # ==================================================
        first_start = scene_time(self)
        title = self.open_lesson(
            "Act 1.4 - Keys and the SEAL Workflow",
            "assets/audio/01_math_crypto/scene_04_keys_and_seal_pipeline.mp3",
        )
        self.show_chapter_plate(
            title,
            "assets/image/01_math_crypto/scene_04_seal_keys.png",
            "Every SEAL key grants a specific cryptographic capability",
            COLOR_ENCRYPTION,
        )
        self.show_key_roles(title)
        self.play_section_beats(first_start, 300, "45:00 - 50:00 | The key family", self.key_beats(), GREEN_C)

        # ==================================================
        # PHAN DOAN 4.2: MICROSOFT SEAL OBJECTS
        # ==================================================
        second_start = scene_time(self)
        self.show_seal_objects(title)
        self.play_section_beats(second_start, 300, "50:00 - 55:00 | Core SEAL objects", self.object_beats(), COLOR_ENCRYPTION)

        # ==================================================
        # PHAN DOAN 4.3: END-TO-END DEPLOYMENT
        # ==================================================
        third_start = scene_time(self)
        self.show_deployment_flow(title)
        self.play_section_beats(third_start, 300, "55:00 - 60:00 | End-to-end lifecycle", self.lifecycle_beats(), COLOR_CIPHERTEXT)

    def show_deployment_flow(self, title):
        subtitle = Text("Five steps from circuit design to verified result", font_size=27, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.2)
        steps = VGroup(
            self.card("1. CIRCUIT\npacking | depth | rotations", COLOR_PLAINTEXT, 2.3, 1.05, 18),
            self.card("2. PARAMETERS\nN | modulus | scale", COLOR_ENCRYPTION, 2.3, 1.05, 18),
            self.card("3. KEYS\nleast privilege", GREEN_C, 2.3, 1.05, 18),
            self.card("4. EVALUATE\nencode | encrypt | compute", PURPLE_C, 2.3, 1.05, 18),
            self.card("5. VERIFY\ndecrypt | decode | compare", COLOR_CIPHERTEXT, 2.3, 1.05, 18),
        ).arrange(RIGHT, buff=0.22).scale(0.9)
        self.play(FadeIn(subtitle), FadeIn(steps[0]))
        for step in steps[1:]:
            self.play(FadeIn(step), run_time=0.45)

        modulus = VGroup(
            *[self.card(bits, COLOR_ENCRYPTION, 1.15, 0.55, 16) for bits in ("60", "40", "40", "60")]
        ).arrange(RIGHT, buff=0.08).shift(LEFT * 3.7 + DOWN * 1.6)
        valid = Text("SEALContext valid", font_size=20, color=GREEN_C).next_to(modulus, DOWN, buff=0.2)
        secret = self.card("SecretKey\nCLIENT", GREEN_C, 1.8, 0.72, 18).shift(DOWN * 1.55)
        eval_keys = self.card("Public + Relin + Galois\nSERVER CAPABILITIES", COLOR_ENCRYPTION, 2.8, 0.72, 17).shift(RIGHT * 3.0 + DOWN * 1.55)
        self.play(FadeIn(modulus), Write(valid), FadeIn(secret), FadeIn(eval_keys))

        encrypted = CiphertextBlock("encrypted result").scale(0.42).shift(RIGHT * 4.8 + DOWN * 2.6)
        baseline = Text("FHE output vs plaintext baseline", font_size=20, color=GREY_B).shift(LEFT * 2.4 + DOWN * 2.65)
        tolerance = Text("|error| < tolerance", font_size=20, color=GREEN_C).next_to(baseline, DOWN, buff=0.18)
        metrics = VGroup(
            *[self.card(metric, COLOR_ENCRYPTION, 1.45, 0.52, 16) for metric in ("Security", "Accuracy", "Latency", "Memory")]
        ).arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.18)
        self.play(FadeIn(encrypted), Write(baseline), Write(tolerance))
        self.play(LaggedStart(*(FadeIn(metric) for metric in metrics), lag_ratio=0.12))
        self.play(FadeOut(VGroup(subtitle, steps, modulus, valid, secret, eval_keys, encrypted, baseline, tolerance, metrics)))

    @staticmethod
    def key_beats():
        return [
            ("Secret key", ["KeyGenerator samples the secret polynomial.", "Decryptor needs it to recover plaintext.", "Exposure compromises every ciphertext under that key."], "Keep the secret key inside the trusted client boundary."),
            ("Public key", ["It enables randomized public-key encryption.", "A data producer can encrypt without learning the secret.", "The server may receive it when encryption is required there."], "Public does not mean optional; it grants encryption capability."),
            ("Relinearization keys", ["They encode key-switching material related to secret powers.", "Evaluator uses them after ciphertext multiplication.", "They reduce a larger ciphertext back to standard size."], "Relin keys grant maintenance, not decryption."),
            ("Galois keys", ["They support selected automorphisms of the ciphertext ring.", "In CKKS these automorphisms appear as slot rotations.", "More rotation steps increase key material and memory."], "Generate the operations the circuit actually needs."),
            ("Key ownership policy", ["Evaluation keys can be shared with the compute server.", "Secret key should remain isolated and access-controlled.", "Key rotation requires re-encryption or migration planning."], "Cryptographic capability should follow least privilege."),
        ]

    @staticmethod
    def object_beats():
        return [
            ("EncryptionParameters", ["Select scheme type CKKS.", "Set polynomial modulus degree.", "Construct a coefficient-modulus chain."], "Parameters describe the cryptographic universe."),
            ("SEALContext", ["Validates parameters and security constraints.", "Builds the linked chain of parameter levels.", "Provides shared precomputation to all core objects."], "Context is the source of compatibility metadata."),
            ("KeyGenerator and key objects", ["Create the secret and public key pair.", "Create RelinKeys for multiplication maintenance.", "Create GaloisKeys for required rotations."], "Key generation follows the circuit capability plan."),
            ("CKKSEncoder, Encryptor, Decryptor", ["Encoder maps vectors to Plaintext at a scale.", "Encryptor converts Plaintext into randomized Ciphertext.", "Decryptor recovers Plaintext for trusted decoding."], "Encoding and encryption are separate transformations."),
            ("Evaluator", ["Runs add, multiply, relinearize, rescale, and rotate.", "It operates without receiving the secret key.", "It requires compatible objects at each operation."], "Evaluator is the untrusted server's main workbench."),
        ]

    @staticmethod
    def lifecycle_beats():
        return [
            ("Step 1: design the circuit", ["Express the workload with CKKS-compatible arithmetic.", "Estimate multiplicative depth and rotation steps.", "Choose packing before selecting parameters."], "Cryptographic setup begins from the computation graph."),
            ("Step 2: create context and keys", ["Instantiate CKKS parameters and SEALContext.", "Generate client secret and public keys.", "Export only required evaluation keys to the server."], "Capabilities are provisioned before data arrives."),
            ("Step 3: encode and encrypt", ["Normalize input values into the expected range.", "Encode packed vectors with the planned scale.", "Encrypt plaintexts using the public key."], "Input preparation determines numerical stability."),
            ("Step 4: evaluate remotely", ["Load ciphertexts under a compatible context.", "Execute arithmetic while tracking level and scale.", "Return an encrypted result without inspecting values."], "The server learns the program shape, not plaintext data."),
            ("Step 5: decrypt, decode, verify", ["The client decrypts with the secret key.", "CKKSEncoder decodes approximate slot values.", "Compare against a plaintext baseline and tolerance."], "Act 1 ends with a complete SEAL mental model."),
        ]
