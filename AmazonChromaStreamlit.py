import json
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def scrape_price_croma(url, product, spec):
    try:
        # Navigate to the URL
        driver.get(url.format(product=product, spec=spec))
        
        # Wait for the price element to load (adjust locator as needed)
        wait = WebDriverWait(driver, 10)
        price_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "amount.plp-srp-new-amount"))
        )
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract data
        product_name_element = soup.find('a', rel='noopener noreferrer')
        price_element = soup.find('span', class_='amount plp-srp-new-amount')
        sprc = str(price_element)
        finalprice = ''.join([i for i in sprc if i.isdigit() or i == ','])
        
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
        return croma_details
    except Exception as e:
        print(f"An error occurred while scraping Croma: {e}")
        return {}


def scrape_price_amazon(url, product, spec):
    try:
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
        return amazon_details
    except Exception as e:
        print(f"An error occurred while scraping Amazon: {e}")
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
        
        # Display results in a table for each product
        if combined_data:
            df_product = pd.DataFrame(combined_data)
            st.write(f"### Comparison Results for {product} {spec}")
            st.markdown(df_product.to_html(escape=False), unsafe_allow_html=True)
            
            # Generate a summary directly
            summary = f"For {product} {spec}, "
            if croma_data and amazon_data:
                summary += f"the price at Croma is {croma_data['Price']} and on Amazon is {amazon_data['Price']}. "
                if croma_data['Price'] < amazon_data['Price']:
                    summary += "Croma offers a better deal."
                else:
                    summary += "Amazon offers a better deal."
            else:
                summary += "data is incomplete for a proper comparison."
            
            st.write("### Summary:")
            st.write(summary)

# Close the browser after scraping
driver.quit()
