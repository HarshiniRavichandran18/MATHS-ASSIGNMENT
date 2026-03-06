import streamlit as st
import pytesseract
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def image_solver():

    st.subheader("📷 Solve from Image")

    uploaded_file = st.file_uploader("Upload problem image")

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(image, caption="Uploaded Image")

        text = pytesseract.image_to_string(image)

        st.write("### Extracted Text")
        st.write(text)

        if "gauss" in text.lower():
            st.success("Detected: Gauss-Seidel Method")

        elif "trapezoidal" in text.lower():
            st.success("Detected: Trapezoidal Rule")

        elif "milne" in text.lower():
            st.success("Detected: Milne Method")