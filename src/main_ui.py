import asyncio
from tkinter import *
from tkinter import ttk
from subprocess import Popen


def start_web_ui():
    return Popen("python -m src.ui.ui", shell=True)


def start_cephalon_damon():
    return Popen("python -m src.cephalon", shell=True)


root = Tk()
ttk.Button(
    root,
    text="Open WebUI",
    command=start_web_ui,
).grid(column=1, row=0)

ttk.Button(
    root,
    text="Start Cephalon",
    command=start_cephalon_damon,
).grid(column=1, row=2)


try:
    root.mainloop()
except KeyboardInterrupt:
    # kill all running python process attacthed to it
    root.destroy()
