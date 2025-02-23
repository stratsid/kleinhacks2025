import os
import http
import json
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
import speech_recognition as sr
from pydub import AudioSegment
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load environment variables from .env file and set OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

def transcribe_audio(filepath):
    recognizer = sr.Recognizer()

    # Convert to WAV if necessary
    if not filepath.endswith(".wav"):
        audio = AudioSegment.from_file(filepath)
        wav_path = filepath.rsplit(".", 1)[0] + ".wav"
        audio.export(wav_path, format="wav")
        filepath = wav_path

    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Transcription: {text}")
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
        y, sr_rate = librosa.load(filepath)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr_rate)
        bpm = round(float(tempo.item()), 2)
        print(f"BPM: {bpm}")
        return bpm
    except Exception as e:
        print(f"Error analyzing BPM: {e}")
        return None

def evaluate_track(transcription, bpm):
    """
    Sends a prompt to the OpenAI model to evaluate the song.
    The prompt asks for a JSON response with the following keys:
      - 'success': a boolean indicating if the song is likely to succeed.
      - 'placeholder1': a one-line factual comparison of BPM, formatted exactly as "AVG BPM: {avg bpm}, Your BPM: {your bpm}" (under 50 characters).
      - 'placeholder2': a concise comparison of common mainstream words (excluding common articles) versus the transcript's words, formatted as:
           "Common Mainstream Words: {mainstream words}\nYour Words: {your words}"
      - 'placeholder3': a concise comparison of common mainstream themes versus the transcript's themes, formatted as:
           "Common themes: {mainstream themes}\nYour themes: {your themes}"
      - 'summary': an in-depth explanation detailing why the track is expected to succeed or fail.
    """
    prompt = (
        f"Evaluate the following track for its potential success in the music market. "
        f"The track has a BPM of {bpm} and the transcript is: {transcription}. "
        "Based on characteristics of successful songs, please provide a JSON response with the following keys: "
        "'success': boolean; "
        "'placeholder1': a one-line factual comparison of BPM, formatted exactly as 'AVG BPM: {avg bpm}, Your BPM: {your bpm}' (under 50 characters); "
        "'placeholder2': a concise comparison of common mainstream words (excluding common articles) versus the transcript's words, "
        "formatted as 'Common Mainstream Words: {mainstream words}\\nYour Words: {your words}'; "
        "'placeholder3': a concise comparison of common mainstream themes versus the transcript's themes, "
        "formatted as 'Common themes: {mainstream themes}\\nYour themes: {your themes}'; "
        "and 'summary': an in-depth explanation of why the track is expected to succeed or fail."
    )
    
    result = ""  # Initialize result to ensure it's defined in case of error
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Replace with your fine-tuned model name if different
            messages=[
                {"role": "system", "content": "You are an expert music market evaluator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        result = response["choices"][0]["message"]["content"]
        print(f"Raw Evaluation Response from OpenAI: {result}")

        # Attempt to extract valid JSON from the result
        start_index = result.find("{")
        end_index = result.rfind("}")
        if start_index == -1 or end_index == -1 or end_index <= start_index:
            raise ValueError("No valid JSON found in the response.")
        json_str = result[start_index:end_index+1]
        evaluation = json.loads(json_str)
        return evaluation
    except Exception as e:
        print(f"Error evaluating track: {e}")
        print("Full raw response was:", result)
        return {"success": False, "placeholder1": "", "placeholder2": "", "placeholder3": "", "summary": "Evaluation failed due to an error."}

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Transcribe the audio and get BPM
    transcription = transcribe_audio(filepath)
    bpm = get_bpm(filepath)

    if transcription is None or bpm is None:
        return jsonify({"message": "Error processing audio file."}), 500

    # Evaluate the track using the fine-tuned OpenAI model
    evaluation = evaluate_track(transcription, bpm)
    
    # Print the evaluation result to the console for debugging
    print("Final Evaluation Output:", evaluation)

    # Return the evaluation along with transcription and BPM
    return jsonify({
        "message": "File uploaded and processed successfully",
        "transcription": transcription,
        "bpm": bpm,
        "evaluation": evaluation
    })

if __name__ == "__main__":
    app.run(debug=True, port=8000)
