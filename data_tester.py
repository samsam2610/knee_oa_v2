from data_analysis import *
from data_form import *
import os

original_path = '/Users/Sam/Dropbox/walking emg data/CCNY_DATA'
list_of_files = os.listdir(original_path)
csv_files = []
for index, file in enumerate(list_of_files):
    if file.endswith('.txt'):
        csv_files.append(file)

for index, file in enumerate(csv_files):

    path = original_path + '/' + csv_files[index]
    # path = '/Users/Sam/Dropbox/Python/KneeOA_v_2/data/File Jul 06, 3 08 23 PM run 12.csv'
    print(path)
    data = read_parse_csv(path)
    # np.savetxt(csv_files[index] + '.csv', data, delimiter=',')

    fs = 25
    angle_index = 0
    acce_index = 4
    gyro_index = 10
    emg_index = 16

    # data = data[0: 1200, :]

    for column in range(angle_index, angle_index+4):
        data[:, column] = [np.cos(i/114.5916) for i in data[:, column]]

    # w = data[:, angle_index]
    # x = data[:, angle_index + 1]
    # y = data[:, angle_index + 2]
    # z = data[:, angle_index + 3]
    #
    # roll = [np.rad2deg(np.arctan2(2*y*w - 2*x*z, 1 - 2*y*y - 2*z*z)) for w, x, y, z in zip(w, x, y, z)]
    # pitch = [np.rad2deg(np.arctan2(2*x*w - 2*y*z, 1 - 2*x*x - 2*z*z)) for w, x, y, z in zip(w, x, y, z)]
    # yaw = [np.rad2deg(np.arcsin(2*x*y + 2*z*w))*-1 for w, x, y, z in zip(w, x, y, z)]
    #
    # data[:, angle_index + 1] = roll
    # data[:, angle_index + 2] = pitch
    # data[:, angle_index + 3] = yaw

    for column in range(emg_index, emg_index+2):
        data[:, column] = data[:, column] - np.mean(data[0:171, column])
        data[:, column] = data[:, column]/max(data[:, column])

    gyro_filter_param = Filter_Parameter(fs=fs, low_cut=0.01, high_cut=1.5, order=4)
    acce_filter_param = Filter_Parameter(fs=fs, low_cut=0.5, high_cut=5, order=4)
    hamstring_filter_param = Filter_Parameter(fs=fs, low_cut=0.01, high_cut=2, order=4)
    quadtricep_filter_param = Filter_Parameter(fs=fs, low_cut=0.01, high_cut=2, order=4)

    time = data[:, -1]
    angle = data[:, angle_index:angle_index+4]
    acce = data[:, acce_index+3:acce_index + 6]
    gyro = data[:, gyro_index+3:gyro_index+6]
    emg = data[:, emg_index:emg_index+2]

    gait_event = data_process(time_data=time,
                              angle_input_data=angle,
                              acce_input_data=acce,
                              gyro_input_data=gyro,
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
              angle_index=angle_index,
              accel_index=acce_index,
              gyro_index=gyro_index,
              emg_index=emg_index)

    print("Hello")
    axs = plot_data(data, 18, 19)
    # save_path = original_path + '/%s.png' % list_of_files[index]
    # plt.savefig(save_path)
