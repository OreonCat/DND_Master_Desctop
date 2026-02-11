from PIL import ImageTk

from api import ApiConnection, ImageWorks
from base_types import AppFrame, GenericLabel, SrollFrame, BookDataComboBox, IntEntry, BooleanCheckbox
import tkinter.ttk as ttk
import tkinter as tk
from game_objects import DndClass, Race, Character, Background, Game


class StartPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Стартовая страница", None, lambda: controller.show_frame(SettingsPage))
        ttk.Button(self, text="Книжные данные", command=lambda: controller.show_frame(BookDataPage)).pack(padx=10, pady=10)
        ttk.Button(self, text="Персонажи", command=lambda: controller.show_frame(CharactersPage)).pack(padx=10, pady=10)
        ttk.Button(self, text="Игры", command=lambda: controller.show_frame(GamesPage)).pack(padx=10, pady=10)


class BookDataPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Книжные данные", lambda: controller.show_frame(StartPage), lambda: controller.show_frame(SettingsPage))
        ttk.Button(self, text="Классы", command=lambda: controller.show_frame(DndClassPage)).pack(padx=10, pady=10)
        ttk.Button(self, text="Расы", command=lambda: controller.show_frame(RacePage)).pack(padx=10, pady=10)
        ttk.Button(self, text="Предыстории", command=lambda: controller.show_frame(BackgroundPage)).pack(padx=10, pady=10)

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

class BackgroundPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Предыстории", lambda: controller.show_frame(BookDataPage), lambda: controller.show_frame(SettingsPage))
        dnd_background = Background.get_all()
        if dnd_background is None:
            GenericLabel(self, text="Необходимо авторизоваться").pack(padx=10, pady=10)
        else:
            for dnd_background in dnd_background:
                GenericLabel(self, text=dnd_background.name).pack(padx=10, pady=10)

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
        ttk.Button(self.new_frame, text="Добавить персонажа", command=lambda: controller.show_frame(CreateCharacterPage)).pack(padx=10, pady=10)

    def char_frame_generator(self, character):
        char_frame = tk.Frame(self.new_frame, bg="white")

        image_tk = ImageWorks.get_image_tk(character.image, 200, 200)
        label = tk.Label(char_frame, image=image_tk, width=200, height=200)
        label.grid(row=0, column=0, rowspan=5)
        label.image = image_tk

        GenericLabel(char_frame, text=character.name, bg="white").grid(row=0, column=1)
        GenericLabel(char_frame, text=f"{character.dnd_class.name} {character.level}ур", bg="white").grid(row=1, column=1)
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
        self.update_is_not_saved = False
        self.edit_info_display = False

        #Character info frame
        info_frame = tk.Frame(self.new_frame, bg="#fcca9a")

        #character image
        image_tk = ImageWorks.get_image_tk(character.image, 400, 300)
        self.image = tk.Label(info_frame, image=image_tk, width=300, height=400)
        self.image.grid(row=0, column=0, rowspan=10)
        self.image.image = image_tk
        self.update_ins_label = GenericLabel(info_frame, text="Изменения не сохранены")
        self.update_button = ttk.Button(info_frame, text="Сохранить изменения", command=lambda: self.update_character())

        #character info labels
        self.name_label = GenericLabel(info_frame, text=character.name, font_weight="bold")
        self.edit_info_button = ttk.Button(info_frame, text="Изменить", command=lambda: self.edit_button_on_click())
        self.dnd_class_label = GenericLabel(info_frame, text=f"Класc: {character.dnd_class.name} | {character.dnd_subclass}")
        self.race_label = GenericLabel(info_frame, text=f"Раса: {character.race.name}")
        self.background_label = GenericLabel(info_frame, text=f"Предыстория: {character.background.name}")
        self.level_label = GenericLabel(info_frame, text=f"Уровень: {character.level} КД: {character.armor_class}")
        self.proficient_bonus_label = GenericLabel(info_frame, text=f"Бонус мастерства: +{character.proficient_bonus}")
        self.speed_label = GenericLabel(info_frame, text=f"Скорость: {character.speed}")
        self.hp_label = GenericLabel(info_frame, text=f"HP: {character.hp}/{character.max_hp}")
        self.initiative_label = GenericLabel(info_frame, text=f"Инициатива: {character.initiative}")
        self.coin_label = GenericLabel(info_frame, text=f"ММ: {character.cooper_coins} СМ: {character.silver_coins} ЗМ: {character.gold_coins}")

        #character labels grid
        self.name_label.grid(row=0, column=1, padx=10)
        self.edit_info_button.grid(row=0, column=2, padx=10)
        self.dnd_class_label.grid(row=1, column=1, padx=10)
        self.race_label.grid(row=2, column=1, padx=10)
        self.background_label.grid(row=3, column=1, padx=10)
        self.level_label.grid(row=4, column=1, padx=10)
        self.proficient_bonus_label.grid(row=5, column=1, padx=10)
        self.speed_label.grid(row=6, column=1, padx=10)
        self.hp_label.grid(row=7, column=1, padx=10)
        self.initiative_label.grid(row=8, column=1, padx=10)
        self.coin_label.grid(row=9, column=1, padx=10)
        info_frame.pack(padx=10, pady=10)

        # button "go to gold"
        ttk.Button(info_frame, text="Вывести в золото", command=lambda: self.renew_coin_label()).grid(row=10, column=1)

        #abilities
        abilities_frame = self.get_abilities_frame()
        abilities_frame.pack(padx=10, pady=10)

        # info_changes
        self.changes_frame = tk.Frame(self.new_frame, bg="#fcca9a")
        GenericLabel(self.changes_frame, text="Изменить персонажа", font_weight="bold").grid(row=0, column=0, columnspan=2)
        GenericLabel(self.changes_frame, text="Имя").grid(row=1, column=0)
        self.name_field = ttk.Entry(self.changes_frame, width=30)
        GenericLabel(self.changes_frame, text="Класс").grid(row=2, column=0)
        self.class_field = BookDataComboBox(self.changes_frame, DndClass)
        GenericLabel(self.changes_frame, text="Раса").grid(row=3, column=0)
        self.race_field = BookDataComboBox(self.changes_frame, Race)
        GenericLabel(self.changes_frame, text="Предыстория").grid(row=4, column=0)
        self.background_field = BookDataComboBox(self.changes_frame, Background)
        GenericLabel(self.changes_frame, text="Уровень").grid(row=5, column=0)
        self.level_field = IntEntry(self.changes_frame, width=30, min_value=1, max_value=20)
        GenericLabel(self.changes_frame, text="Бонус мастерства").grid(row=6, column=0)
        self.proficient_bonus_field = IntEntry(self.changes_frame, width=30, min_value=0)
        GenericLabel(self.changes_frame, text="Класс доспеха").grid(row=7, column=0)
        self.armor_class_field = IntEntry(self.changes_frame, width=30, min_value=0)
        GenericLabel(self.changes_frame, text="Скорость").grid(row=8, column=0)
        self.speed_field = IntEntry(self.changes_frame, width=30, min_value=0)
        GenericLabel(self.changes_frame, text="Max HP").grid(row=9, column=0)
        self.max_hp_field = IntEntry(self.changes_frame, width=30, min_value=1)
        GenericLabel(self.changes_frame, text="Инициатива").grid(row=10, column=0)
        self.initiative_field = IntEntry(self.changes_frame, width=30)
        GenericLabel(self.changes_frame, text="ММ").grid(row=11, column=0)
        self.cooper_coins_field = IntEntry(self.changes_frame, width=30, min_value=0)
        GenericLabel(self.changes_frame, text="СМ").grid(row=12, column=0)
        self.silver_coins_field = IntEntry(self.changes_frame, width=30, min_value=0)
        GenericLabel(self.changes_frame, text="ЗМ").grid(row=13, column=0)
        self.gold_coins_field = IntEntry(self.changes_frame, width=30, min_value=0)
        GenericLabel(self.changes_frame, text="Подкласс").grid(row=14, column=0)
        self.subclass_field = ttk.Entry(self.changes_frame, width=30)
        GenericLabel(self.changes_frame, text="Изображение").grid(row=15, column=0)
        ttk.Button(self.changes_frame, text="Выбрать", command=lambda: self.select_image()).grid(row=15, column=1)
        self.image_selected_label = GenericLabel(self.changes_frame)
        ttk.Button(self.changes_frame, text="Изменить", command=lambda: self.validate_edit_info()).grid(row=17, column=0, columnspan=2)
        self.selected_image = ""



        self.name_field.grid(row=1, column=1)
        self.class_field.grid(row=2, column=1)
        self.race_field.grid(row=3, column=1)
        self.background_field.grid(row=4, column=1)
        self.level_field.grid(row=5, column=1)
        self.proficient_bonus_field.grid(row=6, column=1)
        self.armor_class_field.grid(row=7, column=1)
        self.speed_field.grid(row=8, column=1)
        self.max_hp_field.grid(row=9, column=1)
        self.initiative_field.grid(row=10, column=1)
        self.cooper_coins_field.grid(row=11, column=1)
        self.silver_coins_field.grid(row=12, column=1)
        self.gold_coins_field.grid(row=13, column=1)
        self.subclass_field.grid(row=14, column=1)

    def get_abilities_frame(self):
        abilities_frame = tk.Frame(self.new_frame, bg="#fcca9a")
        ability_iterator = 0
        for ability in self.character.abilities:
            ability_frame = AbilitySubFrame(abilities_frame, ability)
            ability_frame.grid(row=0, column=ability_iterator, padx=5, pady=5, sticky="n")
            ability_iterator += 1
        return abilities_frame

    def renew_coin_label(self):
        self.character.go_to_gold()
        self.coin_label.config(text=f"ММ: {self.character.cooper_coins} СМ: {self.character.silver_coins} ЗМ: {self.character.gold_coins}")
        self.unsaved_changes()

    def unsaved_changes(self):
        if not self.update_is_not_saved:
            self.update_is_not_saved = True
            self.update_ins_label.grid(row=11, column=0)
            self.update_button.grid(row=11, column=1)


    def edit_button_on_click(self):
        if self.edit_info_display:
            self.changes_frame.pack_forget()
            self.edit_info_display = False
        else:
            self.changes_frame.pack(padx=10, pady=10)
            self.edit_info_display = True

    def validate_edit_info(self):
        self.character.change_info(name=self.name_field.get(), dnd_subclass=self.subclass_field.get(),
                                   max_hp=self.max_hp_field.get(), armor_class=self.armor_class_field.get(),
                                   initiative=self.initiative_field.get(), cooper_coins=self.cooper_coins_field.get(),
                                   silver_coins=self.silver_coins_field.get(), gold_coins=self.gold_coins_field.get(),
                                   level=self.level_field.get(), speed=self.speed_field.get(),
                                   proficient_bonus=self.proficient_bonus_field.get(), dnd_class=self.class_field.get(),
                                   race=self.race_field.get(), background=self.background_field.get(),
                                   selected_image=self.selected_image)
        self.refresh_labels()
        self.edit_button_on_click()
        self.unsaved_changes()

    def refresh_labels(self):
        self.name_label.config(text=self.character.name)
        self.dnd_class_label.config(text=f"Класс: {self.character.dnd_class.name} | {self.character.dnd_subclass}")
        self.race_label.config(text=f"Раса: {self.character.race.name}")
        self.background_label.config(text=f"Предыстория: {self.character.background.name}")
        self.level_label.config(text=f"Уровень: {self.character.level} КД: {self.character.armor_class}")
        self.proficient_bonus_label.config(text=f"Бонус мастерства: +{self.character.proficient_bonus}")
        self.speed_label.config(text=f"Скорость: {self.character.speed}")
        self.hp_label.config(text=f"HP: {self.character.hp}/{self.character.max_hp}")
        self.initiative_label.config(text=f"Инициатива: {self.character.initiative}")
        self.coin_label.config(text=f"ММ: {self.character.cooper_coins} СМ: {self.character.silver_coins} ЗМ: {self.character.gold_coins}")
        image_tk = ImageWorks.get_image_tk(self.character.image, 400, 300)
        self.image.config(image=image_tk)
        self.image.image = image_tk

    def update_character(self):
        if self.update_is_not_saved:
            self.update_is_not_saved = False
            self.update_button.grid_forget()
            self.update_ins_label.grid_forget()
            self.character.update_character()


    def select_image(self):
        self.selected_image = ImageWorks.select_image_from_system()
        self.image_selected_label.config(text=self.selected_image)
        self.image_selected_label.grid(column=0, row=16, columnspan=2)




