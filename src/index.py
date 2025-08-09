import numpy as np
import soundfile as sf
import pyaudio
from flask import Flask, jsonify, request, send_from_directory
import threading
import math

app = Flask(__name__)


# Convert from time domain to frequency domain with FFT. 
# And from frequency domain back to time domain with inverse FFT.

def cooley_tukey(x, inverse=False):
    n = len(x)
    #first we check if the recursion is already done and we have only one sample. 
    #if yes, we can return it
    if n <= 1:
        return x
    #pad to next power of 2 if necessary
    if n & (n - 1) != 0:  # Check if n is not a power of 2
        #get next power of 2
        next_power_of_2 = math.ceil(math.log(n, 2))
        # pad x with zeros to the next power of 2
        next_power_of_2 = 2 ** next_power_of_2
        x = np.pad(x, (0, next_power_of_2 - n))
        n = next_power_of_2

        # #if the number of samples is even, we split the samples into two parts
    even = cooley_tukey(x[0::2], inverse)
    odd = cooley_tukey(x[1::2], inverse)
        # Conquer step: combine the even and odd parts
        # We use the twiddle factor to combine the even and odd parts
    result = np.zeros(n, dtype=complex)
    for i in range(n // 2):
        # we have to change the sign of the exponent for inverse FFT
        if inverse:
            w = np.exp(2j * np.pi * i / n)
        else:
            w = np.exp(-2j * np.pi * i / n)
        result[i] = even[i] + w * odd[i]
        result[i + n // 2] = even[i] - w * odd[i]
    # If inverse FFT is requested, we divide the result by 2
    if inverse:
        
        return result / 2
    else:
        return result



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

class AudioProcessing:
    # Load the audio file
# Ensure you have a WAV file named 'testsong.wav' in the same directory
# To run program, use command poetry run src/index.py
    def __init__(self, filename, cutoff_freq=2000):
        self.filename = filename
        # Define the cutoff frequency for low-pass filter in Hz
        self.cutoff_freq = cutoff_freq
    
        self.data, self.samples_per_s = sf.read(filename)

        # If the audio file has multiple channels, convert it to mono. This program can only handle mono.
        if len(self.data.shape) > 1:
            self.data = self.data.mean(axis=1)

        self.fft_data = np.fft.fft(self.data)
        self.cooley_tukey_data = cooley_tukey(self.data)
        self.length_of_cooley_tukey_data = len(self.cooley_tukey_data)
        #own frequency domain conversion for cooley-tukey
        self.frequencies_cooley_tukey = np.fft.fftfreq(self.length_of_cooley_tukey_data, 1 / self.samples_per_s)
        # Get the frequencies corresponding to the FFT bins
        self.frequencies = np.fft.fftfreq(len(self.data), 1 / self.samples_per_s)
        # Time to actually run the analysis
        self.perform_analysis()

# Perform analysis during server startup
    def perform_analysis(self):
        #global low_passed, high_passed, cooley_tukey_time_domain, high_passed_cooley_tukey_time_domain  # Make filtered signals accessible globally
        low_passed_fft = low_pass_filter(self.fft_data, self.frequencies, self.cutoff_freq)
        low_passed_cooley_tukey = low_pass_filter(self.cooley_tukey_data, self.frequencies_cooley_tukey, self.cutoff_freq)
        # Convert back to time domain using inverse Cooley-Tukey FFT
        self.cooley_tukey_time_domain = cooley_tukey(low_passed_cooley_tukey, inverse=True).real  # Convert back to time domain
        self.low_passed = np.fft.ifft(low_passed_fft).real
        high_passed_fft = high_pass_filter(self.fft_data, low_passed_fft)
        self.high_passed = np.fft.ifft(high_passed_fft).real
        high_passed_cooley_tukey = high_pass_filter(self.cooley_tukey_data, low_passed_cooley_tukey)
        # Convert back to time domain using inverse Cooley-Tukey FFT
        self.high_passed_cooley_tukey_time_domain = cooley_tukey(high_passed_cooley_tukey, inverse=True).real



@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/play', methods=['POST'])
def play():
    print(f"Original data length: {len(audio_processor.data)}")
    print(f"NumPy FFT length: {len(audio_processor.fft_data)}")
    print(f"Cooley-Tukey length: {len(audio_processor.cooley_tukey_data)}")
    print(f"Cooley-Tukey frequencies length: {len(audio_processor.frequencies_cooley_tukey)}")
    print(f"Frequencies length: {len(audio_processor.frequencies)}")
    print(f"number of samples per second: {audio_processor.samples_per_s}")
    signal_type = request.json.get('type')
    if signal_type == 'original':
        play_audio(audio_processor.data, audio_processor.samples_per_s)
    elif signal_type == 'low_pass':
        play_audio(audio_processor.low_passed, audio_processor.samples_per_s)
    elif signal_type == 'cooley_tukey':
        play_audio(audio_processor.cooley_tukey_time_domain, audio_processor.samples_per_s)
    elif signal_type == 'cooley_tukey_high_pass':
        play_audio(audio_processor.high_passed_cooley_tukey_time_domain, audio_processor.samples_per_s)
    elif signal_type == 'high_pass':
        play_audio(audio_processor.high_passed, audio_processor.samples_per_s)
    return jsonify({'status': 'playing', 'type': signal_type})



if __name__ == '__main__':
    # Initialize the audio processor when script is run directly
    audio_processor = AudioProcessing('testsong.wav', cutoff_freq=2000)
    app.run(debug=True)
