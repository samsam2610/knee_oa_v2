
class Gait():
    def __init__(self, size_max: int, buffer_factor: float):
        self.gyro = size_max * [0]
        self.acce = size_max * [0]
        self.time = size_max * [0]
        self.buffer_factor = buffer_factor
        self.current_toeoff_peak_time = 0
        self.current_heelstrike_peak_time = 0

    def current_data(self, IMU, toeoff_threshold: float, heelstrike_threshold: float):
        self.gyro = IMU.gyro_sen
        self.acce = IMU.acce_sen
        self.time = IMU.time
        self.imu = IMU
        self.toeoff_threshold = toeoff_threshold
        self.heelstrike_threshold = heelstrike_threshold


    def peak_detect(self, threshold, data, current_peak_time):
        data_peak = min(data)
        data_peak_index = data.index(data_peak)
        data_peak_time = self.time[data_peak_index]
        buffer_time = self.buffer_factor * data_peak_time
        if data_peak < threshold:
            if  (data_peak_time > current_peak_time + buffer_time):
                current_peak_time = data_peak_time
            elif current_peak_time == 0:
                current_peak_time = data_peak_time
            else:
                data_peak_index = -1
        else:
            data_peak_index = -1

        return [data_peak_index, current_peak_time]

    def __get_event_index(self, threshold_value: float, data, peak_time):
        [event_index, current_peak_time] = self.peak_detect(threshold_value, data, peak_time)
        if event_index != -1:
            event_index = self.time[event_index]
        return [event_index, current_peak_time]

    def get_toeoff(self):
        [toeoff_time_index, self.current_toeoff_peak_time] = self.__get_event_index(self.toeoff_threshold, self.gyro, self.current_toeoff_peak_time)
        return toeoff_time_index

    def get_heelstrike(self):
        [heelstrike_time_index, self.current_heelstrike_peak_time] = self.__get_event_index(self.heelstrike_threshold, self.acce, self.current_heelstrike_peak_time)
        return heelstrike_time_index
