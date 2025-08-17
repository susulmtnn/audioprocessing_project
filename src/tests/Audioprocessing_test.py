import unittest
from AudioProcessing import AudioProcessing
import soundfile as sf
import numpy as np

class TestAudioProcessing(unittest.TestCase):
    def setUp(self):
        # Initialize AudioProcessing with a test file
        self.audio_processor = AudioProcessing('testsong.wav', cutoff_freq=2000)
        self.info = sf.info('testsong.wav')
    
    def test_initialization(self):
        # Check if the audio data is loaded correctly
        
        self.assertIsNotNone(self.audio_processor.data, "Audio data should not be None")
        
        #file duration should  be the same as the length of the data divided by the sample rate
        duration_in_seconds = len(self.audio_processor.data) / self.audio_processor.samples_per_s
        duration_according_to_sf = self.info.duration
        self.assertAlmostEqual(duration_in_seconds, duration_according_to_sf, places=2,
            msg="Duration from data length and sample rate should match duration from soundfile info")
        
    def test_fft_data(self):
        # Check if FFT data is computed correctly
        self.assertIsNotNone(self.audio_processor.fft_data, "FFT data should not be None")
        self.assertEqual(len(self.audio_processor.fft_data), len(self.audio_processor.data), "FFT data length should match audio data length. Does not work with padding as my cooley_tukey")

