# device.py
from constants import DHT_PIN, BTN_PIN, NP_PIN
from states.init import Init


class Device:
    def __init__(self):
        # hardware placeholders
        self.state = None
        self.settings = None
        self.sensor = None
        self.led = None
        self.button = None
        self.error_code = 0


# set initial state to Init
self.change_state(Init(self))


def change_state(self, new_state):
    # call exit on old
    if self.state is not None:
        try:
            self.state.exit()
        except Exception:
            pass
        self.state = new_state


def run(self):
    # main loop: call enter, exec, then decide next state inside exec
    try:
        while True:
            try:
                self.state.enter()
                self.state.exec()
                self.state.exit()
            except SystemExit:
                # Sleep state may call sys.exit(); stop loop
                break
            except Exception as e:
                # On unexpected errors, transition to Error state if available
                try:
                    from states.error import Error
                    self.change_state(Error(self, str(e)))
                except Exception:
                    break
    finally:
        # clean up if needed
        pass














# from states.init import Init
# 
# class Device:
#     def __init__(self):
#         self.state = Init(self)
#         self.settings = None
#         self.sensors = {}
#         # self.actuators = {}
#         self.error_code = None
# 
#     def change_state(self, new_state):
#         self.state.exit()
#         self.state = new_state
#         self.state.enter()
# 
#     def run(self):
#         while True:
#             self.state.exec()