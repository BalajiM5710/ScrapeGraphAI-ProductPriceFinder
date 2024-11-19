import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Streamlit UI
st.title("Streamlit + Selenium Demo")

# Setup Selenium in headless mode
try:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Example of scraping Google
    driver.get("https://www.google.com")
    st.write("Successfully opened Google.")
    driver.quit()
except Exception as e:
    st.error(f"Error initializing Selenium: {e}")
