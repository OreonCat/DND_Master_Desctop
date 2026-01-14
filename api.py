import requests

class ApiConnection:
    api_link = "http://127.0.0.1:8000/api/"

    @classmethod
    def get(cls, get_link):
        full_link = cls.api_link + get_link
        response = requests.get(full_link, headers={'Authorization': cls.__get_token()})
        if response.status_code == 403:
            return None
        return response.json()

    @classmethod
    def post(cls, post_link, data):
        full_link = cls.api_link + post_link
        response = requests.post(full_link, data=data)
        return response.json()

    @classmethod
    def login(cls, username, password):
        p_link = "auth/token/login"
        post_result = cls.post(p_link, {"username": username, "password": password})
        if post_result.get("auth_token") is not None:
            token = post_result["auth_token"]
            f = open("token.txt", "w")
            f.write(f"Token {token}")
            f.close()
            return True
        else:
            return False

    @staticmethod
    def __get_token():
        try:
            f = open("token.txt", "r")
        except FileNotFoundError:
            return None
        else:
            token = f.read()
            f.close()
            return token

print(ApiConnection.get("bookdata/race"))
