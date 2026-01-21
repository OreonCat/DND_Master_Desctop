
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

        self.character = character

        #Character info frame
        info_frame = tk.Frame(self.new_frame, bg="#fcca9a")

        #character image
        image_tk = ImageWorks.get_image_tk(character.image, 400, 300)
        image = tk.Label(info_frame, image=image_tk, width=300, height=400)
        image.grid(row=0, column=0, rowspan=10)
        image.image = image_tk

        #character info labels
        self.name_label = GenericLabel(info_frame, text=character.name, font_weight="bold")
        self.race_label = GenericLabel(info_frame, text=f"Раса: {character.race}")
        self.background_label = GenericLabel(info_frame, text=f"Предыстория: {character.background}")
        self.level_label = GenericLabel(info_frame, text=f"Уровень: {character.level} КД: {character.armor_class}")
        self.proficient_bonus_label = GenericLabel(info_frame, text=f"Бонус мастерства: +{character.proficient_bonus}")
        self.speed_label = GenericLabel(info_frame, text=f"Скорость: {character.speed}")
        self.hp_label = GenericLabel(info_frame, text=f"HP: {character.hp}/{character.max_hp}")
        self.initiative_label = GenericLabel(info_frame, text=f"Инициатива: {character.initiative}")
        self.coin_label = GenericLabel(info_frame, text=f"ММ: {character.cooper_coins} СМ: {character.silver_coins} ЗМ: {character.gold_coins}")

        #button "go to gold"
        ttk.Button(info_frame, text="Вывести в золото", command=lambda: self.renew_coin_label()).grid(row=9, column=1)

        #character labels grid
        self.name_label.grid(row=0, column=1, padx=10)
        self.race_label.grid(row=1, column=1, padx=10)
        self.background_label.grid(row=2, column=1, padx=10)
        self.level_label.grid(row=3, column=1, padx=10)
        self.proficient_bonus_label.grid(row=4, column=1, padx=10)
        self.speed_label.grid(row=5, column=1, padx=10)
        self.hp_label.grid(row=6, column=1, padx=10)
        self.initiative_label.grid(row=7, column=1, padx=10)
        self.coin_label.grid(row=8, column=1, padx=10)
        info_frame.pack(padx=10, pady=10)

        abilities_frame = self.get_abilities_frame()
        abilities_frame.pack(padx=10, pady=10)

    def get_abilities_frame(self):
        abilities_frame = tk.Frame(self.new_frame, bg="#fcca9a")
        ability_iterator = 0
        for ability in self.character.abilities:
            ability_frame = AbilitySubFrame(abilities_frame, ability)
            ability_frame.grid(row=0, column=ability_iterator, padx=5, pady=5, sticky="n")
            ability_iterator += 1
        return abilities_frame

    def renew_coin_label(self):
        self.coin_label.config(text=f"ММ: 1250 СМ: {self.character.silver_coins} ЗМ: {self.character.gold_coins}")

#SubFrame
class AbilitySubFrame(tk.Frame):
    def __init__(self, parent, ability):
        tk.Frame.__init__(self, parent, bg="#b35600")
        self.ability = ability
        self.skill_frames = []

        ability_name_label = GenericLabel(self, text=ability.ability, bg="#b35600", fg="white", font_weight="bold")
        self.ability_value_label = GenericLabel(self, text=ability.value, bg="#b35600", fg="white")

        ability_name_label.grid(row=0, column=0)
        self.ability_value_label.grid(row=0, column=3)

        ttk.Button(self, text="-", width=1,command=lambda: self.decrease()).grid(row=0,column=2)
        ttk.Button(self, text="+", width=1,command=lambda: self.increase()).grid(row=0,column=4)

        st_label = GenericLabel(self, text="Спасбросок", bg="#b35600", fg="white")
        self.st_value_label = GenericLabel(self, text=ability.saving_throw, bg="#b35600", fg="white")
        st_label.grid(row=1, column=0)
        self.st_value_label.grid(row=1, column=3)
        self.proficient_button = ttk.Button(self, width=1)
        if ability.is_proficient:
            self.proficient_button.config(text="■", command=lambda: self.make_not_proficient())
        else:
            self.proficient_button.config(text="□", command=lambda: self.make_proficient())
        self.proficient_button.grid(row=1, column=4)

        iterator = 2
        for skill in self.ability.skills:
            self.insert_skill_frames(skill, iterator)
            iterator += 1

    def increase(self):
        self.ability.increase()
        self.ability_value_label.config(text=self.ability.value)
        self.st_value_label.config(text=self.ability.saving_throw)
        for skill_frame in self.skill_frames:
            skill_frame.renew_value_label()

    def decrease(self):
        self.ability.decrease()
        self.ability_value_label.config(text=self.ability.value)
        self.st_value_label.config(text=self.ability.saving_throw)
        for skill_frame in self.skill_frames:
            skill_frame.renew_value_label()

    def make_proficient(self):
        self.ability.make_proficient()
        self.st_value_label.config(text=self.ability.saving_throw)
        self.proficient_button.config(text="■", command=lambda: self.make_not_proficient())

    def make_not_proficient(self):
        self.ability.make_not_proficient()
        self.st_value_label.config(text=self.ability.saving_throw)
        self.proficient_button.config(text="□", command=lambda: self.make_proficient())

    def insert_skill_frames(self, skill, iterator):
        skill_frame = SkillPackedSubController(self, skill)
        skill_frame.skill_name_label.grid(row=iterator, column=0)
        skill_frame.skill_value_label.grid(row=iterator, column=3)
        skill_frame.proficient_button.grid(row=iterator, column=4)
        self.skill_frames.append(skill_frame)



class SkillPackedSubController:
    def __init__(self, parent, skill):
        self.skill = skill
        self.skill_name_label = GenericLabel(parent, text=skill.skill, bg="#b35600", fg="white")
        self.skill_value_label = GenericLabel(parent, text=skill.value, bg="#b35600", fg="white")
        self.proficient_button = ttk.Button(parent, width=1)
        if self.skill.is_proficient:
            self.proficient_button.config(text="■", command=lambda: self.make_not_proficient())
        else:
            self.proficient_button.config(text="□", command=lambda: self.make_proficient())

    def renew_value_label(self):
        self.skill_value_label.config(text=self.skill.value)

    def make_proficient(self):
        self.skill.make_proficient()
        self.renew_value_label()
        self.proficient_button.config(text="■", command=lambda: self.make_not_proficient())

    def make_not_proficient(self):
        self.skill.make_not_proficient()
        self.renew_value_label()
        self.proficient_button.config(text="□", command=lambda: self.make_proficient())

