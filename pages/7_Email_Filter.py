import streamlit as st
from utils.ui import load_css, render_navbar
from utils.model_loader import load_pickle_model

st.set_page_config(page_title="Email Filter | Spam And Scan Detection System", page_icon="📧", layout="wide")
load_css()
render_navbar()

st.markdown("""
<div class='hero-card card'>
    <span class='hero-badge'>Email Filter</span>
    <h1 class='hero-title'>Detect spam email content</h1>
    <p class='hero-copy'>Paste the full email body and check whether the classifier marks it as spam.</p>
</div>
""", unsafe_allow_html=True)

model_data = load_pickle_model("models/text_model.pkl")
if not model_data:
    st.error("Text model not found. Ensure models/text_model.pkl exists.")
else:
    model, vectorizer = model_data
    email_text = st.text_area("Paste email content here", height=220)
    if st.button("Analyze Email"):
        if not email_text:
            st.warning("Please paste the email content first.")
        else:
            with st.spinner("Analyzing email content..."):
                try:
                    vec = vectorizer.transform([email_text])
                    pred = model.predict(vec)[0]
                    prob = model.predict_proba(vec)[0][1]
                    score = int(prob * 100)
                    label = "🚨 Spam" if pred == 1 else "✅ Safe"

                    if pred == 1:
                        st.error(label)
                        reason_text = "The email contains spam-like wording or phishing signals."
                        advice = "Do not click unexpected links, verify sender identity, and avoid giving out personal data."
                    else:
                        st.success(label)
                        reason_text = "The email appears safe, but always verify unknown senders before acting."
                        advice = "Keep login details private, report suspicious emails, and confirm requests through a trusted channel."

                    st.markdown(f"""
                        <div class='score-card'>
                            <div class='score-heading'>Email Threat Score</div>
                            <div class='score-bar'><div class='score-fill' style='width: {score}%;'></div></div>
                            <div class='score-value'>{score}%</div>
                        </div>
                        <div class='reason-card'>
                            <h4>Why this result?</h4>
                            <p>{reason_text}</p>
                        </div>
                        <div class='advice-card'>
                            <h4>Precaution</h4>
                            <p>{advice}</p>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Email filter error: {e}")

