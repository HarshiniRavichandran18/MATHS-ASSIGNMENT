import streamlit as st
import numpy as np
import pandas as pd


def gauss_seidel_app():

    st.header("Gauss-Seidel Method")

    st.write("Solve a system of linear equations using the iterative Gauss-Seidel method.")

    n = st.number_input("Number of Variables", min_value=2, max_value=5, value=3)

    st.caption("Enter coefficients separated by space or comma")

    A = []
    for i in range(n):
        row = st.text_input(f"Row {i+1}", key=f"row_{i}")
        if row:
            A.append([float(x) for x in row.replace(",", " ").split()])

    b_input = st.text_input("Constant Terms (b)")
    x0_input = st.text_input("Initial Guess")

    tol = st.number_input("Tolerance", value=0.0001, format="%.6f")
    max_iter = st.number_input("Maximum Iterations", value=25)

    if st.button("Solve"):

        try:

            A = np.array(A)
            b = np.array([float(i) for i in b_input.replace(",", " ").split()])
            x = np.array([float(i) for i in x0_input.replace(",", " ").split()])

            iterations = []

            for k in range(int(max_iter)):

                x_new = np.copy(x)

                for i in range(n):

                    s1 = sum(A[i][j] * x_new[j] for j in range(i))
                    s2 = sum(A[i][j] * x[j] for j in range(i + 1, n))

                    x_new[i] = (b[i] - s1 - s2) / A[i][i]

                error = np.linalg.norm(x_new - x, ord=np.inf)

                iterations.append(
                    [k + 1] + [round(val, 4) for val in x_new] + [round(error, 6)]
                )

                x = x_new

                if error < tol:
                    break

            columns = ["Iteration"] + [f"x{i+1}" for i in range(n)] + ["Error"]

            df = pd.DataFrame(iterations, columns=columns)

            st.subheader("Iteration Table")
            st.dataframe(df)

            solution = [round(val, 4) for val in x_new]

            st.success(f"Final Solution: {solution}")

        except:
            st.error("Invalid input. Please check matrix and values.")
