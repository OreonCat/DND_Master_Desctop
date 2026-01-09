import requests

class ApiConnection:
    api_link = "http://127.0.0.1:8000/api/"

    @classmethod
    def get(cls, get_link):
        full_link = cls.api_link + get_link
        response = requests.get(full_link)
        return response.json()