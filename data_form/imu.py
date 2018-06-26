import numpy as np
from filter import *

class IMU(object):
    def __init__(self, order: int, size_max: int):
        self._instance = []
        self.order = order
        self.size_max = size_max
        self.head = 0
        self.tail = 0
        self.gx_queue = [0]
        self.gy_queue = [0]
        self.gz_queue = [0]
        self.ax_queue = [0]
        self.ay_queue = [0]
        self.az_queue = [0]
        self.time = [0]

        self.gyro_sen = [0]
        self.acce_sen = [0]

    def delete(self):
        self.gx_queue.pop(self.size_max - 1)
        self.gy_queue.pop(self.size_max - 1)
        self.gz_queue.pop(self.size_max - 1)
        self.ax_queue.pop(self.size_max - 1)
        self.ay_queue.pop(self.size_max - 1)
        self.az_queue.pop(self.size_max - 1)
        self.head += 1


    def add(self, data, time):
        if data.shape[0] == 6:
            if self.size() >= self.size_max:
                self.delete()
            self.gx_queue.append(data[0 + self.order])
            self.gy_queue.append(data[1 + self.order])
            self.gz_queue.append(data[2 + self.order])
            self.ax_queue.append(data[3 - self.order])
            self.ay_queue.append(data[4 - self.order])
            self.az_queue.append(data[5 - self.order])
            self.time.append(time)
            self.tail += 1

    def gyro_filter(self, lowcut, highcut, fs, order):
        self.gx_queue = butter_bandpass_filter(self.gx_queue, lowcut, highcut, fs, order=order).tolist()
        self.gy_queue = butter_bandpass_filter(self.gy_queue, lowcut, highcut, fs, order=order).tolist()
        self.gz_queue = butter_bandpass_filter(self.gz_queue, lowcut, highcut, fs, order=order).tolist()

    def acc_filter(self, lowcut, highcut, fs, order):
        self.ax_queue = butter_bandpass_filter(self.ax_queue, lowcut, highcut, fs, order=order).tolist()
        self.ay_queue = butter_bandpass_filter(self.ay_queue, lowcut, highcut, fs, order=order).tolist()
        self.az_queue = butter_bandpass_filter(self.az_queue, lowcut, highcut, fs, order=order).tolist()

    def return_data(self):
        return [self.gx_queue, self.gy_queue, self.gz_queue, self.ax_queue, self.ay_queue, self.az_queue]


    def get_std(self):
        gx_std = np.std(self.gx_queue)
        gy_std = np.std(self.gy_queue)
        gz_std = np.std(self.gz_queue)
        ax_std = np.std(self.ax_queue)
        ay_std = np.std(self.ay_queue)
        az_std = np.std(self.az_queue)
        return [gx_std, gy_std, gz_std, ax_std, ay_std, az_std]

    def size(self):
        return self.tail - self.head

    def test_func(self, input):
        output = abs(max(input)) + abs(min(input))
        return output

    def get_gyro(self):
        gx_max = self.test_func(self.gx_queue)
        gy_max = self.test_func(self.gy_queue)
        gz_max = self.test_func(self.gz_queue)

        if (gx_max > gy_max and gx_max > gz_max):
            self.gyro_sen = self.gx_queue
            return [self.gyro_sen, 1]
        elif (gy_max > gx_max and gy_max > gz_max):
            self.gyro_sen = self.gy_queue
            return [self.gyro_sen, 2]
        elif (gz_max > gx_max and gz_max > gy_max):
            self.gyro_sen = self.gz_queue
            return [self.gyro_sen, 3]
        else:
            return [self.gyro_sen, 0]


    def get_acc(self):
        ax_max = self.test_func(self.ax_queue)
        ay_max = self.test_func(self.ay_queue)
        az_max = self.test_func(self.az_queue)

        if (ax_max > ay_max and ax_max > az_max):
            self.acce_sen = self.ax_queue
            return [self.acce_sen, 1]
        elif (ay_max > ax_max and ay_max > az_max):
            self.acce_sen = self.ay_queue
            return [self.acce_sen, 2]
        elif (az_max > ax_max and az_max > ay_max):
            self.acce_sen = self.az_queue
            return [self.acce_sen, 3]





