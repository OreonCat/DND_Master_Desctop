from api import ApiConnection, ImageWorks


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
    def __init__(self, api_result, character_link):
        self.id = api_result['id']
        self.skill = api_result['skill']['name']
        self.choice = api_result['skill']['choice']
        self.value = api_result['value']
        self.is_proficient = api_result['is_proficient']
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
    def __init__(self, api_result, character_link):
        self.id = api_result['id']
        self.ability = api_result['ability']['name']
        self.choice = api_result['ability']['choice']
        self.value = api_result['value']
        self.is_proficient = api_result['is_proficient']
        self.saving_throw = api_result['saving_throw']
        self.skills = []
        for skill in api_result['skills']:
            skill_obj = Skill(skill, character_link)
            self.skills.append(skill_obj)
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
    create_link = "characters/create"
    objects = []
    def __init__(self, api_result):
        self.id = api_result['id']
        self.name = api_result['name']
        self.dnd_subclass = api_result['dnd_subclass']
        self.max_hp = api_result['max_hp']
        self.hp = api_result['hp']
        self.armor_class = api_result['armor_class']
        self.initiative = api_result['initiative']
        self.cooper_coins = api_result['cooper_coins']
        self.silver_coins = api_result['silver_coins']
        self.gold_coins = api_result['gold_coins']
        self.is_player = api_result['is_player']
        self.image = api_result['image']
        self.level = api_result['level']
        self.speed = api_result['speed']
        self.proficient_bonus = api_result['proficient_bonus']
        self.dnd_class = DndClass.return_object_by_id(api_result['dnd_class'])
        self.race = Race.return_object_by_id(api_result['race'])
        self.background = Background.return_object_by_id(api_result['background'])
        self.abilities = []
        for ability in api_result['abilities']:
            ability_obj = Ability(ability, self)
            self.abilities.append(ability_obj)
        self.is_updated = False
        self.image_is_updated = False

    @classmethod
    def create(cls, collection, image):
        new_char = {}
        for key, value in collection.items():
            if value != "":
                new_char[key] = value
        print(new_char)
        if image != "":
            image = ImageWorks.copy_image_to_program(image)
            response = ApiConnection.post(cls.create_link, new_char, image)
        else:
            response = ApiConnection.post(cls.create_link, new_char)
        print(response)
        return response == 201


    @classmethod
    def get_all(cls):
        api_objects = ApiConnection.get(cls.get_link)
        if api_objects is None:
            return None
        for api_object in api_objects:
            cls.objects.append(cls(api_object))
        return cls.objects

    @classmethod
    def get_object_by_id(cls, char_id):
        for obj in cls.objects:
            if obj.id == char_id:
                return obj
        return None

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
            self.image_is_updated = True
            self.image = ImageWorks.copy_image_to_program(selected_image)

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
            if self.image_is_updated:
                self.image_is_updated = False
                response = ApiConnection.update(self.update_link, self.id, self.generate_update_json(), self.image)
            else:
                response = ApiConnection.update(self.update_link, self.id, self.generate_update_json())
            if response == 200:
                print("Character updated successfully")
                self.is_updated = False
        for ability in self.abilities:
            ability.update_ability()

class EncounterCharacter:
    def __init__(self, api_request):
        self.id = api_request["id"]
        self.character = Character.get_object_by_id(api_request["character"])
        self.is_enemy = api_request["is_enemy"]
        self.initiative = api_request["initiative"]
        self.is_my_step = api_request["is_my_step"]
        self.hp = api_request["hp"]
        self.max_hp = api_request["max_hp"]

class Encounter:
    def __init__(self, api_request):
        self.id = api_request["id"]
        self.stage = api_request["stage"]
        self.is_start = api_request["is_start"]
        self.is_complete = api_request["is_complete"]
        self.time_start = api_request["time_start"]
        self.time_end = api_request["time_end"]
        self.encounter_characters = []
        for enc_character in api_request["encounter_characters"]:
            self.encounter_characters.append(EncounterCharacter(enc_character))

class Game:
    get_link = "games"
    def __init__(self, api_request):
        self.id = api_request['id']
        self.name = api_request['name']
        self.image = api_request['image']
        self.is_complete = api_request['is_complete']
        self.time_start = api_request['time_start']
        self.time_end = api_request['time_end']
        self.master = api_request['master']
        self.characters = []
        self.encounters = []
        for character in api_request['characters']:
            self.characters.append(Character.get_object_by_id(character["id"]))
        for encounter in api_request['encounters']:
            self.encounters.append(Encounter(encounter))

    @classmethod
    def get_all(cls):
        api_objects = ApiConnection.get(cls.get_link)
        if api_objects is None:
            return []
        new_games =  []
        for api_object in api_objects:
            new_games.append(cls(api_object))
        return new_games



