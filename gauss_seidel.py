import streamlit as st
import numpy as np
import pandas as pd

def gauss_seidel_app():

    st.header("Gauss-Seidel Method")

    n = st.number_input("Number of Variables", min_value=2, max_value=5, value=3)

    st.subheader("Enter Coefficient Matrix (Row-wise)")
    A = []
    for i in range(n):
        row = st.text_input(f"Row {i+1} (space separated)", key=f"row_{i}")
        if row:
            A.append(list(map(float, row.split())))

    b_input = st.text_input("Enter Constant Terms (space separated)")
    x0_input = st.text_input("Enter Initial Guess (space separated)")
    tol = st.number_input("Tolerance", value=0.0001, format="%.6f")
    max_iter = st.number_input("Maximum Iterations", value=25)

    if st.button("Solve"):

        try:
            A = np.array(A)
            b = np.array(list(map(float, b_input.split())))
            x = np.array(list(map(float, x0_input.split())))

            iterations = []

            for k in range(int(max_iter)):
                x_new = np.copy(x)

                for i in range(n):
                    s1 = sum(A[i][j] * x_new[j] for j in range(i))
                    s2 = sum(A[i][j] * x[j] for j in range(i+1, n))
                    x_new[i] = (b[i] - s1 - s2) / A[i][i]

                error = np.linalg.norm(x_new - x, ord=np.inf)
                iterations.append([k+1] + list(x_new) + [error])

                if error < tol:
                    break

                x = x_new

            columns = ["Iteration"] + [f"x{i+1}" for i in range(n)] + ["Error"]
            df = pd.DataFrame(iterations, columns=columns)

            st.dataframe(df)
            rounded_solution = [round(val, 4) for val in x_new]
            st.success(f"Final Solution: {rounded_solution}")

        except:
            st.error("Invalid input! Please check your values.")