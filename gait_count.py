from data_func import *
import numpy as np
import matplotlib.pyplot as plt

from data_form import *
from helper import *
from filter import *

path = '/Users/Sam/Dropbox/Python/Logging data/data/janie walk 1.xlsx'
data = read_data(path)
starting_index = 0
gyro_filter_param = Filter_Parameter(fs=33.33, low_cut=0.5, high_cut=5, order=4)
acce_filter_param = Filter_Parameter(fs=33.33, low_cut=0.5, high_cut=5, order=4)
hamstring_filter_param = Filter_Parameter(fs=33.33, low_cut=0.01, high_cut=2, order=4)
quadtricep_filter_param = Filter_Parameter(fs=33.33, low_cut=0.01, high_cut=2, order=4)

column = 3

t = data[:, 16]
imu_queue = IMU(order=0, size_max=50, special_value=0.0)
emg_queue = EMG(size_max=50)
gait_event = Gait_Event(size_max=50)
gait_cycle = Gait_Cycle()
data_index = [0]
toeoff_time = [0]
heelstrike_time = [0]
count = 0
time_window = 0
print(np.mean(data[0:171, 12]))
for column in range(12, 14):
    data[:, column] = data[:, column] - np.mean(data[0:171, column])
    data[:, column] = data[:, column]/max(data[:, column])

for i in range(data.shape[0]):
    imu_data = data[i, starting_index:starting_index+6]
    emg_data = data[i, 12:14]
    time = t[i]
    imu_queue.add(imu_data, time)
    emg_queue.add(emg_data, time)

    imu_queue.gyro_filter(gyro_filter_param.low_cut, gyro_filter_param.high_cut, gyro_filter_param.fs, gyro_filter_param.order)
    imu_queue.acce_filter(acce_filter_param.low_cut, acce_filter_param.high_cut, acce_filter_param.fs, acce_filter_param.order)

    emg_queue.quadtricep_filter(quadtricep_filter_param.low_cut, quadtricep_filter_param.high_cut, quadtricep_filter_param.fs, quadtricep_filter_param.order)
    emg_queue.hamstring_filter(hamstring_filter_param.low_cut, hamstring_filter_param.high_cut, hamstring_filter_param.fs, hamstring_filter_param.order)


    [gyro_sen, gyro_index] = imu_queue.get_gyro()
    [acc_sen, acc_index] = imu_queue.get_acc()
    index = [gyro_index, acc_index, t[i]]
    data_index.append(index)
    gait_event.current_imu_data(imu_queue, gyro_threshold=-2.5, acce_threshold=-6.5)
    gait_event.current_emg_data(emg_queue, hamstring_threshold=0.4, quadriceps_threshold=0.4)

    gait_event.get_gyro(label='Heel Strike')
    gait_event.get_acce(label='Toe Off')
    gait_event.get_hamstring()
    gait_event.get_quadriceps()

    # gait_cycle.add_imu(gait_event)





for column in range(0, 3):
    x = data[:, column]
    data[:, column] = butter_bandpass_filter(x, gyro_filter_param.low_cut, gyro_filter_param.high_cut, gyro_filter_param.fs, order=gyro_filter_param.order)

for column in range(3, 6):
    x = data[:, column]
    data[:, column] = butter_bandpass_filter(x, acce_filter_param.low_cut, acce_filter_param.high_cut, acce_filter_param.fs, order=acce_filter_param.order)

for column in range(12, 14):
    x = data[:, column]
    data[:, column-2] = butter_lowpass_filter(x, quadtricep_filter_param.high_cut,
                                               quadtricep_filter_param.fs, order=quadtricep_filter_param.order)

data_index = np.asarray(data_index[1:-1])
axs = plot_data(data, 14, 16)


toeoff_time_2nd = np.asarray(gait_event.gyro_data)
toeoff_time_2nd = list(toeoff_time_2nd[:, 1])

heelstrike_time_2nd = np.asarray(gait_event.acce_data)
heelstrike_time_2nd = list(heelstrike_time_2nd[:, 1])

hamstring_time = np.asarray(gait_event.hamstring_data)
hamstring_time = list(hamstring_time[:, 1])

quadtricep_time = np.asarray(gait_event.quadriceps_data)
quadtricep_time = list(quadtricep_time[:, 1])

bla = np.asarray(gait_event.event_data)

for i in range(toeoff_time_2nd.__len__()):
    for j in [2]:
        ax = axs[j]
        ax.axvline(x = toeoff_time_2nd[i], color='r')
for i in range(heelstrike_time_2nd.__len__()):
    for j in [3]:
        ax = axs[j]
        ax.axvline(x = heelstrike_time_2nd[i], color='b')
for i in range(hamstring_time.__len__()):
    for j in [10]:
        ax = axs[j]
        ax.axvline(x = hamstring_time[i], color='c')
for i in range(quadtricep_time.__len__()):
    for j in [11]:
        ax = axs[j]
        ax.axvline(x = quadtricep_time[i], color='m')


plt.show()




