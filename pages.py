from base_types import AppFrame, GenericLabel
import tkinter.ttk as ttk
from game_objects import DndClass

class StartPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Стартовая страница")
        ttk.Button(self, text="Книжные данные", command=lambda: controller.show_frame(BookDataPage)).pack(padx=10, pady=10)

class BookDataPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Книжные данные")
        ttk.Button(self, text="Классы", command=lambda: controller.show_frame(DndClassPage)).pack(padx=10, pady=10)

class DndClassPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Классы")
        dnd_classes = DndClass.get_all()
        for dnd_class in dnd_classes:
            GenericLabel(self, text=dnd_class.name).pack(padx=10, pady=10)