import streamlit as st
import numpy as np
import pandas as pd
import re


# -------------------------------
# Gauss Seidel Algorithm
# -------------------------------
def gauss_seidel(A, b, tol=1e-6, max_iter=50):

    n = len(A)
    x = np.zeros(n)
    table = []

    for k in range(max_iter):

        x_new = np.copy(x)

        for i in range(n):

            s1 = sum(A[i][j] * x_new[j] for j in range(i))
            s2 = sum(A[i][j] * x[j] for j in range(i+1, n))

            x_new[i] = (b[i] - s1 - s2) / A[i][i]

        error = np.linalg.norm(x_new - x)

        row = [k+1] + [round(float(v),4) for v in x_new] + [round(float(error),6)]
        table.append(row)

        if error < tol:
            break

        x = x_new

    return x_new, table


# -------------------------------
# Streamlit App
# -------------------------------
def gauss_seidel_app():

    st.header("Gauss Seidel Method")

    n = st.number_input(
        "Matrix Size (n × n)",
        min_value=2,
        max_value=10,
        value=3,
        step=1
    )

    st.subheader("Enter Matrix A")

    rows = []

    for i in range(n):

        row = st.text_input(
            f"Row {i+1}",
            value=" ".join(["1"]*n)
        )

        rows.append(row)

    b_input = st.text_input(
        "Vector b",
        value=" ".join(["1"]*n)
    )

    if st.button("Solve"):

        try:

            A = []

            for r in rows:

                if r.strip() == "":
                    r = " ".join(["1"] * n)

                values = re.split(r'[ ,]+', r.strip())

                while len(values) < n:
                    values.append("1")

                A.append([float(i) for i in values[:n]])

            if b_input.strip() == "":
                b_input = " ".join(["1"] * n)

            b_values = re.split(r'[ ,]+', b_input.strip())

            while len(b_values) < n:
                b_values.append("1")

            b = [float(i) for i in b_values[:n]]

            A = np.array(A)
            b = np.array(b)

            solution, table = gauss_seidel(A, b)

            columns = ["Iteration"] + [f"x{i+1}" for i in range(n)] + ["Error"]

            df = pd.DataFrame(table, columns=columns)

            st.subheader("Iteration Table")
            st.dataframe(df)

            solution = [round(float(i),4) for i in solution]

            st.success(f"Final Solution: {solution}")

        except Exception as e:

            st.error("Invalid Input Format")
            st.write(e)
