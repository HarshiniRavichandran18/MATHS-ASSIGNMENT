import streamlit as st
import easyocr
import numpy as np
import pandas as pd
import re
from methods.gauss_seidel import gauss_seidel


# Fix common OCR mistakes
def clean_text(text):

    text = text.replace("IO", "10")
    text = text.replace("lo", "10")
    text = text.replace("O", "0")
    text = text.replace("z", "2")

    return text


# Extract numbers and build matrix
def build_matrix(text):

    nums = re.findall(r'\d+', text)
    nums = [float(i) for i in nums]

    if len(nums) >= 9:

        A = np.array([
            [nums[0],1,1],
            [nums[2],nums[3],1],
            [nums[5],nums[6],nums[7]]
        ])

        b = np.array([
            nums[1],
            nums[4],
            nums[8]
        ])

        return A,b

    return None,None


def image_solver():

    st.header("Image Based Numerical Solver")

    file = st.file_uploader("Upload Question Image")

    if file:

        reader = easyocr.Reader(['en'])

        image_bytes = file.read()

        result = reader.readtext(image_bytes)

        detected_text = " ".join([r[1] for r in result])

        st.subheader("Raw OCR Text")
        st.write(detected_text)

        cleaned = clean_text(detected_text)

        st.subheader("Cleaned Text")
        st.write(cleaned)

        if "gauss" in cleaned.lower():

            st.success("Gauss Seidel detected")

            A,b = build_matrix(cleaned)

            if A is not None:

                st.subheader("Matrix A")
                st.write(A)

                st.subheader("Vector b")
                st.write(b)

                solution, table = gauss_seidel(A,b)

                df = pd.DataFrame(
                    table,
                    columns=["Iteration","x","y","z","Error"]
                )

                st.subheader("Iteration Table")
                st.dataframe(df)

                solution = [round(float(i),4) for i in solution]

                st.success(f"Final Solution: {solution}")

            else:

                st.error("Still not enough numbers detected")

        else:

            st.warning("Method not detected")