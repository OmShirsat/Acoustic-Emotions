import os
import librosa
import soundfile as sf
from src.FeatureExtractor import FeatureExtractor
from src.EmotionDetection import EmotionDetector

labels = ['Angry', 'Disgust', 'Fearful', 'Happy', 'Neutral', 'Sad', 'Surprised']

class AudioProcessor:
    def __init__(self, model_path):
        """
        Initialize the audio processor with a pre-trained emotion detection model.
        """
        self.extractor = FeatureExtractor()
        self.detector = EmotionDetector(model_path)

    def split_audio(self, audio_path, segment_duration=5, output_folder="segments"):
        """
        Split audio into smaller segments of a given duration.
        
        :param audio_path: Path to the input audio file.
        :param segment_duration: Duration of each segment in seconds.
        :param output_folder: Folder to save audio segments.
        :return: List of paths to the audio segments.
        """
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Load the audio file
        audio, sr = librosa.load(audio_path, sr=None)

        # Calculate the number of samples per segment
        segment_samples = int(segment_duration * sr)

        # Split the audio into segments
        segments = []
        for i in range(0, len(audio), segment_samples):
            segment = audio[i:i + segment_samples]
            if len(segment) < segment_samples:
                # Pad the last segment with zeros if it is shorter than the required duration
                segment = librosa.util.fix_length(segment, size=segment_samples)
            segment_path = os.path.join(output_folder, f"segment_{i // segment_samples + 1}.wav")
            sf.write(segment_path, segment, sr)
            segments.append(segment_path)

        return segments

    def process_audio(self, audio_path):
        """
        Process the audio file by splitting it and applying emotion detection on each segment.
        
        :param audio_path: Path to the input audio file.
        :return: Dictionary with segment indices and detected emotions.
        """
        # Load audio to get the sample rate
        audio, sr = librosa.load(audio_path, sr=None)
        segment_paths = self.split_audio(audio_path, segment_duration=3)
        results = {}

        for idx, segment_path in enumerate(segment_paths, start=1):
            # Extract features for each segment
            features = self.extractor.extract_features(segment_path)

            # Predict emotion for each segment
            if features is not None:
                emotion = self.detector.predict_emotion(features)
                results[f"Segment {idx}"] = {
                    "emotion": labels[emotion],
                    "start_time": librosa.frames_to_time(idx * len(features) / sr),
                    "end_time": librosa.frames_to_time((idx + 1) * len(features) / sr),
                    "segment_path": segment_path,
                    "emoji": self.map_emotion_to_emoji(emotion)
                }
            else:
                results[f"Segment {idx}"] = {
                    "emotion": "No features extracted",
                    "start_time": None,
                    "end_time": None,
                    "segment_path": segment_path,
                    "emoji": None
                }

        return results

    def map_emotion_to_emoji(self, emotion):
        emoji_map = {
            0: '😠',
            1: '🤢',
            2: '😨',
            3: '😊',
            4: '😐',
            5: '😢',
            6: '😲'
        }
        return emoji_map.get(emotion, '❓')
