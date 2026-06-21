"""
toys/quote_popper.py

Toy 3: Quote Popper.

Click a button and get a random short message from a local list
(see quotes.py).
"""

import tkinter as tk
import random

from quotes import QUOTES


class QuotePopperToy(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        tk.Label(
            self, text="Quote Popper", font=("Segoe UI", 12, "bold"), bg="white"
        ).pack(pady=(10, 0))
        tk.Label(
            self, text="A small message, picked at random.",
            font=("Segoe UI", 9), bg="white", fg="#555555",
        ).pack(pady=(0, 20))

        self.last_quote = None

        self.quote_label = tk.Label(
            self, text="Click below to get a message.",
            font=("Segoe UI", 13), bg="white", fg="#222222",
            wraplength=300, justify="center",
        )
        self.quote_label.pack(pady=20, padx=20)

        tk.Button(
            self, text="Give me a message", font=("Segoe UI", 11, "bold"),
            bg="#3b82f6", fg="white", relief="flat",
            padx=20, pady=10, cursor="hand2",
            command=self._show_random_quote,
        ).pack()

    def _show_random_quote(self):
        choices = QUOTES
        # Avoid showing the exact same quote twice in a row, if there's more than one to pick from.
        if self.last_quote is not None and len(QUOTES) > 1:
            choices = [q for q in QUOTES if q != self.last_quote]

        quote = random.choice(choices)
        self.last_quote = quote
        self.quote_label.config(text=quote)