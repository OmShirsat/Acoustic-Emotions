import librosa
import numpy as np

class FeatureExtractor:
    @staticmethod
    def extract_features(file_path):
        try:
            y, sr = librosa.load(file_path, sr=None)

            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfccs_mean = np.mean(mfccs, axis=1)

            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            chroma_mean = np.mean(chroma, axis=1)

            mel = librosa.feature.melspectrogram(y=y, sr=sr)
            mel_mean = np.mean(mel, axis=1)

            features = np.hstack([mfccs_mean, chroma_mean, mel_mean])
            
            return features
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
