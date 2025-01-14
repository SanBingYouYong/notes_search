import streamlit as st
import base64
import webbrowser as wb

st.set_page_config(layout="centered")

def display_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<div style="display: flex; justify-content: center;"><iframe src="data:application/pdf;base64,{base64_pdf}" width="90%" height="1000" type="application/pdf"></iframe></div>'
    st.markdown(pdf_display, unsafe_allow_html=True)

page_params = st.query_params

if page_params:
    text = page_params.get("file", [""])
    if text:
        pdf_path = base64.b64decode(text).decode()
        st.sidebar.markdown(f"`{pdf_path}`")
        display_pdf(pdf_path)
# TODO: maybe support viewing all PDF in local db