class FalseHeartPulseMachine:
    def __init__(self):
        self.active = False
        self.position = (0, 0)
        self.pulse_count = 0
        self.frequency = 1.0
        self.jitter = 0.0
        self.internal_time = 0.0

    def dock(self, floor):
        floor.register(self)

    def move_to(self, x, y):
        self.position = (x, y)

    def turn_on(self):
        self.active = True

    def turn_off(self):
        self.active = False

    def set_frequency(self, freq):
        self.frequency = freq

    def set_jitter(self, amount):
        self.jitter = amount

    def run(self):
        if not self.active:
            return None
        self.internal_time += self.frequency
        self.pulse_count += 1
        return {
            "pulse": self.pulse_count,
            "time": self.internal_time,
            "jitter": self.jitter
        }
