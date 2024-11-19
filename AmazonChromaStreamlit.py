import streamlit as st
import os

# Function to install and link geckodriver
@st.cache_resource
def install_geckodriver():
    os.system('sbase install geckodriver')  # Install geckodriver
    os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

# Install the geckodriver (runs only once)
_ = install_geckodriver()

# Import Selenium
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

# Set up Selenium to use Firefox in headless mode
opts = FirefoxOptions()
opts.add_argument("--headless")
browser = webdriver.Firefox(options=opts)

# Perform a test by visiting a website
browser.get('http://example.com')

# Display the HTML source in the Streamlit app
st.title("Selenium with Firefox on Streamlit Cloud")
st.subheader("Page Source of Example.com")
st.code(browser.page_source)

# Close the browser after use
browser.quit()
