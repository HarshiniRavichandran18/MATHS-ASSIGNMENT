import streamlit as st
import sympy as sp

def milne_app():

    st.header("Milne’s Predictor-Corrector Method")

    x, y = sp.symbols('x y')

    func_input = st.text_input("Enter dy/dx = f(x,y) (Example: x + y)")
    h = st.number_input("Step Size (h)", value=0.1)

    x_values = st.text_input("Enter x0 x1 x2 x3 (space separated)")
    y_values = st.text_input("Enter y0 y1 y2 y3 (space separated)")

    if st.button("Compute"):

        try:
            f = sp.lambdify((x, y), sp.sympify(func_input), "numpy")

            xs = list(map(float, x_values.split()))
            ys = list(map(float, y_values.split()))

            if len(xs) != 4 or len(ys) != 4:
                st.error("Please enter exactly 4 values for x and y.")
            else:
                y_pred = ys[0] + (4*h/3) * (
                    2*f(xs[1], ys[1])
                    - f(xs[2], ys[2])
                    + 2*f(xs[3], ys[3])
                )

                x4 = xs[3] + h

                y_corr = ys[2] + (h/3) * (
                    f(xs[2], ys[2])
                    + 4*f(xs[3], ys[3])
                    + f(x4, y_pred)
                )

                st.success(f"Predicted y4 = {y_pred:.4f}")
                st.success(f"Corrected y4 = {y_corr:.4f}")

        except:
            st.error("Invalid input! Please check your values.")