from api import ApiConnection

class DndClass:
    get_link = "bookdata/dndclass"

    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    @classmethod
    def get_all(cls):
        ret_list = []
        for cl in ApiConnection.get(cls.get_link):
            ret_list.append(cls(cl['id'], cl['name'], cl['image']))
        return ret_list