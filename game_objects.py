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
        for cl in ApiConnection.get(cls.get_link):
            ret_list.append(cls(cl['id'], cl['name'], cl['image']))
        return ret_list

class DndClass(BookDataClass):
    get_link = "bookdata/dndclass"


class Race(BookDataClass):
    get_link = "bookdata/race"