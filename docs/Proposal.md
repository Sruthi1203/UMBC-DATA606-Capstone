
📄 Proposal: Smart Retail Assortment & Shelf Analytics
1. Title and Author

Project Title: Smart Retail Assortment, Planogram Optimization, and Sales Forecasting with Walmart Data

Prepared for: UMBC Data Science Master Degree Capstone by Dr. Chaojie (Jay) Wang

Author: Sruthi Kapudasi

GitHub Repo: 

LinkedIn: 

PowerPoint Presentation: 

YouTube Video: 

2. Background
What is it about?

This project focuses on developing a retail analytics system that helps optimize product assortment, design efficient planograms (POGs), and forecast sales demand. Using real-world Walmart operational and sales data, the project will explore how data-driven decisions can improve profitability, reduce stockouts, and maximize shelf efficiency.

Why does it matter?

Retailers face continuous challenges with:

Managing thousands of SKUs across multiple departments.

Balancing inventory levels to avoid overstock and stockouts.

Designing planograms that maximize sales within limited shelf space.

Forecasting demand to improve replenishment and profitability.

A data science solution that integrates assortment analysis, planogram design, and demand forecasting can provide actionable insights to retail managers and store planners, ultimately improving customer satisfaction and profitability.

Research Questions

Which products are the top and bottom performers within each department?

How much shelf space should be allocated to each product (planogram) given a linear-foot constraint?

How can machine learning models forecast demand at the department, class, and product level for the next 12 months?

What would be the impact of demand forecasts on profit & loss (P&L) at the item level?

3. Data
Data Sources

Walmart Dataset (Kaggle): https://www.kaggle.com/datasets/ankitrajmishra/walmart

Data Size & Shape

~5,000 rows × ~20 columns (after cleaning: 5,000 rows × 15 columns kept).

File size: ~2 MB (CSV).

Time Period

Transaction dates span across 2024 (synthetic data designed for demonstration).

Row Representation

Each row represents a product sale event at a store with associated attributes (product, sales, promotions, weather, inventory).

Data Dictionary (Key Columns Kept)
Column	Type	Definition	Example Values
transaction_date	datetime	Date & time of sale	2024-03-31 21:46:00
product_id	int	Unique identifier for each product	843
product_name	string	Product description	Fridge
category	string	Department/class of product	Electronics
quantity_sold	int	Number of units sold in this transaction	3
unit_price	float	Price per unit at time of transaction	188.46
inventory_level	int	Current inventory level of the product	246
reorder_point	int	Threshold to trigger reorder	116
reorder_quantity	int	Quantity ordered when reorder is triggered	170
stockout_indicator	bool	Flag if product is stocked out	True / False
promotion_applied	bool	Whether a promotion was applied	True / False
promotion_type	string	Type of promotion	Percentage Discount / None
holiday_indicator	bool	Whether transaction occurred on a holiday	True / False
weather_conditions	string	Weather during the transaction	Sunny, Rainy, Stormy
customer_id	int	Unique ID of customer	2824
customer_loyalty_level	string	Loyalty tier of the customer	Silver, Gold, Platinum, Bronze
payment_method	string	Payment type used	Credit Card, Cash, Digital Wallet
Target / Label Variable

For Forecasting: quantity_sold (units) and sales_value (derived as quantity_sold × unit_price).

For POG Optimization: % sales contribution per product within each department.

Feature Variables (Predictors)

category, product_name

inventory_level, reorder_point, reorder_quantity

promotion_applied, promotion_type

holiday_indicator, weather_conditions

customer_loyalty_level, payment_method

✅ At this point, your proposal covers Sections 1, 2, 3 as required.

Next steps (not in proposal yet but for you):

Create a Jupyter Notebook in notebooks/ → load Walmart dataset, run cleaning steps, calculate sales_value, and do first-level summaries.
