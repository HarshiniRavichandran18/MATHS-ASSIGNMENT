import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np

def trapezoidal_app():

    st.header("Trapezoidal Rule")

    x = sp.symbols('x')

    func_input = st.text_input("Enter function in x (Example: x**2 + 3*x)")
    a = st.number_input("Lower Limit (a)", value=0.0)
    b = st.number_input("Upper Limit (b)", value=1.0)
    n = st.number_input("Number of Subintervals", min_value=1, value=4)

    if st.button("Compute"):

        try:
            f = sp.lambdify(x, sp.sympify(func_input), "numpy")

            h = (b - a) / n
            result = f(a) + f(b)

            steps = []

            for i in range(1, int(n)):
                xi = a + i * h
                result += 2 * f(xi)
                steps.append([i, xi, f(xi)])

            result = (h / 2) * result

            df = pd.DataFrame(steps, columns=["i", "xi", "f(xi)"])

            st.dataframe(df)
            st.success(f"Approximate Integral = {result:.4f}")
        except:
            st.error("Invalid function input.")