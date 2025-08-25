import unittest
from unittest.mock import Mock, patch
from functions.play_signal import play_signal
import numpy as np
from AudioProcessing import AudioProcessing
from flask import Flask
import soundfile as sf

class TestPlaySignal(unittest.TestCase):
    def setUp(self):
          # Create a short test audio file (first 0.5 seconds only)
        # Read just a small portion for faster testing
        data, sample_rate = sf.read('testsong.wav', frames=int(0.5 * 44100))  # 0.1 seconds
        sf.write('test_short.wav', data, sample_rate)
        self.audio_processed = AudioProcessing('test_short.wav', cutoff_freq=2000)
        self.original_signal = 'original'
        self.built_signal_types = ['low_pass_cooley_tukey', 'high_pass_cooley_tukey']
        self.library_signal_types = ['low_pass_fft', 'high_pass_fft']
        self.app = Flask(__name__)
        self.types = ['original', 'low_pass', 'cooley_tukey', 'cooley_tukey_high_pass', 'high_pass']
    
    # patch play_audio to avoid actual audio playback during tests
    @patch('functions.play_signal.play_audio')
    def test_play_signal_outputs(self, mock_play_audio):
        #The test checks that play_audio is called with different signals for each type
        signals = []
        missed_types = []
        for item in self.types:
            #reques context is needed because play_signal expects to be called within a Flask route
            with self.app.test_request_context(json={'type': item}):
                play_signal(item, self.audio_processed)
                if mock_play_audio.call_args is not None:
                    signals.append(mock_play_audio.call_args[0][0])
                else:
                    #if play_audio was not called for this type, add it to the list
                    missed_types.append(item)
                mock_play_audio.reset_mock()
                
        # Check if play_audio was called for all types
        if missed_types:
            print(f"Warning: play_audio was not called for types: {missed_types}")
        #using enumerate to get both index and signal and efficiently compare all pairs
        for i, sig_i in enumerate(signals):
            for j, sig_j in enumerate(signals):
                # Skip self-comparison
                if j > i:
                    self.assertFalse(np.array_equal(sig_i, sig_j), f"Signals for {self.types[i]} and {self.types[j]} should be different")
                    # This confirms that each signal type produces their own output
    
    #patch prevents actual audio playback during tests
    @patch('functions.play_signal.play_audio')
    def test_play_signal_response(self, mock_play_audio):
        #separate test to check that play_signal returns correct response
         #for each type without focusing on the actual audio data played
         #during the test
         #this should check lines 21-23, but i dont know why it doesnt show up in coverage
        for item in self.types:
            with self.app.test_request_context(json={'type': item}):
                response_from_api = play_signal(item, self.audio_processed)
                self.assertEqual(response_from_api.status_code, 200)
                self.assertIn('playing', response_from_api.get_json()['status'])