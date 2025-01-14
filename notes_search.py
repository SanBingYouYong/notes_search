import streamlit as st
import webbrowser as wb
import base64

import whoosh_search as search

st.set_page_config(
    page_title="Notes Search and Visualization", 
    layout="wide",
    initial_sidebar_state="collapsed")


# Title of the web app
st.title("Notes Search and Visualization")

# Input box for search query
query = st.text_input("Enter search query:")
_ = "🖼️"
# Placeholder for search results
if query:
    search_results = search.search_from_existing_index(query)
    st.write("Search results:")
    for result in search_results:
        pdf = search.retrieve_pdf_path(result['tag'], result['folder'])
        pdf_path = pdf_path if pdf else "No PDF path found"
        with st.expander(f"📄{result['tag']} | {result['folder']}"):
            st.write(f"Tag: {result['tag']}")
            st.write(f"Folder: {result['folder']}")
            st.write(f"PDF path: {pdf}")
        if pdf:
            pdf_path_base64 = base64.b64encode(pdf.encode()).decode()
            if st.button("View PDF", key=pdf):
                wb.open_new_tab(f"http://localhost:8501/PDF?file={pdf_path_base64}")
        st.write("---")
    
