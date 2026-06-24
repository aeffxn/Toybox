"""
toys/drift_orb.py

Toy: Drift Orb.

A glowing orb drifts around the canvas on its own, bouncing off
walls with gentle physics. Move your cursor close to it and it gets
repelled — push it around, it'll drift back into its own idle path
over time.
"""

import tkinter as tk
import math
import random
import theme


class DriftOrbToy(tk.Frame):
    FRAME_DELAY_MS = 16
    ORB_RADIUS = 22
    REPEL_RADIUS = 80       # how close before the cursor pushes the orb
    REPEL_STRENGTH = 3.5
    FRICTION = 0.97
    WALL_BOUNCE = 0.7       # energy kept on wall bounce
    IDLE_FORCE = 0.04       # gentle constant nudge to keep it moving when idle

    def __init__(self, parent):
        super().__init__(parent, bg=theme.PANEL)

        theme.toy_title(
            self, "Drift Orb",
            "Move your cursor near it to push it away.",
        )

        self.canvas = tk.Canvas(
            self, bg=theme.VOID, highlightthickness=1,
            highlightbackground=theme.PANEL_EDGE,
        )
        self.canvas.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.orb_x = 200.0
        self.orb_y = 150.0
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)

        self.mouse_x = -999
        self.mouse_y = -999

        # Idle "target" direction — gives the orb a gentle nudge when
        # it slows down, so it never completely stops drifting.
        self._idle_angle = random.uniform(0, 2 * math.pi)

        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Leave>", self._on_mouse_leave)
        self.canvas.bind("<Configure>", self._on_resize)

        self._running = True
        self._animate()

    def _on_mouse_move(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def _on_mouse_leave(self, event):
        self.mouse_x = -999
        self.mouse_y = -999

    def _on_resize(self, event):
        # Keep orb inside new bounds after a resize.
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        r = self.ORB_RADIUS
        self.orb_x = max(r, min(w - r, self.orb_x))
        self.orb_y = max(r, min(h - r, self.orb_y))

    def _animate(self):
        if not self._running:
            return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        r = self.ORB_RADIUS

        if w < 10 or h < 10:
            self.after(self.FRAME_DELAY_MS, self._animate)
            return

        # Cursor repulsion — push the orb away if the mouse is close.
        dx = self.orb_x - self.mouse_x
        dy = self.orb_y - self.mouse_y
        dist = math.hypot(dx, dy)
        if 0 < dist < self.REPEL_RADIUS:
            force = self.REPEL_STRENGTH * (1 - dist / self.REPEL_RADIUS)
            self.vx += (dx / dist) * force
            self.vy += (dy / dist) * force

        # Idle drift force — slowly steer toward the idle angle so the
        # orb never just sits perfectly still.
        speed = math.hypot(self.vx, self.vy)
        if speed < 0.8:
            self._idle_angle += random.uniform(-0.3, 0.3)
            self.vx += math.cos(self._idle_angle) * self.IDLE_FORCE
            self.vy += math.sin(self._idle_angle) * self.IDLE_FORCE

        # Cap max speed so it doesn't fly off the canvas.
        max_speed = 8.0
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed

        self.vx *= self.FRICTION
        self.vy *= self.FRICTION

        self.orb_x += self.vx
        self.orb_y += self.vy

        # Bounce off walls
        if self.orb_x - r < 0:
            self.orb_x = r
            self.vx = abs(self.vx) * self.WALL_BOUNCE
        elif self.orb_x + r > w:
            self.orb_x = w - r
            self.vx = -abs(self.vx) * self.WALL_BOUNCE

        if self.orb_y - r < 0:
            self.orb_y = r
            self.vy = abs(self.vy) * self.WALL_BOUNCE
        elif self.orb_y + r > h:
            self.orb_y = h - r
            self.vy = -abs(self.vy) * self.WALL_BOUNCE

        self._draw()
        self.after(self.FRAME_DELAY_MS, self._animate)

    def _draw(self):
        self.canvas.delete("orb")
        x, y = self.orb_x, self.orb_y
        r = self.ORB_RADIUS
        speed = math.hypot(self.vx, self.vy)

        # Outer glow rings — more rings / wider spread when moving fast.
        glow_layers = 3
        for i in range(glow_layers, 0, -1):
            glow_r = r + (i * 6) + (speed * 1.5)
            alpha_colors = ["#1a1500", "#2a2200", "#3a3010"]
            self.canvas.create_oval(
                x - glow_r, y - glow_r, x + glow_r, y + glow_r,
                fill=alpha_colors[i - 1], outline="", tags="orb",
            )

        # Main orb body
        self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=theme.GLOW, outline=theme.GLOW, width=1, tags="orb",
        )

        # Inner highlight (top-left) for a slight 3D feel
        hr = r * 0.4
        self.canvas.create_oval(
            x - r * 0.4 - hr, y - r * 0.5 - hr,
            x - r * 0.4 + hr, y - r * 0.5 + hr,
            fill="#FFF8C0", outline="", tags="orb",
        )

    def stop(self):
        self._running = False