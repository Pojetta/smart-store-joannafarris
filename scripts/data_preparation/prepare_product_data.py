import pandas as pd
import logging
import pathlib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import DataScrubber class
from scripts.data_scrubber import DataScrubber  # Corrected import path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prepare_product_data():
    logger.info("Loading product data...")
    df_products = pd.read_csv("data/raw/products_data.csv")

    # Create an instance of DataScrubber and pass the dataframe to it
    scrubber = DataScrubber(df_products)

    # Apply data cleaning steps using the scrubber instance
    logger.info("Cleaning product data...")
    df_products = scrubber.remove_duplicate_records()

    # Save prepared data
    save_prepared_data(df_products, "data/prepared/products_data_prepared.csv")

def save_prepared_data(df, path):
    df.to_csv(path, index=False)
    logger.info(f"Data saved to {path}")

if __name__ == "__main__":
    prepare_product_data()
