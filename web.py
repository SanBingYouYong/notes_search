import streamlit as st
import webbrowser as wb
import base64

import whoosh_search as search


# Title of the web app
st.title("Notes Search and Visualization")

# Input box for search query
query = st.text_input("Enter search query:")

# Placeholder for search results
if query:
    search_results = search.search_from_existing_index(query)
    st.write("Search results:")
    for result in search_results:
        st.write(f"Tag: {result['tag']}")
        st.write(f"Folder: {result['folder']}")
        pdf = search.retrieve_pdf_path(result['tag'], result['folder'])
        if pdf:
            st.write(f"PDF path: {pdf}")
            pdf_path_base64 = base64.b64encode(pdf.encode()).decode()
            if st.button("View PDF", key=pdf):
                wb.open_new_tab(f"http://localhost:8501/pdf_display_tab?file={pdf_path_base64}")
        st.write("---")
    
