import streamlit as st
from utils.ui import load_css, render_navbar

st.set_page_config(page_title="About | Spam And Scan Detection System", page_icon="ℹ️", layout="wide")
load_css()
render_navbar()

st.markdown(
    """
    <div class='page-hero'>
        <div>
            <span class='hero-badge'>About</span>
            <h1 class='hero-title'>Meet Spam And Scam Detection System</h1>
            <p class='hero-copy'>A modern threat detection platform built to identify spam, scams, and risky content across text, voice, images, links, QR codes, emails, and financial data.</p>
            <p class='hero-copy'>Designed for clarity, speed, and hands-on security exploration, OmniShield AI helps users spot suspicious content with confidence.</p>
        </div>
        <div class='hero-card card'>
            <h4>What makes it special?</h4>
            <ul>
                <li>Multi-modal scanning that supports 7 content types</li>
                <li>Easy-to-understand results with threat scoring</li>
                <li>Clean interface built for fast threat review</li>
            </ul>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class='grid-3'>
        <div class='section-card card'>
            <h4>Mission</h4>
            <p>To make scam detection intuitive and accessible, so anyone can evaluate risky content quickly.</p>
        </div>
        <div class='section-card card'>
            <h4>Approach</h4>
            <p>Combine machine learning, rule-based filters, and visual scoring into one easy-to-use dashboard.</p>
        </div>
        <div class='section-card card'>
            <h4>Impact</h4>
            <p>Empower users to recognize phishing, fraudulent links, and suspicious messages before they cause harm.</p>
        </div>
    </div>
    <div class='grid-3' style='margin-top:24px;'>
        <div class='feature-card card'>
            <h4>Advanced detection tools</h4>
            <ul>
                <li>Text analyzer finds spammy language and phishing intent.</li>
                <li>Image scanner flags manipulated or fraudulent visuals.</li>
                <li>Voice model converts audio and checks for scammy wording.</li>
            </ul>
        </div>
        <div class='feature-card card'>
            <h4>Secure content review</h4>
            <ul>
                <li>Link detection reveals hidden threats in URLs.</li>
                <li>QR scanning exposes unsafe redirects fast.</li>
                <li>Email filtering highlights phishing and suspicious sender text.</li>
            </ul>
        </div>
        <div class='feature-card card'>
            <h4>Insight-driven design</h4>
            <ul>
                <li>Easy scoring and clear safe/spam feedback.</li>
                <li>Fast access to every tool from the home dashboard.</li>
                <li>Built for demos, learning, and real-time detection practice.</li>
            </ul>
        </div>
    </div>
    <div class='grid-3' style='margin-top:24px;'>
        <div class='feature-card card'>
            <h4>Team</h4>
            <ul class='team-list'>
                <li>Rohit Chakraverty</li>
                <li>Ritu Priya</li>
                <li>Prabhat Kumar</li>
                <li>Rashmi Pacheriya</li>
            </ul>
            <p class='status-chip'>Mentor: Dr. Priti Kumari</p>
        </div>
        <div class='feature-card card'>
            <h4>Design goals</h4>
            <p>Clarity, speed, and thoughtful interface design that keeps security analysis approachable.</p>
        </div>
        <div class='feature-card card'>
            <h4>Future-ready</h4>
            <p>Ready to extend with new detectors, improved scoring, and richer evidence displays.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
