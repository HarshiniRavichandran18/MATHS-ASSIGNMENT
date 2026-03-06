import streamlit as st

def ai_solver():

    st.subheader("🤖 AI Numerical Solver")

    question = st.text_area("Type your numerical methods question")

    if st.button("Solve with AI"):

        if "gauss" in question.lower():
            st.info("Detected Method: Gauss-Seidel")

        elif "trapezoidal" in question.lower():
            st.info("Detected Method: Trapezoidal Rule")

        elif "milne" in question.lower():
            st.info("Detected Method: Milne Predictor-Corrector")

        else:
            st.warning("Method not detected. Please specify the method.")

        st.write("### Step-by-step Solution")
        st.write("1. Identify the given equation")
        st.write("2. Apply the numerical formula")
        st.write("3. Perform iterations")
        st.write("4. Obtain final answer")