#SubFrame
class AbilitySubFrame(tk.Frame):
    def __init__(self, parent, ability):
        tk.Frame.__init__(self, parent, bg="#b35600")
        self.ability = ability
        self.skill_frames = []
        self.character_frame = parent.master.master.master

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
        self.character_frame.unsaved_changes()

    def decrease(self):
        self.ability.decrease()
        self.ability_value_label.config(text=self.ability.value)
        self.st_value_label.config(text=self.ability.saving_throw)
        for skill_frame in self.skill_frames:
            skill_frame.renew_value_label()
        self.character_frame.unsaved_changes()

    def make_proficient(self):
        self.ability.make_proficient()
        self.st_value_label.config(text=self.ability.saving_throw)
        self.proficient_button.config(text="■", command=lambda: self.make_not_proficient())
        self.character_frame.unsaved_changes()

    def make_not_proficient(self):
        self.ability.make_not_proficient()
        self.st_value_label.config(text=self.ability.saving_throw)
        self.proficient_button.config(text="□", command=lambda: self.make_proficient())
        self.character_frame.unsaved_changes()

    def insert_skill_frames(self, skill, iterator):
        skill_frame = SkillPackedSubController(self, skill)
        skill_frame.skill_name_label.grid(row=iterator, column=0)
        skill_frame.skill_value_label.grid(row=iterator, column=3)
        skill_frame.proficient_button.grid(row=iterator, column=4)
        self.skill_frames.append(skill_frame)



