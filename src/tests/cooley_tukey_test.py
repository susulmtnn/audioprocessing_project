import unittest
from unittest import result
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AudioProcessing import AudioProcessing

from functions.cooley_tukey import cooley_tukey

class TestCooleyTukey(unittest.TestCase):

    def test_that_if_recursion_is_done_and_only_one_sample_is_left(self):
        single_sample = [1.0]
        result = cooley_tukey(single_sample)
        self.assertTrue(np.array_equal(result, single_sample), "Single sample should return itself")

    def test_power_of_two_gets_no_input(self):
        list_of_powers_of_two = [2, 4, 8, 16, 32, 64, 128]
        
        for power_of_two in list_of_powers_of_two:
            # Simple array of floating-point numbers
            random_samples = np.random.random(power_of_two)
            print(f"Testing with {power_of_two} samples")
            
            result = cooley_tukey(random_samples)
            self.assertEqual(len(result), power_of_two, 
                f"Power of two of {power_of_two} should not be padded. New length is {len(result)}")

    def test_next_power_of_two_gets_padded(self):
        list_of_powers_of_two = [2, 4, 8, 16, 32, 64, 128]
        
        for i in list_of_powers_of_two:
            # Array with one more than a power of two
            random_samples = np.random.random(i + 1)
            print(f"Testing with {i + 1} samples")
            
            result = cooley_tukey(random_samples)
            self.assertEqual(len(result), 2 * i, 
                f"Array of length {i + 1} should be padded to {2 * i}")
            
    def test_if_can_reconstruct_original_signal(self):
        original_signal = [1.0, 2.0, 3.0, 4.0]
        cooley_tukey_signal = cooley_tukey(original_signal)
        inverse_cooley_tukey = cooley_tukey(cooley_tukey_signal, inverse=True)

        # Check if the reconstructed signal is close to the original
        for i in range(len(original_signal)):
            self.assertAlmostEqual(
                original_signal[i], inverse_cooley_tukey.real[i],
                5,
                f"Forward then inverse FFT should reconstruct original signal at index {i}"
            )

    def test_by_removing_one_sine_wave(self):
        # two sine waves. One with 2500 hz and another with 500 hz
        freq1 = 2500  # Frequency of the first sine wave
        freq2 = 500   # Frequency of the second sine wave
        duration = 1.0  # Duration in seconds
        sample_rate = 65536 #Sample rate chosen to be power of 2 to avoid leakage and it has to be at least twice the highest frequency (Nyquist theorem)

        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        sine_wave1 = np.sin(2 * np.pi * freq1 * t)
        sine_wave2 = np.sin(2 * np.pi * freq2 * t)

        # Combine the two sine waves
        combined_signal = sine_wave1 + sine_wave2
        #scale
        scale= 1.0 / np.max(np.abs(combined_signal))
        combined_signal = combined_signal * scale

        sf.write("testsong_combined_sine_wave.wav", combined_signal, sample_rate)

        # Create an audio processing object with the combined signal
        audio_processor = AudioProcessing("testsong_combined_sine_wave.wav", cutoff_freq=1000)
        result = audio_processor.cooley_tukey_time_domain[:len(sine_wave2)]

        
        # fig, axs = plt.subplots(4, 1, figsize=(12, 8))
        # axs[0].set_title("Sine Wave 1 (2500 Hz)")
        # axs[0].plot(t, sine_wave1)
        # axs[1].set_title("Sine Wave 2 (500 Hz)")
        # axs[1].plot(t, sine_wave2)
        # axs[2].set_title("Combined Signal")
        # axs[2].plot(t, combined_signal)
        # axs[3].set_title("Filtered Result (Cooley-Tukey, Low-pass < 1000 Hz)")
        # axs[3].plot(t, result1)

        # for ax in axs:
        #     ax.set_xlim(0, 0.01)  # Set your desired x-axis range


        # plt.tight_layout()
        # plt.show()

        for i in range(len(sine_wave2)):
            self.assertAlmostEqual(
            result[i], sine_wave2[i]* scale, places=1,
            msg=f"Low-pass filtered Cooley-Tukey result at index {i} should match sine_wave2"
    )
        

if __name__ == "__main__":
    unittest.main()