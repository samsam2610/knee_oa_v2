from helper import *

class Gait_Event():
    def __init__(self, size_max: int):
        self.gyro = size_max * [0]
        self.gyro_data = []
        self.acce = size_max * [0]
        self.acce_data = []
        self.time = size_max * [0]
        self.quadriceps = size_max * [0]
        self.quadriceps_data = []
        self.hamstring_data = []
        self.hamstring = size_max * [0]

        self.gyro_object = peak_finding()
        self.acce_object = peak_finding()

        self.hamstring_object = peak_finding()
        self.quadriceps_object = peak_finding()

        self.event_data = []

    def current_imu_data(self, IMU, gyro_threshold: float, acce_threshold: float):
        self.gyro[:] = IMU.gyro_sen
        self.acce[:] = IMU.acce_sen
        self.time[:] = IMU.time
        self.imu = IMU
        self.gyro_threshold = gyro_threshold
        self.acce_threshold = acce_threshold

    def current_emg_data(self, EMG, hamstring_threshold: float, quadriceps_threshold: float):
        self.hamstring[:] = EMG.hamstring_filtered
        self.quadriceps[:] = EMG.quadtricep_filtered
        self.hamstring_threshold = hamstring_threshold
        self.quadriceps_threshold = quadriceps_threshold

    def get_gyro(self, label=str):
        self.gyro_object.add(value=self.gyro[len(self.gyro) - 1], time=self.time[len(self.time) - 1])
        [loca_value, loca_time, loca_sign, loca_diff] = self.gyro_object.check()
        if loca_time != 0\
                and abs(loca_value) < abs(self.gyro_threshold) \
                and loca_diff > 1 \
                and loca_sign == -1:
            gyro_instance = [loca_value, loca_time]
            self.gyro_data.append(gyro_instance)
            self.event_data.append([loca_value, loca_time, label])

    def get_acce(self, label=str):
        self.acce_object.add(value=self.acce[len(self.acce) - 1], time=self.time[len(self.time) - 1])
        [loca_value, loca_time, loca_sign, loca_diff] = self.acce_object.check()
        if loca_time != 0 \
                and abs(loca_value) > abs(self.acce_threshold)\
                and loca_sign == -1:
            acce_instance = [loca_value, loca_time]
            self.acce_data.append(acce_instance)
            self.event_data.append([loca_value, loca_time, label])

    def get_hamstring(self):
        self.hamstring_object.add(value=self.hamstring[len(self.hamstring) - 1], time=self.time[len(self.time) - 1])
        [loca_value, loca_time, loca_sign, loca_diff] = self.hamstring_object.check()
        if loca_time != 0 \
                and loca_diff > 0.2\
                and loca_sign == 1:
            hamstring_instance = [loca_value, loca_time]
            self.hamstring_data.append(hamstring_instance)
            self.event_data.append([loca_value, loca_time, 'Hamstring'])

    def get_quadriceps(self):
        self.quadriceps_object.add(value=self.quadriceps[len(self.quadriceps) - 1], time=self.time[len(self.time) - 1])
        [loca_value, loca_time, loca_sign, loca_diff] = self.quadriceps_object.check()
        if loca_time != 0 \
                and abs(loca_diff) > 0.2 \
                and loca_sign == 1:
            quadriceps_instance = [loca_value, loca_time]
            self.quadriceps_data.append(quadriceps_instance)
            self.event_data.append([loca_value, loca_time, 'Quadriceps'])



