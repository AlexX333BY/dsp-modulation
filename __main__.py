from wave_generators import *
from wave_audio_generator import generate_mono_wave_audio
from modulation import *
import argparse


def generate_wave_task():
    wave_generators_callbacks = get_wave_generators_callbacks()
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generator', action='store', required=True, help='generator name',
                        choices=wave_generators_callbacks.keys(), dest='generator', type=str)
    parser.add_argument('-r', '--repetitions', action='store', required=False, help='wave repetition count',
                        dest='repetition', type=int, default=1)
    parser.add_argument('-f', '--file', action='store', required=True, help='save file name', dest='file', type=str)
    parser.add_argument('-l', '--length', action='store', required=True, help='wave length', dest='length', type=int)
    args = parser.parse_known_args()[0]
    generate_mono_wave_audio(wave_generators_callbacks[args.generator](args.length), args.file, args.repetition)


def generate_polyharmonic_wave_task():
    wave_generators_callbacks = get_wave_generators_callbacks()
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generators', action='store', required=True, help='generators', nargs='+',
                        choices=wave_generators_callbacks.keys(), dest='generators', type=str)
    parser.add_argument('-r', '--repetitions', action='store', required=False, help='wave repetition count',
                        dest='repetition', type=int, default=1)
    parser.add_argument('-f', '--file', action='store', required=True, help='save file name', dest='file', type=str)
    parser.add_argument('-l', '--length', action='store', required=True, help='wave length', dest='length', type=int)
    args = parser.parse_known_args()[0]
    waves = [wave_generators_callbacks[generator_name](args.length) for generator_name in args.generators]
    generate_mono_wave_audio(combine_to_poly_harmonic(waves), args.file, args.repetition)


def amplitude_modulation_task():
    wave_generators_callbacks = get_wave_generators_callbacks()
    signal_generators_callbacks = get_signal_generators_callbacks()
    parser = argparse.ArgumentParser()
    parser.add_argument('-cw', '--carrier-wave', action='store', required=True, help='carrier wave name',
                        choices=wave_generators_callbacks.keys(), dest='carrier', type=str)
    parser.add_argument('-dw', '--data-wave', action='store', required=True, help='data wave name',
                        choices=wave_generators_callbacks.keys(), dest='data', type=str)
    parser.add_argument('-r', '--repetitions', action='store', required=False, help='wave repetition count',
                        dest='repetition', type=int, default=1)
    parser.add_argument('-f', '--file', action='store', required=True, help='save file name', dest='file', type=str)
    parser.add_argument('-l', '--length', action='store', required=True, help='wave length', dest='length', type=int)
    parser.add_argument('-d', '--depth', action='store', required=False, help='modulation depth', dest='depth',
                        type=int, default=1)
    args = parser.parse_known_args()[0]

    carrier = signal_generators_callbacks[args.carrier](args.length)
    data = wave_generators_callbacks[args.data](args.length)
    modulated = amplitude_modulation(carrier, data, args.depth)
    generate_mono_wave_audio(modulated, args.file, args.repetition)


def frequency_modulation_task():
    wave_generators_callbacks = get_wave_generators_callbacks()
    signal_generators_callbacks = get_signal_with_frequencies_generators_callbacks()
    parser = argparse.ArgumentParser()
    parser.add_argument('-cw', '--carrier-wave', action='store', required=True, help='carrier wave name',
                        choices=wave_generators_callbacks.keys(), dest='carrier', type=str)
    parser.add_argument('-dw', '--data-wave', action='store', required=True, help='data wave name',
                        choices=wave_generators_callbacks.keys(), dest='data', type=str)
    parser.add_argument('-r', '--repetitions', action='store', required=False, help='wave repetition count',
                        dest='repetition', type=int, default=1)
    parser.add_argument('-f', '--file', action='store', required=True, help='save file name', dest='file', type=str)
    parser.add_argument('-l', '--length', action='store', required=True, help='wave length', dest='length', type=int)
    parser.add_argument('-cf', '--carrier-frequency', action='store', required=True, help='carrier wave frequency',
                        dest='carrier_freq', type=int)
    parser.add_argument('-cfd', '--frequency-deviation', action='store', required=True,
                        help='carrier wave frequency deviation', dest='carrier_deviation', type=int)
    args = parser.parse_known_args()[0]

    carrier = signal_generators_callbacks[args.carrier](args.length)
    data = wave_generators_callbacks[args.data](args.length)
    modulated = frequency_modulation(carrier, data, args.carrier_freq, args.carrier_deviation)
    generate_mono_wave_audio(modulated, args.file, args.repetition)


# wave generators


def sine_wave_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--sine-amplitude', action='store', required=True, help='sine amplitude', dest='sine_amp',
                        type=float)
    parser.add_argument('--sine-frequency', action='store', required=True, help='sine frequency', dest='sine_freq',
                        type=int)
    parser.add_argument('--sine-phase', action='store', required=False, help='sine initial phase', dest='sine_phase',
                        type=float, default=0.0)
    args = parser.parse_known_args()[0]
    return generate_sine_wave(args.sine_amp, args.sine_freq, length, args.sine_phase)


def square_wave_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--square-amplitude', action='store', required=True, help='square amplitude', dest='square_amp',
                        type=float)
    parser.add_argument('--square-frequency', action='store', required=True, help='square frequency',
                        dest='square_freq', type=int)
    parser.add_argument('--square-offset', action='store', required=False, help='square initial phase',
                        dest='square_offset', type=float, default=0.0)
    parser.add_argument('--square-duty-cycle', action='store', required=True, help='square duty cycle',
                        dest='square_duty_cycle', type=float)
    args = parser.parse_known_args()[0]
    return generate_square_wave(args.square_amp, args.square_freq, args.square_duty_cycle, length, args.square_offset)


