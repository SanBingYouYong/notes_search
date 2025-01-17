import streamlit as st
import webbrowser as wb
import base64

import whoosh_search as search
from config import load_languages

lang = load_languages()

st.set_page_config(
    page_title=lang['search_title'],
    layout="wide",
    initial_sidebar_state="expanded")

# Title of the web app
st.title(lang['search_title'])

# Input box for search query
query = st.text_input(lang['search_box'])

### PDF LEVEL SEARCH ###
if query:
    search_results = search.search_from_existing_index(query)
    st.write(lang['search_results'])
    for result in search_results:
        pdf = search.retrieve_pdf_path(result['tag'], result['folder'])
        pdf_path = pdf if pdf else lang['pdf_not_found']
        with st.expander(f"`{result['tag']}` | {result['folder']}", expanded=True):
            tag_and_folder = f"{result['tag']}/{result['folder']}"
            st.markdown(f"`{pdf_path}`")
            col1, col2 = st.columns([1, 4])
            with col1:
                search_images = st.button(lang['image_search'], key=tag_and_folder)
            with col2:
                view_pdf = st.button(lang['view_pdf'], key=f"{tag_and_folder}_viewpdf")
            ### IMAGE LEVEL SEARCH ###
            if search_images:
                b64_query = base64.b64encode(query.encode()).decode()
                b64_tag_and_folder = base64.b64encode(tag_and_folder.encode()).decode()
                wb.open_new_tab(f"http://localhost:8501/Image?query={b64_query}&tag_folder={b64_tag_and_folder}")
            if pdf:
                pdf_path_base64 = base64.b64encode(pdf.encode()).decode()
                if view_pdf:
                    wb.open_new_tab(f"http://localhost:8501/PDF?file={pdf_path_base64}")
    
