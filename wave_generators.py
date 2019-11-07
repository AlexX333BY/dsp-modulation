import math
from random import random


def generate_sine_wave(amplitude, frequency, length, initial_phase=0.0):
    assert length >= 0, "Length cannot be negative"
    assert frequency > 0, "Frequency should be positive"
    assert amplitude >= 0, "Amplitude should be non-negative"
    return [generate_sine_signal(i, amplitude, frequency, length, initial_phase) for i in range(length)]


def __generate_carrier_wave(amplitude, frequency, length, signal_generator, offset):
    assert length >= 0, "Length cannot be negative"
    assert frequency > 0, "Frequency should be positive"
    assert 0 <= offset <= 1, "Offset should be between 0 and 1"
    assert amplitude >= 0, "Amplitude should be non-negative"
    period_length = __get_period_length(length, frequency)
    period_wave = [signal_generator(i) for i in range(period_length)]
    offseted_wave = period_wave[int(period_length * offset):] + period_wave[:int(period_length * offset)]
    return offseted_wave * frequency + offseted_wave[:(length % frequency)]


def __get_period_length(length, frequency):
    return length // frequency


def generate_square_wave(amplitude, frequency, duty_cycle, length, offset=0.0):
    assert 0 <= duty_cycle <= 1, "Duty cycle should be between 0 and 1"

    def generate_signal(i):
        return generate_square_signal(i, amplitude, frequency, duty_cycle, length)

    return __generate_carrier_wave(amplitude, frequency, length, generate_signal, offset)


def generate_triangle_wave(amplitude, frequency, length, offset=0.0):
    def generate_signal(i):
        return generate_triangle_signal(i, amplitude, frequency, length)

    return __generate_carrier_wave(amplitude, frequency, length, generate_signal, offset)


def generate_sawtooth_wave(amplitude, frequency, length, offset=0.0):
    def generate_signal(i):
        return generate_sawtooth_signal(i, amplitude, frequency, length)

    return __generate_carrier_wave(amplitude, frequency, length, generate_signal, offset)


def generate_noise_wave(amplitude, length):
    assert length >= 0, "Length cannot be negative"
    assert amplitude >= 0, "Amplitude should be non-negative"
    return [generate_noise_signal(amplitude) for _ in range(length)]


def combine_to_poly_harmonic(waves):
    length = min([len(signal) for signal in waves])
    return [sum([signal[i] for signal in waves]) for i in range(length)]


def generate_sine_signal(i, amplitude, frequency, length, initial_phase=0.0):
    return amplitude * math.sin(frequency * 2 * math.pi * i / length + initial_phase)


def generate_square_signal(i, amplitude, frequency, duty_cycle, length):
    period_length = __get_period_length(length, frequency)
    last_up_pos = int(period_length * duty_cycle)
    return amplitude * (1 if i < last_up_pos else -1)


def generate_triangle_signal(i, amplitude, frequency, length):
    period_length = __get_period_length(length, frequency)
    triangle_middle = period_length // 2
    if i < triangle_middle:
        return 2 * amplitude * i / triangle_middle - amplitude
    elif i == triangle_middle and length % 2 == 1:
        return amplitude
    else:
        return 2 * amplitude * (period_length - i - 1) / triangle_middle - amplitude


def generate_sawtooth_signal(i, amplitude, frequency, length):
    return 2 * amplitude * i / __get_period_length(length, frequency) - amplitude


def generate_noise_signal(amplitude):
    return 2 * amplitude * random() - amplitude
