import io
import pathlib
import pygubu
from cnl_parser import parser
from tkinter import StringVar
from match import cnl_match
from PIL import Image, ImageTk
from orm import select_all

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "helloworld.ui"


class HelloworldApp:
    def display_images(self, imgs):
        self.photo_refs = []
        margin = 0
        for img_bin in imgs:
            print(img_bin[1],end="")
            image_stream = io.BytesIO(img_bin[2])
            image = Image.open(image_stream).resize((350, 150))
            photo = ImageTk.PhotoImage(image)
            self.photo_refs.append(photo)
            self.canvas.create_image(0, margin, anchor="nw", image=photo)
            margin += 150

    def search(self):
        a = cnl_match()
        tmpl = self.cnl_value.get()
        overlapped = []
        try:
            for write in select_all():
                if a.frm_match(parser.parse(tmpl)[0], parser.parse(write[1])[0]):
                    overlapped.append(write)
            self.display_images(overlapped)
            self.errorLabel.set(" ")
        except Exception as e:
            self.errorLabel.set("Введённый текст не соответствует спецификации CNL.")
            print(e)

    def __init__(self, master=None):
        # 1: Create a builder and setup resources path (if you have images)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow', master)
        self.cnl_value = StringVar()
        self.errorLabel = StringVar()

        self.canvas = builder.get_object('canvas1')
        entry = builder.get_object('entry1')
        errorlabel = builder.get_object('label3')
        entry.config(textvariable=self.cnl_value)
        errorlabel.config(textvariable=self.errorLabel)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = HelloworldApp()
    app.run()
