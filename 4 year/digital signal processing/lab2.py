import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


def create_sin_signal(time: int, f_s: int, ampl: int, frequency: int) -> Tuple:
    # Создание синусоидального сигнала
    t = np.linspace(0, time, f_s * time)
    signal = ampl * np.sin(2 * np.pi * frequency * t)
    return t, signal


def sinc(t: float, period: float) -> np.array:
    # sinc функция h(t)
    temp = t * np.pi
    return 1 if temp == 0 else np.sin(temp / period) / temp


def restore_signal(signal: np.array, period: float, t: np.array, new_t: np.array) -> np.array:
    # Восстановление сигнала по формуле
    t_length = len(t)
    restored_signal = np.zeros(t_length)
    for i in range(t_length):
        for n in range(len(signal)):
            restored_signal[i] += signal[n] * sinc(t[i] - new_t[n], period)
    return restored_signal * period


def main():
    time      = 1
    frequency = 5
    f_s       = frequency * 100
    ampl      = 1
    # Генерируем синусодиальный сигнал
    t, sin_signal = create_sin_signal(time, f_s, ampl, frequency)
    # Выбираем частоты для выполнения теоремы Котельникова и её нарушения
    right_f_s = 2 * frequency + 50
    wrong_f_s = 2 * frequency - 5
    # Генерируем сигналы с соответствующими частотами
    right_t, right_sin_signal = create_sin_signal(time, right_f_s, ampl, frequency)
    wrong_t, wrong_sin_signal = create_sin_signal(time, wrong_f_s, ampl, frequency)
    # Находим соответствующие периоды
    right_period = 1 / right_f_s
    wrong_period = 1 / wrong_f_s
    # Восстанавливаем сигналы с соответствующими частотами
    restored_right_signal = restore_signal(right_sin_signal, right_period, t, right_t)
    restored_wrong_signal = restore_signal(wrong_sin_signal, wrong_period, t, wrong_t)
    # Выводим графики
    fig, axis = plt.subplots(1, 2)
    axis[0].plot(sin_signal)
    axis[0].plot(restored_right_signal)
    axis[0].set_title('Теорема выполняется')
    axis[1].plot(sin_signal)
    axis[1].plot(restored_wrong_signal)
    axis[1].set_title('Теорема не выполняется')
    plt.show()


if __name__=='__main__':
    main()
