import math
import numpy as np


def cooley_tukey(x, inverse=False):
    n = len(x)
    '''
    Convert from time domain to frequency domain with FFT. 
    And from frequency domain back to time domain with inverse FFT.
    first we check if the recursion is already done and we have only one sample. 
    if yes, we can return it'''
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
