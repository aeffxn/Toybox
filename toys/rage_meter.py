"""
toys/rage_meter.py

Toy: Rage Meter.

"""

import tkinter as tk
import theme


class RageMeterToy(tk.Frame):
    DRAIN_RATE = 0.004       # how much % drains per frame when not clicking
    CLICK_FILL = 0.1        # how much % each click adds
    FRAME_DELAY_MS = 16
    SHAKE_STEPS = 14

    def __init__(self, parent):
        super().__init__(parent, bg=theme.PANEL)

        theme.toy_title(
            self, "Rage Meter",
            "Click fast to fill the bar before it drains.",
        )

        self.fill = 0.0
        self._shaking = False
        self._shake_step = 0
        self._original_x = None
        self._original_y = None

        # Bar background
        bar_bg = tk.Frame(self, bg=theme.VOID, height=36)
        bar_bg.pack(fill="x", padx=24, pady=(8, 4))
        bar_bg.pack_propagate(False)

        self.bar_fill = tk.Frame(bar_bg, bg=theme.GLOW, width=0)
        self.bar_fill.place(x=0, y=0, relheight=1)

        self.bar_label = tk.Label(
            bar_bg, text="0%", bg=theme.VOID, fg=theme.TEXT_MUTED,
            font=theme.FONT_LABEL,
        )
        self.bar_label.place(relx=0.5, rely=0.5, anchor="center")

        self.status_label = tk.Label(
            self, text="Click the button repeatedly...",
            bg=theme.PANEL, fg=theme.TEXT_MUTED, font=theme.FONT_BODY,
        )
        self.status_label.pack(pady=(4, 14))

        self.button = theme.GlowButton(self, "CLICK ME", self._on_click)
        self.button.pack()

        self._bar_bg = bar_bg
        self._running = True
        self._drain_loop()

    def _on_click(self):
        if self._shaking:
            return
        self.fill = min(1.0, self.fill + self.CLICK_FILL)
        self._update_bar()
        if self.fill >= 1.0:
            self._trigger_rage()

    def _update_bar(self):
        total_w = self._bar_bg.winfo_width()
        fill_w = int(total_w * self.fill)
        self.bar_fill.place(x=0, y=0, relheight=1, width=fill_w)
        pct = int(self.fill * 100)
        self.bar_label.config(text=f"{pct}%")

        if self.fill > 0.75:
            self.bar_fill.config(bg="#E5484D")
            self.bar_label.config(fg=theme.TEXT_MAIN)
            self.status_label.config(text="KEEP GOING!!!", fg="#E5484D")
        elif self.fill > 0.4:
            self.bar_fill.config(bg="#FF9500")
            self.status_label.config(text="Getting there...", fg="#FF9500")
        else:
            self.bar_fill.config(bg=theme.GLOW)
            self.bar_label.config(fg=theme.TEXT_MUTED)
            self.status_label.config(
                text="Click the button repeatedly...", fg=theme.TEXT_MUTED
            )

    def _trigger_rage(self):
        self._shaking = True
        self._shake_step = 0
        self.status_label.config(text="💥 RAGE!", fg="#E5484D")
        self._do_shake()

    def _do_shake(self):
        if self._shake_step >= self.SHAKE_STEPS:
            # Reset after shake
            self.root_window().geometry(
                f"+{self._original_x}+{self._original_y}"
            )
            self.fill = 0.0
            self._shaking = False
            self._update_bar()
            self.status_label.config(
                text="Click the button repeatedly...", fg=theme.TEXT_MUTED
            )
            return

        import random
        win = self.root_window()
        if self._original_x is None:
            self._original_x = win.winfo_x()
            self._original_y = win.winfo_y()

        dx = random.randint(-8, 8)
        dy = random.randint(-8, 8)
        win.geometry(f"+{self._original_x + dx}+{self._original_y + dy}")
        self._shake_step += 1
        self.after(30, self._do_shake)

    def root_window(self):
        return self.winfo_toplevel()

    def _drain_loop(self):
        if not self._running:
            return
        if not self._shaking and self.fill > 0:
            self.fill = max(0.0, self.fill - self.DRAIN_RATE)
            self._update_bar()
        self.after(self.FRAME_DELAY_MS, self._drain_loop)

    def stop(self):
        self._running = False