import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd

def trapezoidal_rule(f,a,b,n):

    h=(b-a)/n

    result=f(a)+f(b)

    rows=[]

    for i in range(1,n):

        x=a+i*h
        fx=f(x)

        rows.append([i,round(x,4),round(fx,4)])

        result+=2*fx

    result=(h/2)*result

    return result,rows


def trapezoidal_app():

    st.header("Trapezoidal Rule Solver")

    func=st.text_input("Enter function","x**2")

    a=st.number_input("Lower limit")
    b=st.number_input("Upper limit",value=4.0)
    n=st.number_input("Number of intervals",value=4)

    if st.button("Solve"):

        x=sp.symbols('x')

        f=sp.lambdify(x,sp.sympify(func),'numpy')

        result,rows=trapezoidal_rule(f,a,b,n)

        df=pd.DataFrame(rows,
        columns=["i","x","f(x)"])

        st.subheader("Intermediate Values")
        st.dataframe(df)

        st.success(f"Integral ≈ {round(result,4)}")