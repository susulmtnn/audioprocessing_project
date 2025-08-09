from functions.play_audio import play_audio
from flask import jsonify, request

def play_signal(signal_type, audio_processor):
    #some prints for testing, might be removed later
    print(f"Original data length: {len(audio_processor.data)}")
    print(f"NumPy FFT length: {len(audio_processor.fft_data)}")
    print(f"Cooley-Tukey length: {len(audio_processor.cooley_tukey_data)}")
    print(f"Cooley-Tukey frequencies length: {len(audio_processor.frequencies_cooley_tukey)}")
    print(f"Frequencies length: {len(audio_processor.frequencies)}")
    print(f"number of samples per second: {audio_processor.samples_per_s}")
    signal_type = request.json.get('type')
    if signal_type == 'original':
        play_audio(audio_processor.data, audio_processor.samples_per_s)
    elif signal_type == 'low_pass':
        play_audio(audio_processor.low_passed, audio_processor.samples_per_s)
    elif signal_type == 'cooley_tukey':
        play_audio(audio_processor.cooley_tukey_time_domain, audio_processor.samples_per_s)
    elif signal_type == 'cooley_tukey_high_pass':
        play_audio(audio_processor.high_passed_cooley_tukey_time_domain, audio_processor.samples_per_s)
    elif signal_type == 'high_pass':
        play_audio(audio_processor.high_passed, audio_processor.samples_per_s)
    return jsonify({'status': 'playing', 'type': signal_type})