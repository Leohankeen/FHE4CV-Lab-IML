from manim import *

from .constants import *


class CiphertextBlock(VGroup):
    def __init__(self, label_text="Encrypted", **kwargs):
        super().__init__(**kwargs)
        self.box = Rectangle(
            width=3.0,
            height=1.5,
            color=COLOR_CIPHERTEXT,
            fill_opacity=0.2,
            stroke_width=DEFAULT_STROKE_WIDTH,
        )
        self.label = Text(label_text, font_size=DEFAULT_FONT_SIZE, color=COLOR_MATH)
        self.label.move_to(self.box)
        self.add(self.box, self.label)


class PlaintextBlock(VGroup):
    def __init__(self, label_text="Data", **kwargs):
        super().__init__(**kwargs)
        self.box = Rectangle(
            width=2.5,
            height=1.2,
            color=COLOR_PLAINTEXT,
            fill_opacity=0.5,
            stroke_width=DEFAULT_STROKE_WIDTH,
        )
        self.label = Text(label_text, font_size=DEFAULT_FONT_SIZE, color=COLOR_MATH)
        self.label.move_to(self.box)
        self.add(self.box, self.label)


class SlotGrid(VGroup):
    def __init__(
        self,
        rows=2,
        cols=12,
        filled_indices=None,
        cell_size=0.34,
        empty_opacity=0.16,
        **kwargs,
    ):
        super().__init__(**kwargs)
        filled_indices = set(filled_indices or [])
        cells = []
        for index in range(rows * cols):
            cell = Square(side_length=cell_size, stroke_color=GREY_C, stroke_width=1)
            if index in filled_indices:
                cell.set_fill(COLOR_PLAINTEXT, opacity=0.78)
            else:
                cell.set_fill(COLOR_NOISE, opacity=empty_opacity)
            cells.append(cell)
        self.cells = VGroup(*cells).arrange_in_grid(rows=rows, cols=cols, buff=0.02)
        self.frame = SurroundingRectangle(self.cells, color=COLOR_CIPHERTEXT, buff=0.08)
        self.add(self.frame, self.cells)


class MatrixGrid(VGroup):
    def __init__(self, rows=5, cols=5, cell_size=0.38, color=COLOR_PLAINTEXT, **kwargs):
        super().__init__(**kwargs)
        cells = []
        for row in range(rows):
            for col in range(cols):
                opacity = 0.18 + 0.08 * ((row + col) % 4)
                cell = Square(side_length=cell_size, stroke_color=color, stroke_width=1)
                cell.set_fill(color, opacity=opacity)
                cells.append(cell)
        self.cells = VGroup(*cells).arrange_in_grid(rows=rows, cols=cols, buff=0.03)
        self.add(self.cells)


class BootstrappingGate(VGroup):
    def __init__(self, label_text="Bootstrapping\nGate", **kwargs):
        super().__init__(**kwargs)
        gate = RoundedRectangle(
            width=2.35,
            height=2.6,
            corner_radius=0.08,
            color=COLOR_ENCRYPTION,
            fill_opacity=0.16,
            stroke_width=DEFAULT_STROKE_WIDTH,
        )
        label = Text(label_text, font_size=24, color=COLOR_ENCRYPTION, line_spacing=0.8)
        label.move_to(gate)
        refresh = Text("refresh", font_size=20, color=COLOR_ENCRYPTION).next_to(gate, UP, buff=0.16)
        self.add(gate, label, refresh)


class DepthMeter(VGroup):
    def __init__(self, label_text="Multiplicative depth", level=0.5, **kwargs):
        super().__init__(**kwargs)
        label = Text(label_text, font_size=22, color=COLOR_MATH)
        track = Rectangle(width=3.6, height=0.22, color=GREY_C, fill_opacity=0.18)
        fill = Rectangle(
            width=max(0.05, 3.6 * level),
            height=0.22,
            color=COLOR_ENCRYPTION,
            fill_opacity=0.75,
            stroke_width=0,
        )
        fill.align_to(track, LEFT)
        self.add(label, VGroup(track, fill))
        self.arrange(DOWN, aligned_edge=LEFT, buff=0.18)


class ResNetBlock(VGroup):
    def __init__(self, label_text="Residual block", **kwargs):
        super().__init__(**kwargs)
        body = RoundedRectangle(
            width=2.2,
            height=0.92,
            corner_radius=0.08,
            color=COLOR_CIPHERTEXT,
            fill_opacity=0.14,
        )
        label = Text(label_text, font_size=18, color=COLOR_MATH).move_to(body)
        skip = ArcBetweenPoints(
            body.get_left() + UP * 0.2,
            body.get_right() + UP * 0.2,
            angle=-TAU / 4,
            color=COLOR_ENCRYPTION,
        )
        self.add(body, label, skip)
