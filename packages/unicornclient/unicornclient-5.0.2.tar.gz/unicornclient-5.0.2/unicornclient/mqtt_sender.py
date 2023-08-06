import queue
import threading

class MQTTSender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue.Queue()
        self.mqtt_client = None

    def set_mqtt_client(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def publish(self, topic, message):
        bundle = (topic, message)
        self.queue.put(bundle)

    def run(self):
        while True:
            bundle = self.queue.get()
            self.publish_one(bundle[0], bundle[1])
            self.queue.task_done()

    def publish_one(self, topic, message):
        self.mqtt_client.client.publish(topic, message)
