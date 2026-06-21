"""
theme.py

"""

import tkinter as tk

# ---------------------------------------------------------------------------
# Color tokens
# ---------------------------------------------------------------------------
VOID = "#0a0a0a"            # main window background, near-black
PANEL = "#161616"           # base panel fill (the "glass" surface)
PANEL_EDGE = "#2a2a2a"      # subtle panel border, used where glow is too much
GLOW = "#FFD60A"            # primary signal yellow — active states, glow borders
GLOW_DIM = "#8a7300"        # muted yellow — inactive icons, secondary accents
GLOW_SOFT = "#3a3320"       # very dim yellow, used as a faint glass tint overlay
TEXT_MAIN = "#EDEDED"       # primary text on dark backgrounds
TEXT_MUTED = "#8f8f8f"      # secondary/help text
DANGER = "#E5484D"          # reserved for destructive actions only

FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 16, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 9)
FONT_LABEL = (FONT_FAMILY, 10, "bold")
FONT_BODY = (FONT_FAMILY, 10)
FONT_BIG_NUMBER = (FONT_FAMILY, 38, "bold")


def make_glass_panel(parent, padx=0, pady=0):

    outer = tk.Canvas(parent, bg=VOID, highlightthickness=0)

    def redraw(event=None):
        outer.delete("glass")
        w = outer.winfo_width()
        h = outer.winfo_height()
        if w < 4 or h < 4:
            return

        glow_layers = [GLOW_DIM, "#5e5314", "#3a3320"]
        for i, color in enumerate(glow_layers):
            inset = i
            outer.create_rectangle(
                inset, inset, w - inset, h - inset,
                outline=color, width=1, tags="glass",
            )

        # The actual glass surface.
        outer.create_rectangle(
            3, 3, w - 3, h - 3,
            fill=PANEL, outline=GLOW, width=1, tags="glass",
        )

    inner = tk.Frame(outer, bg=PANEL)

    outer.create_window(4, 4, anchor="nw", window=inner, tags="inner_window")

    def resize_inner(event=None):
        w = outer.winfo_width()
        h = outer.winfo_height()
        if w > 8 and h > 8:
            outer.itemconfig("inner_window", width=w - 8, height=h - 8)

    def on_configure(event=None):
        redraw(event)
        resize_inner(event)

    outer.bind("<Configure>", on_configure)

    if padx or pady:
        inner.configure(padx=padx, pady=pady)

    return outer, inner


class GlowButton(tk.Button):

    def __init__(self, master, text, command, danger=False, outline=False, **kwargs):
        if outline:
            base_bg = PANEL
            base_fg = GLOW
            hover_bg = GLOW_SOFT
            press_bg = "#2a2410"
        elif danger:
            base_bg = DANGER
            base_fg = VOID
            hover_bg = "#F2666B"
            press_bg = "#C73E42"
        else:
            base_bg = GLOW
            base_fg = VOID
            hover_bg = "#FFE14D"
            press_bg = "#E0BD00"

        self._base_bg = base_bg
        self._hover_bg = hover_bg

        super().__init__(
            master,
            text=text,
            command=command,
            bg=base_bg,
            fg=base_fg,
            activebackground=press_bg,
            activeforeground=base_fg,
            font=FONT_LABEL,
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            **kwargs,
        )
        self.bind("<Enter>", lambda e: self.config(bg=self._hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self._base_bg))


def toy_title(parent, title, subtitle=None):

    tk.Label(
        parent, text=title, font=FONT_TITLE, bg=PANEL, fg=GLOW,
    ).pack(pady=(14, 2))
    if subtitle:
        tk.Label(
            parent, text=subtitle, font=FONT_SUBTITLE, bg=PANEL, fg=TEXT_MUTED,
        ).pack(pady=(0, 12))