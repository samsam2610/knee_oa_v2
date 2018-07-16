from helper import *

class IMU(object):
    def __init__(self, order: int, size_max: int, special_value: float):
        self._instance = []
        self.order = order
        self.size_max = size_max
        [self.gx_queue, self.gy_queue, self.gz_queue] = empty_queue(size_max=size_max, value=0)
        [self.ax_queue, self.ay_queue, self.az_queue] = empty_queue(size_max=size_max, value=0)
        [self.gyro_sen, self.acce_sen, self.time] = empty_queue(size_max=size_max, value=0)
        self.special_value = special_value

    def delete(self):
        self.gx_queue.pop(0)
        self.gy_queue.pop(0)
        self.gz_queue.pop(0)
        self.ax_queue.pop(0)
        self.ay_queue.pop(0)
        self.az_queue.pop(0)
        self.time.pop(0)


    def add(self, data, time):
        if data.shape[0] == 6:
            self.delete()
            self.gx_queue.append(data[0 + self.order])
            self.gy_queue.append(data[1 + self.order])
            self.gz_queue.append(data[2 + self.order])
            self.ax_queue.append(data[3 - self.order])
            self.ay_queue.append(data[4 - self.order])
            self.az_queue.append(data[5 - self.order])
            self.time.append(time)

    def gyro_filter(self, lowcut, highcut, fs, order):
        self.gx_filtered = butter_bandpass_filter(self.gx_queue, lowcut, highcut, fs, order=order).tolist()
        self.gy_filtered = butter_bandpass_filter(self.gy_queue, lowcut, highcut, fs, order=order).tolist()
        self.gz_filtered = butter_bandpass_filter(self.gz_queue, lowcut, highcut, fs, order=order).tolist()

    def acce_filter(self, lowcut, highcut, fs, order):
        self.ax_filtered = butter_bandpass_filter(self.ax_queue, lowcut, highcut, fs, order=order).tolist()
        self.ay_filtered = butter_bandpass_filter(self.ay_queue, lowcut, highcut, fs, order=order).tolist()
        self.az_filtered = butter_bandpass_filter(self.az_queue, lowcut, highcut, fs, order=order).tolist()

    def test_func(self, input):
        # output = abs(max(input)) + abs(min(input))
        output = sum([abs(i) for i in input[:]])
        return output

    def get_gyro(self):
        [self.gyro_sen, ax_loc] = self.__get_sensitive_axis(self.gx_filtered,
                                                            self.gy_filtered,
                                                            self.gz_filtered)

    def get_acce(self):
        [self.acce_sen, ax_loc] = self.__get_sensitive_axis(self.ax_filtered,
                                                            self.ay_filtered,
                                                            self.az_filtered)

    def __get_sensitive_axis(self, data_x, data_y, data_z):
        ax_sen = [0]
        x_max = self.test_func(data_x)
        y_max = self.test_func(data_y)
        z_max = self.test_func(data_z)

        if x_max > y_max and x_max > z_max:
            ax_sen = data_x
            ax_loc = 1
        elif y_max > x_max and y_max > z_max:
            ax_sen = data_y
            ax_loc = 2
        elif z_max > x_max and z_max > y_max:
            ax_sen = data_z
            ax_loc = 3
        else:
            ax_loc = 0

        return [ax_sen, ax_loc]




