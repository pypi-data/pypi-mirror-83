from tkinter import *

from aihelper import Browse, OkButton

from aiextractor import Pipero


class Aiex:
    def __init__(self):
        self.data = None
        self.headers = None
        self.root = Tk()
        self.files = None
        self.listbox = Listbox
        self.button = None

    def looper(self):
        self.files = Browse(self.root, type="file", title="Select your files")
        self.button = OkButton(self.root, function=self.listboxer)
        self.root.mainloop()

    def load_data(self):
        self.data = Pipero(self.files.get())
        self.headers = self.data.extract_headers()

    def listboxer(self):
        self.load_data()
        new_window = Toplevel(self.root)
        new_window.grab_set()
        self.listbox = Listbox(
            master=new_window,
            selectmode=MULTIPLE,
            width=max(map(lambda x: len(x), self.headers)) + 5,
            height=len(self.headers),
        )
        self.listbox.pack(expand=TRUE, fill=BOTH)
        for i in self.headers:
            self.listbox.insert(END, str(i))
        self.listbox.bind("<Double-Button-1>", True)
        OkButton(new_window, function=lambda: self.close(new_window), text="Extract")

    def close(self, window):
        items = [self.headers[int(item)] for item in self.listbox.curselection()]
        self.data.extract_data(items)
        self.data.save_data()
        window.destroy()


if __name__ == "__main__":
    Aiex().looper()
