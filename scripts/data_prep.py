"""
Module 3: Data Preparation Script
File: scripts/data_prep.py

This script triggers individual data preparation processes for
customer, product, and sales data by calling the relevant scripts.

To run it, open a terminal in the root project folder.
Activate the local project virtual environment.
Choose the correct command for your OS to run this script.

python3 scripts/data_prep.py
"""

import pathlib
import sys
import subprocess
import os

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Import logger from utils
from utils.logger import logger  # noqa: E402

# Define script paths
SCRIPTS_DIR = PROJECT_ROOT.joinpath("scripts/data_preparation")

def run_script(script_name):
    """Run a data preparation script."""
    script_path = SCRIPTS_DIR.joinpath(script_name)

    # Set the PYTHONPATH to include the project root for subprocesses
    env = os.environ.copy()
    env['PYTHONPATH'] = str(PROJECT_ROOT)

    result = subprocess.run(
        ["python3", str(script_path)],
        capture_output=True,
        text=True,
        env=env  # Pass the modified environment to subprocess
    )

    if result.returncode == 0:
        logger.info(f"Successfully executed {script_name}")
    else:
        logger.error(f"Error executing {script_name}: {result.stderr}")

def main():
    """Main function to run all data preparation scripts."""
    logger.info("======================")
    logger.info("STARTING data_prep.py")
    logger.info("======================")

    scripts_to_run = [
        "prepare_customer_data.py",
        "prepare_product_data.py",
        "prepare_sales_data.py",
    ]

    for script in scripts_to_run:
        logger.info(f"Running {script}...")
        run_script(script)

    logger.info("======================")
    logger.info("FINISHED data_prep.py")
    logger.info("======================")

if __name__ == "__main__":
    main()
