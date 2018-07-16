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

        self.gyro_peak = peak_finding()
        self.acce_peak = peak_finding()

        self.hamstring_peak = peak_finding()
        self.quadriceps_peak = peak_finding()

        self.hamstring_contract = Threshold()
        self.quadriceps_contract = Threshold()

        self.event_data = []

    def current_imu_data(self, IMU, gyro_threshold: float, acce_threshold: float):
        self.gyro[:] = IMU.gyro_sen
        self.acce[:] = IMU.acce_sen
        self.time[:] = IMU.time
        self.imu = IMU
        self.gyro_threshold = gyro_threshold
        self.acce_threshold = acce_threshold

    def current_emg_data(self, EMG,\
                         hamstring_threshold: float,\
                         quadriceps_threshold: float,\
                         hamstring_contraction_threshold: float,\
                         quadriceps_contraction_threshold: float):
        self.hamstring[:] = EMG.hamstring_filtered
        self.quadriceps[:] = EMG.quadtricep_filtered
        self.hamstring_threshold = hamstring_threshold
        self.quadriceps_threshold = quadriceps_threshold
        self.hamstring_contract.set_threshold(hamstring_contraction_threshold)
        self.quadriceps_contract.set_threshold(quadriceps_contraction_threshold)

    def get_gyro(self, label=str):
        self.gyro_peak.add(value=self.gyro[len(self.gyro) - 1], time=self.time[len(self.time) - 1])
        [loca_value, loca_time, loca_sign, loca_diff] = self.gyro_peak.check()

        [self.gyro_data, self.event_data] = peak_filter(loca_value, loca_time, loca_sign, loca_diff,
                                                        self.gyro_data, self.event_data, 'Gyro 1',
                                                        loca_diff_threshold=1, loca_sign_threhold=-1,
                                                        loca_value_threshold=-abs(self.gyro_threshold))

        [self.gyro_data, self.event_data] = peak_filter(loca_value, loca_time, loca_sign, loca_diff,
                                                        self.gyro_data, self.event_data, 'Gyro 3',
                                                        loca_diff_threshold=4, loca_sign_threhold=-1,
                                                        loca_value_threshold=-abs(self.gyro_threshold))

        [self.gyro_data, self.event_data] = peak_filter(loca_value, loca_time, loca_sign, loca_diff,
                                                        self.gyro_data, self.event_data, 'Gyro 2',
                                                        loca_diff_threshold=4, loca_sign_threhold=1,
                                                        loca_value_threshold=abs(self.gyro_threshold)*3)

    def get_acce(self, label=str):
        self.acce_peak.add(value=self.acce[len(self.acce) - 1], time=self.time[len(self.time) - 1])
        [loca_value, loca_time, loca_sign, loca_diff] = self.acce_peak.check()

        [self.acce_data, self.event_data] = peak_filter(loca_value, loca_time, loca_sign, loca_diff,
                                                        event_instance=self.acce_data,
                                                        event_data=self.event_data,
                                                        event_label='Acce 1',
                                                        loca_sign_threhold=-1,
                                                        loca_value_threshold=abs(self.acce_threshold))

    def get_hamstring(self):
        hamstring_instance = self.get_instance(self.hamstring, self.time)

        self.hamstring_peak.add(value=hamstring_instance["value"], time=hamstring_instance["time"])
        self.hamstring_contract.add(value=hamstring_instance["value"], time=hamstring_instance["time"])

        [loca_value, loca_time, loca_sign, loca_diff] = self.hamstring_peak.check()
        [return_duration, return_start, return_end] = self.hamstring_contract.check()

        [self.hamstring_data, self.event_data] = peak_filter(loca_value, loca_time, loca_sign, loca_diff,
                                                             event_data=self.event_data,
                                                             event_instance=self.hamstring_data,
                                                             event_label='Hamstring',
                                                             loca_diff_threshold=0.2)

        [self.hamstring_data, self.event_data] = threshold_filter(event_start=return_start, event_end=return_end,
                                                                  event_data=self.event_data,
                                                                  event_instance=self.hamstring_data,
                                                                  event_label='Hamstring')

    def get_quadriceps(self):
        quadriceps_instance = self.get_instance(self.quadriceps, self.time)

        self.quadriceps_peak.add(value=quadriceps_instance["value"], time=quadriceps_instance["time"])
        self.quadriceps_contract.add(value=quadriceps_instance["value"], time=quadriceps_instance["time"])

        [loca_value, loca_time, loca_sign, loca_diff] = self.quadriceps_peak.check()
        [return_duration, return_start, return_end] = self.quadriceps_contract.check()

        [self.quadriceps_data, self.event_data] = peak_filter(loca_value, loca_time, loca_sign, loca_diff,
                                                              event_instance=self.quadriceps_data,
                                                              event_data=self.event_data,
                                                              event_label='Quadriceps',
                                                              loca_diff_threshold=0.2)

        [self.quadriceps_data, self.event_data] = threshold_filter(event_start=return_start, event_end=return_end,
                                                                   event_data=self.event_data,
                                                                   event_instance=self.quadriceps_data,
                                                                   event_label='Quadriceps')


    def get_instance(self, input_value, input_time):
        value = input_value[len(input_value) - 1]
        time = input_time[len(input_time) - 1]
        return {"value": value, "time": time}



