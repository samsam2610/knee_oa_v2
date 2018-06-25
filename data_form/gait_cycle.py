
class Gait():
    def __init__(self, IMU):
        self.gyro = IMU.gyro_sen
        self.acce = IMU.acce_sen
        self.time = IMU.time
        self.toeoff_index = 0

    def peak_detect(self, threshold, data, sign):
        data_max = max(map(abs, data))
        if data_max > threshold:
            return data.index(data_max * sign)

    def get_toeoff(self):
        self.toeoff_index = self.peak_detect(2.5, self.gyro, -1)
        toeoff_time = self.time[self.toeoff_index]
        return [toeoff_time, 'hello']
