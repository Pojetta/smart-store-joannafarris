import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger  # Custom logger # noqa: E402

# Paths
DATA_DIR = PROJECT_ROOT / "data"
PREPARED_DATA_DIR = DATA_DIR / "prepared"
DW_DIR = DATA_DIR / "dw"
DW_DIR.mkdir(exist_ok=True)
DB_PATH = DW_DIR / "smart_sales.db"

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Create tables in the data warehouse if they don't exist."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            region TEXT,
            join_date TEXT,
            loyalty_points INTEGER,
            preferred_contact_method TEXT  
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            unit_price_usd REAL NOT NULL,
            stock_quantity INTEGER, 
            supplier TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY,
            sale_date TEXT,
            customer_id INTEGER,
            product_id INTEGER,
            store_id INTEGER,
            campaign_id INTEGER,
            sale_amount_usd INTEGER NOT NULL,
            bonus_points INTEGER,
            payment_type TEXT,        
            FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
            FOREIGN KEY (product_id) REFERENCES product(product_id)
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sales tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sales")

def insert_data(df, table_name, cursor):
    logger.info(f"Inserting data into {table_name} table...")
    df.to_sql(table_name, cursor.connection, if_exists="append", index=False)
    

def load_data_to_db() -> None:
    try:
        # Connect to SQLite – will create the file if it doesn't exist
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create schema and clear existing records
        create_schema(cursor)
        delete_existing_records(cursor)

        # Load prepared data using pandas
        customers_df = pd.read_csv(PREPARED_DATA_DIR / "customers_data_prepared.csv")
        products_df = pd.read_csv(PREPARED_DATA_DIR / "products_data_prepared.csv")
        sales_df = pd.read_csv(PREPARED_DATA_DIR / "sales_data_prepared.csv")
        logger.info(f"Customers DataFrame shape: {customers_df.shape}")
        logger.info(f"Products DataFrame shape: {products_df.shape}")
        logger.info(f"Sales DataFrame shape: {sales_df.shape}")


        # Rename customer columns to match table schema
        customers_df.rename(columns={
            "CustomerID": "customer_id",
            "Name": "name",
            "Region": "region",
            "JoinDate": "join_date",
            "LoyaltyPoints": "loyalty_points",
            "PreferredContactMethod": "preferred_contact_method"
        }, inplace=True)
       
        # Rename product columns to match table schema
        products_df.rename(columns={
            "productid": "product_id",
            "productname": "product_name",
            "category": "category",
            "unitprice": "unit_price_usd",
            "stockquantity": "stock_quantity",
            "supplier": "supplier"
        }, inplace=True)

        # Rename sales columns to match table schema
        sales_df.rename(columns={
            "transactionid": "sale_id",
            "saledate": "sale_date",
            "customerid": "customer_id",
            "productid": "product_id",
            "storeid": "store_id",
            "campaignid": "campaign_id",
            "saleamount": "sale_amount_usd",
            "bonuspoints": "bonus_points",
            "paymenttype": "payment_type"
        }, inplace=True)

        # Insert data into the database
        insert_data(customers_df, "customer", cursor)
        insert_data(products_df, "product", cursor)
        insert_data(sales_df, "sales", cursor)
        logger.info("Data successfully loaded into warehouse.")

    except sqlite3.Error as e:
        logger.error(f"Error connecting to the database: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()