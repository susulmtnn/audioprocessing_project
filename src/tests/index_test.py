import unittest
from index import low_pass_filter, high_pass_filter, play_audio
import numpy as np
import soundfile as sf

#Define the cutoff frequency for low-pass filter in Hz
cutoff_freq = 2000

class Test_Low_pass_filter(unittest.TestCase):
    def setUp(self):
        print("Set up goes here")
        #write mock data for testing
        self.filename = 'testsong.wav'
        self.data, self.samples_per_s = sf.read(self.filename)

        self.fft_data = np.fft.fft(self.data)
#Get the frequencies corresponding to the FFT bins
        self.frequencies = np.fft.fftfreq(len(self.data), 1 / self.samples_per_s)


    def test_low_pass(self):
        result = low_pass_filter(self.fft_data, self.frequencies, cutoff_freq)
        # Check that the filter actually changes the data (they should NOT be equal)
        self.assertFalse(np.array_equal(result, self.fft_data), "Low-pass filter should change the data")

    def test_high_pass(self):
        result = high_pass_filter(self.fft_data, low_pass_filter(self.fft_data, self.frequencies, cutoff_freq))
        # Check that the filter actually changes the data (they should NOT be equal)
        self.assertFalse(np.array_equal(result, self.fft_data), "High-pass filter should change the data")