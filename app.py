from flask import Flask, request, render_template, jsonify
import os
from src.FeatureExtractor import FeatureExtractor
from src.EmotionDetection import EmotionDetector
from src.AudioProcessor import AudioProcessor  

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Labels
labels = ['Angry', 'Disgust', 'Fearful', 'Happy', 'Neutral', 'Sad', 'Surprised']


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('input.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audioFile' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['audioFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract features
    extractor = FeatureExtractor()
    features = extractor.extract_features(file_path)

    # Perform emotion detection
    model_path = 'model/model.keras'
    detector = EmotionDetector(model_path)
    emotion = detector.predict_emotion(features)

    # Map emotions to emojis
    emoji_map = {
        0: '😠',
        1: '🤢',
        2: '😨',
        3: '😊',
        4: '😐',
        5: '😢',
        6: '😲'
    }
    emoji = emoji_map.get(emotion, '❓')

    return render_template('emotion_display.html', emotion=labels[emotion], emoji=emoji)

@app.route('/record', methods=['POST'])
def record_audio():
    if 'recording.wav' not in request.form:
        return jsonify({"error": "No audio data found"}), 400

    audio_blob = request.form['recording.wav'].encode()
    record_path = os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav')
    with open(record_path, 'wb') as f:
        f.write(audio_blob)

    extractor = FeatureExtractor()
    features = extractor.extract_features(record_path)

    model_path = 'model/model.keras'
    detector = EmotionDetector(model_path)
    emotion = detector.predict_emotion(features)
    
    return jsonify({"emotion": labels[emotion]})




@app.route('/diarize', methods=['POST'])
def diarize_audio():
    if 'diarizeFile' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['diarizeFile']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    model_path = 'model/model.keras'

    # Perform diarization
    processor = AudioProcessor(model_path)  
    diarized_segments = processor.process_audio(file_path)

    return render_template('diarize_display.html', segments=diarized_segments)



if __name__ == '__main__':
    app.run(debug=True)
