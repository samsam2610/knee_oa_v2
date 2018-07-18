from data_analysis.data_func import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

from helper import *

def data_plot(gait_event, data,
              gyro_filter_param,
              acce_filter_param,
              hamstring_filter_param,
              quadtricep_filter_param,
              angle_index,
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
        # data[:-1, column] = diff_queue(data[:, column])

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

    # for column in [emg_index+1]:
    #     x = data[:, column]
    #     data[:, column] = butter_highpass_filter(x,
    #                                             cutOff=12,
    #                                             fs=25,
    #                                             order=6)
    #
    # for column in [emg_index+1]:
    #     x = data[:, column]
    #     data[:, column] = abs(hilbert(butter_highpass_filter(x,
    #                                             cutOff=5,
    #                                             fs=25,
    #                                             order=6)))

    axs = plot_data(data, 18, 19)

    # plt.show()
    # print("hello")

    toeoff_time_2nd = np.asarray(gait_event.gyro_data)
    toeoff_time_2nd = list(toeoff_time_2nd[:, 1])

    heelstrike_time_2nd = np.asarray(gait_event.acce_data)
    heelstrike_time_2nd = list(heelstrike_time_2nd[:, 1])

    hamstring_time = np.asarray(gait_event.hamstring_data)
    # hamstring_time = list(hamstring_time[:, 1])

    quadriceps_time = np.asarray(gait_event.quadriceps_data)
    # quadriceps_time = list(quadriceps_time[:, 1])

    def separate_data(data):
        contraction = []
        peak = []
        for index, datas in enumerate(data):
            if data[index, 0] > 0:
                peak.append(data[index, 1])

            elif data[index, 0] == 0:
                contraction.append(data[index, 1])

        return [contraction, peak]

    [hamstring_contraction, hamstring_peak] = separate_data(hamstring_time)
    [quadriceps_contraction, quadriceps_peak] = separate_data(quadriceps_time)

    for i in range(toeoff_time_2nd.__len__()):
        for j in range(13, 16):
            ax = axs[j]
            ax.axvline(x=toeoff_time_2nd[i], color='r')
    for i in range(heelstrike_time_2nd.__len__()):
        for j in range(7, 10):
            ax = axs[j]
            ax.axvline(x=heelstrike_time_2nd[i], color='b')


    for i in range(hamstring_peak.__len__()):
        for j in [16]:
            ax = axs[j]
            ax.axvline(x=hamstring_peak[i], color='c')

    for i in range(hamstring_contraction.__len__()):
        for j in [16]:
            ax = axs[j]
            ax.axvline(x=hamstring_contraction[i], color='r')


    for i in range(quadriceps_peak.__len__()):
        for j in [17]:
            ax = axs[j]
            ax.axvline(x=quadriceps_peak[i], color='m')
    for i in range(quadriceps_contraction.__len__()):
        for j in [17]:
            ax = axs[j]
            ax.axvline(x=quadriceps_contraction[i], color='b')


    # plt.show()
    print("hello")




