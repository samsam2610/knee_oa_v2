from helper.filter import *

class EMG(object):
    def __init__(self, size_max: int):
        self.size_max = size_max
        [self.hamstring_queue, self.quadtricep_queue] = self.empty_queue(value=0)
        self.time = [0] * size_max

    def delete(self):
        self.hamstring_queue.pop(0)
        self.quadtricep_queue.pop(0)
        self.time.pop(0)

    def add(self, data, time):
        if data.shape[0] == 2:
            self.delete()
            self.hamstring_queue.append(data[0])
            self.quadtricep_queue.append(data[1])
            self.time.append(time)

    def hamstring_filter(self, lowcut, highcut, fs, order):
        self.hamstring_filtered = butter_lowpass_filter(self.hamstring_queue, highcut, fs, order=order).tolist()

    def quadtricep_filter(self, lowcut, highcut, fs, order):
        self.quadtricep_filtered = butter_lowpass_filter(self.quadtricep_queue, highcut, fs, order=order).tolist()

    def empty_queue(self, value: float):
        data_x = [value] * self.size_max
        data_y = [value] * self.size_max
        return [data_x, data_y]


