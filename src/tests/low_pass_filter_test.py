import unittest
from unittest.mock import patch
from index import app
from AudioProcessing import AudioProcessing
import numpy as np
import soundfile as sf
from flask import Flask
from functions.low_pass_filter import low_pass_filter

#Define the cutoff frequency for low-pass filter in Hz
cutoff_freq = 2000

class Test_Low_pass_filter(unittest.TestCase):
    def setUp(self):
        self.filename = 'testsong.wav'
        self.data, self.samples_per_s = sf.read(self.filename)

        self.fft_data = np.fft.fft(self.data)
        #Get the frequencies corresponding to the FFT bins
        self.frequencies = np.fft.fftfreq(len(self.data), 1 / self.samples_per_s)


    def test_low_pass(self):
        result = low_pass_filter(self.fft_data, self.frequencies, cutoff_freq)
        # Check if the result is different from the input
        self.assertFalse(np.array_equal(result, self.fft_data), "Low-pass filter did change the data")

    def test_low_pass_no_change_below_cutoff(self):
        # Frequencies below the cutoff should remain unchanged
        low_freqs = np.abs(self.frequencies) <= cutoff_freq
        filtered = low_pass_filter(self.fft_data, self.frequencies, cutoff_freq)
        self.assertTrue(
                np.allclose(filtered[low_freqs], self.fft_data[low_freqs], atol=1e-5),
                msg="Frequencies below cutoff should remain unchanged"
            )