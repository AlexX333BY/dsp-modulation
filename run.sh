function IsPackageInstalled()
{
    dpkg -l $1 &> /dev/null
    return $?
}

if ! IsPackageInstalled audacity
then
    echo "Audacity is not installed"
    exit 1
fi

if ! IsPackageInstalled gimp
then
    echo "GIMP is not installed"
    exit 1
fi

# simple wave generating
python3 __main__.py -t generate-wave -f sine.wav -l 44100 -g sine --sine-amplitude 32000 --sine-frequency 400
python3 __main__.py -t generate-wave -f square.wav -l 44100 -g square --square-amplitude 32000 --square-frequency 400 --square-duty-cycle 0.5
python3 __main__.py -t generate-wave -f triangle.wav -l 44100 -g triangle --triangle-amplitude 32000 --triangle-frequency 400
python3 __main__.py -t generate-wave -f sawtooth.wav -l 44100 -g sawtooth --sawtooth-amplitude 32000 --sawtooth-frequency 400
python3 __main__.py -t generate-wave -f noise.wav -l 44100 -g noise --noise-amplitude 32000
audacity sine.wav square.wav triangle.wav sawtooth.wav noise.wav &> /dev/null

# polyharmonic wave generating
python3 __main__.py -t generate-polyharmonic-wave -l 44100 -f polyharmonic.wav -g sine triangle sawtooth \
    --sine-amplitude 32000 --sine-frequency 400 \
    --triangle-amplitude 32000 --triangle-frequency 200 \
    --sawtooth-amplitude 32000 --sawtooth-frequency 100
audacity polyharmonic.wav &> /dev/null

# amplitude modulation
python3 __main__.py -t amplitude-modulation -f amp-sine-on-square.wav -l 44100 \
    --carrier-wave square --square-frequency 400 --square-duty-cycle 0.5 \
    --data-wave sine --sine-amplitude 32000 --sine-frequency 10
python3 __main__.py -t amplitude-modulation -f amp-triangle-on-sawtooth.wav -l 44100 \
    --carrier-wave sawtooth --sawtooth-frequency 400 \
    --data-wave triangle --triangle-amplitude 32000 --triangle-frequency 10
python3 __main__.py -t amplitude-modulation -f amp-sine-on-noise.wav -l 44100 \
    --carrier-wave noise \
    --data-wave sine --sine-amplitude 32000 --sine-frequency 10
audacity amp-sine-on-square.wav amp-triangle-on-sawtooth.wav amp-sine-on-noise.wav &> /dev/null

# frequency modulation
python3 __main__.py --task frequency-modulation -f freq-square-on-sine.wav -l 44100 \
    --carrier-wave sine --carrier-frequency 400 --frequency-deviation 100 \
    --data-wave square --square-amplitude 32000 --square-frequency 10 --square-duty-cycle 0.5
audacity freq-square-on-sine.wav &> /dev/null

# image anti-aliasing
SOURCE="rgb.bmp"
for width in 3 5 7
do
    python3 __main__.py -t image-anti-aliasing -i "${SOURCE}" -w ${width} -o rgb-aa${width}.bmp
done
gimp ${SOURCE} rgb-aa3.bmp rgb-aa5.bmp rgb-aa7.bmp &> /dev/null

