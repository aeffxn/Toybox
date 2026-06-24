"""
toys/color_shuffle.py

Toy: Color Shuffle.

"""

import tkinter as tk
import random
import theme


BURST_COLORS = [
    "#FF3B30", "#FF9500", "#FFCC00", "#34C759",
    "#00C7BE", "#30B0C7", "#007AFF", "#AF52DE",
    "#FF2D55", "#FF6B35", "#FFD60A",
]


class ColorShuffleToy(tk.Frame):
    BURST_STEPS = 10
    STEP_DELAY_MS = 60

    def __init__(self, parent):
        super().__init__(parent, bg=theme.PANEL)

        theme.toy_title(
            self, "Color Shuffle",
            "Hit the button and watch the color burst.",
        )

        self.display = tk.Frame(self, bg=theme.VOID, height=120)
        self.display.pack(fill="x", padx=14, pady=(0, 10))
        self.display.pack_propagate(False)

        self.color_block = tk.Frame(self.display, bg=theme.GLOW)
        self.color_block.place(relx=0.5, rely=0.5, anchor="center",
                                width=180, height=80)

        self.hex_label = tk.Label(
            self.color_block, text=theme.GLOW, font=(theme.FONT_FAMILY, 11, "bold"),
            bg=theme.GLOW, fg=theme.VOID,
        )
        self.hex_label.place(relx=0.5, rely=0.5, anchor="center")

        theme.GlowButton(self, "Shuffle", self._burst).pack(pady=8)

        self._bursting = False

    def _burst(self):
        if self._bursting:
            return
        self._bursting = True
        self._burst_step(0)

    def _burst_step(self, step):
        if step >= self.BURST_STEPS:
            self._apply_color(theme.GLOW)
            self._bursting = False
            return

        color = random.choice(BURST_COLORS)
        self._apply_color(color)
        self.after(self.STEP_DELAY_MS, lambda: self._burst_step(step + 1))

    def _apply_color(self, color):
        self.color_block.config(bg=color)
        self.hex_label.config(bg=color, text=color)