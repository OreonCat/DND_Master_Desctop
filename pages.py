from api import ApiConnection
from base_types import AppFrame, GenericLabel
import tkinter.ttk as ttk
from game_objects import DndClass, Race


class StartPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Стартовая страница", None, lambda: controller.show_frame(SettingsPage))
        ttk.Button(self, text="Книжные данные", command=lambda: controller.show_frame(BookDataPage)).pack(padx=10, pady=10)
        ttk.Button(self, text="Персонажи", command=lambda: controller.show_frame(CharactersPage)).pack(padx=10, pady=10)


class BookDataPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Книжные данные", lambda: controller.show_frame(StartPage), lambda: controller.show_frame(SettingsPage))
        ttk.Button(self, text="Классы", command=lambda: controller.show_frame(DndClassPage)).pack(padx=10, pady=10)
        ttk.Button(self, text="Расы", command=lambda: controller.show_frame(RacePage)).pack(padx=10, pady=10)

class DndClassPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Классы", lambda: controller.show_frame(BookDataPage), lambda: controller.show_frame(SettingsPage))
        dnd_classes = DndClass.get_all()
        if dnd_classes is None:
            GenericLabel(self, text="Необходимо авторизоваться").pack(padx=10, pady=10)
        else:
            for dnd_class in dnd_classes:
                GenericLabel(self, text=dnd_class.name).pack(padx=10, pady=10)

class RacePage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Расы", lambda: controller.show_frame(BookDataPage), lambda: controller.show_frame(SettingsPage))
        dnd_races = Race.get_all()
        if dnd_races is None:
            GenericLabel(self, text="Необходимо авторизоваться").pack(padx=10, pady=10)
        else:
            for dnd_race in dnd_races:
                GenericLabel(self, text=dnd_race.name).pack(padx=10, pady=10)

class LoginPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Войти", lambda: controller.show_frame(StartPage), lambda: controller.show_frame(SettingsPage))
        self.controller = controller
        self.username = ttk.Entry(self, width=40)
        self.username.pack(padx=10, pady=10)
        self.password = ttk.Entry(self, width=40)
        self.password.pack(padx=10, pady=10)
        ttk.Button(self, text="Войти", command=lambda: self.login()).pack(padx=10, pady=10)

    def login(self):
        username = self.username.get()
        password = self.password.get()
        ApiConnection.login(username, password)
        self.controller.remake_container()
        self.controller.show_frame(StartPage)

class SettingsPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Настройки", lambda: controller.show_frame(StartPage), lambda: controller.show_frame(SettingsPage))
        self.controller = controller
        if ApiConnection.get_username() is None:
            GenericLabel(self, text="Вы не авторизованы").pack(padx=10, pady=10)
        else:
            GenericLabel(self, text=ApiConnection.get_username()).pack(padx=10, pady=10)
        ttk.Button(self, text="Войти", command=lambda: controller.show_frame(LoginPage)).pack(padx=10, pady=10)
        ttk.Button(self, text="Выйти", command=lambda: self.logout()).pack(padx=10, pady=10)


    def logout(self):
        ApiConnection.logout()
        self.controller.remake_container()
        self.controller.show_frame(StartPage)

class CharactersPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Персонажи", lambda: controller.show_frame(StartPage), lambda: controller.show_frame(SettingsPage))
        controller.add_to_frame(CharPage, "char1", "Persona 3")

        ttk.Button(self, text="Персыч 3", command=lambda: controller.show_frame("char1")).pack(padx=10, pady=10)

class CharPage(AppFrame):
    def __init__(self, parent, controller, pure_data):
        super().__init__(parent, pure_data,lambda: controller.show_frame(CharactersPage), lambda: controller.show_frame(SettingsPage))




