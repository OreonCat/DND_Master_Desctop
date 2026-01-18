from api import ApiConnection

class BookDataClass:
    get_link = None

    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    @classmethod
    def get_all(cls):
        api_objects = ApiConnection.get(cls.get_link)
        if api_objects is None:
            return None
        ret_list = []
        for cl in api_objects:
            ret_list.append(cls(cl['id'], cl['name'], cl['image']))
        return ret_list

class DndClass(BookDataClass):
    get_link = "bookdata/dndclass"


class Race(BookDataClass):
    get_link = "bookdata/race"


class Skill:
    def __init__(self, id, skill, value, is_proficient, character_link):
        self.id = id
        self.skill = skill
        self.value = value
        self.is_proficient = is_proficient
        self.character_link = character_link

    def make_proficient(self, val_label, button):
        if not self.is_proficient:
            self.is_proficient = True
            self.value += self.character_link.proficient_bonus
            val_label.config(text = str(self.value))
            button.config(text="■", command=lambda: self.make_not_proficient(val_label, button))

    def make_not_proficient(self, val_label, button):
        if self.is_proficient:
            self.is_proficient = False
            self.value -= self.character_link.proficient_bonus
            val_label.config(text = str(self.value))
            button.config(text="□", command=lambda: self.make_proficient(val_label, button))

class Ability:
    def __init__(self, id, ability, value, is_proficient, saving_throw, character_link):
        self.id = id
        self.ability = ability
        self.value = value
        self.is_proficient = is_proficient
        self.saving_throw = saving_throw
        self.skills = []
        self.character_link = character_link

    def increase(self, label, st_label, skill_labels):
        self.value = self.value + 1
        self.saving_throw = self.saving_throw + 1
        label.config(text=str(self.value))
        st_label.config(text=str(self.saving_throw))
        for skill in self.skills:
            skill.value += 1
        for skill_label in skill_labels:
            new_val = int(skill_label.cget("text")) + 1
            skill_label.config(text=str(new_val))

    def decrease(self, label, st_label, skill_labels):
        self.value = self.value - 1
        self.saving_throw = self.saving_throw - 1
        label.config(text=str(self.value))
        st_label.config(text=str(self.saving_throw))
        for skill in self.skills:
            skill.value -= 1
        for skill_label in skill_labels:
            new_val = int(skill_label.cget("text")) - 1
            skill_label.config(text=str(new_val))

    def make_proficient(self, st_label, button):
        if not self.is_proficient:
            self.is_proficient = True
            self.saving_throw += self.character_link.proficient_bonus
            st_label.config(text=str(self.saving_throw))
            button.config(text="■", command=lambda: self.make_not_proficient(st_label, button))

    def make_not_proficient(self, st_label, button):
        if self.is_proficient:
            self.is_proficient = False
            self.saving_throw -= self.character_link.proficient_bonus
            st_label.config(text=str(self.saving_throw))
            button.config(text="□", command=lambda: self.make_proficient(st_label, button))

class Character:
    get_link = "characters"
    def __init__(self, id,
                 name,
                 dnd_subclass,
                 max_hp,
                 hp,
                 armor_class,
                 initiative,
                 cooper_coins,
                 silver_coins,
                 gold_coins,
                 is_player,
                 image,
                 level,
                 speed,
                 proficient_bonus,
                 dnd_class,
                 race,
                 background):
        self.id = id
        self.name = name
        self.dnd_subclass = dnd_subclass
        self.max_hp = max_hp
        self.hp = hp
        self.armor_class = armor_class
        self.initiative = initiative
        self.cooper_coins = cooper_coins
        self.silver_coins = silver_coins
        self.gold_coins = gold_coins
        self.is_player = is_player
        self.image = image
        self.level = level
        self.speed = speed
        self.proficient_bonus = proficient_bonus
        self.dnd_class = dnd_class
        self.race = race
        self.background = background
        self.abilities = []

    @classmethod
    def get_one(cls, api_result):
        api_objects = api_result
        new_char =  cls(api_objects['id'], api_objects['name'],
                   api_objects['dnd_class'], api_objects['max_hp'], api_objects['hp'],
                   api_objects['armor_class'], api_objects['initiative'],
                   api_objects['cooper_coins'], api_objects['silver_coins'],
                   api_objects['gold_coins'], api_objects['is_player'],
                   api_objects['image'], api_objects['level'],
                   api_objects['speed'], api_objects['proficient_bonus'],
                   api_objects['dnd_class'], api_objects['race'],
                   api_objects['background'])
        for ability_api in api_objects['abilities']:
            ability = Ability(ability_api['id'], ability_api['ability'], ability_api['value'], ability_api['is_proficient'], ability_api['saving_throw'], new_char)
            new_char.abilities.append(ability)
            for skill_api in ability_api['skills']:
                skill = Skill(skill_api['id'], skill_api['skill'], skill_api['value'], skill_api['is_proficient'], new_char)
                ability.skills.append(skill)
        return new_char

    @classmethod
    def get_all(cls):
        api_objects = ApiConnection.get(cls.get_link)
        if api_objects is None:
            return None
        characters = []
        for api_object in api_objects:
            characters.append(cls.get_one(api_object))
        return characters


