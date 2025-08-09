import numpy as np
import pyaudio

def play_audio(signal, samples_per_s):
    # Scale signal so the loudest part is 1.0, then convert to int16 that pyaudio can play
    signal = np.int16(signal / np.max(np.abs(signal)) * 32767)  # Normalize to int16
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=samples_per_s,
                    output=True)
    stream.write(signal.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()