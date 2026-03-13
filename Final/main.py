import streamlit as st
from methods.gauss_seidel import gauss_seidel_app
from methods.trapezoidal_rule import trapezoidal_app
from methods.milne_method import milne_app
from ai_solver import ai_solver
from image_solver import image_solver

st.title("AI Numerical Methods Solver")

menu = st.sidebar.selectbox(
    "Choose Method",
    [
        "Gauss Seidel",
        "Trapezoidal Rule",
        "Milne Method",
        "AI Text Solver",
        "Image Solver"
    ]
)

if menu == "Gauss Seidel":
    gauss_seidel_app()

elif menu == "Trapezoidal Rule":
    trapezoidal_app()

elif menu == "Milne Method":
    milne_app()

elif menu == "AI Text Solver":
    ai_solver()

elif menu == "Image Solver":
    image_solver()