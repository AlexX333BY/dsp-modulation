import math
from random import random


def generate_sine_wave(amplitude, length, initial_phase=0.0):
    assert length >= 0, "Length cannot be negative"
    assert amplitude >= 0, "Amplitude should be non-negative"
    return [amplitude * math.sin(2 * math.pi * i / length + initial_phase) for i in range(length)]


def __offset_wave(wave, offset):
    assert 0 <= offset <= 1, "Offset should be between 0 and 1"
    offset_pos = int(len(wave) * offset)
    return wave[offset_pos:] + wave[:offset_pos]


def generate_square_wave(amplitude, duty_cycle, length, offset=0.0):
    assert 0 <= duty_cycle <= 1, "Duty cycle should be between 0 and 1"
    assert length >= 0, "Length cannot be negative"
    assert amplitude >= 0, "Amplitude should be non-negative"
    result = [amplitude for _ in range(int(length * duty_cycle))] \
             + [-amplitude for _ in range(int(length * duty_cycle), length)]
    return __offset_wave(result, offset)


def generate_triangle_wave(amplitude, length, offset=0.0):
    assert length >= 0, "Length cannot be negative"
    assert amplitude >= 0, "Amplitude should be non-negative"
    left = [2 * amplitude * i / (length // 2) - amplitude for i in range(length // 2)]
    right = left.copy()
    right.reverse()
    return __offset_wave(left + right, offset)


def generate_sawtooth_wave(amplitude, length, offset=0.0):
    assert length >= 0, "Length cannot be negative"
    assert amplitude >= 0, "Amplitude should be non-negative"
    result = [2 * amplitude * i / length - amplitude for i in range(length)]
    return __offset_wave(result, offset)


def generate_noise(amplitude, length):
    assert length >= 0, "Length cannot be negative"
    assert amplitude >= 0, "Amplitude should be non-negative"
    return [2 * amplitude * random() - amplitude for _ in range(length)]


def combine_to_poly_harmonic(signals):
    length = min([len(signal) for signal in signals])
    return [sum([signal[i] for signal in signals]) for i in range(length)]
