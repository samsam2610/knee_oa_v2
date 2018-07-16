from scipy.fftpack import fft, fftshift
from scipy.signal import butter, lfilter, hilbert


def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def butter_lowpass(cutOff, fs, order=4):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='low')
    return b, a


def butter_lowpass_filter(data, cutOff, fs, order=4):
    b, a = butter_lowpass(cutOff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def butter_highpass(cutOff, fs, order=4):
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(order, normalCutoff, btype='high')
    return b, a


def butter_highpass_filter(data, cutOff, fs, order=4):
    b, a = butter_highpass(cutOff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def frequency_domain(data, nfft):
    freq_data = fft(data, nfft)
    freq_data = fftshift(freq_data)
    return freq_data


def peak_filter(loca_value, loca_time, loca_sign, loca_diff, event_instance, event_data, event_label,
                loca_diff_threshold=0, loca_sign_threhold=1, loca_value_threshold=0):
    if loca_time > 0 \
            and loca_sign == loca_sign_threhold \
            and abs(loca_diff) > loca_diff_threshold \
            and abs(loca_value) > loca_value_threshold:

        event_instance.append([loca_value, loca_time])
        event_data.append([loca_value, loca_time, event_label])

    return [event_instance, event_data]


def threshold_filter(event_start, event_end, event_data, event_instance, event_label):
    if event_start > 0 and event_end == 0:
        label = 'Start' + ' ' + event_label
        event_data.append([0, event_start, label])
        event_instance.append([0, event_start])
    elif event_end > 0:
        label = 'End' + ' ' + event_label
        event_data.append([0, event_end, label])
        event_instance.append([0, event_end])

    return [event_instance, event_data]

