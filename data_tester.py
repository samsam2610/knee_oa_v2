from data_analysis import *
from data_form import *
import os

original_path = '/Users/Sam/Dropbox/Python/KneeOA_v_2/data'
list_of_files = os.listdir(original_path)
csv_files = []
for index, file in enumerate(list_of_files):
    if file.endswith('.csv'):
        csv_files.append(file)

for index, file in enumerate(csv_files):

    path = original_path + '/' + csv_files[index]
    data = read_parse_csv(path)

    fs = 25
    accel_index = 4
    gyro_index = 10
    emg_index = 16

    for column in range(emg_index, emg_index+2):
        data[:, column] = data[:, column] - np.mean(data[0:171, column])
        data[:, column] = data[:, column]/max(data[:, column])



    gyro_filter_param = Filter_Parameter(fs=fs, low_cut=0.01, high_cut=1.5, order=4)
    acce_filter_param = Filter_Parameter(fs=fs, low_cut=0.5, high_cut=5, order=4)
    hamstring_filter_param = Filter_Parameter(fs=fs, low_cut=0.01, high_cut=2, order=4)
    quadtricep_filter_param = Filter_Parameter(fs=fs, low_cut=0.01, high_cut=2, order=4)

    time = data[:, -1]
    accel = data[:, accel_index:accel_index+3]
    gyro = data[:, gyro_index:gyro_index+3]
    emg = data[:, emg_index:emg_index+2]

    gait_event = data_process(time_data=time,
                              accel_data=accel,
                              gyro_data=gyro,
                              emg_input_data=emg,
                              gyro_filter_param=gyro_filter_param,
                              acce_filter_param=acce_filter_param,
                              hamstring_filter_param=hamstring_filter_param,
                              quadtricep_filter_param=quadtricep_filter_param)

    data_plot(gait_event=gait_event, data=data,
              gyro_filter_param=gyro_filter_param,
              acce_filter_param=acce_filter_param,
              hamstring_filter_param=hamstring_filter_param,
              quadtricep_filter_param=quadtricep_filter_param,
              accel_index=accel_index,
              gyro_index=gyro_index,
              emg_index=emg_index)

    axs = plot_data(data, 18, 19)
    # save_path = original_path + '/%s.png' % list_of_files[index]
    # plt.savefig(save_path)
