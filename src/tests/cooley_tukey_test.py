import unittest
import numpy as np

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
            

        

if __name__ == "__main__":
    unittest.main()