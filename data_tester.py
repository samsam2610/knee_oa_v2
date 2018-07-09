from data_func import *
import os
original_path = '/Users/Sam/Dropbox/Python/KneeOA_v_2/data'
list_of_files = os.listdir(original_path)
for index, file in enumerate(list_of_files):
    path = original_path + '/' +list_of_files[index]
    data = read_parse_csv(path)
    axs = plot_data(data, 18, 19)
    save_path = original_path + '/%s.png' % list_of_files[index]
    plt.savefig(save_path)

# path = '/Users/Sam/Dropbox/Python/KneeOA_v_2/data/File Jul 06, 3 06 54 PM run 9.csv'
#
#
#
# plt.show()