def __normalize_wave(wave, max_amplitude):
    amplitude_multiplier = max_amplitude / __get_wave_amplitude(wave)
    return [amplitude_multiplier * signal for signal in wave]


def __get_wave_amplitude(wave):
    return max(wave)


def amplitude_modulation(carrier_signal_generator, data_wave, depth=1):
    normalized_data = __normalize_wave(data_wave, 1)
    amplitude_restorer = __get_wave_amplitude(data_wave) / (1 + depth)
    return [(1 + depth * normalized_data[i]) * carrier_signal_generator(i) * amplitude_restorer
            for i in range(len(normalized_data))]


def frequency_modulation(carrier_signal_generator, data_wave, carrier_frequency, frequency_deviation):
    assert frequency_deviation < carrier_frequency, "Frequency deviation should be bigger than carrier frequency"
    normalized_data = __normalize_wave(data_wave, 1)
    amplitude_restorer = __get_wave_amplitude(data_wave)
    return [amplitude_restorer * carrier_signal_generator(i, carrier_frequency + normalized_data[i] * frequency_deviation)
            for i in range(len(normalized_data))]
