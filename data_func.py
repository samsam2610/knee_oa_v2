
import xlrd
import csv
import numpy as np
from matplotlib import pyplot as plt


def read_data(path: str):
    book = xlrd.open_workbook(path)
    col_elements = len(book._sharedstrings[2].split(","))
    row_elements = len(book._sharedstrings)
    data_array = np.zeros([row_elements, col_elements])
    for index_i, value in enumerate(book._sharedstrings):
        data_temp = value.split(",")
        for index_j, data in enumerate(data_temp):
            try:
                data_array[index_i, index_j] = round(float(data), 2)
            except ValueError:
                pass
            if (index_j == col_elements - 1):
                data_array[index_i, index_j] += data_array[index_i, index_j] + data_array[index_i - 1, index_j]
    return data_array

def plot_data(data, n: int, time_index: int):
    fig, axs = plt.subplots(nrows=n, ncols=1, sharex=True, figsize = [20,20])
    x = data[:, time_index]
    for index in range(0, n):
        ax = axs[index]
        y = data[:, index]
        ax.plot(x, y)
        y_major_ticks = np.arange(y.min(), y.max(), abs(y.min() - y.max())/10)
        x_major_ticks = np.arange(0, max(x), 5000)
        ax.set_ylim([y.min(), y.max()])
        ax.set_yticks(y_major_ticks)
        ax.set_xticks(x_major_ticks)
        ax.grid(which='both')
        pass
    return axs

def read_parse_csv(path: str):
    file = open(path)
    raw_data = csv.reader(file)
    data_temp = ''
    data_final = ''
    data_full = []
    time = 0
    for row in raw_data:
        data = str(row[2])
        if 's' in data:
            data_temp = data
        elif 'e' in data and 's' in data_temp:
            data_temp = data_temp + data
            data_final = data_temp
            print(data_final)
            data_temp = ''
        elif 's' in data_temp and not 'e' in data_temp:
            data_temp = data_temp + data

        if 's' in data_final and 'e' in data_final:
            data_elements = data_final.split(',')
            if data_elements.__len__() == 21:
                time = time + float(data_elements[-2])
                data_element = []
                for index, element in enumerate(data_elements[1:-1]):
                    data_element.append(float(element))
                data_element.append(time)
                data_full.append(data_element)

    return(np.asarray(data_full))


