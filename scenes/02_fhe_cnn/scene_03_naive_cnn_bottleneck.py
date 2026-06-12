import sys
import os
import numpy as np
sys.path.append(".")

from manim import *
from scenes.library.constants import *
from scenes.library.storyboard import StoryboardScene

class NaiveCNNBottleneck(StoryboardScene):
    """10-minute lesson: Why naive ciphertext-per-pixel CNNs are inefficient.
    Total duration strictly managed to 600 seconds."""

    def construct(self):
        self.camera.background_color = "#101214"

        # Tiêu đề với hiệu ứng mượt mà (10 giây)
        title = Tex(r"\textbf{The Naive CNN Bottleneck}", font_size=42, color=WHITE)
        self.play(Write(title), run_time=5)
        self.play(title.animate.to_edge(UP).scale(0.8), run_time=5)

        # 2 Phân đoạn chính, mỗi phân đoạn 295 giây
        self.slot_waste(title)
        self.bootstrapping_queue(title)

    def play_audio(self, filename):
        full_path = os.path.abspath(filename)
        if os.path.exists(full_path):
            try:
                self.add_sound(full_path)
                print(f"\n[SUCCESS] Loaded Audio: {full_path}\n")
            except Exception as e:
                print(f"\n[ERROR] Audio issue: {e}\n")
        else:
            print(f"\n[CRITICAL] MISSING AUDIO: {full_path}\n")

    def slot_waste(self, title):
        """Phần 3.1: Sự lãng phí Slot (295 giây)"""
        self.play_audio("assets/audio/02_fhe_cnn/02_03_01.mp3")

        subtitle = Tex(r"3.1 A Vector Processor Carrying One Useful Value", font_size=32, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        # Khung Ciphertext đại diện
        frame = RoundedRectangle(width=10.0, height=3.5, corner_radius=0.1, color=COLOR_CIPHERTEXT, fill_opacity=0.08).shift(DOWN * 0.5)
        frame_lbl = Tex(r"One CKKS Ciphertext ($N = 8192$ slots)", font_size=28, color=COLOR_CIPHERTEXT).next_to(frame, UP)
        
        self.play(Create(frame), Write(frame_lbl), run_time=4)

        # Tạo lưới Slots (Mô phỏng)
        rows, cols = 4, 16
        slots = VGroup(*[
            Square(side_length=0.4, stroke_color=GREY_D, fill_color=BLACK, fill_opacity=1)
            for _ in range(rows * cols)
        ]).arrange_in_grid(rows=rows, cols=cols, buff=0.1).move_to(frame)

        self.play(FadeIn(slots), run_time=4)

        # Đổ dữ liệu ngây thơ: Chỉ 1 pixel
        active_pixel = slots[0]
        pixel_txt = Tex("px", font_size=20, color=WHITE).move_to(active_pixel)
        
        self.play(active_pixel.animate.set_fill(BLUE_C, opacity=1), Write(pixel_txt), run_time=3)
        self.play(Flash(active_pixel, color=BLUE_C), run_time=2)

        # Nhấn mạnh phần lãng phí
        wasted_slots = VGroup(*[slots[i] for i in range(1, len(slots))])
        
        waste_lbl = Tex(r"\textbf{Massive Waste: 8191 Empty Slots}", font_size=36, color=RED_C).next_to(frame, DOWN, buff=0.5)
        self.play(Write(waste_lbl), run_time=3)
        
        self.play(wasted_slots.animate.set_fill(RED_E, opacity=0.4), run_time=4)

        # --- ĐỈNH CAO 3B1B: HOẠT ẢNH QUÉT LÃNG PHÍ (266 giây) ---
        # Chạy một bộ quét (Scanner) liên tục kiểm tra các slot và báo lỗi đỏ
        scan_line = Line(slots.get_corner(UL) + UP*0.2, slots.get_corner(DL) + DOWN*0.2, color=YELLOW)
        scan_line.move_to(slots.get_left() + LEFT*0.2)
        
        self.play(FadeIn(scan_line), run_time=2)

        scan_tracker = ValueTracker(slots.get_left()[0])
        def scan_updater(m):
            m.move_to(np.array([scan_tracker.get_value(), slots.get_center()[1], 0]))
            
        scan_line.add_updater(scan_updater)

        # Quét đi quét lại chậm rãi trong 260 giây (Padding time)
        self.play(scan_tracker.animate.set_value(slots.get_right()[0]), run_time=130, rate_func=there_and_back)
        self.play(scan_tracker.animate.set_value(slots.get_right()[0]), run_time=130, rate_func=there_and_back)
        
        scan_line.remove_updater(scan_updater)

        self.play(FadeOut(VGroup(subtitle, frame, frame_lbl, slots, pixel_txt, waste_lbl, scan_line)), run_time=4)

    def bootstrapping_queue(self, title):
        """Phần 3.2: Kẹt xe Bootstrapping (295 giây)"""
        self.play_audio("assets/audio/02_fhe_cnn/02_03_02.mp3")

        subtitle = Tex(r"3.2 Sparse Ciphertexts Create a Refresh Traffic Jam", font_size=32, color=GREY_B).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=4)

        # Xây dựng trạm Bootstrapping
        gate_box = RoundedRectangle(width=2.5, height=3, corner_radius=0.2, color=GREEN_C, fill_opacity=0.2).shift(RIGHT * 4 + DOWN * 0.5)
        gate_txt = Tex(r"\textbf{Bootstrapping} \\ \textbf{Gate}", font_size=28, color=WHITE).move_to(gate_box)
        gate = VGroup(gate_box, gate_txt)
        
        belt = Line(LEFT * 7.0, RIGHT * 2.5, color=GREY_C, stroke_width=6).shift(DOWN * 1.5)
        self.play(FadeIn(gate), Create(belt), run_time=4)

        latency_txt = Tex(r"Throughput drops significantly!", font_size=36, color=RED_A).next_to(gate, UP, buff=0.5)
        self.play(Write(latency_txt), run_time=3)

        # --- ĐỈNH CAO 3B1B: MÔ PHỎNG HÀNG ĐỢI KẸT XE (279 giây) ---
        # Hàng ngàn Ciphertexts (hình chữ nhật nhỏ) dồn dập tiến vào băng chuyền
        # Gate chỉ xử lý được 1 cái/giây, nhưng có 5 cái/giây tiến vào -> Hàng đợi phình to.
        
        queue_tracker = ValueTracker(0)
        
        # Hàm vẽ lại băng chuyền liên tục
        conveyor_items = always_redraw(
            lambda: self.draw_traffic_jam(queue_tracker.get_value())
        )
        self.add(conveyor_items)

        # Chạy hoạt ảnh trong 270 giây, t tăng từ 0 đến 100
        # Càng về cuối, hàng đợi xếp chồng lên nhau càng cao và dày đặc
        self.play(queue_tracker.animate.set_value(100), run_time=270, rate_func=linear)
        
        self.play(Flash(gate_box, color=RED, line_length=2, num_lines=16), run_time=4)

        # Clean up
        objects_to_remove = [m for m in self.mobjects]
        self.play(FadeOut(Group(*objects_to_remove)), run_time=5)

    def draw_traffic_jam(self, t):
        """Hàm phụ trợ vẽ hàng đợi kẹt xe dựa trên thời gian t"""
        items = VGroup()
        # Số lượng ciphertexts đang chờ (tăng theo thời gian)
        queue_size = int(t * 1.5) 
        
        for i in range(min(queue_size, 60)): # Hiển thị tối đa 60 khối để tránh lag
            # Tính toán vị trí x: dồn lại ở trước cổng Gate (x = 2.5)
            # Khối càng đến sau thì càng xếp hàng dài về bên trái
            x_pos = 2.5 - (i * 0.3)
            y_pos = -1.2
            
            # Nếu tràn ra khỏi băng chuyền, xếp chồng lên trên
            if x_pos < -6.5:
                row = (i // 30)
                x_pos = 2.5 - ((i % 30) * 0.3)
                y_pos = -1.2 + (row * 0.5)

            # Rung lắc nhẹ do kẹt xe
            y_pos += np.sin(t * 5 + i) * 0.05

            ct = Rectangle(width=0.25, height=0.4, color=RED_C, fill_opacity=0.8)
            ct.move_to(np.array([x_pos, y_pos, 0]))
            items.add(ct)
            
        return items