import pickle, tabulate
from .pldata import PayloadData

_HEADERS = ("ID", "status", "key", "Deadline", "Payment", "Payment details", "Contact")

class Database:
    """
    Handles registered payloads data
    """
    def __init__(self):
        self.payloads = {}
        self.current_file = None

    def exist(self, payload_id):
        """
        Returns if a payload exists
        :param payload_id: str
        :return: bool
        """
        return payload_id in self.payloads

    def get(self, payload_id):
        """
        Returns payload by given id
        :param payload_id: str
        :return: PayloadData
        """
        if self.exist(payload_id):
            return self.payloads[payload_id]
        else:
            return None

    def add(self, payload):
        """
        Adds new payload to the database
        :param payload: PayloadData
        :return: None
        """
        if not self.exist(payload.id):
            self.payloads[payload.id] = payload

    def remove(self, payload_id, get_client=False):
        """
        Removes payload from database by given id and returns it if 'get client' is true
        :param payload_id: str
        :param get_client: bool
        :return: None
        """
        if get_client:
            return self.payloads.pop(payload_id, None)
        else:
            if self.exist(payload_id):
                del self.payloads[payload_id]

    def save_to_file(self, path=None):
        """
        Saves database to file in binary format
        :param path: str; location of the target file
        :return: None
        """
        payloads = self.payloads.values()
        payloads = [payload.serialize() for payload in payloads]
        if not path and self.current_file:
            path = self.current_file
        elif not path:
            raise Exception("Filename not specified")
        with open(path, "wb") as dbfile:
         pickle.dump(payloads, dbfile, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, path):
        """
        Loads database from file
        :param path: str; location of the database file
        :return: None
        """
        with open(path, "rb") as dbfile:
            payloads = pickle.load(dbfile)
            for payload in payloads:
                self.add(PayloadData(payload['id'],
                                     payload['payment'],
                                     payload['time_limit'],
                                     payload['payment_details'],
                                     payload['contact']))
            self.current_file = path

    def print_payload(self, payload_id):
        """
        Prints a payload
        :param payload_id: str
        :return: None
        """
        payload = self.get(payload_id)
        if payload:
            print(tabulate.tabulate([payload.get_summary()], headers=_HEADERS))
        else:
            print ('Payload not found')

    def print(self):
        """
        Prints all payloads in database
        :return: None
        """
        values = self.payloads.values()
        lst = []
        for payload in values:
            lst.append(payload.get_summary())

        print(tabulate.tabulate(lst, headers=_HEADERS))

