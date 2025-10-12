
class AbstractState:
    def __init__(self, device):
        self.device = device

    def enter(self):
        pass

    def esec(self):
        pass

    def exit(self):
        pass