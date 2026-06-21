"""
app.py

Fidget Toy Collection.

"""

import tkinter as tk

import theme
from toys.cursor_tracker import CursorTrackerToy
from toys.kite_flyer import KiteFlyerToy
from toys.clicker import ClickerToy
from toys.quote_popper import QuotePopperToy
from toys.spinner import SpinnerToy


TOY_REGISTRY = [
    ("Cursor Tracker", CursorTrackerToy),
    ("Kite Flyer", KiteFlyerToy),
    ("Clicker", ClickerToy),
    ("Quote Popper", QuotePopperToy),
    ("Spinner Wheel", SpinnerToy),
]


class SidebarItem(tk.Frame):

    def __init__(self, parent, text, on_click):
        super().__init__(parent, bg=theme.VOID)
        self._on_click = on_click
        self.active = False

        self.indicator = tk.Frame(self, bg=theme.VOID, width=3)
        self.indicator.pack(side="left", fill="y")

        self.label = tk.Label(
            self, text=text, font=theme.FONT_BODY, bg=theme.VOID,
            fg=theme.TEXT_MUTED, anchor="w", padx=14, pady=10,
        )
        self.label.pack(side="left", fill="x", expand=True)

        for widget in (self, self.label):
            widget.bind("<Button-1>", lambda e: self._on_click())
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)

    def set_active(self, active):
        self.active = active
        if active:
            self.indicator.config(bg=theme.GLOW)
            self.label.config(fg=theme.GLOW, font=(theme.FONT_FAMILY, 10, "bold"))
        else:
            self.indicator.config(bg=theme.VOID)
            self.label.config(fg=theme.TEXT_MUTED, font=theme.FONT_BODY)

    def _on_enter(self, event):
        if not self.active:
            self.label.config(fg=theme.TEXT_MAIN)

    def _on_leave(self, event):
        if not self.active:
            self.label.config(fg=theme.TEXT_MUTED)


class FidgetToyApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Fidget Toy Collection")
        self.root.geometry("820x560")
        self.root.minsize(680, 460)
        self.root.configure(bg=theme.VOID)

        self.current_toy_frame = None
        self.sidebar_items = []

        self._build_layout()
        self._show_toy(0)

    def _build_layout(self):
        # Sidebar -----------------------------------------------------
        sidebar = tk.Frame(self.root, bg=theme.VOID, width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="FIDGET TOYS", bg=theme.VOID, fg=theme.GLOW,
            font=(theme.FONT_FAMILY, 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(20, 4))
        tk.Label(
            sidebar, text=f"{len(TOY_REGISTRY)} loaded", bg=theme.VOID,
            fg=theme.TEXT_MUTED, font=theme.FONT_SUBTITLE,
        ).pack(anchor="w", padx=16, pady=(0, 16))

        tk.Frame(sidebar, bg=theme.PANEL_EDGE, height=1).pack(fill="x", padx=16, pady=(0, 8))

        for index, (name, _) in enumerate(TOY_REGISTRY):
            item = SidebarItem(sidebar, name, on_click=lambda i=index: self._show_toy(i))
            item.pack(fill="x", pady=1)
            self.sidebar_items.append(item)

        # Main content area --------------------------------------------
        content_outer = tk.Frame(self.root, bg=theme.VOID)
        content_outer.pack(side="left", fill="both", expand=True, padx=16, pady=16)

        self.panel_canvas, self.content_area = theme.make_glass_panel(content_outer)
        self.panel_canvas.pack(fill="both", expand=True)

    def _show_toy(self, index):
        if self.current_toy_frame is not None:
            if hasattr(self.current_toy_frame, "stop"):
                self.current_toy_frame.stop()
            self.current_toy_frame.destroy()

        for i, item in enumerate(self.sidebar_items):
            item.set_active(i == index)

        name, toy_class = TOY_REGISTRY[index]
        self.current_toy_frame = toy_class(self.content_area)
        self.current_toy_frame.pack(fill="both", expand=True)


def main():
    root = tk.Tk()
    FidgetToyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()