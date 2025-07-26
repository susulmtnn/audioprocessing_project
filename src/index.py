import numpy as np
import soundfile as sf
import pyaudio

# Load the audio file
# Ensure you have a WAV file named 'testsong.wav' in the same directory
# To run program, use command poetry run src/index.py
filename = 'testsong.wav'
data, samples_per_s = sf.read(filename)

#Define the cutoff frequency for low-pass filter in Hz
cutoff_freq = 2000

# if the audio file has multiple channels, convert it to mono. This pregram can only handle mono.
if len(data.shape) > 1:
    data = data.mean(axis=1)

# convert from time domain to frequency domain with FFT
# TODO : Rewrite with own FFT
fft_data = np.fft.fft(data)
#Get the frequencies corresponding to the FFT bins
frequencies = np.fft.fftfreq(len(data), 1 / samples_per_s)

def low_pass_filter(fft_data, freqs, cutoff_freq):
# we keep the frequencies below the cutoff frequency
    filtered_fft = fft_data.copy()
# Loop throug frequencies by index and frequency and set to zero if above cutoff
    for i, f in enumerate(freqs):
        if abs(f) > cutoff_freq:
            filtered_fft[i] = 0
    return filtered_fft

def high_pass_filter(original_fft, low_pass_fft):
 # we deduct low-pass from original
    return original_fft - low_pass_fft

#Frequency domain filtering
low_passed_fft = low_pass_filter(fft_data, frequencies, cutoff_freq)
#Inverse FFT to convert back to time domain
low_passed = np.fft.ifft(low_passed_fft).real

# #Frequency domain filtering
high_passed_fft = high_pass_filter(fft_data, low_passed_fft)
#Inverse FFT to convert back to time domain
high_passed = np.fft.ifft(high_passed_fft).real

# using pyaudio to play the audio
def play_audio(signal, samples_per_s):
    #scale signal so the loudest part is 1.0, then converts to int16 that pyaudio can play
    signal = np.int16(signal / np.max(np.abs(signal)) * 32767)  # Normalize to int16
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=samples_per_s,
                    output=True)
    stream.write(signal.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

# Play both filtered versions
print("Playing original audio...")
play_audio(data, samples_per_s)

print("Playing LOW-pass filtered...")
play_audio(low_passed, samples_per_s)

print("Playing HIGH-pass filtered...")
play_audio(high_passed, samples_per_s)
