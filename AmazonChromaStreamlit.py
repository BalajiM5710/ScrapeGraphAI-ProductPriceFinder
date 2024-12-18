import json
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from groq import Groq

# ------------- Settings for Pages ----------- 
st.set_page_config(layout="wide")

# ------------- Setup for WebDriver -----------
def init_driver():
    """Initialize Selenium WebDriver with headless mode"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1200')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# ------------- Scraping Functions -----------
def scrape_price_croma(url, product, spec):
    try:
        driver = init_driver()
        driver.get(url.format(product=product, spec=spec))
        time.sleep(5)  # Wait for page to load
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract details for Croma
        product_name_element = soup.find('a', rel='noopener noreferrer')
        price_element = soup.find('span', class_='amount plp-srp-new-amount')
        sprc = str(price_element)
        finalprice = ''
        for i in sprc:
            if i.isdigit() or i == ',':
                finalprice += i
        rating = soup.find('span', class_='rating-text')
        offer = soup.find('span', class_='discount discount-mob-plp discount-newsearch-plp')
        delivery = soup.find('span', class_='delivery-text-msg')
        link_element = soup.find('a', rel='noopener noreferrer')
        product_link = link_element['href'] if link_element else "N/A"
        
        # Prepare the response
        croma_details = {}
        if price_element:
            croma_details = {
                "Site": "Croma",
                "Product Name": f"{product} {spec}",
                "Price": finalprice.strip(),
                "Rating": rating.text.strip() if rating else "N/A",
                "Offer": offer.text.strip() if offer else "N/A",
                "Delivery": delivery.text.strip() if delivery else "N/A",
                "Product Link": f'<a href="https://www.croma.com{product_link}" target="_blank">Click Here</a>'
            }
        driver.quit()
        return croma_details
    except Exception as e:
        print(f"An error occurred while scraping Croma: {e}")
        driver.quit()
        return {}

def scrape_price_amazon(url, product, spec):
    try:
        driver = init_driver()
        driver.get(url.format(product=product, spec=spec))
        time.sleep(5)  # Wait for page to load
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract details for Amazon
        product_name = soup.find('span', class_="a-size-medium a-color-base a-text-normal")
        price_element = soup.find('span', class_='a-price-whole')
        rating = soup.find('i', class_='a-icon a-icon-star-small a-star-small-4')
        offer = "6%"  # Amazon static discount (you can scrape dynamically if needed)
        delivery = soup.find('span', class_='a-color-base a-text-bold')
        link_element = soup.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        product_link = link_element['href'] if link_element else "N/A"
        
        # Prepare the response
        amazon_details = {}
        if price_element:
            amazon_details = {
                "Site": "Amazon",
                "Product Name": f"{product} {spec}",
                "Price": price_element.text.strip(),
                "Rating": rating.text.strip() if rating else "N/A",
                "Offer": offer,
                "Delivery": delivery.text.strip() if delivery else "N/A",
                "Product Link": f'<a href="https://www.amazon.in{product_link}" target="_blank">Click Here</a>'
            }
        driver.quit()
        return amazon_details
    except Exception as e:
        print(f"An error occurred while scraping Amazon: {e}")
        driver.quit()
        return {}

# ---------------- Page & UI/UX Components ------------------------
def main_sidebar():
    st.header("Product Price Comparison - Croma vs Amazon")
    site_extraction_page()

def site_extraction_page():
    # CSV upload and data extraction
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
            
            # Display results in a table for each product
            if combined_data:
                df_product = pd.DataFrame(combined_data)
                st.write(f"### Comparison Results for {product} {spec}")
                st.markdown(df_product.to_html(escape=False), unsafe_allow_html=True)
                
                # Prepare Groq API request for comparison summary
                final_result = {"Croma": croma_data, "Amazon": amazon_data}
                client = Groq(api_key='xxxxxxx')
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"Here is the data for two products: {json.dumps(final_result)}. Based on the data, which website (Croma or Amazon) is better for purchasing and why? This should look like how an end user would read a summary of this comparison."
                        }
                    ],
                    model="llama3-70b-8192",
                )
                
                # Output the Groq response for each product
                st.write("### Groq Summary:")
                st.markdown(f"<div>{chat_completion.choices[0].message.content}</div>", unsafe_allow_html=True)

# ---------------- Main Function ----------------
if __name__ == "__main__":
    main_sidebar()
