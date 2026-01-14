import tkinter as tk
from pages import StartPage, BookDataPage, DndClassPage, RacePage

pages = (StartPage, BookDataPage, DndClassPage, RacePage)

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("DND MASTER")
        self.geometry("800x600")
        self.frames = {}
        self.config(background = "#fcca9a")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for page in pages:
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        print(self.frames)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

main = MainApp()
main.mainloop()
