from functions.play_audio import play_audio
from flask import jsonify, request

def play_signal(signal_type, audio_processor):
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