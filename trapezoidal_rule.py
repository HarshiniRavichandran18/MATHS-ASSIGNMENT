import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np


def trapezoidal_app():

    st.header("Trapezoidal Rule")

    st.write("Approximate definite integral using the Trapezoidal Rule.")

    x = sp.symbols('x')

    func_input = st.text_input("Enter function f(x)", "x**2 + 3*x")

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
                fxi = f(xi)

                result += 2 * fxi

                steps.append([i, round(xi, 4), round(fxi, 4)])

            result = (h / 2) * result

            df = pd.DataFrame(steps, columns=["i", "xi", "f(xi)"])

            st.subheader("Calculation Table")
            st.dataframe(df)

            st.info(f"Step Size (h) = {round(h,4)}")

            st.success(f"Approximate Integral = {round(result,4)}")

        except:
            st.error("Invalid function input.")
