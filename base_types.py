import tkinter as tk
from tkinter import ttk

class AppFrame(tk.Frame):
    def __init__(self, parent, header_label_text):
        super().__init__(parent, bg="#fcca9a")
        tk.Label(self, text=header_label_text, bg="#b35600", fg="white", font=("Arial", 14)).pack(fill="x")

class GenericLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg="#fcca9a", font=("Arial", 14), *args, **kwargs)
