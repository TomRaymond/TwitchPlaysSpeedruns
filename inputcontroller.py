import autopy, time # https://github.com/autopilot-rs/autopy

class KeyboardInput:
    repeat_delay = 0.05 # rate at which held inputs are repeated

    @staticmethod
    def hold_for_seconds(keys, seconds):
        heldTime = 0
        while(heldTime < seconds):
            for key in keys: # tap every key down
                autopy.key.toggle(key, True)
            # delay before next tap and tick up our counter
            time.sleep(KeyboardInput.repeat_delay)
            heldTime += KeyboardInput.repeat_delay  
        for key in keys: # key up event for all keys
                autopy.key.toggle(key, False)

class KeyInput:
    keys = []
    hold_time = 0
    def __init__(self, keys, hold_time):
        self.keys = keys
        self.hold_time = hold_time