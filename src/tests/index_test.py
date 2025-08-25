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
        #write mock data for testing
        self.filename = 'testsong.wav'
        self.data, self.samples_per_s = sf.read(self.filename)

        self.fft_data = np.fft.fft(self.data)
#Get the frequencies corresponding to the FFT bins
        self.frequencies = np.fft.fftfreq(len(self.data), 1 / self.samples_per_s)


    def test_low_pass(self):
        result = low_pass_filter(self.fft_data, self.frequencies, cutoff_freq)
        # Check if the result is different from the input
        self.assertFalse(np.array_equal(result, self.fft_data), "Low-pass filter did not change the data")
