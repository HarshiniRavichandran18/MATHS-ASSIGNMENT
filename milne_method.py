import streamlit as st
import sympy as sp
import pandas as pd


def milne_app():

    st.header("Milne's Predictor-Corrector Method")

    st.write("Solve differential equations using Milne’s Predictor-Corrector method.")

    x, y = sp.symbols('x y')

    func_input = st.text_input("Enter dy/dx = f(x,y)", "x + y")

    h = st.number_input("Step Size (h)", value=0.1)

    x_values = st.text_input("Enter x0 x1 x2 x3")
    y_values = st.text_input("Enter y0 y1 y2 y3")

    if st.button("Compute"):

        try:

            f = sp.lambdify((x, y), sp.sympify(func_input), "numpy")

            xs = [float(i) for i in x_values.replace(",", " ").split()]
            ys = [float(i) for i in y_values.replace(",", " ").split()]

            if len(xs) != 4 or len(ys) != 4:
                st.error("Enter exactly 4 values.")
                return

            y_pred = ys[0] + (4*h/3) * (
                2*f(xs[1], ys[1]) - f(xs[2], ys[2]) + 2*f(xs[3], ys[3])
            )

            x4 = xs[3] + h

            y_corr = ys[2] + (h/3) * (
                f(xs[2], ys[2]) + 4*f(xs[3], ys[3]) + f(x4, y_pred)
            )

            table = pd.DataFrame({
                "Step": ["Predicted y4", "Corrected y4"],
                "Value": [round(y_pred,4), round(y_corr,4)]
            })

            st.subheader("Prediction & Correction")
            st.table(table)

        except:
            st.error("Invalid input values.")
