import streamlit as st
from utils.ui import load_css, render_navbar
from utils.model_loader import load_pickle_model

st.set_page_config(page_title="Link Detection | Spam And Scan Detection System", page_icon="🔗", layout="wide")
load_css()
render_navbar()

st.markdown("""
<div class='hero-card card'>
    <span class='hero-badge'>Link Detection</span>
    <h1 class='hero-title'>Scan suspicious URLs</h1>
    <p class='hero-copy'>Paste a link to check if it is likely to be phishing or scam content.</p>
</div>
""", unsafe_allow_html=True)

model_data = load_pickle_model("models/link_model.pkl")
if not model_data:
    st.error("Link model not found. Make sure models/link_model.pkl exists.")
else:
    model, vectorizer = model_data
    label_map = {
        0: "benign",
        1: "defacement",
        2: "phishing",
        3: "malware",
    }

    url = st.text_input("Enter URL to scan")
    if st.button("Scan"):
        if not url:
            st.warning("Please enter a URL.")
        else:
            with st.spinner("Scanning the link..."):
                try:
                    vec = vectorizer.transform([url])
                    pred = model.predict(vec)[0]
                    label = label_map.get(pred, "unknown")
                    label_text = f"Prediction: {label} ({pred})"

                    if pred == 0:
                        advice = "This URL appears benign, but only open links from trusted sources."
                        reason_text = "No strong phishing or malware indicators were detected."
                    elif pred == 1:
                        advice = "Defacement content may be unsafe. Avoid accessing this site and report it if needed."
                        reason_text = "The URL resembles defacement or tampering patterns."
                    elif pred == 2:
                        advice = "Do not visit this link. It may be a phishing attempt designed to steal credentials."
                        reason_text = "This URL shows characteristics typical of phishing scams."
                    elif pred == 3:
                        advice = "This site may host malware. Do not download files or enter information."
                        reason_text = "The URL appears similar to known malware delivery patterns."
                    else:
                        advice = "Exercise caution with unknown or suspicious links."
                        reason_text = "The model could not identify a clear label."

                    st.success(label_text)
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
                    st.error(f"Link prediction error: {e}")

