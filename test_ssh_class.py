from time import sleep
from random import random


class TestSSH:
    def __init__(self, *args, **kwargs):
        self.params = kwargs
        self.args = args
        sleep(random())
        print(f'test - connected to {self.params["host"]} with user {self.params["username"]}')

    def ConnectHandler(*args, **kwargs):
        return TestSSH(*args, **kwargs)

    def disconnect(self):
        print(f'disconnected from {self.params["host"]}')

    def send_command(self, command, **kwargs):
        if 'debug' in self.params.keys():
            print(f'sending command to {self.params["host"]}: {command}')
        if 'show router' in command:
            with open('test_show_output.txt') as f:
                return f.read().strip()
        return 'Command sent: ' + command
