def __normalize_wave(wave, max_amplitude):
    amplitude_multiplier = min(1, max_amplitude / max(wave))
    return [amplitude_multiplier * signal for signal in wave]


def amplitude_modulation(carrier_wave, data_wave, depth=1):
    normalized_carrier = __normalize_wave(carrier_wave, 1)
    normalized_data = __normalize_wave(data_wave, 1)
    modulated_wave_length = min(len(normalized_carrier), len(normalized_data))
    return [(1 + depth * normalized_data[i]) * normalized_carrier[i] for i in range(modulated_wave_length)]


def frequency_modulation(carrier_signal_generator, data_wave, carrier_frequency, frequency_deviation):
    assert frequency_deviation < carrier_frequency, "Frequency deviation should be bigger than carrier frequency"
    normalized_data = __normalize_wave(data_wave, 1)

    return [carrier_signal_generator(i, carrier_frequency + normalized_data[i] * frequency_deviation)
            for i in range(len(normalized_data))]
