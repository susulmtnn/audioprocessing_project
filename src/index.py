import numpy as np
import soundfile as sf
import pyaudio
from flask import Flask, jsonify, request, send_from_directory
import threading
import math
from functions.cooley_tukey import cooley_tukey
from functions.low_pass_filter import low_pass_filter
from functions.high_pass_filter import high_pass_filter
from functions.play_audio import play_audio
from AudioProcessing import AudioProcessing
from functions.play_signal import play_signal

# TO DO: clean up imports, remove unused ones

app = Flask(__name__)

audio_processor = AudioProcessing('testsong.wav', cutoff_freq=2000)

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

@app.route('/play', methods=['POST'])
def play():
    signal_type = request.json.get('type')
    play_signal(signal_type, audio_processor)
    return jsonify({'status': 'playing', 'type': signal_type})


if __name__ == '__main__':
    # Initialize the audio processor when script is run directly
    app.run(debug=True)
