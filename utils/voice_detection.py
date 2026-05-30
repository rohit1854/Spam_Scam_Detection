import speech_recognition as sr
import pickle
from pathlib import Path
import os
import subprocess

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "text_model.pkl"


def load_text_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Model load error: {e}")
        return None


def get_ffmpeg_executable():
    """Return a usable ffmpeg executable path, using PATH or imageio-ffmpeg."""
    from shutil import which

    ffmpeg_exe = which("ffmpeg")
    if ffmpeg_exe:
        return ffmpeg_exe

    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def convert_to_wav_ffmpeg(audio_path):
    """Convert audio using ffmpeg command line tool."""
    file_ext = Path(audio_path).suffix.lower()
    if file_ext == ".wav":
        return audio_path

    ffmpeg_exe = get_ffmpeg_executable()
    if ffmpeg_exe is None:
        return None

    wav_path = audio_path.replace(file_ext, ".wav")

    try:
        subprocess.run(
            [ffmpeg_exe, "-i", audio_path, "-acodec", "pcm_s16le", "-ar", "44100", wav_path, "-y"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30,
            check=True,
        )
        if os.path.exists(wav_path):
            return wav_path
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except Exception:
                pass
        print(f"FFmpeg conversion error: {e}")

    return None


def convert_to_wav_pydub(audio_path):
    """Convert audio file to WAV format using pydub."""
    file_ext = Path(audio_path).suffix.lower()
    if file_ext == ".wav":
        return audio_path
    
    try:
        from pydub import AudioSegment
    except ImportError:
        return None

    # Configure pydub to use a bundled ffmpeg binary if available
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        AudioSegment.converter = ffmpeg_exe
    except Exception:
        pass

    try:
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.replace(file_ext, ".wav")
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        print(f"Pydub conversion error: {e}")
        return None


def convert_to_wav(audio_path):
    """Try multiple methods to convert audio to WAV."""
    # Prefer ffmpeg first when available, as it is more reliable and avoids pydub warnings.
    wav_path = convert_to_wav_ffmpeg(audio_path)
    if wav_path and os.path.exists(wav_path):
        return wav_path

    # Try pydub as fallback
    wav_path = convert_to_wav_pydub(audio_path)
    if wav_path and os.path.exists(wav_path):
        return wav_path

    return None


def speech_to_text(audio_path):
    """Convert audio file to text using Google Speech Recognition."""
    if not os.path.exists(audio_path):
        return f"Audio file not found at {audio_path}"
    
    file_size = os.path.getsize(audio_path)
    if file_size == 0:
        return "Audio file is empty (0 bytes)"
    
    # Convert to WAV if necessary
    file_ext = Path(audio_path).suffix.lower()
    if file_ext != ".wav":
        wav_path = convert_to_wav(audio_path)
        if wav_path is None:
            return "Cannot convert audio format. Install pydub and imageio-ffmpeg or ffmpeg for audio conversion support."
        if not os.path.exists(wav_path):
            return f"Failed to create converted WAV file"
        audio_path = wav_path
    
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
    except Exception as e:
        return f"Error reading audio file: {str(e)}"

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio. Try clearer audio or English language."
    except sr.RequestError as e:
        return f"Speech service error: {str(e)}. Check your internet connection."
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def predict_voice_spam(audio_path):
    """Predict if audio content is spam after transcribing."""
    model_data = load_text_model()
    if not model_data:
        return "Text model unavailable", "Error", 0

    model, vectorizer = model_data
    text = speech_to_text(audio_path)
    
    # Check for error messages
    if any(err in text.lower() for err in ["error", "not found", "unavailable", "could not", "cannot", "failed"]):
        return text, "Error", 0

    try:
        vec = vectorizer.transform([text])
        pred = model.predict(vec)[0]
        prob = model.predict_proba(vec)[0][1]
        return text, "🚨 Spam Detected" if pred == 1 else "✅ Safe", int(prob * 100)
    except Exception as e:
        return text, f"Prediction error: {str(e)}", 0


if __name__ == "__main__":
    result = predict_voice_spam("sample.wav")
    print(result)
