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

if __name__ == "__main__":
    unittest.main()