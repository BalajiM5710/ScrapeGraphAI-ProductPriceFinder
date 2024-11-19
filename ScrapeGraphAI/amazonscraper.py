import json
from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import os
import csv
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

# Function to scrape data for a single product-spec combination from Amazon
def scrape_product_amazon(product, spec):
    # Update the Amazon URL dynamically
    query = f"{product} {spec}".replace(" ", "+")
    source_url = f"https://www.amazon.in/s?k={query}&ref=nb_sb_noss"
    
    # Update the prompt dynamically for Amazon
    prompt = f"""Extract the prices of {product} {spec} from the Amazon India webpage. 
    Extract only if the {product} {spec} are the same as {product} {spec} found in Amazon search results and return the results in the following JSON format:
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
output_json_path = "output_amazon.json"  # Output JSON path

results = []

try:
    with open(input_csv_path, mode="r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product = row["Product"]
            spec = row["Spec"]
            scraped_data = scrape_product_amazon(product, spec)
            
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

# Write results to the output JSON
try:
    with open(output_json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(results, jsonfile, ensure_ascii=False, indent=4)
    print(f"Scraping results saved to {output_json_path}")
except Exception as e:
    print(f"Error writing the output JSON: {e}")
