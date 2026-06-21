"""
toys/clicker.py

Toy 2: Clicker / Counter.

The simplest toy: click a button, the count goes up, and the
button briefly "punches" (scales down then back up) for a bit
of tactile feedback.
"""

import tkinter as tk


class ClickerToy(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        tk.Label(
            self, text="Clicker", font=("Segoe UI", 12, "bold"), bg="white"
        ).pack(pady=(10, 0))
        tk.Label(
            self, text="Click the button. That's it. That's the toy.",
            font=("Segoe UI", 9), bg="white", fg="#555555",
        ).pack(pady=(0, 20))

        self.count = 0
        self.count_var = tk.StringVar(value="0")

        tk.Label(
            self, textvariable=self.count_var, font=("Segoe UI", 36, "bold"),
            bg="white", fg="#3b82f6",
        ).pack(pady=(0, 20))

        self.button = tk.Button(
            self, text="Click me", font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", fg="white", relief="flat",
            padx=24, pady=12, cursor="hand2",
            command=self._on_click,
        )
        self.button.pack()

        reset_btn = tk.Button(
            self, text="Reset", font=("Segoe UI", 9), bg="#e5e5e5",
            relief="flat", padx=10, pady=4, cursor="hand2",
            command=self._reset,
        )
        reset_btn.pack(pady=12)

    def _on_click(self):
        self.count += 1
        self.count_var.set(str(self.count))
        self._punch_animation()

    def _reset(self):
        self.count = 0
        self.count_var.set("0")

    def _punch_animation(self, step=0):
        """
        Fakes a 'punch' (squash) effect by briefly shrinking then
        restoring the button's padding over a few quick frames.
        """
        steps = [(18, 8), (24, 12)]  # (padx, pady) shrink then restore
        if step < len(steps):
            padx, pady = steps[step]
            self.button.config(padx=padx, pady=pady)
            self.after(40, lambda: self._punch_animation(step + 1))