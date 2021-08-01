from Crypto.Cipher import AES as aes
import os

class AES:
    """
    Encryption and decryption handler
    """
    def __init__(self, key=None):
        """
        :param key: 128 bit key
        """
        self.__key  = key if key else os.urandom(16)
        self.__aes = aes.new(self.__key, aes.MODE_EAX)
        self.__nonce = self.__aes.nonce

    def get_key(self):
        """
        Returns cipher key
        :return: bytes
        """
        return self.__key

    def set_nonce(self, nonce):
        """
        Set nonce encryption's nonce value
        :param nonce: bytes
        :return: None
        """
        self.__nonce = nonce

    def encrypt_file(self, filename):
        """
        Encrypts given file by path
        :param filename: str
        :return: None
        """
        with open(filename, "rb+") as _file:
            data = _file.read()
            cipher_data, tag = self.__aes.encrypt_and_digest(data)
            self.__write_to_file(_file, bytearray(self.__nonce + cipher_data))

    def decrypt_file(self, filename):
        """
        Decrypts given file by path
        :param filename:
        :return: None
        """
        with open(filename, "rb+") as _file:
            cipher_data = _file.read()
            nonce = cipher_data[0:16]
            self.__aes = aes.new(self.__key, aes.MODE_EAX, nonce)
            original_data = self.__aes.decrypt(cipher_data[16:])
            self.__write_to_file(_file, original_data)

    @staticmethod
    def __write_to_file(_file, data):
        """
        Writes binary data to file
        :param _file: File
        :param data: binary
        :return: None
        """
        _file.seek(0)
        _file.write(data)
        _file.truncate()

if __name__ == "__main__":
    '''text = "hello"
    print (text)
    key = os.urandom(16)
    a = aes.new(key, aes.MODE_EAX)
    nonce = a.nonce
    c, t = a.encrypt_and_digest(text.encode("utf-8"))
    print (c)
    c = nonce + c
    print (len(nonce), len(c[16:]))
    n = c[0:16]
    print (n, nonce)
    a = aes.new(key, aes.MODE_EAX, n)
    o = a.decrypt(c[16:])
    print (o)
    print (o.decode())

    filename = "test.txt"
    key = "TfPi9MW/rqIjmiyqmNS77w=="
    a = AES(b64decode(key))
    a.encrypt_file(filename)

    a = AES(b64decode(key))
    a.decrypt_file(filename)'''