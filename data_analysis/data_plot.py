from data_analysis.data_func import *
import numpy as np
import matplotlib.pyplot as plt

from helper import *

def data_plot(gait_event, data,
              gyro_filter_param,
              acce_filter_param,
              hamstring_filter_param,
              quadtricep_filter_param,
              accel_index,
              gyro_index,
              emg_index):

    path = '/Users/Sam/Dropbox/Python/Logging data/data/janie walk 1.xlsx'

    for column in range(gyro_index, gyro_index+6):
        x = data[:, column]
        data[:, column] = butter_bandpass_filter(x,
                                                 gyro_filter_param.low_cut,
                                                 gyro_filter_param.high_cut,
                                                 gyro_filter_param.fs,
                                                 order=gyro_filter_param.order)

    for column in range(accel_index, accel_index+6):
        x = data[:, column]
        data[:, column] = butter_bandpass_filter(x,
                                                 acce_filter_param.low_cut,
                                                 acce_filter_param.high_cut,
                                                 acce_filter_param.fs,
                                                 order=acce_filter_param.order)

    for column in range(emg_index, emg_index+2):
        x = data[:, column]
        data[:, column] = butter_lowpass_filter(x,
                                                  quadtricep_filter_param.high_cut,
                                                  quadtricep_filter_param.fs,
                                                  order=quadtricep_filter_param.order)

    axs = plot_data(data, 18, 19)
    plt.show()

    toeoff_time_2nd = np.asarray(gait_event.gyro_data)
    toeoff_time_2nd = list(toeoff_time_2nd[:, 1])

    heelstrike_time_2nd = np.asarray(gait_event.acce_data)
    heelstrike_time_2nd = list(heelstrike_time_2nd[:, 1])

    hamstring_time = np.asarray(gait_event.hamstring_data)
    hamstring_time = list(hamstring_time[:, 1])

    quadtricep_time = np.asarray(gait_event.quadriceps_data)
    quadtricep_time = list(quadtricep_time[:, 1])

    for i in range(toeoff_time_2nd.__len__()):
        for j in [2]:
            ax = axs[j]
            ax.axvline(x=toeoff_time_2nd[i], color='r')
    for i in range(heelstrike_time_2nd.__len__()):
        for j in [3]:
            ax = axs[j]
            ax.axvline(x=heelstrike_time_2nd[i], color='b')
    for i in range(hamstring_time.__len__()):
        for j in [10]:
            ax = axs[j]
            ax.axvline(x=hamstring_time[i], color='c')
    for i in range(quadtricep_time.__len__()):
        for j in [11]:
            ax = axs[j]
            ax.axvline(x=quadtricep_time[i], color='m')

    plt.show()




