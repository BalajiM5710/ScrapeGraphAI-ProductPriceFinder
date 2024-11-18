import csv
from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import os
import json
import re
import pandas as pd

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
        "temperature": 0,  # Adjust temperature for LLM creativity (0 for deterministic output)
    },
    "verbose": True,
}

# Function to scrape data for a single product-spec combination
def scrape_product(product, spec):
    # Update the Flipkart URL dynamically
    query = f"{product} {spec}".replace(" ", "%20")
    source_url = f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    
    # Update the prompt dynamically
    prompt = f"""Extract the prices of {product} {spec} from the Flipkart webpage. extract only if the product name and specs given to you truly matches the product name in the flipkart web and return the result in the following JSON format:
    {{
        "products": [
            {{
                "name": "<product_name>",
                "price": "<price>",
                "buy_link": "<link>"
            }}
        ]
    }}"""
    
    # Initialize the SmartScraperGraph
    smart_scraper_graph = SmartScraperGraph(
        prompt=prompt,
        source=source_url,
        config=graph_config
    )
    
    # Run the scraper
    try:
        result = smart_scraper_graph.run()
        try:
            # Parse the JSON output
            parsed_result = json.loads(result)
            return parsed_result.get("products", [])
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON for {product} {spec}")
            return []
    except Exception as e:
        print(f"Error during scraping for {product} {spec}: {e}")
        return []

# Read input CSV and scrape data for each row
input_csv_path = "products.csv"  # Replace with your input CSV path
output_csv_path = "output.csv"  # Output CSV path

results = []

try:
    with open(input_csv_path, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product = row["Product"]
            spec = row["Spec"]
            scraped_data = scrape_product(product, spec)
            
            for item in scraped_data:
                results.append({
                    "Product": product,
                    "Spec": spec,
                    "Name": item.get("name", ""),
                    "Price": item.get("price", ""),
                    "Buy Link": item.get("buy_link", "")
                })
except Exception as e:
    print(f"Error reading the input CSV: {e}")

# Write results to the output CSV
try:
    df = pd.DataFrame(results)
    df.to_csv(output_csv_path, index=False)
    print(f"Scraping results saved to {output_csv_path}")
except Exception as e:
    print(f"Error writing the output CSV: {e}")