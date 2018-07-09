
class peak_finding():
    def __init__(self):
        self.left_side = 0
        self.right_side = 0
        self.left_time = 0
        self.sign = 1
        self.started = False
        self.ended = True
        self.current = 0
        self.current_time = 0
        self.diff_value = 0

    def add(self, value, time):
        self.current = value
        self.current_time = time

    def diff_data(self, side_value):
        self.diff_value = self.current - side_value

    def check(self):
        return_value = 0
        return_time = 0
        return_sign = 0
        return_diff = 0
        if self.started == True and self.ended == False:
            self.diff_data(self.left_side)
            if self.diff_value != 0:
                current_sign = self.diff_value / abs(self.diff_value)
                if current_sign == self.sign:
                    self.left_side = self.current
                    self.left_time = self.current_time
                elif current_sign == self.sign*(-1):
                    self.right_side = self.current
                    self.started = False
                    self.ended = True
                    return_value = self.left_side
                    return_time = self.left_time
                    return_sign = self.sign
                    return_diff = abs(self.current - self.starting_value)


        elif self.ended == True:
            self.diff_data(self.right_side)
            if self.diff_value != 0:
                self.sign = self.diff_value / abs(self.diff_value)
                self.started = True
                self.ended = False
                self.left_side = self.current
                self.starting_value = self.current

        return [return_value, return_time, return_sign, return_diff]

