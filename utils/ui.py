from pathlib import Path
import streamlit as st


def load_css() -> None:
    css_path = Path(__file__).resolve().parent.parent / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def render_navbar() -> None:
    params = st.query_params
    page_param = params.get("page")
    if isinstance(page_param, list):
        current_page = page_param[0] if page_param else ""
    else:
        current_page = page_param or ""

    home_active = "active" if current_page in ("", "1_Home", "Home") else ""
    about_active = "active" if current_page in ("9_About", "About") else ""

    st.markdown(
        f"""
        <nav class='top-nav'>
            <div class='nav-brand'>Spam And Scan Detection System</div>
            <div class='nav-links'>
                <a class='nav-link {home_active}' href='/' target='_self'>Home</a>
                <a class='nav-link {about_active}' href='/?page=About' target='_self'>About</a>
            </div>
        </nav>
        """,
        unsafe_allow_html=True,
    )
