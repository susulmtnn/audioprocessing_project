import numpy as np
import soundfile as sf
import pyaudio
from flask import Flask, jsonify, request, send_from_directory
import threading

app = Flask(__name__)

# Load the audio file
# Ensure you have a WAV file named 'testsong.wav' in the same directory
# To run program, use command poetry run src/index.py
filename = 'testsong.wav'
data, samples_per_s = sf.read(filename)

# Define the cutoff frequency for low-pass filter in Hz
cutoff_freq = 2000

# If the audio file has multiple channels, convert it to mono. This program can only handle mono.
if len(data.shape) > 1:
    data = data.mean(axis=1)

# Convert from time domain to frequency domain with FFT
# TODO: Rewrite with own FFT
fft_data = np.fft.fft(data)
# Get the frequencies corresponding to the FFT bins
frequencies = np.fft.fftfreq(len(data), 1 / samples_per_s)

def low_pass_filter(fft_data, freqs, cutoff_freq):
    # We keep the frequencies below the cutoff frequency
    filtered_fft = fft_data.copy()
    # Loop through frequencies by index and frequency and set to zero if above cutoff
    for i, f in enumerate(freqs):
        if abs(f) > cutoff_freq:
            filtered_fft[i] = 0
    return filtered_fft

def high_pass_filter(original_fft, low_pass_fft):
    # We deduct low-pass from original
    return original_fft - low_pass_fft

# Perform analysis during server startup
def perform_analysis():
    global low_passed, high_passed  # Make filtered signals accessible globally
    low_passed_fft = low_pass_filter(fft_data, frequencies, cutoff_freq)
    low_passed = np.fft.ifft(low_passed_fft).real
    high_passed_fft = high_pass_filter(fft_data, low_passed_fft)
    high_passed = np.fft.ifft(high_passed_fft).real

perform_analysis()  # Analyze audio file at startup

# Using pyaudio to play the audio
def play_audio(signal, samples_per_s):
    # Scale signal so the loudest part is 1.0, then convert to int16 that pyaudio can play
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

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/play', methods=['POST'])
def play():
    signal_type = request.json.get('type')
    if signal_type == 'original':
        play_audio(data, samples_per_s)
    elif signal_type == 'low_pass':
        play_audio(low_passed, samples_per_s)
    elif signal_type == 'high_pass':
        play_audio(high_passed, samples_per_s)
    return jsonify({'status': 'playing', 'type': signal_type})

if __name__ == '__main__':
    app.run(debug=True)
