import logging

class MissingInfoException(Exception):
    pass

class Handler():
    def __init__(self, manager):
        self.manager = manager
        self.last_ping_id = None

    def handle(self, message):
        payload = message.header

        if 'type' not in payload:
            logging.warning("Ignored because no type")
            return

        payload_type = payload['type']
        payload.pop('type')

        self.manager.forward(payload_type, payload)
