
from api import ApiConnection, ImageWorks
from base_types import AppFrame, GenericLabel, SrollFrame
import tkinter.ttk as ttk
import tkinter as tk
from game_objects import DndClass, Race, Character


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

class CharactersPage(SrollFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Персонажи", lambda: controller.show_frame(StartPage), lambda: controller.show_frame(SettingsPage))
        self.characters = Character.get_all()
        self.controller = controller

        if self.characters is None:
            GenericLabel(self.new_frame, text="Вы не авторизованы").pack(padx=10, pady=10)
        else:
            for character in self.characters:
                self.char_frame_generator(character)

    def char_frame_generator(self, character):
        char_frame = tk.Frame(self.new_frame, bg="white")

        image_tk = ImageWorks.get_image_tk(character.image, 200, 200)
        label = tk.Label(char_frame, image=image_tk, width=200, height=200)
        label.grid(row=0, column=0, rowspan=5)
        label.image = image_tk

        GenericLabel(char_frame, text=character.name, bg="white").grid(row=0, column=1)
        GenericLabel(char_frame, text=f"{character.dnd_class} {character.level}ур", bg="white").grid(row=1, column=1)
        GenericLabel(char_frame, text=f"{character.hp}/{character.max_hp}", bg="white").grid(row=2, column=1)

        char_frame.pack(padx=10, pady=10)
        self.controller.add_to_frame(page=CharPage, page_name=character.name, pure_data=character)
        but_link = character.name
        if character.is_player:
            GenericLabel(char_frame, text="Игрок").grid(row=3, column=1)
        else:
            GenericLabel(char_frame, text="NPC").grid(row=3, column=1)
        ttk.Button(char_frame, text="Подробнее", command=lambda: self.controller.show_frame(but_link)).grid(row=4, column=1)

class CharPage(SrollFrame):
    def __init__(self, parent, controller, character):
        super().__init__(parent, character.name ,lambda: controller.show_frame(CharactersPage), lambda: controller.show_frame(SettingsPage))

        info_frame = tk.Frame(self.new_frame, bg="#fcca9a")

        image_tk = ImageWorks.get_image_tk(character.image, 400, 300)
        image = tk.Label(info_frame, image=image_tk, width=300, height=400)
        image.grid(row=0, column=0, rowspan=10)
        image.image = image_tk

        GenericLabel(info_frame, text=character.name, font_weight="bold").grid(row=0, column=1, padx=10)
        GenericLabel(info_frame, text=f"Раса: {character.race}").grid(row=1, column=1, padx=10)
        GenericLabel(info_frame, text=f"Предыстория: {character.background}").grid(row=2, column=1, padx=10)
        GenericLabel(info_frame, text=f"Уровень: {character.level} КД: {character.armor_class}").grid(row=3, column=1, padx=10)
        GenericLabel(info_frame, text=f"Бонус мастерства: +{character.proficient_bonus}").grid(row=4, column=1, padx=10)
        GenericLabel(info_frame, text=f"Скорость: {character.speed}").grid(row=5, column=1, padx=10)
        GenericLabel(info_frame, text=f"HP: {character.hp}/{character.max_hp}").grid(row=6, column=1, padx=10)
        GenericLabel(info_frame, text=f"Инициатива: {character.initiative}").grid(row=7, column=1, padx=10)
        GenericLabel(info_frame, text=f"ММ: {character.cooper_coins} СМ: {character.silver_coins} ЗМ: {character.gold_coins}").grid(row=8, column=1, padx=10)
        ttk.Button(info_frame, text="Вывести в золото").grid(row=9, column=1)
        info_frame.pack(padx=10, pady=10)

        self.abilities_frame = tk.Frame(self.new_frame, bg="#fcca9a")
        ability_iterator = 0
        for ability in character.abilities:
            self.ability_gen(ability, ability_iterator)
            ability_iterator += 1
        self.abilities_frame.pack(padx=10, pady=10)

    def ability_gen(self, ability, iterator):
        ability_frame = tk.Frame(self.abilities_frame, background="#b35600")

        GenericLabel(ability_frame, text=ability.ability, bg="#b35600", fg="white", font_weight="bold").grid(row=0, column=0)
        ability_value = GenericLabel(ability_frame, text=ability.value, bg="#b35600", fg="white")
        ability_value.grid(row=0, column=3)

        GenericLabel(ability_frame, text="Спасбросок", bg="#b35600", fg="white").grid(row=1, column=0)
        saving_trow_value = GenericLabel(ability_frame, text=ability.saving_throw, bg="#b35600", fg="white")
        saving_trow_value.grid(row=1, column=3)


        if ability.is_proficient:
            prof_button = ttk.Button(ability_frame, text="■", width=1, command=lambda: ability.make_not_proficient(saving_trow_value, prof_button))
        else:
            prof_button = ttk.Button(ability_frame, text="□", width=1, command=lambda: ability.make_proficient(saving_trow_value, prof_button))
        prof_button.grid(row=1, column=4)

        skill_iterator = 2
        skill_value_labels = []
        for skill in ability.skills:
            GenericLabel(ability_frame, text=skill.skill, bg="#b35600", fg="white").grid(row=skill_iterator, column=0)
            skill_value_label = GenericLabel(ability_frame, text=skill.value, bg="#b35600", fg="white")
            skill_value_label.grid(row=skill_iterator, column=3)
            skill_value_labels.append(skill_value_label)
            self.skill_buttons(skill, ability_frame, skill_value_label, skill_iterator)
            skill_iterator += 1

        ttk.Button(ability_frame, text="-", width=1,
                   command=lambda: ability.decrease(ability_value, saving_trow_value, skill_value_labels)).grid(row=0,
                                                                                            column=2)
        ttk.Button(ability_frame, text="+", width=1,
                   command=lambda: ability.increase(ability_value, saving_trow_value, skill_value_labels)).grid(row=0,
                                                                                            column=4)

        ability_frame.grid(row=0, column=iterator, padx=5, pady=5, sticky="n")

    def skill_buttons(self, skill, ability_frame, skill_value_label, iterator):
        if skill.is_proficient:
            skill_button = ttk.Button(ability_frame, text="■", width=1,
                                      command=lambda: skill.make_not_proficient(skill_value_label, skill_button))
        else:
            skill_button = ttk.Button(ability_frame, text="□", width=1,
                                      command=lambda: skill.make_proficient(skill_value_label, skill_button))
        skill_button.grid(row=iterator, column=4)




