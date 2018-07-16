

def diff_queue(data):
    diff_data = [abs(j-i) for i, j in zip(data, data[1:])]
    return diff_data


def sign_queue(data):
    previous_sign = 1
    return_sign = []
    for index, instance in enumerate(data):
        if instance != 0:
            current_sign = instance/abs(instance)
        else:
            current_sign = previous_sign

        return_sign.append(current_sign)
        previous_sign = current_sign

    return return_sign


def return_true_value(sign, input_value):
    return_value = [i * j for i, j in zip(sign, input_value)]
    return_value.insert(0, return_value[0])
    return return_value



def empty_queue(size_max: int, value: float):
    data_x = [value] * size_max
    data_y = [value] * size_max
    data_z = [value] * size_max
    return [data_x, data_y, data_z]