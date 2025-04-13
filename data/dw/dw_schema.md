### Dimension Table: customers

| column_name     | data_type | description                          |
|-----------------|-----------|--------------------------------------|
| customer_id     | INTEGER   | Primary key, referenced by the sales table                          |
| name            | TEXT      | Full name of the customer (cannot be null)            |
| region          | TEXT      | Customer’s geographical region       |
| join_date       | TEXT      | Date the customer joined (YYYY-MM-DD)|
| loyalty_points  | INTEGER   | Number of loyalty points             |
| contact_method  | TEXT      | Preferred method of contact          |


### Dimension Table: products

| column_name      | data_type | description                        |
|------------------|-----------|------------------------------------|
| product_id       | INTEGER   | Primary key, referenced by the sales table                        |
| product_name     | TEXT      | Name of the product (cannot be null)|
| category         | TEXT      | Product category                   |
| unit_price_usd   | REAL      | Price per unit in USD (cannot be null)|
| stock_quantity   | INTEGER   | Quantity in stock                  |
| supplier         | TEXT      | Supplier of the product            |


### Fact Table: sales

| column_name      | data_type | description                                        |
|------------------|-----------|----------------------------------------------------|
| sale_id          | INTEGER   | Primary key                                        |
| sale_date        | TEXT      | Date of the sale                                   |
| customer_id      | INTEGER   | Foreign key, references the customers table                  |
| product_id       | INTEGER   | Foreign key, references the products table                    |
| store_id         | INTEGER   | ID of the store where the sale occurred            |
| campaign_id      | INTEGER   | ID of the campaign associated with the sale        |
| sale_amount_usd  | INTEGER   | Amount of the sale in USD (cannot be null)         |
| bonus_points     | INTEGER   | Loyalty points awarded for the sale                |
| payment_type     | TEXT      | Method of payment used                             |
