import speech_recognition as sr
import pickle
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "text_model.pkl"


def load_text_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None


def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Unable to understand audio"
    except sr.RequestError:
        return "Speech service unavailable"
    except Exception:
        return "Error in speech recognition"


def predict_voice_spam(audio_path):
    model_data = load_text_model()
    if not model_data:
        return "Text model unavailable", "Unknown", 0

    model, vectorizer = model_data
    text = speech_to_text(audio_path)
    if text.startswith("Unable") or text.startswith("Speech") or text.startswith("Error"):
        return text, "Unknown", 0

    try:
        vec = vectorizer.transform([text])
        pred = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0][1]
        return text, "Spam" if pred == 1 else "Safe", int(prob * 100)
    except Exception:
        return text, "Unknown", 0


if __name__ == "__main__":
    result = predict_voice_spam("sample.wav")
    print(result)
