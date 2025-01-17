import streamlit as st
import config

st.set_page_config(
    page_title="⚙️ Settings | 设置",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚙️ Settings | 设置")

config_file = config.CONFIG_FILE
config_data = config.load_config(config_file)

# relevant settings
tesseract_path = st.text_input("Tesseract Path:", config_data.get("tesseract_path"))

current_lang = config_data.get("lang")
supported_langs = config_data.get("supported_langs")
language = st.selectbox("Language:", ["en", "中文"], index=supported_langs.index(current_lang))

# not-so-relevant settings
data_path = st.text_input("Data Path:", config_data.get("data_path"))

# Save updated config values
if st.button("Save"):
    new_config_data = config_data | {  # fancy new grammar to merge dict with latter overwriting
        "tesseract_path": tesseract_path,
        "lang": language,
        "data_path": data_path
    }
    config.save_config(new_config_data, config_file)
    st.success("Configuration saved successfully!")
# if st.button("Reload"):
#     config_data = config.load_config(config_file)
#     st.success("Configuration reloaded successfully!")

