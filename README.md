# 🟡 Toybox

![Python](https://img.shields.io/badge/Python-3.8%2B-yellow?style=flat-square&logo=python&logoColor=black)
![GUI](https://img.shields.io/badge/GUI-Tkinter-black?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-black?style=flat-square)

A desktop "fidget toy" collection built entirely in Python with Tkinter — a handful of small, self-contained interactive toys, wrapped in a custom black & yellow UI. Pick a toy from the sidebar, mess with it, switch to another.

---

## 📑 Table of Contents

- [Toys Included](#-toys-included)
- [Planned / Coming Soon](#-planned--coming-soon)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [The Theme](#-the-theme)
- [Adding a New Toy](#-adding-a-new-toy)

---

## 🎮 Toys Included

| Toy | What it does |
|---|---|
| **Cursor Tracker** | A glowing dot eases toward your mouse cursor, leaving a short fading trail behind it |
| **Kite Flyer** | A small kite is flown by your cursor, tied to a fixed anchor point by a string that sags when still and pulls taut when moving fast |
| **Clicker** | Click a button, the counter goes up, with a little "punch" animation on every click |
| **Quote Popper** | Click for a random short message from a local list — no internet involved, just a list of strings |
| **Spinner Wheel** | Click and drag sideways to flick the wheel — it spins and gradually slows down due to simulated friction |

---

## 🚧 Planned / Coming Soon

This project is being built incrementally — new toys get added over time. Currently planned:

- [ ] **Keystroke Detector** — captures key presses with a unique animation per key
- [ ] **Sandbox** — a falling-particle physics sandbox with selectable materials (sand, water, stone, ice, fire) that interact with each other realistically
- [ ] **Doodle Pad** — a simple freehand drawing canvas
- [ ] **Color Shuffle** — a button that bursts the UI's accent color momentarily
- [ ] **Sound Pads** — a grid of pads that each play a short sound on click
- [ ] **Particle Burst** — a burst of particles wherever you click
- [ ] **Rage Meter** — a button that fills up with rapid clicking, then triggers something once maxed
- [ ] **Drift Orb** — a shape that floats around on its own and reacts when nudged by the cursor

---

## 🛠 Requirements

- Python 3.8+
- `tkinter` — included with most Python installations

Check if you have Python:

```bash
python3 --version
```

Check if you have tkinter:

```bash
python3 -m tkinter
```

A small test window should pop up. If you get a `No module named tkinter` error:

| OS | Fix |
|---|---|
| Windows | Reinstall Python from python.org, make sure "tcl/tk and IDLE" is checked during setup |
| macOS | `brew install python-tk` |
| Ubuntu/Debian | `sudo apt install python3-tk` |
| Fedora | `sudo dnf install python3-tkinter` |

---

## 📦 Installation

```bash
git clone https://github.com/aeffxn/Toybox.git
cd glass-toybox
python3 main.py
```

---

## 📂 Project Structure

```
Toybox/
├── main.py             # entry point — run this
├── app.py              # app shell: sidebar navigation, toy switching
├── theme.py             # shared color tokens + glass panel/button helpers
├── quotes.py             # local message list used by the Quote Popper
└── toys/
    ├── __init__.py
    ├── cursor_tracker.py
    ├── kite_flyer.py
    ├── clicker.py
    ├── quote_popper.py
    └── spinner.py
```

Each toy lives in its own file inside `toys/` and is completely self-contained — no toy depends on another toy's code.

---

## ⚙️ How It Works

- **`app.py`** builds the window shell: a sidebar listing every registered toy, and a main panel that displays whichever one is currently selected.
- Every toy is a `tkinter.Frame` subclass that knows how to build and run itself. When you click a toy in the sidebar, the previous toy's frame is destroyed and the new one is created in its place inside the main panel.
- Toys that animate continuously (Cursor Tracker, Kite Flyer, Spinner Wheel) use Tkinter's `.after()` method to schedule the next animation frame roughly every 16ms (~60 FPS), and implement a `stop()` method that's called automatically when you switch away from them — this stops the animation loop instead of letting it keep running invisibly in the background.
- **`theme.py`** centralizes every color and font used across the whole app, plus two reusable helpers: `make_glass_panel()` (builds the glowing-border panel look) and `GlowButton` (a themed button with hover/press states). Every toy imports from here instead of hardcoding its own colors.
- **`quotes.py`** is just a plain Python list of strings, kept separate from the Quote Popper's UI code so the list can be edited or expanded without touching any logic.

---

## 🎨 The Theme

The app uses a black background with a single yellow accent color (`#FFD60A`) applied consistently across every toy — buttons, borders, glowing highlights, and the active sidebar indicator.

**A note on "glass":** I really wanted to implement the full Liquid Glass just like in iOS 26 and above, but Tkinter has no way to blur the actual desktop behind the window — that requires OS-level compositor support that plain Tkinter doesn't expose. What's used here instead is a "glass panel" effect: a handful of nested rectangles drawn on a `Canvas`, fading from dim yellow toward the panel's base color, to fake a soft glowing border. It's a deliberate stand-in for true glass/blur, not an attempt to fake something it can't actually do. In future updates I will try to make it better, but this is all I can do for now :)

---

## ➕ Adding a New Toy

The architecture is built so adding another toy doesn't require touching any existing toy's code. To add one:

1. Create a new file in `toys/`, e.g. `toys/my_new_toy.py`
2. Inside it, define a class that subclasses `tk.Frame`, builds its own UI in `__init__`, and (if it animates) implements a `stop()` method:

```python
import tkinter as tk
import theme

class MyNewToy(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=theme.PANEL)
        theme.toy_title(self, "My New Toy", "A short description.")
        # ... build the rest of the toy's UI here ...

    def stop(self):
        # only needed if this toy has a running animation loop
        self._running = False
```

3. In `app.py`, import the new class and add one line to `TOY_REGISTRY`:

```python
from toys.my_new_toy import MyNewToy

TOY_REGISTRY = [
    # ...existing toys...
    ("My New Toy", MyNewToy),
]
```

That's it — the sidebar entry, navigation, and panel switching are all handled automatically by the existing app shell.

---