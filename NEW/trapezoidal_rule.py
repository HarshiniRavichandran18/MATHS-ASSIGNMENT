import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np

def trapezoidal_app():

    st.header("Trapezoidal Rule")

    st.info(
        "Trapezoidal Rule is a numerical integration method used to "
        "approximate definite integrals by dividing the region into "
        "trapezoids and summing their areas."
    )

    x = sp.symbols('x')

    func_input = st.text_input("Enter function f(x)", "x**2")

    a = st.number_input("Lower Limit (a)", value=0.0)
    b = st.number_input("Upper Limit (b)", value=1.0)

    n = st.number_input("Number of Subintervals", min_value=1, value=4)

    if st.button("Compute"):

        try:

            f = sp.lambdify(x, sp.sympify(func_input), "numpy")

            h = (b - a) / n

            xi_values = []
            f_values = []

            result = f(a) + f(b)

            for i in range(1, int(n)):

                xi = a + i * h
                fx = f(xi)

                xi_values.append(xi)
                f_values.append(fx)

                result += 2 * fx

            integral = (h / 2) * result

            table = pd.DataFrame({
                "i": range(1, int(n)),
                "xi": np.round(xi_values,6),
                "f(xi)": np.round(f_values,6)
            })

            st.subheader("Calculation Table")
            st.dataframe(table)

            st.success(f"Approximate Integral = {integral:.6f}")

        except:
            st.error("Invalid function input.")