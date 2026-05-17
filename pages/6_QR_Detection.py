import streamlit as st
import numpy as np
from utils.ui import load_css, render_navbar
from utils.model_loader import load_pickle_model

st.set_page_config(page_title="QR Detection | Spam And Scan Detection System", page_icon="🔳", layout="wide")
load_css()
render_navbar()

st.markdown("""
<div class='hero-card card'>
    <span class='hero-badge'>QR Detection</span>
    <h1 class='hero-title'>Scan QR code payloads</h1>
    <p class='hero-copy'>Upload an image containing a QR code and analyze the decoded text for threats.</p>
</div>
""", unsafe_allow_html=True)

file = st.file_uploader("Upload QR code image", type=["jpg", "jpeg", "png"])
if file:
    try:
        import cv2

        with st.spinner("Decoding QR code and checking for threats..."):
            model_data = load_pickle_model("models/link_model.pkl")
            if not model_data:
                st.error("Link model not found. Make sure models/link_model.pkl exists.")
            else:
                model, vectorizer = model_data
                data_bytes = file.read()
                np_arr = np.frombuffer(data_bytes, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                detector = cv2.QRCodeDetector()
                data, _, _ = detector.detectAndDecode(img)

                if not data:
                    st.warning("No QR code detected in the image.")
                else:
                    vec = vectorizer.transform([data])
                    pred = model.predict(vec)[0]
                    st.write("**QR Data:**", data)
                    st.write("**Prediction:**", pred)
    except ImportError:
        st.error("OpenCV is not installed. Install opencv-python to use QR detection.")
    except Exception as e:
        st.error(f"QR detection error: {e}")
