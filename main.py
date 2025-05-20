#print(a.frm_match(parser.parse('элемент поверхности объекта.')[0], parser.parse('красный железный элемент поверхности объекта узла сборки.')[0]))
import io

import ply.lex
# helloworld.py
from match import cnl_match
from cnl_parser import parser
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import StringVar
from PIL import Image, ImageTk

import pygubu
from orm import select_all

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "helloworld.ui"

class HelloworldApp:
    def display_images(self, imgs):
        margin = 0
        for img_bin in imgs:
            image_stream = io.BytesIO(img_bin)
            image = Image.open(image_stream).resize((350, 150))
            print(image)

            photo = ImageTk.PhotoImage(image)
            self.photo_refs.append(photo)
            self.canvas.create_image(0, margin, anchor="nw", image=photo)
            margin += 150


    def search(self):
        self.photo_refs = []
        a = cnl_match()
        tmpl = self.cnl_value.get()
        overlapped = []
        try:
            for write in select_all():
                if a.frm_match(parser.parse(tmpl)[0], parser.parse(write[1])[0]):
                   overlapped.append(write[2])
            self.display_images(overlapped)
        except ply.lex.LexError:
            print("Введённый текст не соответствует спецификации CNL.")

    def __init__(self, master=None):
        # 1: Create a builder and setup resources path (if you have images)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('mainwindow', master)
        self.cnl_value = StringVar()

        self.canvas = builder.get_object('canvas1')
        entry = builder.get_object('entry1')
        entry.config(textvariable=self.cnl_value)
        builder.connect_callbacks(self)
    def run(self):
        self.mainwindow.mainloop()



if __name__ == '__main__':
    app = HelloworldApp()
    app.run()
