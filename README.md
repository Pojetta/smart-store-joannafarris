# smart-store-joannafarris

This project creates a space for experimenting and learning about Business Intellegence.

All commands are for macOS.

## Project initialization
1. Create a new repository in GitHub with a default README file.
2. Create a Projects folder on your machine from your Home directory and clone your new repository to it:
```
cd ~
mkdir Projects
cd Projects
git clone https://github.com/Pojetta/smart-store-joannafarris
```
3. Open your project repository in VS Code.
4. Add a .gitignore file and a requirements.txt.
5. Create and activate a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```
6. Install dependencies
```
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
```

## Organize: Add raw data, basic scripts and log
1. With your project open in VS Code, create folders: data/raw, scripts, and utils
2. Create files within data/raw
   - customer_data.csv
   - products_data.csv
   - sales_data.csv
3. Copy and paste data from the data/raw files in the GitHub repo to your newly created data/raw files.
4. Create file within scripts
   - data_prep.py 
5. Copy and paste code from the scripts/data_prep.py file in the GitHub repo to your newly created data_prep.py file.
6. Create file within utils
   - logger.py
7. Copy and paste code from the logger.py file in the GitHub repo to your newly created logger.py file.

## Execute python script
```
python3 scripts/data_prep.py
```

