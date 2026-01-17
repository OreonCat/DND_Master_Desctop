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




class GenericLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg="#fcca9a", font=("Arial", 14), *args, **kwargs)
