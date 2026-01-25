from api import ApiConnection

class BookDataClass:
    get_link = None
    objects = []

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
        cls.objects = ret_list
        return ret_list

    @classmethod
    def return_object_by_id(cls, id):
        for obj in cls.objects:
            if obj.id == id:
                return obj
        return None

    @classmethod
    def get_names(cls):
        return [item.name for item in cls.objects]

    @classmethod
    def get_values(cls):
        return {item.name : item.id for item in cls.objects}


class DndClass(BookDataClass):
    get_link = "bookdata/dndclass"


class Race(BookDataClass):
    get_link = "bookdata/race"

class Background(BookDataClass):
    get_link = "bookdata/background"


class Skill:
    update_link = "skills/update/"
    def __init__(self, id, skill, choice, value, is_proficient, character_link):
        self.id = id
        self.skill = skill
        self.choice = choice
        self.value = value
        self.is_proficient = is_proficient
        self.character_link = character_link
        self.is_updated = False

    def make_proficient(self):
        if not self.is_proficient:
            self.is_proficient = True
            self.value += self.character_link.proficient_bonus
            self.is_updated = True

    def make_not_proficient(self):
        if self.is_proficient:
            self.is_proficient = False
            self.value -= self.character_link.proficient_bonus
            self.is_updated = True

    def generate_update_json(self):
        return {
            "value": self.value,
            "is_proficient": self.is_proficient,
        }

    def update(self):
        response = ApiConnection.update(self.update_link, self.id, self.generate_update_json())
        if response == 200:
            print(f"Skill {self.choice} {self.character_link.name} updated successfully")

class Ability:
    update_link = "abilities/update/"
    def __init__(self, id, ability, choice, value, is_proficient, saving_throw, character_link):
        self.id = id
        self.ability = ability
        self.choice = choice
        self.value = value
        self.is_proficient = is_proficient
        self.saving_throw = saving_throw
        self.skills = []
        self.character_link = character_link
        self.is_updated = False

    def increase(self):
        self.value = self.value + 1
        self.saving_throw = self.saving_throw + 1
        for skill in self.skills:
            skill.value += 1
        self.is_updated = True

    def decrease(self):
        self.value = self.value - 1
        self.saving_throw = self.saving_throw - 1
        for skill in self.skills:
            skill.value -= 1
        self.is_updated = True

    def make_proficient(self):
        if not self.is_proficient:
            self.is_proficient = True
            self.saving_throw += self.character_link.proficient_bonus
        self.is_updated = True

    def make_not_proficient(self):
        if self.is_proficient:
            self.is_proficient = False
            self.saving_throw -= self.character_link.proficient_bonus

    def generate_update_json(self):
        return {
            "value": self.value,
            "is_proficient": self.is_proficient,
            "saving_throw": self.saving_throw,
        }

    def update_ability(self):
        if self.is_updated:
            response = ApiConnection.update(self.update_link, self.id, self.generate_update_json())
            if response == 200:
                self.is_updated = False
                print(f"Ability {self.character_link.name} {self.choice} updated.")
                for skill in self.skills:
                    skill.update()
        else:
            for skill in self.skills:
                if skill.is_updated:
                    skill.update()
                    skill.is_updated = False






class Character:
    get_link = "characters"
    update_link = "characters/update/"
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

        self.is_updated = False

    @classmethod
    def get_one(cls, api_result):
        api_objects = api_result
        dnd_class = DndClass.return_object_by_id(api_objects['dnd_class'])
        race = Race.return_object_by_id(api_objects['race'])

        background = Background.return_object_by_id(api_objects['background'])
        new_char =  cls(api_objects['id'], api_objects['name'],
                   api_objects['dnd_subclass'], api_objects['max_hp'], api_objects['hp'],
                   api_objects['armor_class'], api_objects['initiative'],
                   api_objects['cooper_coins'], api_objects['silver_coins'],
                   api_objects['gold_coins'], api_objects['is_player'],
                   api_objects['image'], api_objects['level'],
                   api_objects['speed'], api_objects['proficient_bonus'],
                   dnd_class, race, background)
        for ability_api in api_objects['abilities']:
            ability = Ability(ability_api['id'], ability_api['ability']['name'], ability_api['ability']['choice'], ability_api['value'], ability_api['is_proficient'], ability_api['saving_throw'], new_char)
            new_char.abilities.append(ability)
            for skill_api in ability_api['skills']:
                skill = Skill(skill_api['id'], skill_api['skill']['name'], skill_api['skill']['choice'], skill_api['value'], skill_api['is_proficient'], new_char)
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

    def go_to_gold(self):
        if self.cooper_coins >= 10 or self.gold_coins >= 10:
            self.silver_coins += self.cooper_coins // 10
            self.cooper_coins = self.cooper_coins % 10
            self.gold_coins += self.silver_coins // 10
            self.silver_coins = self.silver_coins % 10
            self.is_updated = True

    def change_info(self,name,
                 dnd_subclass,
                 max_hp,
                 armor_class,
                 initiative,
                 cooper_coins,
                 silver_coins,
                 gold_coins,
                 level,
                 speed,
                 proficient_bonus,
                 dnd_class,
                 race,
                 background,
                 selected_image):

        if name != "":
            self.name = name
        if dnd_subclass != "":
            self.dnd_subclass = dnd_subclass
        if max_hp != "":
            self.max_hp = int(max_hp)
            self.hp = self.max_hp
        if armor_class != "":
            self.armor_class = int(armor_class)
        if initiative != "":
            self.initiative = int(initiative)
        if cooper_coins != "":
            self.cooper_coins = int(cooper_coins)
        if silver_coins != "":
            self.silver_coins = int(silver_coins)
        if gold_coins != "":
            self.gold_coins = int(gold_coins)
        if level != "":
            self.level = int(level)
        if speed != "":
            self.speed = int(speed)
        if proficient_bonus != "":
            self.proficient_bonus = int(proficient_bonus)
        if dnd_class != "":
            self.dnd_class = DndClass.return_object_by_id(dnd_class)
        if race != "":
            self.race = Race.return_object_by_id(race)
        if background != "":
            self.background = Background.return_object_by_id(background)
        if selected_image != "":
            #IN DEVELOP
            print(selected_image)

        self.is_updated = True

    def generate_update_json(self):
        return {
            "name": self.name,
            "dnd_subclass": self.dnd_subclass,
            "max_hp": self.max_hp,
            "armor_class": self.armor_class,
            "initiative": self.initiative,
            "cooper_coins": self.cooper_coins,
            "silver_coins": self.silver_coins,
            "gold_coins": self.gold_coins,
            "level": self.level,
            "speed": self.speed,
            "proficient_bonus": self.proficient_bonus,
            "dnd_class": self.dnd_class.id,
            "race": self.race.id,
            "background": self.background.id
        }

    def update_character(self):
        if self.is_updated:
            response = ApiConnection.update(self.update_link, self.id, self.generate_update_json())
            if response == 200:
                print("Character updated successfully")
                self.is_updated = False
        for ability in self.abilities:
            ability.update_ability()


