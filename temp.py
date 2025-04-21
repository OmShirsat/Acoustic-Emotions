import matplotlib.pyplot as plt
from flask import Flask, request, render_template, jsonify
import os
from src.FeatureExtractor import FeatureExtractor
from src.EmotionDetection import EmotionDetector
from src.AudioProcessor import AudioProcessor 


def create_emotion_timeline(segments, output_path="png/timeline.png"):
    fig, ax = plt.subplots(figsize=(10, 2))

    # Iterate through segments and add them to the timeline
    for segment_name, segment_details in segments.items():
        start_time = int(segment_details["start_time"] * 1000)  # Convert to milliseconds
        end_time = int(segment_details["end_time"] * 1000)      # Convert to milliseconds
        emotion = segment_details["emotion"]
        emoji = segment_details["emoji"]
        duration = end_time - start_time

        # Plot a rectangle for each segment
        ax.barh(0, duration, left=start_time, color="#87CEEB", edgecolor="black", height=0.4)
        ax.text(start_time + duration / 2, 0,emoji , ha="center", va="center", fontsize=14)

    # Customize the timeline
    ax.set_yticks([])
    ax.set_xlabel("Time (seconds)")
    ax.set_title("Emotion Timeline")
    ax.set_xlim(0, max(segment["end_time"]*1000 for segment in segments.values()))

    ax.set_ylim(-1, 1)

    # Save the timeline as an image
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    model_path = 'model/model.keras'
    file_path='uploads\he-prabhu-ye-kya-hua-audio-meme-download.mp3'
    # Perform diarization
    processor = AudioProcessor(model_path)  # Assuming AudioProcessor has the diarization method
    diarized_segments = processor.process_audio(file_path)

    print(diarized_segments)
    create_emotion_timeline(diarized_segments)

main()
