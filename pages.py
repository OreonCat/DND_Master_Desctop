from base_types import AppFrame, GenericLabel
import tkinter.ttk as ttk
from game_objects import DndClass, Race


class StartPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Стартовая страница", None)
        ttk.Button(self, text="Книжные данные", command=lambda: controller.show_frame(BookDataPage)).pack(padx=10, pady=10)


class BookDataPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Книжные данные", lambda: controller.show_frame(StartPage))
        ttk.Button(self, text="Классы", command=lambda: controller.show_frame(DndClassPage)).pack(padx=10, pady=10)
        ttk.Button(self, text="Расы", command=lambda: controller.show_frame(RacePage)).pack(padx=10, pady=10)

class DndClassPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Классы", lambda: controller.show_frame(BookDataPage))
        dnd_classes = DndClass.get_all()
        if dnd_classes is None:
            GenericLabel(self, text="Необходимо авторизоваться").pack(padx=10, pady=10)
        else:
            for dnd_class in dnd_classes:
                GenericLabel(self, text=dnd_class.name).pack(padx=10, pady=10)

class RacePage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Расы", lambda: controller.show_frame(BookDataPage))
        dnd_races = Race.get_all()
        if dnd_races is None:
            GenericLabel(self, text="Необходимо авторизоваться").pack(padx=10, pady=10)
        else:
            for dnd_race in dnd_races:
                GenericLabel(self, text=dnd_race.name).pack(padx=10, pady=10)