import json
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from groq import Groq

# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Setup WebDriver (Headless mode for deployment)
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Setup Groq client
client = Groq(api_key='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')

# Function to scrape data from Croma
def scrape_price_croma(url, product, spec, driver):
    try:
        driver.get(url.format(product=product, spec=spec))
        time.sleep(5)  # Wait for page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_name_element = soup.find('a', rel='noopener noreferrer')
        price_element = soup.find('span', class_='amount plp-srp-new-amount')
        
        if price_element:
            st.write(f"Scraped price for {product} {spec}: {price_element.text.strip()}")
        else:
            st.write(f"No price found for {product} {spec}")

        # Extract other data...
        # Continue with the rest of the scraping...

        return {"Product": product, "Price": price_element.text.strip() if price_element else "N/A"}
    except Exception as e:
        st.write(f"An error occurred while scraping Croma: {e}")
        return {}

# Function to scrape data from Amazon
def scrape_price_amazon(url, product, spec, driver):
    try:
        driver.get(url.format(product=product, spec=spec))
        time.sleep(5)  # Wait for page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_name = soup.find('span', class_="a-size-medium a-color-base a-text-normal")
        price_element = soup.find('span', class_='a-price-whole')

        if price_element:
            st.write(f"Scraped price for {product} {spec}: {price_element.text.strip()}")
        else:
            st.write(f"No price found for {product} {spec}")

        # Continue with the rest of the scraping...

        return {"Product": product, "Price": price_element.text.strip() if price_element else "N/A"}
    except Exception as e:
        st.write(f"An error occurred while scraping Amazon: {e}")
        return {}

# ---------------- Page & UI/UX Components ------------------------
def main_sidebar():
    # 1.Vertical Menu
    st.header("Product Price Comparison - Croma vs Amazon")
    product_comparison_page()

def product_comparison_page():
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV with Product and Specifications", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Products to Scrape")
        st.write(df.head())  # Debugging: show the first few rows

        # Setup the WebDriver (Headless mode)
        driver = setup_driver()
        
        # Iterate over each row in the CSV and scrape data
        for index, row in df.iterrows():
            product = row['Product']
            spec = row['Spec']

            st.write(f"### Scraping data for {product} {spec}...")

            with st.spinner(f'Scraping data from Croma for {product} {spec}...'):
                croma_url = "https://www.croma.com/searchB?q={product}%3Arelevance&text={product} {spec}"
                croma_data = scrape_price_croma(croma_url, product, spec, driver)

            with st.spinner(f'Scraping data from Amazon for {product} {spec}...'):
                amazon_url = "https://www.amazon.in/s?k={product}+{spec}&i=todays-deals&crid=2HFP9FZW24UX4&sprefix={product}+{spec}%2Ctodays-deals%2C186&ref=nb_sb_noss_"
                amazon_data = scrape_price_amazon(amazon_url, product, spec, driver)

            # Combine the data into a single DataFrame for display
            combined_data = []
            if croma_data:
                combined_data.append(croma_data)
            if amazon_data:
                combined_data.append(amazon_data)

            if combined_data:
                df_product = pd.DataFrame(combined_data)
                st.write("### Comparison Results")
                st.write(df_product)  # Debugging: Display the DataFrame
                st.markdown(df_product.to_html(escape=False), unsafe_allow_html=True)
            else:
                st.write(f"No data found for {product} {spec}")

        # Close the browser after scraping
        driver.quit()

if __name__ == "__main__":
    main_sidebar()
