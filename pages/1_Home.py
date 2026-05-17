import matplotlib.pyplot as plt
import streamlit as st
from utils.ui import load_css, render_navbar

st.set_page_config(page_title="Home | Spam And Scan Detection System", page_icon="🏠", layout="wide")
load_css()
render_navbar()

st.markdown(
    """
    <div class='page-hero'>
        <div>
            <span class='hero-badge'>Spam And Scan Detection System</span>
            <h1 class='hero-title'>Defend every channel with intelligent scam protection.</h1>
            <p class='hero-copy'>OmniShield AI brings text, image, voice, link, QR, email, and credit scanning into one polished security dashboard.</p>
            <p class='hero-copy'>Scan suspicious content instantly, review clear threat insights, and stay one step ahead of fraud.</p>
        </div>
        <div class='hero-card card'>
            <h4>Why OmniShield?</h4>
            <ul>
                <li>One dashboard for 7 detection tools</li>
                <li>Fast safe/spam verdicts and threat scoring</li>
                <li>Modern, content-first interface for security review</li>
            </ul>
            <img class='hero-image' src='data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%232563eb"/><stop offset="1" stop-color="%23a855f7"/></linearGradient></defs><path d="M60 12 L22 32 V68 C22 94 40 108 60 114 C80 108 98 94 98 68 V32 Z" fill="url(%23g)" stroke="%23fff" stroke-width="5" opacity="0.98"/><path d="M44 60 L54 74 L76 44" fill="none" stroke="%23fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>' alt='Shield graphic' />
        </div>
    </div>
    <div class='page-subtitle'>How the platform works</div>
    <div class='grid-3'>
        <div class='section-card card'>
            <h4>Collect</h4>
            <p>Submit text, images, voice, links, QR codes, email content, or credit inputs for rapid analysis.</p>
        </div>
        <div class='section-card card'>
            <h4>Detect</h4>
            <p>Machine learning and rule-based checks identify scam patterns, phishing language, and suspicious metadata.</p>
        </div>
        <div class='section-card card'>
            <h4>Explain</h4>
            <p>Receive transparent results with a clear threat score, safe/spam verdict, and short explanation for each finding.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

feature_labels = ["Text", "Image", "Voice", "Link", "QR", "Email", "Credit"]
feature_sizes = [20, 15, 15, 20, 10, 10, 10]
feature_colors = ["#60a5fa", "#818cf8", "#38bdf8", "#2563eb", "#7c3aed", "#38bdf8", "#22c55e"]
fig, ax = plt.subplots(figsize=(5, 5), facecolor="#020613")
fig.patch.set_facecolor("#020613")
ax.set_facecolor("#020613")
wedges, texts, autotexts = ax.pie(
    feature_sizes,
    labels=feature_labels,
    autopct="%1.0f%%",
    startangle=140,
    colors=feature_colors,
    textprops={"color": "#f8fafc", "weight": "bold", "fontsize": 10},
    wedgeprops={"edgecolor": "#0f172a", "linewidth": 1.5},
)
ax.set_title("Threat coverage by detector", color="#93c5fd", fontsize=16, pad=20)
for text in texts + autotexts:
    text.set_color("#f8fafc")
ax.axis("equal")

st.markdown("<div class='page-subtitle'>Project coverage</div>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.pyplot(fig, transparent=True)
with col2:
    st.markdown(
        """
        <div class='hero-card chart-card card'>
            <h4>Coverage snapshot</h4>
            <p>Each slice represents a detector module in the system.</p>
            <ul>
                <li><strong>Text</strong>: spam and phishing phrase detection.</li>
                <li><strong>Link</strong>: URL safety and phishing checks.</li>
                <li><strong>Voice</strong>: scam audio analysis.</li>
                <li><strong>Image</strong>: suspicious visual content screening.</li>
                <li><strong>Email</strong>: phishing and spam filtering.</li>
                <li><strong>QR</strong>: redirect and safety validation.</li>
                <li><strong>Credit</strong>: fraud risk score analysis.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class='page-subtitle'>Explore feature workflows</div>
    <div class='grid-3'>
        <div class='feature-card card'>
            <h4>Text Detection</h4>
            <p>Scan messages for scam keywords, suspicious phrasing, and hidden fraud signals.</p>
            <a class='link-button' href='/?page=Text%20Detection' target='_self'>Open Text Detection</a>
        </div>
        <div class='feature-card card'>
            <h4>Image Detection</h4>
            <p>Check images for forged content, spam visuals, and misleading graphics.</p>
            <a class='link-button' href='/?page=Image%20Detection' target='_self'>Open Image Detection</a>
        </div>
        <div class='feature-card card'>
            <h4>Link Detection</h4>
            <p>Analyze URLs for phishing, malicious redirects, and hidden threats.</p>
            <a class='link-button' href='/?page=Link%20Detection' target='_self'>Open Link Detection</a>
        </div>
    </div>
    <div class='grid-2' style='margin-top:24px;'>
        <div class='feature-card card'>
            <h4>Voice Detection</h4>
            <p>Convert spoken audio into text and screen voice notes for scam language.</p>
            <a class='link-button' href='/?page=Voice%20Detection' target='_self'>Open Voice Detection</a>
        </div>
        <div class='feature-card card'>
            <h4>QR Detection</h4>
            <p>Inspect QR codes for suspicious redirects and unsafe payloads.</p>
            <a class='link-button' href='/?page=QR%20Detection' target='_self'>Open QR Detection</a>
        </div>
    </div>
    <div class='grid-2' style='margin-top:24px;'>
        <div class='feature-card card'>
            <h4>Email Filter</h4>
            <p>Evaluate emails for phishing, spoofing, and spam risk before trusting the sender.</p>
            <a class='link-button' href='/?page=Email%20Filter' target='_self'>Open Email Filter</a>
        </div>
        <div class='feature-card card'>
            <h4>Credit Detection</h4>
            <p>Detect credit application fraud, unusual financial patterns, and suspicious scoring signals.</p>
            <a class='link-button' href='/?page=Credit%20Detection' target='_self'>Open Credit Detection</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
