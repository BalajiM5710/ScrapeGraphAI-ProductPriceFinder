import csv
import json
import os
from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import pandas as pd
import time

# Load environment variables from a .env file
load_dotenv()

# Fetch GROQ API key from environment variables
api_key = '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'
if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Please set it in your .env file.")

# Define the configuration for ScrapeGraphAI
graph_config = {
    "llm": {
        "model": "groq/llama3-70b-8192",  # Replace with the correct GROQ model name
        "api_key": api_key,
        "temperature": 0,  # Adjust temperature for deterministic output
    },
    "verbose": True,
}

# Scraping function for Flipkart
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

# Scraping function for Amazon
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

# Helper function for scraping with SmartScraperGraph
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

# Function to process input CSV, scrape data, and save results
def process_and_scrape(input_csv_path, output_flipkart_csv, output_amazon_json):
    results_flipkart = []
    results_amazon = []
    
    try:
        with open(input_csv_path, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = row.get("Product", "").strip()
                spec = row.get("Spec", "").strip()

                if not product or not spec:
                    print(f"[WARNING] Missing product or spec in row: {row}")
                    continue

                # Scrape Flipkart
                flipkart_data = scrape_product_flipkart(product, spec)
                for item in flipkart_data:
                    results_flipkart.append({
                        "Product": product,
                        "Spec": spec,
                        "Name": item.get("name", ""),
                        "Price": item.get("price", ""),
                        "Buy Link": item.get("buy_link", ""),
                    })

                # Scrape Amazon
                amazon_data = scrape_product_amazon(product, spec)
                for item in amazon_data:
                    results_amazon.append({
                        "Product": product,
                        "Spec": spec,
                        "Name": item.get("name", ""),
                        "Price": item.get("price", ""),
                        "Buy Link": item.get("buy_link", ""),
                    })

                # Delay to prevent rate limiting
                time.sleep(2)
    except Exception as e:
        print(f"[ERROR] Error processing input CSV: {e}")

    # Write Flipkart results to CSV
    try:
        pd.DataFrame(results_flipkart).to_csv(output_flipkart_csv, index=False)
        print(f"[INFO] Flipkart results saved to {output_flipkart_csv}")
    except Exception as e:
        print(f"[ERROR] Error saving Flipkart results: {e}")

    # Write Amazon results to JSON
    try:
        with open(output_amazon_json, 'w', encoding='utf-8') as jsonfile:
            json.dump(results_amazon, jsonfile, ensure_ascii=False, indent=4)
        print(f"[INFO] Amazon results saved to {output_amazon_json}")
    except Exception as e:
        print(f"[ERROR] Error saving Amazon results: {e}")

# File paths
input_csv_path = "products.csv"
output_flipkart_csv = "output_flipkart.csv"
output_amazon_json = "output_amazon.json"

# Run the scraping process
process_and_scrape(input_csv_path, output_flipkart_csv, output_amazon_json)

