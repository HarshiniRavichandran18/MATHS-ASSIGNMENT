import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
import speech_recognition as sr
import re


# ------------------------------------------------
# VOICE INPUT
# ------------------------------------------------
def voice_input():

    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            st.info("🎤 Listening... Speak your math problem")

            audio = r.listen(source)

        text = r.recognize_google(audio)

        st.success("Voice Input Detected:")
        st.write(text)

        return text

    except:
        st.error("Voice recognition failed")
        return ""


# ------------------------------------------------
# GAUSS SEIDEL METHOD
# ------------------------------------------------
def gauss_seidel(A, b, tol=1e-6, max_iter=50):

    n = len(A)
    x = np.zeros(n)

    steps = []

    for k in range(max_iter):

        x_new = np.copy(x)

        for i in range(n):

            if A[i][i] == 0:
                raise ValueError("Zero on diagonal. Cannot apply Gauss Seidel.")

            s1 = sum(A[i][j]*x_new[j] for j in range(i))
            s2 = sum(A[i][j]*x[j] for j in range(i+1,n))

            x_new[i] = (b[i] - s1 - s2)/A[i][i]

        error = np.linalg.norm(x_new-x)

        steps.append([k+1] + list(np.round(x_new,6)) + [round(error,6)])

        if error < tol:
            break

        x = x_new

    return x_new, steps


# ------------------------------------------------
# EXTRACT EQUATIONS
# ------------------------------------------------
def extract_equations(text):

    pattern = r'([\-+0-9xyzXYZ\s]+=[\-+0-9\s]+)'
    eqs = re.findall(pattern,text)

    return [e.strip() for e in eqs]


# ------------------------------------------------
# BUILD MATRIX
# ------------------------------------------------
def build_matrix(equations):

    variables = sorted(set(re.findall(r'[xyz]'," ".join(equations).lower())))

    A=[]
    b=[]

    for eq in equations:

        left,right = eq.split("=")

        left = re.sub(r'(\d)([xyz])',r'\1*\2',left.lower())

        expr = sp.sympify(left)

        row=[]

        for v in variables:
            row.append(expr.coeff(sp.Symbol(v)))

        A.append(row)
        b.append(float(right))

    return np.array(A,dtype=float),np.array(b,dtype=float),variables


# ------------------------------------------------
# TRAPEZOIDAL RULE
# ------------------------------------------------
def trapezoidal_rule(func,a,b,n):

    if n <= 0:
        raise ValueError("n must be greater than zero")

    x = sp.symbols('x')

    func = re.sub(r'(\d)(x)',r'\1*\2',func)

    f = sp.lambdify(x,sp.sympify(func),"numpy")

    h = (b-a)/n

    xs=[a+i*h for i in range(n+1)]
    ys=[f(i) for i in xs]

    result = ys[0] + ys[-1]

    for i in range(1,n):
        result += 2*ys[i]

    result = (h/2)*result

    return result,xs,ys


# ------------------------------------------------
# SIMPSON RULE
# ------------------------------------------------
def simpson_rule(func,a,b,n):

    if n <= 0:
        raise ValueError("n must be greater than zero")

    if n % 2 != 0:
        raise ValueError("For Simpson rule n must be even")

    x=sp.symbols('x')

    func = re.sub(r'(\d)(x)',r'\1*\2',func)

    f=sp.lambdify(x,sp.sympify(func),"numpy")

    h=(b-a)/n

    xs=[a+i*h for i in range(n+1)]
    ys=[f(i) for i in xs]

    result = ys[0]+ys[-1]

    for i in range(1,n):

        if i%2==0:
            result += 2*ys[i]
        else:
            result += 4*ys[i]

    result = (h/3)*result

    return result,xs,ys


# ------------------------------------------------
# GRAPH
# ------------------------------------------------
def plot_function(xs,ys):

    fig,ax = plt.subplots()

    ax.plot(xs,ys,marker="o")

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title("Function Graph")

    st.pyplot(fig)


# ------------------------------------------------
# MAIN AI SOLVER
# ------------------------------------------------
def ai_solver():

    st.title("AI Numerical Methods Solver")


    # MANUAL INPUT
    st.subheader("Manual Input")

    manual_question = st.text_area(
        "Type your math problem",
        placeholder="Evaluate (x^3 + 2x) from 0 to 4 using trapezoidal rule with n=4"
    )

    solve_manual = st.button("Solve Manual Question")


    # VOICE INPUT
    st.subheader("Voice Input")

    voice_question=""

    if st.button("🎤 Start Voice Input"):
        voice_question = voice_input()

    solve_voice = st.button("Solve Voice Question")


    # SELECT QUESTION
    if solve_manual and manual_question!="":
        question = manual_question

    elif solve_voice and voice_question!="":
        question = voice_question

    else:
        question=""


    # SOLVER ENGINE
    if question!="":

        text = question.lower()


        # GAUSS SEIDEL
        if "gauss" in text:

            st.subheader("Detected Method: Gauss Seidel")

            equations = extract_equations(question)

            if len(equations) < 2:
                st.error("Could not detect equations")
                return

            A,b,vars = build_matrix(equations)

            solution,steps = gauss_seidel(A,b)

            columns = ["Iteration"] + vars + ["Error"]

            df = pd.DataFrame(steps,columns=columns)

            st.dataframe(df)

            result={}

            for i,v in enumerate(vars):
                result[v] = round(float(solution[i]),6)

            st.success(f"Final Solution: {result}")


        # TRAPEZOIDAL RULE
        elif "trapezoidal" in text:

            st.subheader("Detected Method: Trapezoidal Rule")

            func_match = re.search(r'\((.*?)\)',question)

            if func_match is None:
                st.error("Function not detected")
                return

            func = func_match.group(1)

            numbers = re.findall(r'-?\d+',question)

            if len(numbers) < 3:
                st.error("Could not detect limits or n value")
                return

            a=float(numbers[0])
            b=float(numbers[1])
            n=int(numbers[-1])

            if n<=0:
                st.error("n must be greater than zero")
                return

            result,xs,ys = trapezoidal_rule(func,a,b,n)

            table = pd.DataFrame({"x":xs,"f(x)":ys})

            st.dataframe(table)

            plot_function(xs,ys)

            st.success(f"Approximate Integral = {result:.4f}")


        # SIMPSON RULE
        elif "simpson" in text:

            st.subheader("Detected Method: Simpson Rule")

            func_match = re.search(r'\((.*?)\)',question)

            if func_match is None:
                st.error("Function not detected")
                return

            func = func_match.group(1)

            numbers = re.findall(r'-?\d+',question)

            if len(numbers) < 3:
                st.error("Could not detect limits or n value")
                return

            a=float(numbers[0])
            b=float(numbers[1])
            n=int(numbers[-1])

            if n%2!=0:
                st.error("For Simpson rule n must be even")
                return

            result,xs,ys = simpson_rule(func,a,b,n)

            table = pd.DataFrame({"x":xs,"f(x)":ys})

            st.dataframe(table)

            plot_function(xs,ys)

            st.success(f"Approximate Integral = {result:.4f}")

        else:

            st.warning("Method not detected. Mention Gauss Seidel / Trapezoidal / Simpson.")
