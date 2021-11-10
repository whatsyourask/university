from scipy.io import wavfile
import numpy as np
from scipy.signal.windows import hann
import matplotlib.pyplot as plt


def get_windows(data: list, window: int, step: int) -> np.array:
    # Идём по сигналу с шагом 16 и берём по 256
    data_length = len(data) // window
    windows     = np.zeros((data_length, window))
    hann_window = hann(window)
    for i in range(data_length):
        temp_window = data[i * step: i * step + window]
        # Умножаем каждый элементе списка на hann
        windows[i] = hann_window * temp_window
    return windows


def get_fft(windows: np.array) -> np.array:
    # Применяем для каждого элемента функцию np.fft.fft и берём [:, : длина // 2]
    rows, columns = windows.shape
    fft           = np.zeros((rows, columns))
    for i, window in enumerate(windows, 0):
        # Берём модуль от вычисленных значений после функции np.fft.fft
        fft[i] = np.abs(np.fft.fft(window))
    return fft[:, :columns // 2]


def get_mean_rows(ffts: np.array, n) -> np.array:
    # Вычисляем среднее fft
    rows, columns = ffts.shape
    rows //= n
    mean_rows = np.zeros((rows, columns))
    for i in range(rows):
        mean_rows[i] = np.mean(ffts[i * n: i * n + n, :], axis=0)
    return mean_rows


def get_spectrograms(mean_rows: np.array) -> tuple:
    # Транспонируем усреднённые значения и берём логарифм по основанию 10
    # от каждого элемента
    log_mean_rows = np.log10(mean_rows)
    spectrogram   = log_mean_rows.T
    # После просмотра данных, определяем, где тишина на спектрограмме, а где голос
    spectrogram_with_silence = spectrogram[:, 0: 300]
    spectrogram_with_voice   = spectrogram[:, 600: 1200]
    return spectrogram, spectrogram_with_silence, spectrogram_with_voice


def show_results(spectrograms: tuple, window: int, rate: int) -> None:
    # Вывод спектрограмм и графика
    fig, axis = plt.subplots(1, 3)
    axis[0].set_title('Спектрограмма с тишиной')
    axis[0].imshow(spectrograms[0])
    axis[1].set_title('Спектрограмма с голосом')
    axis[1].imshow(spectrograms[1])
    axis[0].invert_yaxis()
    axis[1].invert_yaxis()
    axis[2].set_title('Зависимость частоты от времени')
    axis[2].plot(np.argmax(spectrograms[1], axis=0) * rate / window)
    plt.show()


def main():
    rate, data   = wavfile.read('voice.wav')
    window       = 256
    step         = 64 // 4
    windows      = get_windows(data, window, step)
    ffts         = get_fft(windows)
    mean_rows    = get_mean_rows(ffts, 3)
    spectrograms = get_spectrograms(mean_rows)
    show_results(spectrograms[1:], window, rate)


if __name__=='__main__':
    main()
