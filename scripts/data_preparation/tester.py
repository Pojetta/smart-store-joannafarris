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
    df_customers = scrubber.parse_dates_to_add_standard_datetime('JoinDate')
    #df_customers = scrubber.filter_column_outliers()

    # Save prepared data
    save_prepared_data(df_customers, "data/prepared/customers_data_prepared.csv")

def save_prepared_data(df, path):
    df.to_csv(path, index=False)
    logger.info(f"Data saved to {path}")

if __name__ == "__main__":
    prepare_customer_data()

Results of mine:
CustomerID,Name,Region,JoinDate,LoyaltyPoints,PreferredContactMethod,StandardDateTime
1001,William White,East,11/11/21,150,Text,2021-11-11
1002,Wylie Coyote,East,2/14/23,240,Text,2023-02-14
1003,Dan Brown,West,10/19/23,330,Text,2023-10-19
1004,Chewbacca,West,11/9/22,285,Text,2022-11-09
1005,Dr Who,North,8/18/23,315,Call,2023-08-18
1006,Tiffany James,South,6/7/21,60,Text,2021-06-07
1007,Susan Johnson,South,6/30/23,30,Email,2023-06-30
1008,Tony Stark,North,5/1/20,345,Text,2020-05-01
1009,Jason Bourne,West,12/1/20,405,Email,2020-12-01
1010,Hermione Granger,East,12/9/22,90,Text,2022-12-09
1011,Hermione Grager,East,12/9/22,150,Text,2022-12-09

CustomerID,Name,Region,JoinDate,LoyaltyPoints,PreferredContactMethod
1001,William White,East,11/11/21,150,Text
1002,Wylie Coyote,East,2/14/23,240,Text
1003,Dan Brown,West,10/19/23,330,Text
1004,Chewbacca,West,11/9/22,285,Text
1005,Dr Who,North,8/18/23,315,Call
1006,Tiffany James,South,6/7/21,60,Text
1007,Susan Johnson,South,6/30/23,30,Email
1008,Tony Stark,North,5/1/20,345,Text
1009,Jason Bourne,West,12/1/20,405,Email
1010,Hermione Granger,East,12/9/22,90,Text
1011,Hermione Grager,East,12/9/22,150,Text

CustomerID,Name,Region,JoinDate,LoyaltyPoints,PreferredContactMethod
1001,William White,East,11/11/21,150,Text
1002,Wylie Coyote,East,2/14/23,240,Text
1003,Dan Brown,West,10/19/23,330,Text
1004,Chewbacca,West,11/9/22,285,Text
1005,Dr Who,North,8/18/23,315,Call
1006,Tiffany James,South,6/7/21,60,Text
1007,Susan Johnson,South,6/30/23,30,Email
1008,Tony Stark,North,5/1/20,345,Text
1009,Jason Bourne,West,12/1/20,405,Email
1010,Hermione Granger,East,12/9/22,90,Text
1011,Hermione Grager,East,12/9/22,150,Text

"""
scripts/data_preparation/prepare_customers_data.py

This script reads customer data from the data/raw folder, cleans the data, 
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove outliers
- Ensure consistent formatting

-----------------------------------
How to Run:
1. Open a terminal in the main root project folder.
2. Activate the local project virtual environment.
3. Choose the correct commands for your OS to run this script:

Example (Windows/PowerShell) - do NOT include the > prompt:
> .venv\Scripts\activate
> py scripts\data_preparation\prepare_customers_data.py

Example (Mac/Linux) - do NOT include the $ prompt:
$ source .venv/bin/activate
$ python3 scripts/data_preparation/prepare_customers_data.py

NOTE: I use the ruff linter. 
It warns if all import statements are not at the top of the file.  
I was having trouble with the relative paths, so I  
temporarily add the project root before I can import. 
By adding this comment at the end of an import line noqa: E402
ruff will ignore the warning on just that line. 
"""

import pathlib
import sys
import pandas as pd

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger  # noqa: E402

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("prepared")

# -------------------
# Reusable Functions
# -------------------

def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw data from CSV.

    Args:
        file_name (str): Name of the CSV file to read.
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")
    file_path = RAW_DATA_DIR.joinpath(file_name)
    logger.info(f"Reading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")
    return df

def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save cleaned data to CSV.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        file_name (str): Name of the output file.
    """
    logger.info(f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}")
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.
    How do you decide if a row is duplicated?
    Which do you keep? Which do you delete?

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")
    initial_count = len(df)
    df = df.drop_duplicates()
    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} duplicate rows")
    logger.info(f"{len(df)} records remaining after removing duplicates.")
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values by filling or dropping.
    This logic is specific to the actual data and business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logger.info(f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}")
    
    # Log missing values count before handling
    missing_before = df.isna().sum().sum()
    logger.info(f"Total missing values before handling: {missing_before}")
    
    # TODO: Fill or drop missing values based on business rules
    # Example:
    # df['CustomerName'].fillna('Unknown', inplace=True)
    # df.dropna(subset=['CustomerID'], inplace=True)
    
    # Log missing values count after handling
    missing_after = df.isna().sum().sum()
    logger.info(f"Total missing values after handling: {missing_after}")
    logger.info(f"{len(df)} records remaining after handling missing values.")
    return df

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers based on thresholds.
    This logic is very specific to the actual data and business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")
    initial_count = len(df)
    
    # TODO: Define numeric columns and apply rules for outlier removal
    # Example:
    # df = df[(df['Age'] > 18) & (df['Age'] < 100)]
    
    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} outlier rows")
    logger.info(f"{len(df)} records remaining after removing outliers.")
    return df


def main() -> None:
    """
    Main function for processing customer data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_customers_data.py")
    logger.info("==================================")

    logger.info(f"Root project folder: {PROJECT_ROOT}")
    logger.info(f"data / raw folder: {RAW_DATA_DIR}")
    logger.info(f"data / prepared folder: {PREPARED_DATA_DIR}")
    logger.info(f"scripts folder: {PROJECT_ROOT.joinpath('scripts')}")

    input_file = "customers_data.csv"
    output_file = "customers_data_prepared.csv"
    
    # Read raw data
    df = read_raw_data(input_file)

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")
    
    # Clean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip()
    
    # Log if any column names changed
    changed_columns = [f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Remove duplicates
    df = remove_duplicates(df)

    # Handle missing values
    df = handle_missing_values(df)

    # Remove outliers
    df = remove_outliers(df)

    # Save prepared data
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info("FINISHED prepare_customers_data.py")
    logger.info("==================================")

# -------------------
# Conditional Execution Block
# -------------------

if __name__ == "__main__":
    main()