class SkillPackedSubController:
    def __init__(self, parent, skill):
        self.skill = skill
        self.character_frame = parent.master.master.master.master
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
        self.character_frame.unsaved_changes()

    def make_not_proficient(self):
        self.skill.make_not_proficient()
        self.renew_value_label()
        self.proficient_button.config(text="□", command=lambda: self.make_proficient())
        self.character_frame.unsaved_changes()


class CreateCharacterPage(AppFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Создать персонажа",
                         lambda: controller.show_frame(CharactersPage),
                         lambda: controller.show_frame(SettingsPage))

        self.controller = controller

        form_frame = tk.Frame(self, background="#fcca9a")

        GenericLabel(form_frame, text="Имя").grid(row=0, column=0)
        GenericLabel(form_frame, text="Класс").grid(row=1, column=0)
        GenericLabel(form_frame, text="Раса").grid(row=2, column=0)
        GenericLabel(form_frame, text="Происхождение").grid(row=3, column=0)
        GenericLabel(form_frame, text="Уровень").grid(row=4, column=0)
        GenericLabel(form_frame, text="Бонус мастерства").grid(row=5, column=0)
        GenericLabel(form_frame, text="КД").grid(row=6, column=0)
        GenericLabel(form_frame, text="Скорость").grid(row=7, column=0)
        GenericLabel(form_frame, text="Макс. хп").grid(row=8, column=0)
        GenericLabel(form_frame, text="Инициатива").grid(row=9, column=0)
        GenericLabel(form_frame, text="ММ").grid(row=10, column=0)
        GenericLabel(form_frame, text="СМ").grid(row=11, column=0)
        GenericLabel(form_frame, text="ЗМ").grid(row=12, column=0)
        GenericLabel(form_frame, text="Подклас").grid(row=13, column=0)
        GenericLabel(form_frame, text="Игрок").grid(row=14, column=0)
        GenericLabel(form_frame, text="Изображение").grid(row=15, column=0)
        ttk.Button(form_frame, text="Выбрать", command=lambda: self.choose_image()).grid(row=15, column=1)

        self.chosen_image_link = None

        self.name_field = ttk.Entry(form_frame)
        self.class_field = BookDataComboBox(form_frame, DndClass)
        self.race_field = BookDataComboBox(form_frame, Race)
        self.background_field = BookDataComboBox(form_frame, Background)
        self.level_field = IntEntry(form_frame, min_value=1, max_value=20)
        self.proficient_bonus_field = IntEntry(form_frame, min_value=0)
        self.armor_class_field = IntEntry(form_frame)
        self.speed_field = IntEntry(form_frame, min_value=0)
        self.max_hp_field = IntEntry(form_frame, min_value=0)
        self.initiative_field = IntEntry(form_frame)
        self.cooper_coins_field = IntEntry(form_frame, min_value=0)
        self.silver_coins_field = IntEntry(form_frame, min_value=0)
        self.gold_coins_field = IntEntry(form_frame, min_value=0)
        self.subclass_field = ttk.Entry(form_frame)
        self.chosen_image_label = GenericLabel(form_frame, text="")
        self.is_player_checkbox = BooleanCheckbox(form_frame)

        self.name_field.grid(row=0, column=1)
        self.class_field.grid(row=1, column=1)
        self.race_field.grid(row=2, column=1)
        self.background_field.grid(row=3, column=1)
        self.level_field.grid(row=4, column=1)
        self.proficient_bonus_field.grid(row=5, column=1)
        self.armor_class_field.grid(row=6, column=1)
        self.speed_field.grid(row=7, column=1)
        self.max_hp_field.grid(row=8, column=1)
        self.initiative_field.grid(row=9, column=1)
        self.cooper_coins_field.grid(row=10, column=1)
        self.silver_coins_field.grid(row=11, column=1)
        self.gold_coins_field.grid(row=12, column=1)
        self.subclass_field.grid(row=13, column=1)
        self.is_player_checkbox.grid(row=14, column=1)
        self.chosen_image_label.grid(row=16, column=0, columnspan=2)

        ttk.Button(form_frame, text="Создать", command=lambda: self.create()).grid(row=17, column=0, columnspan=2)

        form_frame.pack()

        self.required_error_label = GenericLabel(self, fg="red")

    def choose_image(self):
        text =  ImageWorks.select_image_from_system()
        self.chosen_image_link = text
        self.chosen_image_label.config(text=text)

    def check_required_fields(self):
        if (self.name_field.get() != "" and self.class_field.get() != "" and self.race_field.get() != ""
                and self.background_field.get() != "" and self.subclass_field.get() != ""):
            self.required_error_label.pack_forget()
            return True
        else:
            self.required_error_label.config(text="Поля имя, класс, раса, и подкласс обязательны к заполнению")
            self.required_error_label.pack()
            return False

    def create(self):
        if self.check_required_fields():
            character_collect = {
                "name": self.name_field.get(),
                "dnd_subclass": self.subclass_field.get(),
                "max_hp": self.max_hp_field.get(),
                "hp": self.max_hp_field.get(),
                "armor_class": self.armor_class_field.get(),
                "initiative": self.initiative_field.get(),
                "cooper_coins": self.cooper_coins_field.get(),
                "silver_coins": self.silver_coins_field.get(),
                "gold_coins": self.gold_coins_field.get(),
                "is_player": self.is_player_checkbox.get(),
                "level": self.level_field.get(),
                "speed": self.speed_field.get(),
                "proficient_bonus": self.proficient_bonus_field.get(),
                "dnd_class": self.class_field.get(),
                "race": self.race_field.get(),
                "background": self.background_field.get(),
            }
            image = self.chosen_image_link
            is_created = Character.create(character_collect, image)
            if is_created:
                self.controller.remake_container()
            else:
                self.required_error_label.config(text="Вероятно такой персонаж уже существует")
                self.required_error_label.pack()

