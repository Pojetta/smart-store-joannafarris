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

def prepare_customer_data():
    logger.info("Loading customer data...")
    df_customers = pd.read_csv("data/raw/customers_data.csv")

    # Create an instance of DataScrubber and pass the dataframe to it
    scrubber = DataScrubber(df_customers)

    # Apply data cleaning steps using the scrubber instance
    logger.info("Cleaning customer data...")
    df_customers = scrubber.remove_duplicate_records()
    df_sales = scrubber.parse_dates_to_add_standard_datetime('JoinDate')

    # Save prepared data
    save_prepared_data(df_customers, "data/prepared/customers_data_prepared.csv")

def save_prepared_data(df, path):
    df.to_csv(path, index=False)
    logger.info(f"Data saved to {path}")

if __name__ == "__main__":
    prepare_customer_data()
