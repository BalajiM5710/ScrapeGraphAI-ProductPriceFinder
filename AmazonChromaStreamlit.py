import json
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up headless Chrome driver
def create_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)
    return driver

# Scrape product data from Croma
def scrape_price_croma(driver, url, product, spec):
    try:
        driver.get(url.format(product=product, spec=spec))
        # Wait for the product title or any key element to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-title"))
        )
        # Extract product details
        product_title = driver.find_element(By.CSS_SELECTOR, "h1.product-title").text
        price_element = driver.find_element(By.CLASS_NAME, "amount.plp-srp-new-amount")
        rating = driver.find_element(By.CLASS_NAME, "rating-text")
        offer = driver.find_element(By.CLASS_NAME, "discount.discount-mob-plp")
        delivery = driver.find_element(By.CLASS_NAME, "delivery-text-msg")
        link_element = driver.find_element(By.CSS_SELECTOR, "a[rel='noopener noreferrer']")
        product_link = link_element.get_attribute('href') if link_element else "N/A"

        croma_details = {
            "Site": "Croma",
            "Product Name": f"{product} {spec}",
            "Price": price_element.text.strip(),
            "Rating": rating.text.strip() if rating else "N/A",
            "Offer": offer.text.strip() if offer else "N/A",
            "Delivery": delivery.text.strip() if delivery else "N/A",
            "Product Link": f'<a href="{product_link}" target="_blank">Click Here</a>'
        }
        return croma_details
    except Exception as e:
        print(f"Error scraping Croma: {e}")
        return {}

# Streamlit interface
st.title("Product Price Comparison - Croma")

# User input for CSV file or URL
uploaded_file = st.file_uploader("Upload CSV with Product and Specifications", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Products to Scrape")
    st.dataframe(df)

    # Create Selenium driver
    driver = create_webdriver()

    for index, row in df.iterrows():
        product = row['Product']
        spec = row['Spec']
        st.write(f"### Scraping data for {product} {spec}...")

        with st.spinner(f'Scraping data from Croma for {product} {spec}...'):
            croma_url = "https://www.croma.com/searchB?q={product}%3Arelevance&text={product} {spec}"
            croma_data = scrape_price_croma(driver, croma_url, product, spec)
        
        if croma_data:
            df_product = pd.DataFrame([croma_data])
            st.write(f"### Results for {product} {spec}")
            st.markdown(df_product.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.write(f"No data found for {product} {spec}.")

    # Quit the browser after scraping
    driver.quit()
