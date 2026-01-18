import tkinter as tk
from tkinter import ttk

from api import ApiConnection


class AppFrame(tk.Frame):
    def __init__(self, parent, header_label_text, back_link, settings_link):
        super().__init__(parent, bg="#fcca9a")
        header_frame = tk.Frame(self, bg="#b35600")
        tk.Label(header_frame, text=header_label_text, bg="#b35600", fg="white", font=("Arial", 14)).pack(side="top")
        if back_link is not None:
            ttk.Button(header_frame, text="Назад", command=back_link).pack(side="right")
        ttk.Button(header_frame, text="Настройки", command=settings_link).pack(side="right")
        header_frame.pack(side="top", fill="x")


class SrollFrame(AppFrame):
    def __init__(self, parent, header_label_text, back_link, settings_link):
        super().__init__(parent, header_label_text, back_link, settings_link)
        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        self.new_frame = tk.Frame(canvas, background="#fcca9a")
        window_id = canvas.create_window((0, 0), window=self.new_frame, anchor="nw")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self.new_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(window_id, width=e.width))

class GenericLabel(tk.Label):
    def __init__(self, parent, bg="#fcca9a", font_family="Arial", font_size=14, font_weight = "", *args, **kwargs):
        super().__init__(parent, bg=bg, font=(font_family, font_size, font_weight), *args, **kwargs)
