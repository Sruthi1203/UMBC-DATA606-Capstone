
# UMBC DATA606 Capstone –  Retail Analytics and Forecasting – a Machine Learning Approach


**Project Preface:** Optimizing Retail Assortment, Planograms, and Demand Forecasting using Walmart Sales Data  

**Prepared for:** Dr. Chaojie (Jay) Wang  

**Author:** Sruthi Kapudasi 

**GitHub Repository:** https://github.com/Sruthi1203/UMBC-DATA606-Capstone/blob/main/docs/Proposal.md

**LinkedIn Profile:** https://www.linkedin.com/in/sruthi-kapudasi/

**PowerPoint Presentation:** 

---

## Background

Retailers like Walmart manage thousands of products across diverse departments and must balance **inventory, shelf space, and customer demand** to stay profitable. Poor assortment choices, inefficient shelf layouts (planograms), or inaccurate demand forecasts can lead to **stockouts, overstocks, and revenue loss**.  

This project leverages Walmart sales data to perform **assortment analysis, planogram optimization, demand forecasting, and profit simulations** to support better decision-making for inventory and merchandising teams.  

---

## Project Objective

The goal of this project is to design a **data-driven retail analytics system** that can:  
1. Identify **top and bottom performers** in each department.  
2. Recommend **optimized assortments** that maximize sales and minimize low-sellers.  
3. Generate **dynamic planograms (POGs)** based on store shelf constraints.  
4. Forecast **monthly demand for the next 12 months** using ML models.  
5. Simulate **Profit & Loss (P&L)** outcomes under different assortment and forecast scenarios.  

---

## Why it Matters

Accurate assortment and planogram decisions directly impact:  
- **Retailers** → Increased sales and improved shelf productivity.  
- **Suppliers** → Better visibility of high-performing products.  
- **Customers** → Reduced stockouts, improved shopping experience.  
- **Businesses** → Stronger margins and operational efficiency.  

---

## Research Questions

1. **Can Walmart’s product assortment be improved?**  
2. **How can we restructure planograms efficiently?**  
3. **Can machine learning methods reliably forecast demand for the next 12 months?**  
4. **What’s the P&L impact with the updated assortment?**  

---

## Data

### Data Source:
- **Walmart Sales Dataset** (From Kaggle) : https://www.kaggle.com/datasets/ankitrajmishra/walmart: 5000 rows x 28 columns

### Data Overview:
- **Dataset size:** ~5,000 rows
- **Shape:** 5,000 rows × 28 columns  
- **Time period:** Transactions across a year (2024)  
- **Observation unit:** Each row represents a sales transaction for a product  

### Column Data Types and Dictionary

| Column Name | Data Type | Definition | Example Values |
|-------------|-----------|------------|----------------|
| transaction_date | datetime | Timestamp of transaction | 2024-03-31 21:46 |
| product_id | int | Unique identifier for product | 843 |
| product_name | string | Product description | Fridge, TV |
| category | string | Product department/category | Electronics |
| quantity_sold | int | Units sold in transaction | 3 |
| unit_price | float | Retail price of product | 499.28 |
| inventory_level | int | Current available stock | 412 |
| reorder_point | int | Stock threshold to reorder | 99 |
| reorder_quantity | int | Quantity ordered when triggered | 177 |
| stockout_indicator | bool | True if item stocked out | True |
| promotion_applied | bool | True if promotion applied | False |
| promotion_type | string | Promotion type (if any) | Percentage Discount |
| holiday_indicator | bool | Transaction during holiday | True |
| weather_conditions | string | Weather context | Sunny, Rainy |
| customer_id | int | Unique identifier for customer | 4657 |
| customer_loyalty_level | string | Customer loyalty tier | Silver |
| payment_method | string | Mode of payment | Credit Card |
| sales_value | float | Transaction sales value | 3052.72 |

---

### Target Variables and Feature Candidates

**Primary ML Tasks:**
- **Demand Forecasting (Time Series / Regression)**  
  - Target: `quantity_sold` aggregated at product/department level  
  - Features: `promotion_applied`, `holiday_indicator`, `weather_conditions`, `unit_price`, lagged sales  

**Secondary Tasks:**
- **Assortment Optimization** → Identify low-sellers (bottom performers) and recommend assortment refinement  
- **Planogram Simulation** → Use `linear feet`, `shelves`, and `facings` to allocate products  

---

## Features

**Sales & Inventory Features:**  
- Quantity sold, unit price, sales value  
- Inventory levels, reorder point, reorder quantity  
- Stockout frequency  

**Customer & Context Features:**  
- Loyalty level, payment method  
- Holiday flag, weather conditions  
- Promotion type applied  

**Engineered Features:**  
- Weekly and monthly aggregated sales  
- Sell-through % (sales / inventory)  
- Contribution % to department sales  
- Forecasted demand (12 months forward)
  
Together, they enable more accurate forecasting, better inventory management, and optimized sales strategies.
---
