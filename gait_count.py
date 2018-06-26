from data_func import *
import numpy as np
import matplotlib.pyplot as plt

from data_form import *
from filter import *

path = '/Users/Sam/Dropbox/Python/Logging data/data/janie walk 2.xlsx'
data = read_data(path)
starting_index = 0
fs = 33.33
lowcut = 0.5
highcut = 5
order = 4
column = 3

t = data[:, 16]
data_queue = IMU(0, 50)
data_index = [0]
toeoff_time = [0]
count = 0
time_window = 0


for i in range (data.shape[0]):
    imu_data = data[i, starting_index:starting_index+6]
    time = t[i]
    data_queue.add(imu_data, time)
    data_queue.acc_filter(lowcut, highcut, fs, order)
    data_queue.gyro_filter(lowcut, highcut, fs, order)
    [gyro_sen, gyro_index] = data_queue.get_gyro()
    [acc_sen, acc_index] = data_queue.get_acc()
    index = [gyro_index, acc_index, t[i]]
    data_index.append(index)
    gait = Gait(data_queue)
    [yo, hello] = gait.get_toeoff()
    toeoff_time.append(yo)


    # index.append(t[i])


for column in range(0, 6):
    x = data[:, column]
    data[:, column] = butter_bandpass_filter(x, lowcut, highcut, fs, order=order)

data_index = np.asarray(data_index[1:-1])
axs = plot_data(data, 14, 16)


# for i in range(data_index.shape[0]):
#     for j in range(1,3):
#         ax = axs[j*3-3 + int(data_index[i, j-1]) - 1]
#         ax.axvline(x = data_index[i, 2])
#         pass

for i in range(toeoff_time.__len__()):
    ax = axs[2]
    ax.axvline(x = toeoff_time[i])

plt.show()




