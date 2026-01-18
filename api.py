import os

from PIL import Image, ImageTk
import requests

class ApiConnection:
    api_link = "http://127.0.0.1:8000/api/"
    token_file = "token.txt"
    username = None
    __token = None

    @classmethod
    def get(cls, get_link):
        if cls.__get_token() is None:
            return None
        full_link = cls.api_link + get_link
        response = requests.get(full_link, headers={'Authorization': cls.__get_token()})
        print(f"get запрос к {get_link} статус код: {response.status_code}")
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
        print("Старт логина")
        p_link = "auth/token/login"
        post_result = cls.post(p_link, {"username": username, "password": password})
        if post_result.get("auth_token") is not None:
            token = post_result["auth_token"]
            f = open(cls.token_file, "w")
            cls.__token = f"Token {token}"
            f.write(f"Token {token}")
            f.close()
            return True
        else:
            return False

    @classmethod
    def __get_token(cls):
        if cls.__token is not None:
            return cls.__token
        try:
            f = open(cls.token_file, "r")
        except FileNotFoundError:
            return None
        else:
            token = f.read()
            if token == "":
                return None
            f.close()
            cls.__token = token
            return token

    @classmethod
    def is_authenticated(cls):
        return cls.__get_token() is not None

    @classmethod
    def logout(cls):
        cls.__token = None
        if cls.__get_token() is not None:
            cls.__token = None
            cls.username = None
            f = open(cls.token_file, "w")
            f.write("")
            f.close()

    @classmethod
    def get_username(cls):
        if not cls.is_authenticated():
            return None
        if cls.username is None:
            cls.username = cls.get("my_username")["username"]
        return cls.username

#http://127.0.0.1:8000/media/characters/photo_2025-11-23_10-16-40.jpg

class ImageWorks:
    media_root = "media/"
    @classmethod
    def get_image(cls, url):
        file_name = url.split("/")[-1]
        if file_name not in os.listdir(cls.media_root):
            cls.download_image(url, file_name)
        return cls.media_root + file_name

    @classmethod
    def download_image(cls, url, file_name):
        print(f"Download {url}")
        try:
            response = requests.get(url, stream=True)
        except requests.exceptions.RequestException as e:
            print(e)
        else:
            with open(cls.media_root + file_name, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

    @classmethod
    def get_image_tk(cls, url, width=100, height=100):
        image_pil = Image.open(cls.get_image(url))
        image_pil.thumbnail((height, width))
        image_tk = ImageTk.PhotoImage(image_pil)
        return image_tk


