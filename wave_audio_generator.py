import wave
from array import array

__SAMPLE_WIDTH_IN_BYTES = 2


def __normalize_to_2byte(wave_data):
    amplitude_multiplier = min(1, (2 ** (8 * __SAMPLE_WIDTH_IN_BYTES) - 1) / max(wave_data))
    return [int(amplitude_multiplier * signal) for signal in wave_data]


def generate_mono_wave_audio(wave_data, output_file_path, repetition_count=1):
    file = wave.open(output_file_path, 'w')
    file.setnchannels(1)
    file.setsampwidth(__SAMPLE_WIDTH_IN_BYTES)
    file.setframerate(len(wave_data))
    file.setnframes(repetition_count)

    short_signal = array('h', __normalize_to_2byte(wave_data))
    file_data = bytearray()
    for i in range(repetition_count):
        file_data.extend(short_signal)
    file.writeframes(file_data)
    file.close()
