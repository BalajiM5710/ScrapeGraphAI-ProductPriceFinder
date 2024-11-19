
# README.md

### Try It Out:
You can try out the application by using this (#) and see how the scraper works in real-time.

## Product Price Scraper with Groq API Integration

This repository contains a web scraper for fetching product prices and details from Amazon, Croma, and Flipkart. The scraped data is enhanced with Groq API to generate insightful comparisons. This system is designed to support multiple products from a CSV and display the results on a neat Streamlit-based UI.

### Video Explanations:
- **[Functionality Explanation Video](#)**  
- **[Code Explanation Video](#)**

### Features & Highlights:
- **Multiple Product Scraping**: Automatically fetch product prices, specs, and other details from Croma, Amazon, and Flipkart.
- **Neat Visualization**: Results are displayed in a table format in Streamlit.
- **Groq API Integration**: Compares products based on pricing and features using advanced AI models for insights.
- **CSV Input**: Users can input a CSV file with product and specification details for batch processing.
  
### Tech Stack:
- **Streamlit**: For building the user interface (UI) and visualizing results.
- **Selenium**: For web scraping Amazon, Croma, and Flipkart.
- **Groq API**: Used for generating summaries and making comparisons between the products.
- **BeautifulSoup**: For parsing HTML data and extracting necessary information.
- **Pandas**: For handling CSV data and organizing the final output.
- **ScrapeGraphAI**: A web scraping LLM model for extracting data from websites (Amazon and Flipkart).
  
### How It Works:
1. **Groq API**:  
   The **Groq API** is used to generate summaries and insights based on the scraped product data. After scraping the product details from the websites, the Groq API compares them, helping users decide where to buy a particular product based on multiple factors such as price, delivery options, and ratings.

2. **Scraping Logic**:
   - **Amazon Scraper**: Scrapes product prices, details, and links for Amazon. It uses **Selenium** and **BeautifulSoup** to parse HTML pages. The product is searched based on the product name and specification.
   - **Croma Scraper**: Similar to the Amazon scraper but specific to the Croma website.
   - **Flipkart Scraper**: Uses the same principles to extract product information from Flipkart.

3. **CSV Input**:  
   Users can upload a CSV file that contains product names and their specifications (e.g., “iPhone 15, 128GB”). Each product is then processed, and the relevant data is fetched from each eCommerce site. The results are shown in a neat table format.

### CSV Format:
Ensure your input CSV has the following format:

| Product      | Spec     |
|--------------|----------|
| iPhone 15    | 128GB    |
| MacBook Air  | M2       |

### Usage Instructions:
1. **Prepare CSV File**: 
   - Format the CSV as shown above.
   - It's advisable to limit the CSV to **3 products** to avoid overloading the Groq API. Large requests may cause the model’s API call to fail.
   
2. **Run Streamlit App**:  
   - Install dependencies: `pip install -r requirements.txt`
   - Run the Streamlit app: `streamlit run app.py`

3. **View Results**:  
   - Once the products are scraped, results will be displayed in a table showing product names, prices, and buying links for each product across the websites.

### Important Note:
- **Avoid CSV Spamming**: Please do not input a large CSV file with too many products as it may slow down the API calls. Stick to **3 products** for optimal performance with Groq API.

### ScrapeGraphAI and Its Limitations:
- **ScrapeGraphAI** was utilized for advanced LLM-based scraping. However, due to some unsolvable errors and time constraints, it could not be fully integrated into the Streamlit UI for seamless deployment. While it offers great potential for automated scraping and AI-driven insights, the limitations in deployment led to relying on standard scraping with Selenium for the UI version of the tool.


### Groq API and LLM Used:
This project uses **Groq's Llama3-70b-8192 model** for summarization and making product comparisons, which helps analyze product data and provide insights for the best buying options.

---
