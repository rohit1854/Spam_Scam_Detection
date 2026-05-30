import base64
import streamlit as st
from utils.ui import load_css, render_navbar
from utils.voice_detection import predict_voice_spam
import os

st.set_page_config(page_title="Voice Detection | Spam And Scan Detection System", page_icon="🎤", layout="wide")
load_css()
render_navbar()

st.markdown("""
<div class='hero-card card'>
    <span class='hero-badge'>Voice Detection</span>
    <h1 class='hero-title'>Scan audio for scam text</h1>
    <p class='hero-copy'>Upload an audio file and we'll transcribe it and check for spam content.</p>
</div>
""", unsafe_allow_html=True)

accepted_audio = ["wav", "mp3", "m4a", "ogg", "flac", "aac"]

st.markdown(
    """
    <div class='audio-input-label'>
        <span>🎙️</span>
        <div>Upload your audio file</div>
    </div>
    <div class='audio-input-note'>Supported formats: wav, mp3, m4a, ogg, flac, aac</div>
    """,
    unsafe_allow_html=True,
)

st.info("⚠️ Note: Audio transcription uses Google Speech Recognition, which requires an internet connection and works best with clear audio in English.")

file = st.file_uploader("Choose an audio file", type=accepted_audio, accept_multiple_files=False)

if file:
    st.markdown("**Uploaded file:** " + file.name)
    st.audio(file, format=f"audio/{file.name.split('.')[-1]}")
    
    if st.button("Analyze Audio", type="primary"):
        try:
            # Save uploaded file using original extension so conversion can run correctly
            original_ext = os.path.splitext(file.name)[1] or ".wav"
            temp_path = f"temp_voice{original_ext}"
            with open(temp_path, "wb") as f:
                f.write(file.read())
            
            st.write("✅ Audio file saved")
            
            # Check if file exists
            if not os.path.exists(temp_path):
                st.error("❌ Failed to save audio file")
            else:
                file_size = os.path.getsize(temp_path)
                st.write(f"✅ File size: {file_size} bytes")
            
            with st.spinner("🔄 Transcribing audio... (this may take 10-30 seconds)"):
                text, label, score = predict_voice_spam(temp_path)
            
            st.subheader("📝 Transcribed Text:")
            st.write(text)
            
            st.subheader("🔍 Analysis Result:")
            if "error" in label.lower():
                st.error(f"⚠️ {label}")
            elif "spam" in label.lower():
                st.error(f"🚨 {label}")
            else:
                st.success(f"✅ {label}")
            
            st.subheader("📊 Threat Score:")
            st.progress(min(score / 100, 1.0))
            st.metric("Threat Level", f"{score}%")
            
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
            converted_wav = os.path.splitext(temp_path)[0] + ".wav"
            if converted_wav != temp_path and os.path.exists(converted_wav):
                os.remove(converted_wav)
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
else:
    st.info("Upload an audio file to get started")
