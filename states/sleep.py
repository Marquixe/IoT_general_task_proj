from states import AbstractState
import sys

class Sleep(AbstractState):
    def __init__(self, device):
        super().__init__(device)

    def exec(self):
        sys.exit(0)