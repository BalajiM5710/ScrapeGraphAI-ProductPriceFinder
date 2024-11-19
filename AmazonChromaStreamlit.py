import subprocess
import streamlit as st

def get_chromium_version():
    try:
        # Run the command to get Chromium version
        version = subprocess.check_output(["chromium", "--version"], text=True).strip()
        return version
    except Exception as e:
        return f"Error: {str(e)}"

# Display the Chromium version in Streamlit
st.write("Chromium Version:", get_chromium_version())
