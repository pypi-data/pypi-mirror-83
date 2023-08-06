
import json

from . import message

class Mission():
    def __init__(self, manager):
        self.manager = manager

    def send(self, msg):
        self.manager.sender.send(msg)

    def publish(self, topic, msg):
        self.manager.mqtt_sender.publish(topic, msg)

    def post(self, name, data):
        msg = message.Message({'type': 'mission', 'name': name})
        if isinstance(data, dict):
            msg.set_body(json.dumps(data).encode())
        else:
            msg.set_body(data)
        self.send(msg)

    def forward(self, name, task):
        self.manager.forward(name, task)
