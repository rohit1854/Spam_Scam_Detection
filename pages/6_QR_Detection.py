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
        try:
            import cv2
        except ImportError:
            st.error("OpenCV is not installed. Install opencv-python to use QR detection.")
            st.info("Install with: `pip install opencv-python` in the Python environment running Streamlit, then restart Streamlit.")
            raise

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

                # Primary detection attempt
                data, points, _ = detector.detectAndDecode(img)

                # Try multi-decoding if single decode failed
                if not data:
                    try:
                        ok, decoded_info, points, _ = detector.detectAndDecodeMulti(img)
                        if ok and decoded_info:
                            # decoded_info can be a list of strings
                            first = decoded_info[0]
                            data = first if first else None
                    except Exception:
                        pass

                # Try simple preprocessing (grayscale + Otsu threshold) if still not found
                if not data:
                    try:
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        data, points, _ = detector.detectAndDecode(th)
                    except Exception:
                        pass

                # Fallback to pyzbar if available (often more tolerant)
                if not data:
                    try:
                        from pyzbar.pyzbar import decode
                        decoded = decode(img)
                        if decoded:
                            data = decoded[0].data.decode('utf-8')
                    except ImportError:
                        # pyzbar not installed — provide guidance but don't fail
                        st.info("For additional QR decoding tolerance you can install `pyzbar` (requires the zbar library).")
                    except Exception:
                        pass

                if not data:
                    st.warning("No QR code detected in the image. Try a clearer image or crop tightly around the QR code.")
                else:
                    vec = vectorizer.transform([data])
                    pred = model.predict(vec)[0]

                    # Map numeric prediction to human-readable label and advice
                    label_map = {
                        0: "benign",
                        1: "defacement",
                        2: "phishing",
                        3: "malware",
                    }

                    label = label_map.get(pred, "unknown")

                    if pred == 0:
                        advice = "This QR payload appears benign. Still verify the destination before sharing or clicking."
                        reason_text = "No strong indicators of phishing or malware were detected in the decoded payload."
                    elif pred == 1:
                        advice = "Defacement-like payloads may indicate tampering. Avoid following the link and report it."
                        reason_text = "The decoded payload resembles defacement or altered content patterns."
                    elif pred == 2:
                        advice = "Likely phishing: do not follow the link or provide credentials. Treat it as suspicious."
                        reason_text = "Decoded content shows characteristics common to phishing attempts."
                    elif pred == 3:
                        advice = "May host malware: do not download anything or follow instructions from the linked site."
                        reason_text = "Decoded content resembles known malware-distribution patterns."
                    else:
                        advice = "Exercise caution with unknown payloads. Inspect manually before interacting."
                        reason_text = "The model could not determine a clear label for this payload."

                    st.write("**QR Data:**", data)
                    st.success(f"Prediction: {label} ({pred})")
                    st.markdown(f"""
                        <div class='reason-card'>
                            <h4>Why this result?</h4>
                            <p>{reason_text}</p>
                        </div>
                        <div class='advice-card'>
                            <h4>Precaution</h4>
                            <p>{advice}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    st.info("Label mapping: benign=0, defacement=1, phishing=2, malware=3")
    except Exception as e:
        msg = str(e)
        # Common binary import error with mismatched numpy/opencv
        if "numpy.core.multiarray" in msg or "multiarray failed to import" in msg:
            st.error("QR detection error: numpy C-extension import failed (binary mismatch).")
            st.info("This commonly happens when OpenCV was built against a different NumPy ABI. Fix by installing a compatible NumPy and OpenCV in the same environment and restarting Streamlit:")
            st.code("pip install --upgrade pip\n# install a NumPy version compatible with your OpenCV wheel\npip install --upgrade numpy==1.26.4\npip install --upgrade opencv-python\n# then restart Streamlit\nstreamlit run app.py", language='bash')
        else:
            st.error(f"QR detection error: {msg}")
