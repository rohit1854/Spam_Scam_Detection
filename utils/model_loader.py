import pickle
import streamlit as st

@st.cache_resource
def load_pickle_model(path):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error(f"❌ File not found: {path}")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None