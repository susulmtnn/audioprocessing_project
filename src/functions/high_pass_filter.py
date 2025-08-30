
def high_pass_filter(original_fft, low_pass_fft):
    ''' We deduct low-pass from original '''
    return original_fft - low_pass_fft