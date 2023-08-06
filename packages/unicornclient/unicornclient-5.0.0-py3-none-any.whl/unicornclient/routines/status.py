from unicornclient import spy
from unicornclient import routine
from unicornclient import message
from unicornclient import version

class Routine(routine.Routine):
    def __init__(self):
        routine.Routine.__init__(self)

    def process(self, data):
        self.send_status()

    def send_status(self):
        status = self.get_status()
        payload = {
            'type':'status',
            'status': status
        }
        self.mission.send(message.Message(payload))

    def get_status(self):
        status = {
            'version': version.VERSION,
            'serial' : spy.get_serial(),
            'machine_id': spy.get_machine_id(),
            'hostname': spy.get_hostname(),
            'kernel': spy.get_kernel(),
            'uptime': spy.get_uptime(),
            'local_ip': spy.get_local_ip(),
            'interfaces': spy.get_macs(),
            'temp': spy.get_temp(),
            'ssid': spy.get_ssid(),
            'signal_level': spy.get_signal_level(),
            'written_kbytes': spy.get_written_kbytes(),
            'cpu_frequency': spy.get_cpu_frequency(),
        }
        return status
