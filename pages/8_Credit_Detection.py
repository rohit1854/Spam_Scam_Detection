import streamlit as st
from utils.ui import load_css, render_navbar
from utils.model_loader import load_pickle_model
import pandas as pd
import numpy as np

st.set_page_config(page_title="Credit Detection | Spam And Scan Detection System", page_icon="💳", layout="wide")
load_css()
render_navbar()

st.markdown("""
<div class='hero-card card'>
    <span class='hero-badge'>Credit Detection</span>
    <h1 class='hero-title'>Detect credit fraud risk</h1>
    <p class='hero-copy'>Enter sample numeric values and let the model predict if the input is suspicious.</p>
</div>
""", unsafe_allow_html=True)

model_data = load_pickle_model("models/credit_model.pkl")
if not model_data:
    st.error("Credit model not found. Ensure models/credit_model.pkl exists.")
else:
    # Support either (model, columns) or plain model objects saved in the pickle.
    if isinstance(model_data, tuple):
        # Accept tuples of length >=2 where first element is model and second is columns
        if len(model_data) >= 2:
            model, columns = model_data[0], model_data[1]
        else:
            model = model_data[0]
            columns = None
    else:
        model = model_data
        # common sklearn attribute when training from DataFrame
        columns = getattr(model, "feature_names_in_", None)

    # If columns is a numpy array, convert to list
    if isinstance(columns, np.ndarray):
        try:
            columns = columns.tolist()
        except Exception:
            columns = None

    # If columns still None, try to infer number of input features from model attributes
    n_features = getattr(model, "n_features_in_", None)
    if columns is None:
        if n_features is None and hasattr(model, "coef_"):
            coef = getattr(model, "coef_")
            try:
                # coef_ may be 1D or 2D depending on estimator
                if coef.ndim == 1:
                    n_features = coef.shape[0]
                else:
                    n_features = coef.shape[1]
            except Exception:
                n_features = None

        if n_features is not None and isinstance(n_features, int) and n_features > 0:
            columns = [f"feature_{i+1}" for i in range(n_features)]
        else:
            # Fallback to a small set of placeholder features
            columns = [f"feature_{i+1}" for i in range(5)]

    # Ensure columns is a list
    if not isinstance(columns, (list, tuple)):
        try:
            columns = list(columns)
        except Exception:
            columns = [f"feature_{i+1}" for i in range(5)]

    # Extend missing feature columns to satisfy model input size
    if n_features is None:
        n_features = getattr(model, "n_features_in_", None)
        if n_features is None and hasattr(model, "coef_"):
            coef = getattr(model, "coef_")
            try:
                if coef.ndim == 1:
                    n_features = coef.shape[0]
                else:
                    n_features = coef.shape[1]
            except Exception:
                n_features = None

    if n_features is not None and isinstance(n_features, int) and n_features > len(columns):
        extra_columns = [f"feature_{i+1}" for i in range(len(columns), n_features)]
        columns = list(columns) + extra_columns

    if len(columns) == 0:
        st.error("Credit model columns are invalid or unavailable.")
    else:
        st.write("Enter sample values for the first five features:")
        inputs = {}
        for col in columns[:5]:
            inputs[col] = st.number_input(col, value=0.0)

        if st.button("Predict Fraud"):
            with st.spinner("Evaluating credit fraud risk..."):
                try:
                    df = pd.DataFrame([inputs])
                    df = df.reindex(columns=columns, fill_value=0)
                    pred = model.predict(df)[0]
                    if pred == 1:
                        st.error("🚨 Fraud detected")
                    else:
                        st.success("✅ Legitimate application")
                except Exception as e:
                    st.error(f"Credit prediction error: {e}")
