import os

class SystemState:
    @property
    def frozen(self):
        return os.path.exists(".frozen")

state = SystemState()
