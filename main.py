import tkinter as tk
from pages import StartPage, BookDataPage, DndClassPage, RacePage, LoginPage, SettingsPage, CharactersPage


class MainApp(tk.Tk):
    pages = (StartPage, BookDataPage, DndClassPage, RacePage, LoginPage, SettingsPage, CharactersPage)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("DND MASTER")
        self.geometry("800x600")
        self.frames = {}
        self.config(background = "#fcca9a")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.make_container()

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def remake_container(self):
        for frame in self.frames.values():
            frame.destroy()
        self.make_container()

    def make_container(self):
        for page in self.pages:
            frame = page(self.container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def add_to_frame(self, page, page_name, pure_data: None):
        frame = page(self.container, self, pure_data)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")





main = MainApp()
main.mainloop()
