"""
toys/cursor_tracker.py

Toy 1: Cursor Tracker.

A small circle that follows the mouse cursor inside this panel,
but with a slight delay.
"""

import tkinter as tk


class CursorTrackerToy(tk.Frame):
    DOT_RADIUS = 14
    EASE_FACTOR = 0.15   # how quickly the dot catches up (0-1, higher = snappier)
    FRAME_DELAY_MS = 16  # roughly 60 frames per second

    def __init__(self, parent):
        super().__init__(parent, bg="white")

        tk.Label(
            self, text="Cursor Tracker", font=("Segoe UI", 12, "bold"), bg="white"
        ).pack(pady=(10, 0))
        tk.Label(
            self, text="Move your mouse around the box below.",
            font=("Segoe UI", 9), bg="white", fg="#555555",
        ).pack(pady=(0, 10))

        self.canvas = tk.Canvas(self, bg="#f2f2f2", highlightthickness=1,
                                  highlightbackground="#cccccc")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Track mouse position relative to the canvas.
        self.target_x = 200
        self.target_y = 150
        self.dot_x = 200
        self.dot_y = 150

        self.dot = self.canvas.create_oval(
            self.dot_x - self.DOT_RADIUS, self.dot_y - self.DOT_RADIUS,
            self.dot_x + self.DOT_RADIUS, self.dot_y + self.DOT_RADIUS,
            fill="#3b82f6", outline="",
        )

        self.canvas.bind("<Motion>", self._on_mouse_move)

        self._running = True
        self._animate()

    def _on_mouse_move(self, event):
        self.target_x = event.x
        self.target_y = event.y

    def _animate(self):
        if not self._running:
            return

        # Move the dot a fraction of the remaining distance to the target.
        # This produces a smooth "catching up" effect instead of an instant snap.
        self.dot_x += (self.target_x - self.dot_x) * self.EASE_FACTOR
        self.dot_y += (self.target_y - self.dot_y) * self.EASE_FACTOR

        self.canvas.coords(
            self.dot,
            self.dot_x - self.DOT_RADIUS, self.dot_y - self.DOT_RADIUS,
            self.dot_x + self.DOT_RADIUS, self.dot_y + self.DOT_RADIUS,
        )

        self.after(self.FRAME_DELAY_MS, self._animate)

    def stop(self):
        """Called when navigating away from this toy, to stop the animation loop."""
        self._running = False