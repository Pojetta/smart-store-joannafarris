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

def prepare_sales_data():
    logger.info("Loading sales data...")
    df_sales = pd.read_csv("data/raw/sales_data.csv")

    # Create an instance of DataScrubber and pass the dataframe to it
    scrubber = DataScrubber(df_sales)

    # Apply data cleaning steps using the scrubber instance
    logger.info("Cleaning sales data...")
    df_sales = scrubber.remove_duplicate_records()
    df_sales = scrubber.parse_dates_to_add_standard_datetime('SaleDate')

    # Save prepared data
    save_prepared_data(df_sales, "data/prepared/sales_data_prepared.csv")

def save_prepared_data(df, path):
    df.to_csv(path, index=False)
    logger.info(f"Data saved to {path}")

if __name__ == "__main__":
    prepare_sales_data()
