
import xlrd
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
                data_array[index_i, index_j] = float(data)
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



