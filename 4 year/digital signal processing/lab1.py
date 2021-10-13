import numpy as np
import matplotlib.pyplot as plt


def create_sin_signal(time: int, counts: int, ampl: int, frequency: int) -> np.array:
    # Создание синусоидального сигнала
    t = np.linspace(0, time, counts * time)
    return ampl * np.sin(2 * np.pi * frequency * t)


def create_uni_signal(ampl: int, counts: int, time: int) -> np.array:
    # Создание сигнала с равномерным распределением
    return np.random.uniform(-ampl, ampl, counts * time)


def create_quant_lines(m: int, bits: int) -> np.array:
    # Создание прямых для квантования
    # от -M до M, в количестве 2 ^ B
    return np.int16(np.linspace(-m, m, 2 ** bits))


def quantization(signal: np.array, quantization_lines: np.array) -> np.array:
    # Находим точки квантования среди точек линий квантования
    # которые пересекаются с синусоидой
    quantization_points = []
    for point in signal:
        distances = []
        for line in quantization_lines:
            distance = np.abs(point - line)
            distances.append(distance)
        new_point_ind = np.argmin(distances)
        quantization_points.append(quantization_lines[new_point_ind])
    return np.array(quantization_points)


def calculate_snr(signal: np.array, quantization_noise: np.array) -> float:
    # Вычисление отношения сигнал-шум
    return 10 * np.log10(np.var(signal) / np.var(quantization_noise))


def show_results(theory_snr, sin_snr, uni_snr, sin_quantization_noise, uni_quantization_noise) -> None:
    print(f'Теоретическое отношение сигнал-шум: {theory_snr}\n')
    print(f'Смоделированное отношение сигнал-шум для синусоидального сигнала: {sin_snr}\n')
    print(f'Смоделированное отношение сигнал-шум для сигнала с равномерным распределением: {uni_snr}\n')
    plt.figure('Синусоидальный сигнал')
    plt.hist(sin_quantization_noise)
    plt.figure('Сигнал с равномерным распределением')
    plt.hist(uni_quantization_noise)
    plt.show()


def main():
    frequency = 10
    counts = 1000
    time = 1
    ampl = 4000
    m = 10000
    bits = 8
    theory_snr = 6 * bits - 7.2
    # Генерируем синусодиальный сигнал и с равномерным распределением
    sin_signal = create_sin_signal(time, counts, ampl, frequency)
    uni_signal = create_uni_signal(ampl, counts, time)
    # Создаём линии квантования
    quantization_lines = create_quant_lines(m, bits)
    # Квантование сигналов
    quantized_sin_signal = quantization(sin_signal, quantization_lines)
    quantized_uni_signal = quantization(uni_signal, quantization_lines)
    # Находим шум с квантованием
    sin_quantization_noise = sin_signal - quantized_sin_signal
    uni_quantization_noise = uni_signal - quantized_uni_signal
    # Вычисляем отношения для каждого вида сигналов
    sin_snr = calculate_snr(sin_signal, sin_quantization_noise)
    uni_snr = calculate_snr(uni_signal, uni_quantization_noise)
    show_results(theory_snr, sin_snr, uni_snr, sin_quantization_noise, uni_quantization_noise)


if __name__=='__main__':
    main()
