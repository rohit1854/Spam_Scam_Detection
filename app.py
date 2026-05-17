import runpy
from pathlib import Path

import streamlit as st
from utils.ui import load_css, render_navbar

params = st.query_params
page_param = params.get("page")
if isinstance(page_param, list):
    current_page = page_param[0] if page_param else ""
else:
    current_page = page_param or ""

page_routes = {
    "Text Detection": "pages/2_Text_Detection.py",
    "Image Detection": "pages/3_Image_Detection.py",
    "Voice Detection": "pages/5_Voice_Detection.py",
    "Link Detection": "pages/4_Link_Detection.py",
    "QR Detection": "pages/6_QR_Detection.py",
    "Email Filter": "pages/7_Email_Filter.py",
    "Credit Detection": "pages/8_Credit_Detection.py",
    "About": "pages/9_About.py",
}

if current_page in page_routes:
    target_file = Path(__file__).resolve().parent / page_routes[current_page]
    if target_file.exists():
        with st.spinner("Loading page..."):
            runpy.run_path(str(target_file), run_name="__main__")
    else:
        st.error(f"Page not found: {target_file}")
    st.stop()

st.set_page_config(page_title="Spam And Scan Detection System", page_icon="🛡️", layout="wide")
load_css()
render_navbar()

st.markdown(
    """
    <div class='page-hero'>
        <div>
            <span class='hero-badge'>Spam And Scan Detection System</span>
            <h1 class='hero-title'>Detect spam, scams, and threats across every format</h1>
            <p class='hero-copy'>Use the top navigation for Home and About, with all detection tools accessible from the Home page feature cards.</p>
        </div>
        <div class='hero-card card'>
            <h4>All-in-one security dashboard</h4>
            <p>One page for every detection tool, with direct navigation links to all model workflows and threat scans.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class='grid-3'>
        <div class='feature-card card'>
            <h4>Text Detection</h4>
            <p>Analyze messages for spam and scam content.</p>
            <a class='link-button' href='/?page=Text%20Detection' target='_self'>Open Text Detection</a>
        </div>
        <div class='feature-card card'>
            <h4>Image Detection</h4>
            <p>Scan images for fraudulent or malicious content.</p>
            <a class='link-button' href='/?page=Image%20Detection' target='_self'>Open Image Detection</a>
        </div>
        <div class='feature-card card'>
            <h4>Voice Detection</h4>
            <p>Convert voice notes to text and classify scam audio.</p>
            <a class='link-button' href='/?page=Voice%20Detection' target='_self'>Open Voice Detection</a>
        </div>
        <div class='feature-card card'>
            <h4>Link Detection</h4>
            <p>Identify phishing, malware, and suspicious URLs.</p>
            <a class='link-button' href='/?page=Link%20Detection' target='_self'>Open Link Detection</a>
        </div>
        <div class='feature-card card'>
            <h4>QR Detection</h4>
            <p>Inspect QR codes for scams and dangerous redirects.</p>
            <a class='link-button' href='/?page=QR%20Detection' target='_self'>Open QR Detection</a>
        </div>
        <div class='feature-card card'>
            <h4>Email Filter</h4>
            <p>Evaluate email content for phishing and spam risk.</p>
            <a class='link-button' href='/?page=Email%20Filter' target='_self'>Open Email Filter</a>
        </div>
    </div>
    <div class='grid-2' style='margin-top:24px;'>
        <div class='feature-card card'>
            <h4>Credit Detection</h4>
            <p>Assess credit-related scam risk using the built-in scoring model.</p>
            <a class='link-button' href='/?page=Credit%20Detection' target='_self'>Open Credit Detection</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
