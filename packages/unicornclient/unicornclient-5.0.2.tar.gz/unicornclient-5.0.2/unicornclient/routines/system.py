import subprocess

from unicornclient import routine

class Routine(routine.Routine):
    def __init__(self):
        routine.Routine.__init__(self)
        self.authorized_commands = ['reboot', 'halt']

    def process(self, data):
        command = data['command'] if 'command' in data else None

        if command in self.authorized_commands:
            subprocess.call(command, shell=True)