#IN DEVELOP
class GamesPage(SrollFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, "Игры", lambda: controller.show_frame(StartPage),
                         lambda: controller.show_frame(SettingsPage))

        self.controller = controller
        games = Game.get_all()
        for game in games:
            game_frame = self.get_game_frame(game)
            game_frame.pack(padx=10, pady=10)

    def get_game_frame(self, game):
        game_frame = tk.Frame(self.new_frame, bg="white")

        game_image_tk = ImageWorks.get_image_tk(game.image, 400, 400)
        game_image = tk.Label(game_frame, image=game_image_tk, width=200, height=200)
        game_image.image = game_image_tk
        game_image.grid(row=0, column=0, rowspan=3)

        GenericLabel(game_frame, text=game.name, bg="white").grid(row=0, column=1)
        GenericLabel(game_frame, text=game.time_start, bg="white").grid(row=1, column=1)
        self.controller.add_to_frame(page=GamePage, page_name=game.name, pure_data=game)
        name_for_button = game.name
        ttk.Button(game_frame, text="Перейти", command=lambda: self.controller.show_frame(name_for_button)).grid(row=2, column=1)
        return game_frame


class GamePage(SrollFrame):
    def __init__(self, parent, controller, game):
        super().__init__(parent, game.name, lambda: controller.show_frame(GamesPage), lambda: controller.show_frame(SettingsPage))

        self.controller = controller
        self.game = game

        info_frame = tk.Frame(self.new_frame, bg="#fcca9a")

        image_tk = ImageWorks.get_image_tk(game.image, 400, 400)
        image = tk.Label(info_frame, image=image_tk, width=400, height=400)
        image.image = image_tk
        image.grid(row=0, column=0, rowspan=2)
        GenericLabel(info_frame, text=game.name, font_weight="bold").grid(row=0, column=1)
        GenericLabel(info_frame, text=f"Дата начала: {game.time_start}", font_weight="bold").grid(row=1, column=1)
        info_frame.pack(padx=10, pady=10)

        #CHARACTERS
        self.characters_frame = tk.Frame(self.new_frame, bg="#fcca9a")
        GenericLabel(self.characters_frame, text="Игроки", font_size=20, font_weight="bold").pack(padx=10, pady=10)
        self.list_characters_frame = tk.Frame(self.characters_frame, bg="#fcca9a")
        for character in game.characters:
            char_frame = self.get_character_frame(character, self.list_characters_frame)
            char_frame.pack(padx=10, pady=10)
        self.list_characters_frame.pack(padx=10, pady=10)
        ttk.Button(self.characters_frame, text="Добавить", command=lambda: self.add_character_display()).pack(padx=10, pady=10)
        self.add_character_frame = tk.Frame(self.characters_frame, bg="gray")
        self.characters_frame.pack(padx=10, pady=10)

        #ENCOUNTERS
        self.encounters_frame = tk.Frame(self.new_frame, bg="#fcca9a")
        GenericLabel(self.encounters_frame, text="Битвы", font_size=20, font_weight="bold").pack(padx=10, pady=10)
        self.encounters_list_frame = tk.Frame(self.encounters_frame, bg="#fcca9a")
        for encounter in game.encounters:
            enc_frame = self.get_encounter_frame(encounter)
            enc_frame.pack(padx=10, pady=10)
        self.encounters_list_frame.pack(padx=10, pady=10)
        self.encounters_frame.pack(padx=10, pady=10)

    def get_character_frame(self, character, parent, add_action=False):
        char_frame = tk.Frame(parent, bg="white")

        image_tk = ImageWorks.get_image_tk(character.image, 200, 300)
        image = tk.Label(char_frame, image=image_tk, width=200, height=200)
        image.image = image_tk
        image.grid(row=0, column=0, rowspan=4)
        GenericLabel(char_frame, text=character.name, bg="white").grid(row=0, column=1)
        GenericLabel(char_frame, text=f"{character.dnd_class.name} {character.level} ур.", bg="white").grid(row=1, column=1)
        ttk.Button(char_frame, text="Подробнее", command=lambda: self.controller.show_frame(character.name)).grid(row=2,
                                                                                                                  column=1)
        if add_action:
            ttk.Button(char_frame, text="Добавить", command=lambda: self.add_character(character, char_frame)).grid(row=3, column=1)
        else:
            ttk.Button(char_frame, text="Удалить", command=lambda: self.delete_character_from_game(char_frame, character)).grid(row=3, column=1)
        return char_frame

    def add_character_display(self):
        if self.add_character_frame.winfo_manager() == "pack":
            self.add_character_frame.pack_forget()
            for child in self.add_character_frame.winfo_children():
                child.destroy()
        else:
            for character in Character.objects:
                if character not in self.game.characters:
                    char_frame = self.get_character_frame(character, self.add_character_frame, True)
                    char_frame.pack(padx=10, pady=10)
            self.add_character_frame.pack(padx=10, pady=10)

    def delete_character_from_game(self, frame, character):
        self.game.remove_character(character)
        frame.pack_forget()
        frame.destroy()

    def add_character(self, character, add_frame):
        char_frame = self.get_character_frame(character, self.list_characters_frame)
        self.game.add_character(character)
        char_frame.pack(padx=10, pady=10)
        add_frame.pack_forget()

    def get_encounter_frame(self, encounter):
        encounter_frame = tk.Frame(self.encounters_list_frame, bg="white")
        GenericLabel(encounter_frame, text=encounter.time_start, bg="white", font_weight="bold").pack(padx=10, pady=10)
        GenericLabel(encounter_frame, text=f"Ход {encounter.stage}", bg="white").pack(padx=10, pady=10)
        return encounter_frame


