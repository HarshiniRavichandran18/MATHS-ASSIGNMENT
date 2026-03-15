import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


# -------------------------
# Trapezoidal Rule
# -------------------------
def trapezoidal_single(f, a, b, n):

    h = (b-a)/n
    x_vals = np.linspace(a,b,n+1)
    y_vals = f(x_vals)

    result = h*((y_vals[0]+y_vals[-1])/2 + np.sum(y_vals[1:-1]))

    return result, x_vals, y_vals, h


# -------------------------
# Plot Trapezoids
# -------------------------
def plot_trapezoids(f,a,b,n,x_vals,y_vals):

    x_curve = np.linspace(a,b,200)
    y_curve = f(x_curve)

    fig, ax = plt.subplots()

    ax.plot(x_curve,y_curve,label="f(x)")
    ax.scatter(x_vals,y_vals)

    for i in range(n):

        xs = [x_vals[i],x_vals[i],x_vals[i+1],x_vals[i+1]]
        ys = [0,y_vals[i],y_vals[i+1],0]

        ax.fill(xs,ys,alpha=0.3)

    ax.set_title("Trapezoidal Approximation")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()

    return fig


# -------------------------
# Streamlit App
# -------------------------
def trapezoidal_app():

    st.header("Trapezoidal Rule Solver")

    func = st.text_input(
        "Enter function f(x)",
        "x^2"
    )

    a = st.number_input("Lower Limit (a)", value=0.0)
    b = st.number_input("Upper Limit (b)", value=2.0)

    n = st.number_input(
        "Number of Intervals",
        min_value=1,
        value=4
    )

    if st.button("Calculate"):

        try:

            # Fix user function
            func = func.replace("^","**")
            func = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', func)

            x = sp.symbols('x')

            f = sp.lambdify(x, sp.sympify(func),'numpy')

            result, x_vals, y_vals, h = trapezoidal_single(f,a,b,n)

            # Step table
            table = []

            for i in range(len(x_vals)):

                weight = 1

                if i!=0 and i!=len(x_vals)-1:
                    weight = 2

                table.append([
                    i,
                    round(x_vals[i],4),
                    round(y_vals[i],4),
                    weight
                ])

            df = pd.DataFrame(
                table,
                columns=["i","xᵢ","f(xᵢ)","Weight"]
            )

            st.subheader("Step Table")
            st.dataframe(df)

            st.write(f"Step size h = {round(h,4)}")

            st.success(
                f"Approximate Integral = {round(result,4)}"
            )

            # Graph
            st.subheader("Trapezoidal Graph")

            fig = plot_trapezoids(f,a,b,n,x_vals,y_vals)

            st.pyplot(fig)

        except Exception as e:

            st.error("Invalid function format")
            st.write(e)
