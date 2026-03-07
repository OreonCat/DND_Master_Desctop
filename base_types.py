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

class BookDataComboBox(ttk.Combobox):
    def __init__(self, parent, data_class, *args, **kwargs):
        self.display_text = data_class.get_names()
        self.values_collection = data_class.get_values()
        super().__init__(parent, values=self.display_text, *args, **kwargs)

    def get(self):
        actual_choice = super().get()
        return self.values_collection[actual_choice] if actual_choice != "" else ""

class IntEntry(ttk.Entry):
    def __init__(self, parent, min_value=None, max_value=None, *args, **kwargs):
        self.var = tk.StringVar()
        super().__init__(parent, textvariable=self.var, *args, **kwargs)
        self.var.trace("w", self.check_int)
        self.min_value = min_value
        self.max_value = max_value

    def check_int(self, *args):
        check_var = self.var.get()
        if not check_var == "" and not check_var == "-" and not check_var.lstrip('-').isdigit():
            self.var.set(self.var.get()[:-1])
        else:
            if not self.var.get() == "" and not self.var.get() == "-":
                if self.min_value is not None and int(self.var.get()) < self.min_value:
                    self.var.set(str(self.min_value))
                if self.max_value is not None and int(self.var.get()) > self.max_value:
                    self.var.set(str(self.max_value))

    def clear(self):
        self.var.set("")

class BooleanCheckbox(ttk.Checkbutton):
    def __init__(self, parent, *args, **kwargs):
        self.boolean_var = tk.BooleanVar()
        style = ttk.Style()
        style.configure("TCheckbutton", background="#fcca9a")
        super().__init__(parent, variable = self.boolean_var, style="TCheckbutton", *args, **kwargs)

    def get(self):
        return self.boolean_var.get()






