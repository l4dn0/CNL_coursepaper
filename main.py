# # -*- coding: utf-8 -*-
# from match import cnl_match
#
# try :
#     from cnl_parser import parser
#     a = cnl_match()
#     print(a.frm_match(parser.parse('элемент поверхности объекта.')[0], parser.parse('красный железный элемент поверхности объекта узла сборки.')[0]))
#
#     # print(parser.parse('диспетчер формирует рейсы. диспетчер формирует рейсы.'))
#     # print(parser.parse('температурное условие надежной работы [системы автоматизации и [элементов и  устройств] систем автоматизации] в закрытых помещениях. '))
#     # print(parser.parse('температурное условие надежной работы [системы автоматизации и [элементов и  устройств] систем автоматизации] на открытых палубах. '))
#     pass
#
# except Exception as e:
#     print(e)
#





# helloworld.py
import pathlib
import tkinter as tk
import tkinter.ttk as ttk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "helloworld.ui"


class HelloworldApp:
    def __init__(self, master=None):
        # 1: Create a builder and setup resources path (if you have images)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        # 2: Load a ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow', master)

        # 4: Connect callbacks
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    app = HelloworldApp()
    app.run()