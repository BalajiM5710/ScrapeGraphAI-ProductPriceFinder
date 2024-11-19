import streamlit as st
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from groq import Groq

# Groq Client Setup
client = Groq(api_key='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')

# Web scraping functions
@st.cache_resource
def get_driver():
    """Initialize and return a Selenium WebDriver instance."""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def scrape_price_croma(driver, url, product, spec):
    """Scrape product details from Croma."""
    try:
        driver.get(url.format(product=product, spec=spec))
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Scrape details
        price_element = soup.find('span', class_='amount plp-srp-new-amount')
        sprc = str(price_element)
        finalprice = ''.join([i for i in sprc if i.isdigit() or i == ','])
        rating = soup.find('span', class_='rating-text')
        offer = soup.find('span', class_='discount discount-mob-plp discount-newsearch-plp')
        delivery = soup.find('span', class_='delivery-text-msg')
        link_element = soup.find('a', rel='noopener noreferrer')
        product_link = link_element['href'] if link_element else "N/A"

        return {
            "Site": "Croma",
            "Product Name": f"{product} {spec}",
            "Price": finalprice.strip(),
            "Rating": rating.text.strip() if rating else "N/A",
            "Offer": offer.text.strip() if offer else "N/A",
            "Delivery": delivery.text.strip() if delivery else "N/A",
            "Product Link": f'<a href="https://www.croma.com{product_link}" target="_blank">Click Here</a>',
        }
    except Exception as e:
        print(f"Error scraping Croma: {e}")
        return {}


def scrape_price_amazon(driver, url, product, spec):
    """Scrape product details from Amazon."""
    try:
        driver.get(url.format(product=product, spec=spec))
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Scrape details
        price_element = soup.find('span', class_='a-price-whole')
        rating = soup.find('i', class_='a-icon a-icon-star-small a-star-small-4')
        delivery = soup.find('span', class_='a-color-base a-text-bold')
        link_element = soup.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        product_link = link_element['href'] if link_element else "N/A"

        return {
            "Site": "Amazon",
            "Product Name": f"{product} {spec}",
            "Price": price_element.text.strip() if price_element else "N/A",
            "Rating": rating.text.strip() if rating else "N/A",
            "Delivery": delivery.text.strip() if delivery else "N/A",
            "Product Link": f'<a href="https://www.amazon.in{product_link}" target="_blank">Click Here</a>',
        }
    except Exception as e:
        print(f"Error scraping Amazon: {e}")
        return {}

# Streamlit UI
st.title("Product Price Comparison - Croma vs Amazon")

uploaded_file = st.file_uploader("Upload CSV with Product and Specifications", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Products to Scrape")
    st.dataframe(df)

    # Get the driver instance
    driver = get_driver()

    # Iterate over each row in the CSV and scrape data
    results = []
    for _, row in df.iterrows():
        product = row['Product']
        spec = row['Spec']
        st.write(f"### Scraping data for {product} {spec}...")

        with st.spinner(f'Scraping data from Croma for {product} {spec}...'):
            croma_url = "https://www.croma.com/searchB?q={product}%3Arelevance&text={product} {spec}"
            croma_data = scrape_price_croma(driver, croma_url, product, spec)

        with st.spinner(f'Scraping data from Amazon for {product} {spec}...'):
            amazon_url = "https://www.amazon.in/s?k={product}+{spec}"
            amazon_data = scrape_price_amazon(driver, amazon_url, product, spec)

        # Combine and display results
        combined_data = [croma_data, amazon_data]
        results.extend(combined_data)
        st.write(f"### Comparison Results for {product} {spec}")
        st.markdown(pd.DataFrame(combined_data).to_html(escape=False), unsafe_allow_html=True)

        # Groq summary
        final_result = {"Croma": croma_data, "Amazon": amazon_data}
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Based on this data {json.dumps(final_result)}, which site is better and why?",
            }],
            model="llama3-70b-8192",
        )
        st.write("### Groq Summary:")
        st.markdown(chat_completion.choices[0].message.content)

    driver.quit()
