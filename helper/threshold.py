

class Threshold():
    def __init__(self):
        self.threshold = float
        self.starting_time = float
        self.current_value = float
        self.current_time = float
        self.current_duration = float
        self.started = False
        self.ended = True

    def add(self, value, time):
        self.current_value = value
        self.current_time = time

    def set_threshold(self, threshold):
        self.threshold = threshold

    def check(self):
        return_duration = 0
        return_end = 0
        return_start = 0
        if self.current_value > self.threshold\
                and not self.started\
                and self.ended:
            self.starting_time = self.current_time
            self.started = True
            self.ended = False
            return_start = self.starting_time
        elif self.current_value > self.threshold\
                and self.started\
                and not self.ended:
            self.current_duration = self.current_time - self.starting_time
        elif self.current_value < self.threshold\
                and self.started\
                and not self.ended:
            self.current_duration = self.current_time - self.starting_time
            self.started = False
            self.ended = True
            return_start = self.starting_time
            return_end = self.current_time
            return_duration = self.current_duration

        return [return_duration, return_start, return_end]
