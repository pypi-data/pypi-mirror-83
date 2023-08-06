
import json

from . import message

class Mission():
    def __init__(self, manager):
        self.manager = manager

    def send(self, msg: message.Message):
        self.manager.sender.send(msg)

    def publish(self, topic, data):
        self.manager.mqtt_sender.publish(topic, self.serialize(data))

    def post(self, name, data):
        msg = message.Message({'type': 'mission', 'name': name})
        msg.set_body(self.serialize(data))
        self.send(msg)

    def serialize(self, data):
        if isinstance(data, dict):
            data = json.dumps(data).encode()
        return data

    def forward(self, name, task):
        self.manager.forward(name, task)