def triangle_wave_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--triangle-amplitude', action='store', required=True, help='triangle amplitude',
                        dest='triangle_amp',
                        type=float)
    parser.add_argument('--triangle-frequency', action='store', required=True, help='triangle frequency',
                        dest='triangle_freq', type=int)
    parser.add_argument('--triangle-offset', action='store', required=False, help='triangle initial phase',
                        dest='triangle_offset', type=float, default=0.0)
    args = parser.parse_known_args()[0]
    return generate_triangle_wave(args.triangle_amp, args.triangle_freq, length, args.triangle_offset)


def sawtooth_wave_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--sawtooth-amplitude', action='store', required=True, help='sawtooth amplitude',
                        dest='sawtooth_amp',
                        type=float)
    parser.add_argument('--sawtooth-frequency', action='store', required=True, help='sawtooth frequency',
                        dest='sawtooth_freq', type=int)
    parser.add_argument('--sawtooth-offset', action='store', required=False, help='sawtooth initial phase',
                        dest='sawtooth_offset', type=float, default=0.0)
    args = parser.parse_known_args()[0]
    return generate_sawtooth_wave(args.sawtooth_amp, args.sawtooth_freq, length, args.sawtooth_offset)


def noise_wave_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--noise-amplitude', action='store', required=True, help='noise amplitude', dest='noise_amp',
                        type=float)
    args = parser.parse_known_args()[0]
    return generate_noise_wave(args.noise_amp, length)


def get_wave_generators_callbacks():
    return {'sine': sine_wave_generator,
            'square': square_wave_generator,
            'triangle': triangle_wave_generator,
            'sawtooth': sawtooth_wave_generator,
            'noise': noise_wave_generator
            }


# signal generators with variable frequency


def get_sine_signal_generator_with_frequency(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--sine-phase', action='store', required=False, help='sine initial phase', dest='sine_phase',
                        type=float, default=0.0)
    args = parser.parse_known_args()[0]
    return lambda i, frequency: generate_sine_signal(i, 1, frequency, length, args.sine_phase)


def get_square_signal_generator_with_frequency(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--square-duty-cycle', action='store', required=True, help='square duty cycle',
                        dest='square_duty_cycle', type=float)
    args = parser.parse_known_args()[0]
    return lambda i, frequency: generate_square_signal(i, 1, frequency, args.square_duty_cycle, length)


def get_triangle_signal_generator_with_frequency(length):
    return lambda i, frequency: generate_triangle_signal(i, 1, frequency, length)


def get_sawtooth_signal_generator_with_frequency(length):
    return lambda i, frequency: generate_sawtooth_signal(i, 1, frequency, length)


def get_noise_signal_generator_with_frequency():
    return lambda i, frequency: generate_noise_signal(1)


def get_signal_with_frequencies_generators_callbacks():
    return {'sine': get_sine_signal_generator_with_frequency,
            'square': get_square_signal_generator_with_frequency,
            'triangle': get_triangle_signal_generator_with_frequency,
            'sawtooth': get_sawtooth_signal_generator_with_frequency,
            'noise': lambda length: get_noise_signal_generator_with_frequency
            }


# signal generators


def get_sine_signal_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--sine-frequency', action='store', required=True, help='sine frequency', dest='sine_freq',
                        type=int)
    args = parser.parse_known_args()[0]
    generator = get_sine_signal_generator_with_frequency(length)
    return lambda i: generator(i, args.sine_freq)


def get_square_signal_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--square-frequency', action='store', required=True, help='square frequency',
                        dest='square_freq', type=int)
    args = parser.parse_known_args()[0]
    generator = get_square_signal_generator_with_frequency(length)
    return lambda i: generator(i, args.square_freq)


def get_triangle_signal_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--triangle-frequency', action='store', required=True, help='triangle frequency',
                        dest='triangle_freq', type=int)
    args = parser.parse_known_args()[0]
    generator = get_triangle_signal_generator_with_frequency(length)
    return lambda i: generator(i, args.triangle_freq)


def get_sawtooth_signal_generator(length):
    parser = argparse.ArgumentParser()
    parser.add_argument('--sawtooth-frequency', action='store', required=True, help='sawtooth frequency',
                        dest='sawtooth_freq', type=int)
    args = parser.parse_known_args()[0]
    generator = get_sawtooth_signal_generator_with_frequency(length)
    return lambda i: generator(i, args.sawtooth_freq)


def get_noise_signal_generator():
    return lambda i: generate_noise_signal(1)


def get_signal_generators_callbacks():
    return {'sine': get_sine_signal_generator,
            'square': get_square_signal_generator,
            'triangle': get_triangle_signal_generator,
            'sawtooth': get_sawtooth_signal_generator,
            'noise': lambda length: get_noise_signal_generator
            }


def main():
    tasks_callbacks = {'generate-wave': generate_wave_task,
                       'generate-polyharmonic-wave': generate_polyharmonic_wave_task,
                       'amplitude-modulation': amplitude_modulation_task,
                       'frequency-modulation': frequency_modulation_task
                       }

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--task', action='store', required=True, help='task name',
                        choices=tasks_callbacks.keys(), dest='task', type=str)

    args = parser.parse_known_args()[0]
    tasks_callbacks[args.task]()


if __name__ == "__main__":
    main()
