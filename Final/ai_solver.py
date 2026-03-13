import streamlit as st
import numpy as np
import pandas as pd
import re
from methods.gauss_seidel import gauss_seidel


def extract_equations(text):

    lines = text.split("\n")

    A = []
    b = []

    for line in lines:

        if "=" in line:

            left, right = line.split("=")

            nums = re.findall(r'[-+]?\d+', left)

            if len(nums) == 3:

                A.append([float(nums[0]), float(nums[1]), float(nums[2])])
                b.append(float(right))

    return np.array(A), np.array(b)


def ai_solver():

    st.header("AI Numerical Solver")

    question = st.text_area("Type your question")

    if st.button("Solve"):

        text = question.lower()

        if "gauss" in text:

            st.success("Detected Gauss Seidel Method")

            A, b = extract_equations(question)

            if len(A) == 3:

                solution, table = gauss_seidel(A, b)

                df = pd.DataFrame(
                    table,
                    columns=["Iteration", "x", "y", "z", "Error"]
                )

                st.subheader("Iteration Table")
                st.dataframe(df)

                solution = [round(float(i), 4) for i in solution]

                st.success(f"Final Solution: {solution}")

            else:

                st.error("Could not detect 3 equations properly")

        else:

            st.warning("Method not detected")