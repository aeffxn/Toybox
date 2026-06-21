"""
toys/spinner.py

Toy 4: Spinner Wheel.

Click and drag (or just click) the wheel to "flick" it, and it
spins with friction, slowing down until it stops.
"""

import tkinter as tk
import math


class SpinnerToy(tk.Frame):
    FRICTION = 0.985        # speed is multiplied by this every frame (closer to 1 = spins longer)
    MIN_SPEED = 0.05        # below this, we just stop to avoid an endless tiny spin
    FRAME_DELAY_MS = 16
    NUM_SPOKES = 8

    def __init__(self, parent):
        super().__init__(parent, bg="white")

        tk.Label(
            self, text="Spinner Wheel", font=("Segoe UI", 12, "bold"), bg="white"
        ).pack(pady=(10, 0))
        tk.Label(
            self, text="Click and drag sideways across the wheel to flick it.",
            font=("Segoe UI", 9), bg="white", fg="#555555",
        ).pack(pady=(0, 10))

        self.canvas = tk.Canvas(self, bg="#f2f2f2", highlightthickness=1,
                                  highlightbackground="#cccccc")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.angle = 0.0       # current rotation, in degrees
        self.speed = 0.0       # degrees per frame
        self._last_drag_x = None
        self._spokes = []

        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

        self._running = True
        self._animate()

    def _on_resize(self, event):
        # Redraw the wheel centered whenever the panel is resized.
        self._draw_wheel()

    def _center(self):
        return self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2

    def _draw_wheel(self):
        self.canvas.delete("wheel")
        cx, cy = self._center()
        radius = min(cx, cy) - 20
        if radius <= 0:
            return

        # Outer ring
        self.canvas.create_oval(
            cx - radius, cy - radius, cx + radius, cy + radius,
            outline="#3b82f6", width=4, tags="wheel",
        )

        # Spokes, so the rotation is actually visible.
        for i in range(self.NUM_SPOKES):
            spoke_angle = math.radians(self.angle + (360 / self.NUM_SPOKES) * i)
            x_end = cx + radius * math.cos(spoke_angle)
            y_end = cy + radius * math.sin(spoke_angle)
            self.canvas.create_line(
                cx, cy, x_end, y_end, fill="#3b82f6", width=2, tags="wheel"
            )

        # Center hub
        self.canvas.create_oval(
            cx - 10, cy - 10, cx + 10, cy + 10,
            fill="#3b82f6", outline="", tags="wheel",
        )

    def _on_press(self, event):
        self._last_drag_x = event.x
        self.speed = 0.0  # stop momentum while actively dragging

    def _on_drag(self, event):
        if self._last_drag_x is not None:
            dx = event.x - self._last_drag_x
            # Horizontal drag distance becomes rotation speed.
            self.speed = dx * 0.8
            self.angle += self.speed
            self._last_drag_x = event.x
            self._draw_wheel()

    def _on_release(self, event):
        self._last_drag_x = None
        # speed stays as-is from the last drag movement, so it keeps spinning.

    def _animate(self):
        if not self._running:
            return

        if abs(self.speed) > self.MIN_SPEED:
            self.angle = (self.angle + self.speed) % 360
            self.speed *= self.FRICTION
            self._draw_wheel()
        elif self.speed != 0.0:
            self.speed = 0.0  # snap tiny residual speed to a full stop

        self.after(self.FRAME_DELAY_MS, self._animate)

    def stop(self):
        self._running = False