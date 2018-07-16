from helper import *

class ANGLE():
    def __init__(self, size_max: int):
        self._instance = []
        self.size_max = size_max
        [self.x_queue, self.y_queue, self.z_queue] = empty_queue(size_max=size_max, value=0)
        [self.w_queue, self.time, self.w_diff] = empty_queue(size_max=size_max, value=0)
        [self.x_diff, self.y_diff, self.z_diff] = empty_queue(size_max=size_max, value=0)
        [self.x_signed, self.y_signed, self.z_signed] = empty_queue(size_max=size_max, value=0)
        self.fused_value = [0] * size_max

    def delete(self):
        self.w_queue.pop(0)
        self.x_queue.pop(0)
        self.y_queue.pop(0)
        self.z_queue.pop(0)
        self.time.pop(0)

    def add(self, data, time):
        if data.shape[0] == 4:
            self.delete()
            self.w_queue.append(data[0])
            self.x_queue.append(data[1])
            self.y_queue.append(data[2])
            self.z_queue.append(data[3])
            self.time.append(time)

    def true_value(self):
        self.calculate_diff()
        self.x_signed = return_true_value(self.x_diff, self.x_queue)
        self.y_signed = return_true_value(self.y_diff, self.y_queue)
        self.z_signed = return_true_value(self.z_diff, self.z_queue)

    def fused_data(self):
        self.true_value()
        for index in range(len(self.x_signed)):
            self.fused_value[index] = self.x_signed[index] + self.y_signed[index] + self.z_signed[index]

    def calculate_diff(self):
        self.x_diff = diff_queue(self.x_queue)
        self.y_diff = diff_queue(self.y_queue)
        self.z_diff = diff_queue(self.z_queue)
        self.x_diff = sign_queue(self.x_diff)
        self.y_diff = sign_queue(self.y_diff)
        self.z_diff = sign_queue(self.z_diff)









