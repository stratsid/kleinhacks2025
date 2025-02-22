import http
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import librosa
import speech_recognition as sr
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)  # Enable CORS for local testing

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def transcribe_audio(filepath):
    recognizer = sr.Recognizer()

    # Convert to WAV if necessary
    if not filepath.endswith(".wav"):
        audio = AudioSegment.from_file(filepath)
        filepath = filepath.rsplit(".", 1)[0] + ".wav"
        audio.export(filepath, format="wav")

    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Transcription: {text}")  # Print transcription to console
            return text
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
            return None
        except sr.RequestError:
            print("Could not request results, check internet connection")
            return None
        except http.client.RemoteDisconnected:
            print("Remote end closed connection without response")
            return None

def get_bpm(filepath):
    try:
        y, sr = librosa.load(filepath)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = round(float(tempo.item()), 2)
        print(f"BPM: {bpm}")  # Print BPM to console
        return bpm
    except Exception as e:
        print(f"Error analyzing BPM: {e}")
        return None

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Transcribe the audio and print it
    transcription = transcribe_audio(filepath)

    # Get BPM and print it
    bpm = get_bpm(filepath)

    return jsonify({"message": "File uploaded successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
