import streamlit as st
import numpy as np
import pandas as pd
import re


def gauss_seidel(A, b, tol=1e-4, max_iter=50):

    n = len(b)
    x = np.zeros(n)

    table = []

    for k in range(max_iter):

        x_new = x.copy()

        for i in range(n):

            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i+1,n))

            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        error = np.linalg.norm(x_new - x)

        table.append([k+1, x_new[0], x_new[1], x_new[2], error])

        if error < tol:
            return x_new, table

        x = x_new

    return x, table


def gauss_seidel_app():

    st.header("Gauss Seidel Method")

    st.write("Enter coefficients of equations")

    # Default example values added
    a1 = st.text_input("Row 1 of Matrix A", value="10 1 1")
    a2 = st.text_input("Row 2 of Matrix A", value="2 10 1")
    a3 = st.text_input("Row 3 of Matrix A", value="2 2 10")

    b_input = st.text_input("Vector b", value="12 13 14")

    if st.button("Solve"):

        try:

            row1 = [float(i) for i in re.split(r'[ ,]+', a1.strip())]
            row2 = [float(i) for i in re.split(r'[ ,]+', a2.strip())]
            row3 = [float(i) for i in re.split(r'[ ,]+', a3.strip())]

            b = [float(i) for i in re.split(r'[ ,]+', b_input.strip())]

            A = np.array([row1,row2,row3])
            b = np.array(b)

            solution, table = gauss_seidel(A,b)

            df = pd.DataFrame(
                table,
                columns=["Iteration","x","y","z","Error"]
            )

            st.subheader("Iteration Table")
            st.dataframe(df)

            solution = [round(float(i),4) for i in solution]

            st.success(f"Final Solution: {solution}")

        except:

            st.error("Invalid input format")