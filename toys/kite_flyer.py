"""
toys/kite_flyer.py

Toy 5: Kite Flyer.

A small kite that follows the mouse cursor the same way the old
tracker dot did, but now it's drawn as a diamond shape that banks
in the direction it's moving, has a shortribbon tail behind it,
and is connected to a fixed anchor point at the bottom of the canvas
by a string (the anchor point is ofc a human).
"""

import math
import tkinter as tk

import theme


class KiteFlyerToy(tk.Frame):
    EASE_FACTOR = 0.12
    FRAME_DELAY_MS = 16
    KITE_SIZE = 16            # half-width of the kite diamond
    TAIL_SEGMENTS = 4
    STRING_SEGMENTS = 14      # how many straight pieces approximate the curve

    def __init__(self, parent):
        super().__init__(parent, bg=theme.PANEL)

        theme.toy_title(
            self, "Kite Flyer",
            "Move your mouse to fly the kite. Watch the string.",
        )

        self.canvas = tk.Canvas(
            self, bg=theme.VOID, highlightthickness=1,
            highlightbackground=theme.PANEL_EDGE,
        )
        self.canvas.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        # Kite position (eased toward the mouse, same idea as the old tracker).
        self.kite_x = 200
        self.kite_y = 120
        self.target_x = 200
        self.target_y = 120

        # Heading angle, in radians, used to rotate/bank the kite shape.
        # Smoothed over time so the kite doesn't snap its rotation instantly.
        self.heading = -math.pi / 2  # pointing "up" initially

        self.tail = []

        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Configure>", lambda e: self._draw())

        self._running = True
        self._animate()

    def _on_mouse_move(self, event):
        self.target_x = event.x
        self.target_y = event.y

    def _anchor_point(self):
        """The fixed point the string is tied to — bottom center of the canvas."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        return w / 2, max(h - 12, 12)

    def _animate(self):
        if not self._running:
            return

        prev_x, prev_y = self.kite_x, self.kite_y

        self.kite_x += (self.target_x - self.kite_x) * self.EASE_FACTOR
        self.kite_y += (self.target_y - self.kite_y) * self.EASE_FACTOR

        dx = self.kite_x - prev_x
        dy = self.kite_y - prev_y
        speed = math.hypot(dx, dy)

        # Only update heading if actually moving, otherwise keep the last
        # known heading instead of snapping back to a default angle.
        if speed > 0.05:
            target_heading = math.atan2(dy, dx)
            # Smooth the heading change too, so banking looks gradual.
            self.heading = self._lerp_angle(self.heading, target_heading, 0.2)

        self.tail.append((self.kite_x, self.kite_y))
        if len(self.tail) > self.TAIL_SEGMENTS + 1:
            self.tail.pop(0)

        self._draw(speed=speed)
        self.after(self.FRAME_DELAY_MS, self._animate)

    @staticmethod
    def _lerp_angle(current, target, factor):
        """Interpolates between two angles the short way around the circle."""
        diff = (target - current + math.pi) % (2 * math.pi) - math.pi
        return current + diff * factor

    def _draw(self, speed=0.0):
        self.canvas.delete("kite")
        anchor_x, anchor_y = self._anchor_point()

        self._draw_string(anchor_x, anchor_y, speed)
        self._draw_tail()
        self._draw_kite()
        self._draw_anchor(anchor_x, anchor_y)

    def _draw_string(self, anchor_x, anchor_y, speed):

        kx, ky = self.kite_x, self.kite_y

        sag_amount = max(4, 40 - speed * 3)

        points = []
        for i in range(self.STRING_SEGMENTS + 1):
            t = i / self.STRING_SEGMENTS
            x = anchor_x + (kx - anchor_x) * t
            y = anchor_y + (ky - anchor_y) * t
            # Bow the midsection downward using a simple parabola that's
            # zero at both ends (t=0 and t=1) and maximum at the middle.
            bow = sag_amount * (t * (1 - t) * 4)
            points.append((x, y + bow))

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            self.canvas.create_line(
                x1, y1, x2, y2, fill=theme.GLOW_DIM, width=1, tags="kite"
            )

    def _draw_tail(self):
        """A short fading ribbon trailing behind the kite's recent path."""
        if len(self.tail) < 2:
            return
        for i in range(len(self.tail) - 1):
            x1, y1 = self.tail[i]
            x2, y2 = self.tail[i + 1]
            # Older segments are thinner and dimmer.
            fade = (i + 1) / len(self.tail)
            width = max(1, int(3 * fade))
            self.canvas.create_line(
                x1, y1, x2, y2, fill=theme.GLOW_SOFT, width=width, tags="kite"
            )

    def _draw_kite(self):

        cx, cy = self.kite_x, self.kite_y
        size = self.KITE_SIZE

        # Diamond points in local space (pointing along +x before rotation):
        # nose, right wing, tail notch, left wing.
        local_points = [
            (size * 1.3, 0),
            (0, size * 0.7),
            (-size * 0.6, 0),
            (0, -size * 0.7),
        ]

        cos_h = math.cos(self.heading)
        sin_h = math.sin(self.heading)

        world_points = []
        for lx, ly in local_points:
            rx = lx * cos_h - ly * sin_h
            ry = lx * sin_h + ly * cos_h
            world_points.append((cx + rx, cy + ry))

        flat_points = [coord for point in world_points for coord in point]
        self.canvas.create_polygon(
            flat_points, fill=theme.GLOW, outline=theme.GLOW, tags="kite"
        )

        # A thin center spine for a bit of extra kite-like detail.
        nose_x, nose_y = world_points[0]
        tail_x, tail_y = world_points[2]
        self.canvas.create_line(
            nose_x, nose_y, tail_x, tail_y, fill=theme.VOID, width=1, tags="kite"
        )

    def _draw_anchor(self, anchor_x, anchor_y):
        """A small marker showing where the string is tied off."""
        r = 4
        self.canvas.create_oval(
            anchor_x - r, anchor_y - r, anchor_x + r, anchor_y + r,
            fill=theme.GLOW_DIM, outline="", tags="kite",
        )

    def stop(self):
        self._running = False