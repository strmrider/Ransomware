from tkinter import *

class FilesList(Toplevel):
    """
    Encrypted files list gui component
    """
    def __init__(self, files):
        Toplevel.__init__(self)
        self.title("Encrypted files")
        self.geometry('600x370')
        self.resizable(False, False)
        title = Label(self, text="The files below are encrypted ({} files):".format(len(files)))
        title.place(x=15, y=10)
        self.set_files(files)

    def set_files(self, files):
        """
        Setd teh files for display
        :param files: list;
        :return: None
        """
        text = Text(self, wrap=WORD, height=20, width=70)
        scroll = Scrollbar(text)
        #scroll.pack(side=RIGHT, fill=Y)
        #text.yscrollcommand = scroll.set
        text.place(x=15, y=30)

        for _file in files:
            text.insert(INSERT, _file)
            text.insert(INSERT, "\n")

    def open(self):
        self.mainloop()

if __name__ == "__main__":
    fl = FilesList(["C://test//details.py", "C://test//details.py", "C://test//details.py"])
    fl.open()