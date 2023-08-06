from aireport.tools import *
from tkinter import *

from aihelper import Browse, OkButton

from aireport.tools import Lims


def tools_ui():
    root = Tk()
    br = Browse(parent=root, type="dir", title="Select Folder", initial="")
    br.pack()
    ok = OkButton(root, function=c, directory=br, root=root)
    ok.pack()
    root.mainloop()


def c(directory):
    directory = directory.get()
    x = Lims(directory)
    x.compile()


if __name__ == "__main__":
    tools_ui()
