import streamlit as st

st.title("User Details Form")

name = st.text_input("Enter your name")

age = st.text_input("Enter your age")

if st.button("Submit"):
    st.write("Name:", name)
    st.write("Age:", age)
