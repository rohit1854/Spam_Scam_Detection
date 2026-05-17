import streamlit as st
from utils.ui import load_css, render_navbar
from utils.model_loader import load_pickle_model

st.set_page_config(page_title="Text Detection | Spam And Scan Detection System", page_icon="📝", layout="wide")
load_css()
render_navbar()

st.markdown("""
<div class='hero-card card'>
    <span class='hero-badge'>Text Detection</span>
    <h1 class='hero-title'>Analyze message spam risk</h1>
    <p class='hero-copy'>Paste text content and get a clear spam prediction plus threat score.</p>
</div>
""", unsafe_allow_html=True)

model_data = load_pickle_model("models/text_model.pkl")
if not model_data:
    st.error("Text model not found. Ensure models/text_model.pkl exists.")
else:
    model, vectorizer = model_data
    text = st.text_area("Enter message here", height=200)
    if st.button("Analyze"):
        if not text:
            st.warning("Enter a message before analyzing.")
        else:
            with st.spinner("Analyzing your message..."):
                try:
                    vec = vectorizer.transform([text])
                    pred = model.predict(vec)[0]
                    prob = model.predict_proba(vec)[0][1]
                    score = int(prob * 100)

                    suspicious_phrases = [
                        "verify your account", "urgent", "click below", "login", "password", "bank", "payment", "transaction", "account", "confirm", "suspend", "limited time", "security alert"
                    ]
                    found = [phrase for phrase in suspicious_phrases if phrase in text.lower()]
                    if pred == 1:
                        st.error("🚨 Spam Detected")
                        reason_text = "Suspicious indicators found in the message."
                        if found:
                            reason_text = f"Suspicious phrases detected: {', '.join(found[:5])}."
                        advice = "Avoid clicking unknown links, do not share personal or login details, and verify the sender before responding."
                    else:
                        st.success("✅ Safe Content")
                        reason_text = "The message appears normal but always stay cautious with unknown senders."
                        advice = "Check the sender address, avoid sharing sensitive information, and confirm unexpected requests separately."

                    st.markdown(f"""
                        <div class='score-card'>
                            <div class='score-heading'>Threat Score</div>
                            <div class='score-bar'><div class='score-fill' style='width: {score}%;'></div></div>
                            <div class='score-value'>{score}%</div>
                        </div>
                        <div class='reason-card'>
                            <h4>Why this result?</h4>
                            <p>{reason_text}</p>
                        </div>
                        <div class='advice-card'>
                            <h4>Safety suggestion</h4>
                            <p>{advice}</p>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Prediction error: {e}")
