import streamlit as st
import os

@st.experimental_singleton
def install_chromedriver():
    # Install ChromeDriver using seleniumbase
    os.system('sbase install chromedriver')
    # Link ChromeDriver to the system path
    os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/chromedriver /home/appuser/venv/bin/chromedriver')

_ = install_chromedriver()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up ChromeOptions
options = Options()
options.add_argument("--headless")  # Run in headless mode for Streamlit Cloud
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize ChromeDriver
service = Service('/home/appuser/venv/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=options)

# Test the setup
driver.get("http://example.com")
st.write(driver.page_source)
