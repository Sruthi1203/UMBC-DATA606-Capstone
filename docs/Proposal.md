
# UMBC DATA606 Capstone –  Retail Analytics and Forecasting – a Machine Learning Approach


**Project Preface:** Optimizing Retail Assortment, Planograms, and Demand Forecasting using Walmart Sales Data  

**Prepared for:** Dr. Chaojie (Jay) Wang  

**Author:** Sruthi Kapudasi 

**GitHub Repository:** https://github.com/Sruthi1203/UMBC-DATA606-Capstone/blob/main/docs/Proposal.md

**LinkedIn Profile:** https://www.linkedin.com/in/sruthi-kapudasi/

**PowerPoint Presentation:** https://1drv.ms/p/c/adc96775138c6f23/Eb3UQikATjhAuOKxIAfoBqUBQM5KsEkwXa7WNBDljEiJvQ?e=INFV5L

**Youtube Link:** https://youtu.be/K85N9Bf_TpQ

---

## Background

This project focuses on analyzing Walmart’s transaction-level retail data from **January–September 2024** to understand product performance, customer behavior, and the impact of promotions, holidays, and weather.  
The primary objective is to build a **time-series forecasting model** that predicts **sales for next year** at a **product × store** level.


---

## Project Objective

The goal of this project is to get accurate sales forecasting helps retail managers make decisions on:
- Inventory planning & replenishment  
- Promotion strategy  
- Reducing stockouts  
- Understanding customer purchasing patterns  
- Improving operational efficiency 

---

## Why it Matters

Accurate assortment and planogram decisions directly impact:  
- **Retailers** → Increased sales and improved shelf productivity.  
- **Suppliers** → Better visibility of high-performing products.  
- **Customers** → Reduced stockouts, improved shopping experience.  
- **Businesses** → Stronger margins and operational efficiency.  

---

## Research Questions

1. Which product categories, stores, and products are top/bottom performers?  
2. How do promotions, holidays, customer loyalty, and weather influence sales?  
3. Can we forecast weekly sales demand for  2025 using  2024 data?  
4. What are the most important features that drive retail demand?  
5. Can a store owner use this model to plan inventory and reduce out-of-stock events? 

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


| Column Name | Data Type | Description | Example Values |
|-------------|-----------|-------------|----------------|
| `product_id` | int/string | Unique product identifier | 101, 202 |
| `product_name` | string | Name of the product | "Organic Apples" |
| `category` | string | Product category | "Grocery", "Electronics" |
| `quantity_sold` | int | Units sold in the transaction | 1, 3 |
| `unit_price` | float | Price per unit | 4.99 |
| `transaction_date` | datetime | Date of purchase | 2024-03-15 |
| `store_id` | int/string | Store identifier | 5, "NY03" |
| `store_location` | string | City or region of store | "Houston", "Dallas" |
| `inventory_level` | int | Inventory available at time of sale | 120 |
| `reorder_quantity` | int | Next reorder quantity | 40 |
| `supplier_lead_time` | int | Days required to restock | 7 |
| `customer_age` | int | Age of customer | 34 |
| `customer_gender` | string | Gender | "M", "F" |
| `customer_income` | float | Annual income | 55000 |
| `customer_loyalty_level` | string | Loyalty tier | "Silver", "Gold" |
| `payment_method` | string | Mode of payment | "Card", "Cash" |
| `promotion_applied` | int (0/1) | Whether promo used | 0, 1 |
| `promotion_type` | string | Type of promotion | "BOGO", "PriceCut" |
| `weather_conditions` | string | Weather during purchase | "Sunny", "Rainy" |
| `holiday_indicator` | int (0/1) | If purchase was on a holiday | 0, 1 |
| `weekday` | int | Day number | 1–7 |
| `stockout_indicator` | int (0/1) | Whether product was stocked-out | 0, 1 |
| `year` | int | Extracted year | 2024 |
| `month` | int | Month of year | 1–12 |
| `day` | int | Day of month | 1–31 |
| `dayofweek` | int | Numeric weekday | 0–6 |
| `is_weekend` | int | Weekend flag | 0, 1 |
| `cost_of_goods` | float | Derived feature = quantity × price | 15.75 |

---

### Target Variables and Feature Candidates

**Primary ML Tasks:**
- **Demand Forecasting (Time Series / Regression)**  
  - Target: `quantity_sold` aggregated at product/department level  
  - Features: `promotion_applied`, `holiday_indicator`, `weather_conditions`, `unit_price`, lagged sales  

This becomes the **label (y)** for all machine learning models.


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
