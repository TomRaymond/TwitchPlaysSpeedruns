import time
import event

class Timer:
    delta_time = 0
    _previous_time = 0
    _timers = []
    @staticmethod
    def init_timer():
        Timer._previous_time = time.time()
    @staticmethod
    def update_delta_time(): # update delta timer variable and all timers with it
        Timer.delta_time = time.time() - Timer._previous_time
        Timer._previous_time = time.time()
        for timer in Timer._timers:
            timer._update()

    def __init__(self, seconds, paused = False):
        self.startTime = seconds
        self.currentTime = seconds
        self.isPaused = paused        
        Timer._timers.append(self)
    def reset(self):
        self.currentTime = self.startTime
    def unpause(self):
        self.isPaused = False
    def pause(self):
        self.isPaused = True
    def _update(self):
        pass
    
class Stopwatch(Timer):
    def __init__(self, start_time = 0, paused = False):
        super(Stopwatch, self).__init__(start_time, paused)
    def _update(self):
        if(self.isPaused): return        
        self.currentTime += Timer.delta_time

    def reset(self):
        self.currentTime = 0

class Countdown(Timer):
    def __init__(self, start_time = 0, paused = False):
        super(Countdown, self).__init__(start_time, paused)
        self._completion_event = event.EventHandler(event.Event(), self) # event that fires when countdown hits zero
    def _update(self):
        if(self.isPaused): return

        self.currentTime -= Timer.delta_time
        if(self.currentTime <= 0):
            self.isPaused = True            
            self._completion_event.call()

    def reset(self):
        self.currentTime = self.startTime
        self.isPaused = False

    def subscribe(self, func):
        self._completion_event += func

    def unsubscribe(self, func):
        self._completion_event -= func
    
    __iadd__ = subscribe
    __isub__ = unsubscribe


###EXAMPLE###
'''def print_trigger(sender, args):
    print("Triggered")
    sender.reset()

countdown = Countdown(start_time=1)
countdown += print_trigger

Timer.init_timer()

while True:
    Timer.update_delta_time()'''