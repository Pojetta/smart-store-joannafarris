from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from pathlib import Path

# Define paths using pathlib
PROJECT_ROOT = Path(__file__).resolve().parent.parent
JDBC_JAR_PATH = PROJECT_ROOT / "lib" / "sqlite-jdbc-3.49.1.0.jar"
DB_PATH = PROJECT_ROOT / "data" / "dw" / "smart_sales.db"

# Check if JDBC JAR exists
if not JDBC_JAR_PATH.exists():
    print(f"JDBC JAR file not found at {JDBC_JAR_PATH}")
else:
    print(f"Using JDBC JAR from: {JDBC_JAR_PATH}")

# Create SparkSession with the JDBC jar
spark = SparkSession.builder \
    .appName("SQLiteTest") \
    .config("spark.jars", str(JDBC_JAR_PATH)) \
    .config("spark.driver.extraClassPath", str(JDBC_JAR_PATH)) \
    .getOrCreate()

# Set Spark's log level to WARN to reduce output
spark.sparkContext.setLogLevel("ERROR")

try:
    # Define the JDBC URL
    DB_URL = f"jdbc:sqlite:{str(DB_PATH)}"

    # Read from the SQLite database
    df = spark.read.format("jdbc") \
        .option("url", DB_URL) \
        .option("dbtable", "product") \
        .option("driver", "org.sqlite.JDBC") \
        .load()


    df.show()

except Exception as e:
    print(f"Error loading data: {e}")

finally:
    spark.stop()
