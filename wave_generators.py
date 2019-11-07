import math
from random import random


def generate_sine_wave(amplitude, frequency, length, initial_phase=0.0):
    assert length >= 0, "Length cannot be negative"
    assert frequency > 0, "Frequency should be positive"
    assert amplitude >= 0, "Amplitude should be non-negative"
    return [amplitude * math.sin(frequency * 2 * math.pi * i / length + initial_phase) for i in range(length)]


def __generate_carrier_wave(amplitude, frequency, length, period_wave_generator, offset):
    assert length >= 0, "Length cannot be negative"
    assert frequency > 0, "Frequency should be positive"
    assert 0 <= offset <= 1, "Offset should be between 0 and 1"
    assert amplitude >= 0, "Amplitude should be non-negative"
    period_length = length // frequency
    period_wave = [amplitude * signal for signal in period_wave_generator(period_length)]
    print(period_wave_generator(period_length))
    offseted_wave = period_wave[int(period_length * offset):] + period_wave[:int(period_length * offset)]
    return offseted_wave * frequency + offseted_wave[:(length % frequency)]


def generate_square_wave(amplitude, frequency, duty_cycle, length, offset=0.0):
    assert 0 <= duty_cycle <= 1, "Duty cycle should be between 0 and 1"

    def generate_period(period_length):
        return [1] * int(period_length * duty_cycle) + [-1] * (period_length - int(period_length * duty_cycle))

    return __generate_carrier_wave(amplitude, frequency, length, generate_period, offset)


def generate_triangle_wave(amplitude, frequency, length, offset=0.0):
    def generate_period(period_length):
        left = [2 * i / (period_length // 2) - 1 for i in range(period_length // 2)]
        right = left.copy()
        right.reverse()
        return left + ([1] if period_length % 2 == 1 else []) + right

    return __generate_carrier_wave(amplitude, frequency, length, generate_period, offset)


def generate_sawtooth_wave(amplitude, frequency, length, offset=0.0):
    def generate_period(period_length):
        return [2 * i / period_length - 1 for i in range(period_length)]

    return __generate_carrier_wave(amplitude, frequency, length, generate_period, offset)


def generate_noise_wave(amplitude, length):
    assert length >= 0, "Length cannot be negative"
    assert amplitude >= 0, "Amplitude should be non-negative"
    return [2 * amplitude * random() - amplitude for _ in range(length)]


def combine_to_poly_harmonic(waves):
    length = min([len(signal) for signal in waves])
    return [sum([signal[i] for signal in waves]) for i in range(length)]
