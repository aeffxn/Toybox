"""
toys/doodle_pad.py

Toy: Doodle Pad.

"""

import tkinter as tk
import theme


COLORS = [
    ("#FFD60A", "Yellow"),
    ("#FFFFFF", "White"),
    ("#E5484D", "Red"),
    ("#34C759", "Green"),
    ("#007AFF", "Blue"),
    ("#FF9500", "Orange"),
    ("#AF52DE", "Purple"),
    ("#0a0a0a", "Eraser"),
]

BRUSH_SIZES = [2, 5, 10, 18]


class DoodlePadToy(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=theme.PANEL)

        theme.toy_title(
            self, "Doodle Pad",
            "Left click to draw. Right click to erase.",
        )

        self.brush_color = theme.GLOW
        self.brush_size = 4
        self._last_x = None
        self._last_y = None

        self._build_toolbar()

        self.canvas = tk.Canvas(
            self, bg=theme.VOID, highlightthickness=1,
            highlightbackground=theme.PANEL_EDGE, cursor="crosshair",
        )
        self.canvas.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<ButtonPress-3>", self._on_press_erase)
        self.canvas.bind("<B3-Motion>", self._on_drag_erase)
        self.canvas.bind("<ButtonRelease-3>", self._on_release)

    def _build_toolbar(self):
        toolbar = tk.Frame(self, bg=theme.PANEL)
        toolbar.pack(fill="x", padx=14, pady=(0, 8))

        # Color swatches
        tk.Label(toolbar, text="Color", bg=theme.PANEL,
                  fg=theme.TEXT_MUTED, font=theme.FONT_SUBTITLE).pack(side="left", padx=(0, 6))
        for hex_color, name in COLORS:
            swatch_bg = "#2a2a2a" if name == "Eraser" else hex_color
            b = tk.Frame(toolbar, bg=swatch_bg, width=22, height=22, cursor="hand2")
            b.pack(side="left", padx=2)
            b.bind("<Button-1>", lambda e, c=hex_color: self._set_color(c))
            b.pack_propagate(False)

        tk.Frame(toolbar, bg=theme.PANEL_EDGE, width=1).pack(
            side="left", fill="y", padx=10, pady=4
        )

        # Brush sizes
        tk.Label(toolbar, text="Size", bg=theme.PANEL,
                  fg=theme.TEXT_MUTED, font=theme.FONT_SUBTITLE).pack(side="left", padx=(0, 6))
        for size in BRUSH_SIZES:
            btn = tk.Button(
                toolbar, text=str(size),
                bg=theme.VOID, fg=theme.TEXT_MUTED,
                relief="flat", font=theme.FONT_SUBTITLE,
                padx=6, pady=2, cursor="hand2",
                command=lambda s=size: self._set_size(s),
            )
            btn.pack(side="left", padx=2)

        tk.Frame(toolbar, bg=theme.PANEL_EDGE, width=1).pack(
            side="left", fill="y", padx=10, pady=4
        )

        # Clear button
        theme.GlowButton(toolbar, "Clear", self._clear, danger=True).pack(
            side="left", padx=2
        )

    def _set_color(self, color):
        self.brush_color = color

    def _set_size(self, size):
        self.brush_size = size

    def _on_press(self, event):
        self._last_x = event.x
        self._last_y = event.y

    def _on_drag(self, event):
        if self._last_x is not None:
            self._draw_stroke(self._last_x, self._last_y, event.x, event.y, self.brush_color)
        self._last_x = event.x
        self._last_y = event.y

    def _on_press_erase(self, event):
        self._last_x = event.x
        self._last_y = event.y

    def _on_drag_erase(self, event):
        if self._last_x is not None:
            self._draw_stroke(self._last_x, self._last_y, event.x, event.y, theme.VOID)
        self._last_x = event.x
        self._last_y = event.y

    def _on_release(self, event):
        self._last_x = None
        self._last_y = None

    def _draw_stroke(self, x1, y1, x2, y2, color):
        r = self.brush_size
        self.canvas.create_line(
            x1, y1, x2, y2,
            fill=color, width=r * 2, capstyle="round", joinstyle="round",
        )

    def _clear(self):
        self.canvas.delete("all")