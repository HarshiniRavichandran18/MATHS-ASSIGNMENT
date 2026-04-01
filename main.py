import streamlit as st

from methods.gauss_seidel import gauss_seidel_app
from methods.trapezoidal_rule import trapezoidal_app
from methods.milne_method import milne_app
from ai_solver import ai_solver
from image_solver import image_solver

st.set_page_config(
    page_title="Numerical Methods AI Calculator",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Numerical Methods Smart Calculator")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "Gauss Seidel Solver",
        "Trapezoidal Rule",
        "Milne Predictor Corrector",
        "AI Math Solver",
        "Image Question Solver"
    ]
)

if page == "Gauss Seidel Solver":
    gauss_seidel_app()

elif page == "Trapezoidal Rule":
    trapezoidal_app()

elif page == "Milne Predictor Corrector":
    milne_app()

elif page == "AI Math Solver":
    ai_solver()

elif page == "Image Question Solver":
    image_solver()
