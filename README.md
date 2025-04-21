# smart-store-joannafarris

This project explores Business Intelligence (BI) concepts using Python, Spark, and SQLite. It focuses on extracting, transforming, and analyzing sales data for a fictional smart store to uncover insights that support real business decisions.

---

## ✅ Project Setup (Initial Weeks)

This section summarizes how the project environment was created and organized.

### Repository Initialization
- Create a new GitHub repository with a default README.
- Clone the repo into a `Projects` folder on macOS:
   ```bash
   cd ~
   mkdir Projects
   cd Projects
   git clone https://github.com/Pojetta/smart-store-joannafarris
### Python Environment Setup
- Create and activate a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```
- Install dependencies
```
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
```

### Project Structure
- `data/raw/` – Original CSV files
- `data/prepared/` – Cleaned and transformed data
- `data/dw/` – SQLite data warehouse
- `scripts/` – Python scripts for data prep and OLAP analysis
- `utils/` – Shared utilities like logging

---

## 📊 P6 OLAP Analysis Project

### **Section 1: The Business Goal**

**Goal:**  
Understand regional and category-based sales performance in order to make smarter inventory distribution decisions for the upcoming quarter.

**Why it matters:**  
Knowing which products sell best in which regions allows the business to align inventory more effectively, reducing waste and improving availability where demand is highest.

---

### **Section 2: Data Source**

- **Source:** Data warehouse built from raw CSV files using SQLite
- **Accessed using:** Spark and JDBC
- **Tables used:**
  - `sales`: includes sale date, store ID, product ID, customer ID, and sales amount
  - `product`: includes product ID and category
  - `customer`: includes customer ID and region

---

### **Section 3: Tools**

- **JupyterLab** for step-by-step analysis
- **Python with PySpark** for data transformation and OLAP operations
- **SQLite** as the data warehouse backend
- **Seaborn / Matplotlib** for visualizations

This toolset provided flexibility, transparency, and reusability while supporting deep data exploration.

---

### **Section 4: Workflow & Logic**

- Started a Spark session and connected to the SQLite data warehouse
- Loaded the `sales`, `product`, and `customer` tables
- Performed slicing by filtering sales from 2023 onward
- Diced the data by:
  - Product category and **store-based** region (mapped from `store_id`)
  - Product category and **customer-based** region (from the `customer` table)
- Performed drilldowns by:
  - Year → Quarter → Month (based on `sale_date`)
- Aggregated sales using `SUM(sale_amount_usd)`
- Visualized the results using grouped bar charts and line charts

---

### **Section 5: Results**

- A **grouped bar chart** revealed total sales by product category and store region
- A **line chart** showed month-by-month sales trends
- Significant differences appeared between store-region and customer-region groupings
- Monthly trends showed consistent drops and spikes that may be seasonal

---

### **Section 6: Suggested Business Action**

- Adjust inventory distribution based on region-category performance
- Increase supply in regions where certain product categories outperform
- Consider region-specific promotions informed by customer-region trends

---

### **Section 7: Challenges**

- Resolving column conflicts during joins required careful use of table aliases
- Mapping `store_id` to `region` involved hardcoding logic in Spark
- Maintaining consistent aggregation levels during drilldowns took extra validation


