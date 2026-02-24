import streamlit as st
from gauss_seidel import gauss_seidel_app
from trapezoidal_rule import trapezoidal_app
from milne_method import milne_app

st.set_page_config(page_title="Numerical Methods Calculator", layout="wide")

st.title("📐 Numerical Methods Calculator")

method = st.sidebar.selectbox(
    "Select Method",
    ["Gauss-Seidel Method", "Trapezoidal Rule", "Milne Predictor-Corrector"]
)

if method == "Gauss-Seidel Method":
    gauss_seidel_app()

elif method == "Trapezoidal Rule":
    trapezoidal_app()

elif method == "Milne Predictor-Corrector":
    milne_app()