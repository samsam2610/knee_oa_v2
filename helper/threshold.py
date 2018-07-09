

class threshold ():
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.starting_time = float
        self.current_value = float
        self.current_time = float
        self.current_duration = float
        self.started = False
        self.ended = True

    def add(self, current_value, current_time):
        self.current_value = current_value
        self.current_time = current_time

    def check(self):
        return_duration = 0
        if self.current_value > self.threshold\
                and not self.started\
                and self.ended:
            self.starting_time = self.current_time
            self.started = True
            self.ended = False
        elif self.current_value < self.threshold\
                and self.started\
                and not self.ended:
            self.current_duration = self.current_time - self.starting_time
            self.started = False
            self.ended = True
            return_duration = self.current_duration

        return return_duration
