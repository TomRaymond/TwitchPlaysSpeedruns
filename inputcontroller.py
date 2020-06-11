import autopy, time # https://github.com/autopilot-rs/autopy

class KeyboardInput:
    repeat_delay = 0.05 # rate at which held inputs are repeated

    @staticmethod
    def hold_for_seconds(seconds, *args):
        heldTime = 0
        while(heldTime < seconds):
            for key in args: # tap every key down
                autopy.key.toggle(key, True)
            # delay before next tap and tick up our counter
            time.sleep(KeyboardInput.repeat_delay)
            heldTime += KeyboardInput.repeat_delay  
        for key in args: # key up event for all keys
                autopy.key.toggle(key, False)