import csv
import json
import os
from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import time
import requests

load_dotenv()

api_key = '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'
if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

graph_config = {
    "llm": {
        "model": "groq/llama3-70b-8192",
        "api_key": api_key,
        "temperature": 0,
    },
    "verbose": True,
}

def scrape_product_flipkart(product, spec):
    query = f"{product} {spec}".replace(" ", "%20")
    source_url = f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    prompt = f"""
    Extract the prices of {product} {spec} from the Flipkart webpage. Extract only if the product name and specs match exactly.
    Return the result in JSON format:
    {{
        "products": [
            {{
                "name": "<product_name>",
                "price": "<price>",
                "buy_link": "<link>"
            }}
        ]
    }}
    """
    return scrape_graph(prompt, source_url, product, spec, "Flipkart")

def scrape_product_amazon(product, spec):
    query = f"{product} {spec}".replace(" ", "+")
    source_url = f"https://www.amazon.in/s?k={query}&ref=nb_sb_noss"
    prompt = f"""
    Extract the prices of {product} {spec} from the Amazon India webpage. Extract only if the product name and specs match exactly.
    Return the result in JSON format:
    {{
        "products": [
            {{
                "name": "<product_name>",
                "price": "<price>",
                "buy_link": "<link>"
            }}
        ]
    }}
    """
    return scrape_graph(prompt, source_url, product, spec, "Amazon")

def scrape_graph(prompt, source_url, product, spec, platform_name):
    smart_scraper_graph = SmartScraperGraph(prompt=prompt, source=source_url, config=graph_config)
    try:
        result = smart_scraper_graph.run()
        try:
            parsed_result = json.loads(result)
            return parsed_result.get("products", [])
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON from {platform_name} for {product} {spec}: {result}")
            return []
    except Exception as e:
        print(f"[ERROR] Scraping failed for {platform_name} - {product} {spec}: {e}")
        return []

def communicate_with_google_api(data):
    url = "YOUR_GOOGLE_API_URL"
    headers = {"Authorization": f"Bearer YOUR_API_KEY"}
    query = """
    Given the scraped data for products from Flipkart and Amazon, find the best price for each product.
    For each product, compare the prices from both platforms and return the product with the lowest price, including the platform and buy link.
    """
    data_to_send = {
        "query": query,
        "data": data
    }
    try:
        response = requests.post(url, json=data_to_send, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def process_and_summarize(input_csv_path):
    combined_results = []

    try:
        with open(input_csv_path, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = row.get("Product", "").strip()
                spec = row.get("Spec", "").strip()

                if not product or not spec:
                    print(f"[WARNING] Missing product or spec in row: {row}")
                    continue

                flipkart_data = scrape_product_flipkart(product, spec)
                amazon_data = scrape_product_amazon(product, spec)

                for item in flipkart_data:
                    combined_results.append({
                        "Product": product,
                        "Spec": spec,
                        "Name": item.get("name", ""),
                        "Price": parse_price(item.get("price", "")),
                        "Platform": "Flipkart",
                        "Buy Link": item.get("buy_link", "")
                    })

                for item in amazon_data:
                    combined_results.append({
                        "Product": product,
                        "Spec": spec,
                        "Name": item.get("name", ""),
                        "Price": parse_price(item.get("price", "")),
                        "Platform": "Amazon",
                        "Buy Link": item.get("buy_link", "")
                    })

                time.sleep(2)
    except Exception as e:
        print(f"[ERROR] Error processing input CSV: {e}")
        return

    ai_response = communicate_with_google_api(combined_results)
    if ai_response:
        print("AI Response:", ai_response)
    else:
        print("Failed to communicate with Google AI Studio API")

def parse_price(price_str):
    try:
        return float(price_str.replace("₹", "").replace(",", "").strip())
    except ValueError:
        return float('inf')

input_csv_path = "products.csv"
process_and_summarize(input_csv_path)
