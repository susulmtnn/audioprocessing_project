import numpy as np
import soundfile as sf
from functions.cooley_tukey import cooley_tukey
from functions.low_pass_filter import low_pass_filter
from functions.high_pass_filter import high_pass_filter

class AudioProcessing:
# Load the audio file
# Ensure you have a WAV file named 'testsong.wav' in the same directory
# To run program, use command poetry run src/index.py
    def __init__(self, filename, cutoff_freq=1000):
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
        #global low_passed, high_passed, cooley_tukey_time_domain, high_passed_cooley_tukey_time_domain 
        low_passed_fft = low_pass_filter(self.fft_data, self.frequencies, self.cutoff_freq)
        self.low_passed_cooley_tukey = low_pass_filter(self.cooley_tukey_data, self.frequencies_cooley_tukey, self.cutoff_freq)
        # Convert back to time domain using inverse Cooley-Tukey FFT
        self.cooley_tukey_time_domain = cooley_tukey(self.low_passed_cooley_tukey, inverse=True).real  # Convert back to time domain
        self.low_passed = np.fft.ifft(low_passed_fft).real
        high_passed_fft = high_pass_filter(self.fft_data, low_passed_fft)
        self.high_passed = np.fft.ifft(high_passed_fft).real
        high_passed_cooley_tukey = high_pass_filter(self.cooley_tukey_data, self.low_passed_cooley_tukey)
        # Convert back to time domain using inverse Cooley-Tukey FFT
        self.high_passed_cooley_tukey_time_domain = cooley_tukey(high_passed_cooley_tukey, inverse=True).real
