import streamlit as st
import base64
import webbrowser as wb

import whoosh_search as search

st.set_page_config(layout="wide")

page_params = st.query_params

if page_params:
    query = page_params.get("query", [""])
    tag_folder = page_params.get("tag_folder", [""])
    if query and tag_folder:
        query = base64.b64decode(query).decode()
        tag_folder = base64.b64decode(tag_folder).decode()
        st.sidebar.markdown(f"{query} in `{tag_folder}`")
        results = search.search_from_existing_sub_index(query, tag_folder)
        img_paths = {
            res['file']: search.retrieve_img_path(tag_folder, res['file'])
            for res in results
        }
        cols = st.columns(3)
        for i, (file, img_path) in enumerate(img_paths.items()):
            if img_path:
                with cols[i % 3]:
                    st.image(img_path, use_container_width=True, caption=file)
            else:
                st.warning(f"No image found for `{file}`")
# TODO: maybe support selecting a tag/pdf folder to search images in (but with PDF already why don't you just Ctrl F)