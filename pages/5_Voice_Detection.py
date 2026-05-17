import streamlit as st
from utils.ui import load_css, render_navbar
from utils.voice_detection import predict_voice_spam

st.set_page_config(page_title="Voice Detection | Spam And Scan Detection System", page_icon="🎤", layout="wide")
load_css()
render_navbar()

st.markdown("""
<div class='hero-card card'>
    <span class='hero-badge'>Voice Detection</span>
    <h1 class='hero-title'>Scan audio for scam text</h1>
    <p class='hero-copy'>Upload a WAV file and convert speech into text for spam analysis.</p>
</div>
""", unsafe_allow_html=True)

file = st.file_uploader("Upload audio file", type=["wav"])
if file:
    if st.button("Analyze Audio"):
        try:
            with st.spinner("Transcribing audio and analyzing for spam..."):
                with open("temp.wav", "wb") as f:
                    f.write(file.read())
                text, label, score = predict_voice_spam("temp.wav")
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.write("**Transcribed Text:**", text)
                st.write("**Result:**", label)
                st.write("**Threat Score:**", f"{score} %")
                st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Voice detection error: {e}")
