
import logging

from . import sender
from . import manager
from . import client
from . import config
from . import mqtt_client
from . import mqtt_sender

class Agent():
    def __init__(self):
        logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)

    def main(self):
        _manager = manager.Manager()
        _sender = sender.Sender()
        _client = client.Client()
        _mqtt_sender = mqtt_sender.MQTTSender()
        _mqtt_client = mqtt_client.MQTTClient()

        _client.set_manager(_manager)
        _mqtt_client.set_manager(_manager)

        _sender.set_client(_client)
        _mqtt_sender.set_mqtt_client(_mqtt_client)
        _manager.set_sender(_sender)
        _manager.set_mqtt_sender(_mqtt_sender)

        _sender.start()
        _client.start()
        _mqtt_sender.start()
        _mqtt_client.start()
        _manager.start_default()

def main():
    agent = Agent()
    agent.main()

if __name__ == '__main__':
    main()
