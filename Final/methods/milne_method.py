import streamlit as st

def milne_app():

    st.header("Milne Predictor–Corrector Method")

    st.write("Example Differential Equation:  dy/dx = x + y")

    st.write("Default example values are already filled. You can change them if needed.")

    # Default values
    x0 = st.number_input("x0", value=0.0)
    x1 = st.number_input("x1", value=0.1)
    x2 = st.number_input("x2", value=0.2)
    x3 = st.number_input("x3", value=0.3)

    y0 = st.number_input("y0", value=1.0000)
    y1 = st.number_input("y1", value=1.1052)
    y2 = st.number_input("y2", value=1.2214)
    y3 = st.number_input("y3", value=1.3499)

    h = st.number_input("Step Size (h)", value=0.1)

    if st.button("Solve"):

        # Differential equation
        f = lambda x, y: x + y

        # Predictor formula
        y4_pred = y0 + (4*h/3) * (2*f(x1,y1) - f(x2,y2) + 2*f(x3,y3))

        x4 = x3 + h

        # Corrector formula
        y4_corr = y2 + (h/3) * (f(x2,y2) + 4*f(x3,y3) + f(x4,y4_pred))

        st.subheader("Results")

        st.write("Predicted y4 =", round(y4_pred,4))
        st.write("Corrected y4 =", round(y4_corr,4))
