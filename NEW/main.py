import streamlit as st
from gauss_seidel import gauss_seidel_app
from trapezoidal_rule import trapezoidal_app
from milne_method import milne_app
from ai_solver import ai_solver
from image_solver import image_solver

st.set_page_config(page_title="AI Numerical Methods Solver", layout="wide")

st.title("🧠 AI Numerical Methods Calculator")

menu = st.sidebar.selectbox(
    "Choose Module",
    [
        "AI Question Solver",
        "Solve from Image",
        "Gauss-Seidel Method",
        "Trapezoidal Rule",
        "Milne Predictor-Corrector"
    ]
)

if menu == "AI Question Solver":
    ai_solver()

elif menu == "Solve from Image":
    image_solver()

elif menu == "Gauss-Seidel Method":
    gauss_seidel_app()

elif menu == "Trapezoidal Rule":
    trapezoidal_app()

elif menu == "Milne Predictor-Corrector":
    milne_app()