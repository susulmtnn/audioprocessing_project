def low_pass_filter(fft_data, freqs, cutoff_freq):
    ''' We keep the frequencies below the cutoff frequency'''
    filtered_fft = fft_data.copy()
    # Loop through frequencies by index and frequency and set to zero if above cutoff
    for i, f in enumerate(freqs):
        if abs(f) > cutoff_freq:
            filtered_fft[i] = 0
    return filtered_fft