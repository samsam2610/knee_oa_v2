import numpy as np
from data_form import *
from helper import *

def data_process(time_data,
                 accel_data,
                 gyro_data,
                 emg_input_data,
                 gyro_filter_param,
                 acce_filter_param,
                 hamstring_filter_param,
                 quadtricep_filter_param):

    imu_queue = IMU(order=0, size_max=50, special_value=0.0)
    emg_queue = EMG(size_max=20)
    gait_event = Gait_Event(size_max=50)

    for i in range(time_data.size):
        imu_data = np.concatenate((gyro_data[i, :], accel_data[i, :]), axis=0)
        emg_data = emg_input_data[i, :]
        time = time_data[i]
        imu_queue.add(imu_data, time)
        emg_queue.add(emg_data, time)

        imu_queue.gyro_filter(gyro_filter_param.low_cut,
                              gyro_filter_param.high_cut,
                              gyro_filter_param.fs,
                              gyro_filter_param.order)

        imu_queue.acce_filter(acce_filter_param.low_cut,
                              acce_filter_param.high_cut,
                              acce_filter_param.fs,
                              acce_filter_param.order)

        emg_queue.quadtricep_filter(quadtricep_filter_param.low_cut,
                                    quadtricep_filter_param.high_cut,
                                    quadtricep_filter_param.fs,
                                    quadtricep_filter_param.order)

        emg_queue.hamstring_filter(hamstring_filter_param.low_cut,
                                   hamstring_filter_param.high_cut,
                                   hamstring_filter_param.fs,
                                   hamstring_filter_param.order)

        gait_event.current_imu_data(imu_queue, gyro_threshold=-2.5, acce_threshold=-6.5)
        gait_event.current_emg_data(emg_queue, hamstring_threshold=0.4, quadriceps_threshold=0.4)

        gait_event.get_gyro(label='Heel Strike')
        gait_event.get_acce(label='Toe Off')
        gait_event.get_hamstring()
        gait_event.get_quadriceps()

    return gait_event
