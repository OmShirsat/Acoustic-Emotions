from tensorflow.keras.models import load_model
import numpy as np

class EmotionDetector:
    def __init__(self, model_path):
        # Load the trained model
        self.model = load_model(model_path)

    def predict_emotion(self, features):
        # Ensure the input features have the correct shape for the CNN model
        features = np.expand_dims(features, axis=0)  # Expanding dims for single input (batch size)
        
        # Make a prediction
        prediction = self.model.predict(features)
        # Return the index of the predicted emotion 
        predicted_emotion = np.argmax(prediction)
        
        return predicted_emotion



