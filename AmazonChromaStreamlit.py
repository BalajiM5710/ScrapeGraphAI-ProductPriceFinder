import json
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from groq import Groq

# Set up Groq client
client = Groq(api_key='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')

# Configure Selenium WebDriver
@st.cache_resource
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver = get_driver()

def scrape_price_croma(url, product, spec):
    try:
        driver.get(url.format(product=product, spec=spec))
        time.sleep(5)  # Wait for page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract details for Croma
        price_element = soup.find('span', class_='amount plp-srp-new-amount')
        rating = soup.find('span', class_='rating-text')
        offer = soup.find('span', class_='discount discount-mob-plp discount-newsearch-plp')
        delivery = soup.find('span', class_='delivery-text-msg')
        link_element = soup.find('a', rel='noopener noreferrer')
        product_link = link_element['href'] if link_element else "N/A"

        croma_details = {
            "Site": "Croma",
            "Product Name": f"{product} {spec}",
            "Price": price_element.text.strip() if price_element else "N/A",
            "Rating": rating.text.strip() if rating else "N/A",
            "Offer": offer.text.strip() if offer else "N/A",
            "Delivery": delivery.text.strip() if delivery else "N/A",
            "Product Link": f'<a href="https://www.croma.com{product_link}" target="_blank">Click Here</a>' if product_link != "N/A" else "N/A",
        }

        return croma_details
    except Exception as e:
        st.error(f"An error occurred while scraping Croma: {e}")
        return {}

def scrape_price_amazon(url, product, spec):
    try:
        driver.get(url.format(product=product, spec=spec))
        time.sleep(5)  # Wait for page to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract details for Amazon
        price_element = soup.find('span', class_='a-price-whole')
        rating = soup.find('i', class_='a-icon a-icon-star-small a-star-small-4')
        delivery = soup.find('span', class_='a-color-base a-text-bold')
        link_element = soup.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        product_link = link_element['href'] if link_element else "N/A"

        amazon_details = {
            "Site": "Amazon",
            "Product Name": f"{product} {spec}",
            "Price": price_element.text.strip() if price_element else "N/A",
            "Rating": rating.text.strip() if rating else "N/A",
            "Offer": "N/A",
            "Delivery": delivery.text.strip() if delivery else "N/A",
            "Product Link": f'<a href="https://www.amazon.in{product_link}" target="_blank">Click Here</a>' if product_link != "N/A" else "N/A",
        }

        return amazon_details
    except Exception as e:
        st.error(f"An error occurred while scraping Amazon: {e}")
        return {}

# Streamlit UI
st.title("Product Price Comparison - Croma vs Amazon")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV with Product and Specifications", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Products to Scrape")
    st.dataframe(df)

    # Iterate over each row in the CSV and scrape data
    for index, row in df.iterrows():
        product = row['Product']
        spec = row['Spec']

        st.write(f"### Scraping data for {product} {spec}...")

        with st.spinner(f'Scraping data from Croma for {product} {spec}...'):
            croma_url = "https://www.croma.com/searchB?q={product}%3Arelevance&text={product} {spec}"
            croma_data = scrape_price_croma(croma_url, product, spec)

        with st.spinner(f'Scraping data from Amazon for {product} {spec}...'):
            amazon_url = "https://www.amazon.in/s?k={product}+{spec}&i=todays-deals&crid=2HFP9FZW24UX4&sprefix={product}+{spec}%2Ctodays-deals%2C186&ref=nb_sb_noss_"
            amazon_data = scrape_price_amazon(amazon_url, product, spec)

        # Combine the data into a single DataFrame for display
        combined_data = []
        if croma_data:
            combined_data.append(croma_data)
        if amazon_data:
            combined_data.append(amazon_data)

        if combined_data:
            df_product = pd.DataFrame(combined_data)
            st.write(f"### Comparison Results for {product} {spec}")
            st.markdown(df_product.to_html(escape=False), unsafe_allow_html=True)

            # Prepare Groq API request for comparison summary
            final_result = {"Croma": croma_data, "Amazon": amazon_data}
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"Here is the data for two products: {json.dumps(final_result)}. Based on the data, which website (Croma or Amazon) is better for purchasing and why? This should look like how an end user would read a summary of this comparison."
                        }
                    ],
                    model="llama3-70b-8192",
                )
                st.write("### Groq Summary:")
                st.markdown(f"<div>{chat_completion.choices[0].message.content}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred while processing with Groq: {e}")

# Close the browser after scraping
driver.quit()
