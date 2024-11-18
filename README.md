Here's an updated version of the README with the placeholders for the video links you requested:

---

# Product Price Scraper

## Overview

This is a web-based application built using **Streamlit** and **Python**, which allows users to upload a CSV file containing product names and specifications. It then scrapes product prices and related information from multiple e-commerce platforms, specifically **Amazon** and **Flipkart**, by utilizing the **Google AI Studio's LLM API** for intelligent web scraping. 

The app presents the gathered data in a clean and interactive manner, displaying product names, specifications, prices, and direct purchase links. The scraper intelligently extracts only the relevant product details, ensuring users receive accurate and up-to-date pricing information.

## Features

### 1. **CSV Upload**
   - Users can upload a CSV file containing product names and specifications. The app processes the file and uses the data to search for products on various e-commerce platforms.
   
### 2. **Smart Scraping with Google AI Studio LLM API**
   - The application integrates with **Google AI Studio's LLM API** for advanced, context-aware web scraping.
   - The scraper intelligently understands the product name and specification context to extract the most relevant and accurate data from Flipkart and Amazon.
   - The LLM API ensures that the scraped data is accurate by filtering out irrelevant results and presenting only the correct product details.

### 3. **Interactive Product Data Display**
   - After scraping, the results are displayed interactively within the app. The data includes:
     - **Product Name**
     - **Specifications**
     - **Price**
     - **Buy Link (direct link to the product page)**
   
### 4. **Price Comparison**
   - The app compares the prices of the same product across **Flipkart** and **Amazon** and displays the lowest price along with the respective platform’s details.
   
### 5. **Automatic Data Processing**
   - The app automatically handles missing or incomplete product data, ensuring that only valid products are processed.
   - It generates a clean and easily interpretable summary that highlights the lowest price and best deal available.

### 6. **Customizable Column Selection**
   - Users can select the primary column for product names, which ensures flexibility in handling different CSV formats.
   
### 7. **User-Friendly Interface**
   - The app uses **Streamlit**, providing an intuitive and user-friendly web interface where users can interact with the product data.
   - The interface is designed to allow seamless file upload, data display, and scraping execution with minimal user input.

## Technologies Used

- **Streamlit**: For building the interactive web app interface.
- **Python**: The programming language used to implement the backend logic.
- **Google AI Studio's LLM API**: For advanced language model-based web scraping, which intelligently understands product names and specifications.
- **Pandas**: For handling and processing the CSV data.
- **CSV**: For input data (products and specifications).
- **Time**: To manage the scraping process and prevent rate limiting.

## Setup and Installation

### Prerequisites

- Python 3.x installed
- An IDE or text editor (e.g., VS Code, PyCharm)
- Access to the **Google AI Studio's LLM API** (API key required)

### Installation Steps

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/product-price-scraper.git
    cd product-price-scraper
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your **Google AI Studio API key**:
    - Obtain an API key from **Google AI Studio** (if you haven't already).
    - In the code, replace the placeholder `your_api_key` with your actual API key for the LLM API.

4. Run the application:
    ```bash
    streamlit run app.py
    ```

5. Open the application in your browser (Streamlit should automatically open it):
    ```
    http://localhost:8501
    ```

## Usage

1. **Upload CSV File**: Click on the file uploader to select and upload your CSV file. The CSV should have at least two columns: one for product names and another for specifications. Ensure that each row has a valid product name and specification.
   
2. **Select Primary Column**: Once the CSV file is uploaded, the app will automatically display the first few rows. You will be prompted to select the column that contains the product names.

3. **Execute Scraping**: After selecting the primary column, click the "Execute Scraping" button to start the scraping process. The app will use Google AI Studio's LLM API to intelligently scrape product prices from **Amazon** and **Flipkart** based on the provided product names and specifications.

4. **View Results**: Once the scraping is complete, the results will be displayed. You will see:
    - **Product Name**
    - **Specification**
    - **Lowest Price**
    - **Buy Link** (which will redirect to the platform's product page)

5. **Download or View Data**: After scraping, you can download the processed results or simply view them directly on the page.

## Example CSV Format

The CSV file should look like this:

| Product Name          | Spec           |
|-----------------------|----------------|
| iPhone 13             | 128GB          |
| Samsung Galaxy S21    | 256GB          |
| Lenovo ThinkPad X1    | i7, 16GB RAM   |

## How the Scraper Works

### 1. **Google AI Studio LLM Integration**
   - We have integrated **Google AI Studio's LLM API** to enhance the web scraping process. The LLM is capable of understanding complex product queries and scraping the relevant data based on the context of the product name and specifications provided.
   - The scraper communicates with the API, which intelligently analyzes the webpage content and extracts structured product information in JSON format.

### 2. **Scraping Flipkart and Amazon**
   - The scraper uses URLs dynamically generated for **Flipkart** and **Amazon** based on the product name and specification provided in the CSV.
   - It then fetches the product's price and link by parsing the HTML of the respective product pages.

### 3. **Price Comparison Logic**
   - After scraping data from both platforms, the app compares the prices of the same product across Amazon and Flipkart.
   - It identifies the platform offering the lowest price and displays this information to the user, along with a direct link to the product page for easy purchasing.

## Troubleshooting

- **No results returned**: If no results are returned, check if the product name and specification are clearly defined in the CSV file.
- **Error with API Key**: Ensure that the **Google AI Studio LLM API** key is valid and correctly added to the configuration file.
- **Slow response times**: Web scraping may take time depending on the website's structure. Ensure your internet connection is stable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to **Google AI Studio** for providing the powerful LLM API that made this advanced web scraping solution possible.
- **Streamlit** for making it easy to develop interactive web applications with Python.

## Videos

- [Functionality Explanation Video](https://drive.google.com/file/d/1BU1t1FhVD_9JoO7y1BLaPKq4kzNk3Mbl/view?usp=sharing)
- [Code Explanation Video](https://drive.google.com/file/d/110Gtf1KIIQUZE2mPn8sBltA_3ysoikfC/view?usp=sharing)

---

This updated README now includes placeholders for the video links under the "Videos" section, which you can replace with the actual URLs to your explanation videos.
