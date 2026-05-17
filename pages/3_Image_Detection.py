import streamlit as st
import numpy as np
from utils.ui import load_css, render_navbar

st.set_page_config(page_title="Image Detection | Spam And Scan Detection System", page_icon="🖼️", layout="wide")
load_css()
render_navbar()

st.markdown("""
<div class='hero-card card'>
    <span class='hero-badge'>Image Detection</span>
    <h1 class='hero-title'>Upload an image to scan</h1>
    <p class='hero-copy'>The image model checks for visual spam signals in uploaded screenshots or photos.</p>
</div>
""", unsafe_allow_html=True)

file = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
if file:
    try:
        with st.spinner("Scanning the image for scam patterns..."):
            from tensorflow.keras.models import load_model
            from tensorflow.keras.preprocessing import image as keras_image

            model = load_model("models/image_model.h5")
            img = keras_image.load_img(file, target_size=(224, 224))
            arr = keras_image.img_to_array(img) / 255.0
            arr = np.expand_dims(arr, axis=0)

            pred = model.predict(arr)[0][0]
            label = "🚨 Spam" if pred > 0.5 else "✅ Safe"

            st.image(file, caption="Uploaded image", use_column_width=True)
            st.success(label)
            st.write(f"Confidence: {pred:.2f}")
    except ImportError:
        st.error("TensorFlow is not installed. Install tensorflow-cpu to use image detection.")
    except Exception as e:
        st.error(f"Image error: {e}")
