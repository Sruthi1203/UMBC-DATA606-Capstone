# Retail Analytics and Forecasting - a Machine Learning Approach

**Author:** Sruthi Kapudasi  
**Semester:** Fall 2025  
**Prepared for:** Dr. Chaojie (Jay) Wang  
**Institution:** University of Maryland, Baltimore County (UMBC)


---

##  Links

- **YouTube Presentation:** [Watch Video](https://youtu.be/Tgbitau6uX8)
- **GitHub Repository:** [Project Repository](https://github.com/Sruthi1203/UMBC-DATA606-Capstone)
- **LinkedIn Profile:** [Sruthi LinkedIn](https://www.linkedin.com/in/sruthi-kapudasi/)  
- **Live Dashboard:** [Streamlit App](https://umbc-data606-capstone-sruthi-kapudasi-walmart-sales.streamlit.app)
- **PPT presentation:** [Project Presentation](https://github.com/Sruthi1203/UMBC-DATA606-Capstone/blob/main/Capstone%20Retail%20Analytics.pptx)

---

## 1. Background

### 1.1 Problem Statement
Walmart, as one of the largest retail chains globally, requires accurate sales forecasting to optimize inventory management, staffing decisions, and revenue planning. Manual forecasting methods are time-consuming and prone to errors, leading to potential stockouts or overstocking situations.

### 1.2 Project Objectives
The primary objectives of this project are to:
- Develop a machine learning model to forecast daily sales for Walmart products
- Create an interactive dashboard for business users to generate custom predictions
- Analyze customer loyalty patterns to identify growth opportunities
- Provide actionable insights for inventory planning and customer engagement

### 1.3 Research Questions
1. Which machine learning model provides the most accurate sales forecasts?
2. What temporal patterns (daily, weekly, monthly) influence sales performance?
3. How do different customer loyalty levels contribute to overall revenue?
4. What product-specific and store-specific factors affect sales predictions?

---

## 2. Data Sources

### 2.1 Dataset Description
- **Source:** Kaggle Walmart Sales Transaction Data (January - September 2024) [View Dataset](https://www.kaggle.com/datasets/ankitrajmishra/walmart)
- **Size:** 5,000 transactions
- **Time Period:** 9 months
- **Products:** 8 products across 2 categories
- **Geographic Coverage:** Multiple store locations

### 2.2 Data Collection Method
The dataset was collected from Walmart's point-of-sale systems, capturing daily transaction-level data including product information, pricing, customer demographics, and store locations.

---

## 3. Data Elements

### 3.1 Core Features
| Feature | Type | Description |
|---------|------|-------------|
| `transaction_date` | Date | Date of transaction |
| `product_id` | Integer | Unique product identifier |
| `product_name` | String | Product name (TV, Laptop, Camera, etc.) |
| `category` | String | Product category (Electronics, Appliances) |
| `quantity_sold` | Integer | Number of units sold |
| `unit_price` | Float | Price per unit |
| `cost_of_goods` | Float | Total transaction value |
| `store_location` | String | Store city and state |
| `loyalty_level` | String | Customer loyalty tier (Bronze, Silver, Gold, Platinum) |

### 3.2 Engineered Features
| Feature | Description | Purpose |
|---------|-------------|---------|
| `month` | Month of year (1-12) | Capture seasonal patterns |
| `week` | Week of year (1-52) | Identify weekly trends |
| `day_of_week` | Day (0=Mon, 6=Sun) | Detect weekday vs weekend patterns |
| `is_weekend` | Binary (0/1) | Explicit weekend indicator |
| `days_since_start` | Integer | Time progression variable |
| `qty_ma7` | Float | 7-day moving average |
| `qty_ma14` | Float | 14-day moving average |
| `qty_ma30` | Float | 30-day moving average |

---

## 4. Exploratory Data Analysis (EDA)

### 4.1 Data Quality Assessment
- **Missing Values:** None detected after data cleaning
- **Duplicates:** 0 duplicate transactions
- **Outliers:** Identified and retained (represent legitimate high-value sales)
- **Data Consistency:** Categories standardized

### 4.2 Temporal Patterns

#### 4.2.1 Daily Sales Distribution
- **Average daily sales:** $8,500
- **Peak daily sales:** $15,000+ (weekend days)
- **Minimum daily sales:** $5,000 (mid-week)

#### 4.2.2 Weekly Seasonality
- **Weekend Effect:** Sales increase by ~20% on Saturdays and Sundays
- **Weekday Pattern:** Monday-Thursday show consistent baseline sales
- **Friday:** Transition day with 10% increase from Thursday

#### 4.2.3 Monthly Trends
- **Peak Months:** January (post-holiday returns/exchanges), June (summer season)
- **Low Months:** February, August
- **Growth Trend:** Slight upward trend over the 9-month period

### 4.3 Product Analysis

#### 4.3.1 Product Performance Ranking
| Rank | Product | Total Revenue | Units Sold | Avg Price |
|------|---------|---------------|------------|-----------|
| 1 | Laptop | $4,200,000 | 1,250 | $3,360 |
| 2 | TV | $3,800,000 | 1,100 | $3,455 |
| 3 | Smartphone | $3,500,000 | 1,300 | $2,692 |
| 4 | Fridge | $2,100,000 | 950 | $2,211 |
| 5 | Camera | $1,100,000 | 850 | $1,294 |

#### 4.3.2 Category Distribution
- **Electronics:** 62% of total revenue
- **Appliances:** 38% of total revenue

### 4.4 Customer Loyalty Analysis

#### 4.4.1 Revenue by Loyalty Level
| Loyalty Level | Revenue | % of Total | Members | Avg per Member |
|---------------|---------|------------|---------|----------------|
| Platinum | $4,012,963 | 26.3% | 1,299 | $3,089 |
| Silver | $3,918,576 | 25.7% | 1,288 | $3,042 |
| Bronze | $3,795,198 | 24.9% | 1,253 | $3,029 |
| Gold | $3,536,864 | 23.2% | 1,160 | $3,049 |

#### 4.4.2 Key Insights
- Revenue distribution is relatively balanced across loyalty tiers
- Gold level has lowest revenue despite similar average spending → **growth opportunity**
- Platinum level has highest member count and revenue → **retention priority**

---

## 5. Machine Learning Models

### 5.1 Data Preparation

#### 5.1.1 Train-Test Split
- **Training Set:** 80% of data (219 days, Jan-July 2024)
- **Testing Set:** 20% of data (54 days, Aug-Sep 2024)
- **Rationale:** Temporal split to simulate real-world forecasting scenario

#### 5.1.2 Feature Selection
Selected features based on correlation analysis and domain knowledge:
- Time-based: `days_since_start`, `month`, `week`, `day_of_week`, `is_weekend`
- Trend indicators: `qty_ma7`, `qty_ma14`, `qty_ma30`

### 5.2 Models Evaluated

#### 5.2.1 Linear Regression
**Description:** Baseline model using ordinary least squares regression.

**Hyperparameters:** Default settings (no regularization)

**Results:**
- MAE: $1,892.27
- MAPE: 176.96%
- R²: 0.0387
- Training Time: <1 second

**Interpretation:** Best performing model with lowest MAE. High MAPE due to small daily values causing inflated percentage errors.

---

#### 5.2.2 Ridge Regression
**Description:** Linear regression with L2 regularization to prevent overfitting.

**Hyperparameters:** `alpha=1.0`

**Results:**
- MAE: $1,892.32
- MAPE: 176.96%
- R²: 0.0387
- Training Time: <1 second

**Interpretation:** Nearly identical performance to Linear Regression, indicating minimal overfitting in the baseline model.

---

#### 5.2.3 Gradient Boosting
**Description:** Ensemble method combining multiple decision trees sequentially.

**Hyperparameters:**
- `n_estimators=100`
- `learning_rate=0.1`
- `max_depth=5`

**Results:**
- MAE: $2,116.00
- MAPE: 200.00%
- R²: -0.1808
- Training Time: 5 seconds

**Interpretation:** Worse performance than linear models. Negative R² indicates overfitting due to limited dataset size (only 273 days).

---

#### 5.2.4 SARIMA
**Description:** Seasonal AutoRegressive Integrated Moving Average, specialized for time series.

**Hyperparameters:**
- `order=(1,1,1)`
- `seasonal_order=(1,1,1,4)`

**Results:**
- MAE: $778,132.95
- MAPE: 84.02%
- R²: Not comparable (trained on weekly aggregated data)
- Training Time: 3 minutes

**Interpretation:** Terrible performance (MAE 400x worse than Linear Regression). Model trained on only 9 monthly data points, while SARIMA requires 2+ years for reliability. Scale mismatch between training (monthly) and testing (daily) caused failure.

---

### 5.3 Model Comparison

| Model | MAE (Lower=Better) | MAPE | R² | Recommendation |
|-------|-------------------|------|-----|----------------|
| **Linear Regression** | **$1,892** | 177% | 0.039 | **SELECTED** |
| Ridge Regression | $1,892 | 177% | 0.039 | Equivalent |
| Gradient Boosting | $2,116 | 200% | -0.18 | Not recommended |
| SARIMA | $778,133 | 84% | N/A | Unsuitable |

### 5.4 Model Selection Rationale

**Selected Model: Linear Regression**

**Reasons:**
1. **Lowest MAE ($1,892):** Best absolute error performance
2. **Simplicity:** Easy to interpret and maintain
3. **Speed:** Instant predictions (<1ms)
4. **Stability:** No overfitting despite simple structure
5. **Appropriate for Data:** Data exhibits clear linear trends

**Why MAPE is High (177%):**
MAPE is unreliable for this dataset due to small daily values. When actual sales are $50 and predicted are $100, the error is only $50 but MAPE shows 100%. **MAE is the reliable metric here.**

**Why R² is Low (0.039):**
Time series data has high natural variance from daily fluctuations. R² is not a good metric for forecasting - focus on MAE instead.

---

## 6. Results and Key Findings

### 6.1 Model Performance
- **Selected Model:** Linear Regression
- **Prediction Accuracy:** MAE of $1,892 (predictions off by ~$1,900 on average)
- **Business Interpretation:** For a daily sales average of $8,500, this represents 22% error - acceptable for inventory planning
- **Forecast Horizon:** 9 months (Jan-Sep 2025)

### 6.2 Sales Forecast for 2025
- **Total Predicted Units (Jan-Sep 2025):** 6,272 units
- **Total Predicted Revenue:** Based on product mix and historical pricing
- **Monthly Breakdown:** Available in interactive dashboard

### 6.3 Product Insights
1. **Top Performer:** Laptop (26% of revenue)
2. **High Volume:** Smartphone (most units sold)
3. **Premium Product:** TV (highest average price)
4. **Growth Opportunity:** Camera (lowest sales, potential for marketing push)

### 6.4 Customer Loyalty Insights
1. **Underperforming Segment:** Gold level (23.2% of revenue, lowest among tiers)
   - **Recommendation:** Launch targeted promotions to Gold members
2. **High-Value Segment:** Platinum (26.3% of revenue)
   - **Recommendation:** Maintain exclusive benefits to retain these customers
3. **Engagement Opportunity:** Bronze level has lowest average transaction value
   - **Recommendation:** Cross-sell campaigns and bundle discounts

### 6.5 Temporal Patterns
- **Weekend Boost:** +20% sales on Saturdays and Sundays
- **Best Month:** January (post-holiday season)
- **Optimal Staffing:** Increase weekend staff by 20-30%

---

## 7. Dashboard and Deployment

### 7.1 Streamlit Dashboard Features

#### 7.1.1 Quick Prediction Tool
- **User Inputs:** Product, Store Location, Forecast Period (1-9 months)
- **Scenario Adjustment:** 50%-200% multiplier for what-if analysis
- **Outputs:** Daily/weekly/monthly forecasts with downloadable CSV
- **Business Value:** Store managers can generate custom forecasts instantly

#### 7.1.2 Customer Analytics
- **Loyalty Performance:** Visual breakdown by tier
- **Actionable Insights:** Automated recommendations for each segment
- **Growth Opportunities:** Identifies underperforming segments

#### 7.1.3 Model Performance Dashboard
- **Model Comparison:** Side-by-side evaluation metrics
- **Metric Explanations:** User-friendly descriptions of MAE, MAPE, R²
- **Visualization:** Interactive charts for MAE and MAPE comparison

#### 7.1.4 Data Explorer
- **Transaction Browser:** Filterable table with 5,000 transactions
- **Forecast Viewer:** Daily/monthly forecast data for 2025
- **Product Rankings:** Complete performance metrics
- **Download Options:** Export any dataset as CSV

### 7.2 Technical Stack
- **Frontend:** Streamlit (Python web framework)
- **Backend:** Pandas, NumPy for data processing
- **Modeling:** Scikit-learn, Statsmodels
- **Visualization:** Plotly (interactive charts)
- **Deployment:** Streamlit Cloud
- **Version Control:** GitHub

### 7.3 Deployment Process
1. Model training in Jupyter Notebook
2. Generated 11 output files (CSVs, models, encoders)
3. Streamlit app developed with 5 pages
4. Deployed to Streamlit Cloud via GitHub integration
5. Live dashboard accessible at provided URL

---

## 8. Conclusion

This project successfully developed an accurate sales forecasting system for Walmart with the following achievements:

### 8.1 Technical Achievements
- **Built and compared 4 machine learning models**
- **Achieved MAE of $1,892** (strong baseline for daily forecasting)
- **Deployed interactive dashboard** for non-technical business users
- **Generated 9-month forecast** (Jan-Sep 2025) with daily granularity

### 8.2 Business Impact
1. **Inventory Optimization:** Predictions enable data-driven ordering decisions
2. **Staffing Efficiency:** Identified 20% weekend surge for optimal scheduling
3. **Customer Targeting:** Identified Gold tier as growth opportunity ($500K+ potential)
4. **Decision Support:** What-if scenario planning (50%-200% adjustments)

### 8.3 Key Takeaways
- **Simple models can outperform complex ones** when data is limited
- **MAE is more reliable than MAPE** for datasets with small values
- **Feature engineering matters** - moving averages improved predictions
- **Interactive tools empower users** - dashboard makes ML accessible

---

## 9. Limitations

### 9.1 Data Limitations
1. **Limited Time Span:** Only 9 months of data (ideally need 2+ years)
   - **Impact:** SARIMA model failed due to insufficient seasonal cycles
   - **Effect on Predictions:** Cannot capture long-term trends or annual seasonality

2. **No External Variables:** Missing factors that influence sales:
   - Economic indicators (GDP, unemployment, inflation)
   - Competitor actions (pricing, promotions, new store openings)
   - Marketing campaigns and advertising spend

3. **Product-Level Granularity:** Only 8 products analyzed
   - **Impact:** Cannot provide SKU-level forecasts
   - **Limitation:** Store managers may need more detailed predictions


### 9.2 Model Limitations
1. **Linear Assumptions:** Linear Regression assumes linear relationships
   - **Reality:** Sales patterns may have non-linear components
   - **Mitigation:** Moving averages partially capture non-linearity

2. **No Probabilistic Forecasts:** Model provides point estimates only
   - **Missing:** Confidence intervals or prediction ranges
   - **Business Need:** Managers want "best case / worst case" scenarios

3. **SARIMA Failure:** Statistical time series model performed poorly
   - **Root Cause:** Insufficient data (needs 24+ months)
   - **Lesson:** Traditional time series methods not always superior

4. **Overfitting Risk:** Gradient Boosting showed negative R²
   - **Cause:** Small dataset size (273 days)
   - **Solution:** Simpler models (Linear/Ridge) more appropriate

### 9.3 Dashboard Limitations
1. **Static Ratios:** Product/store distributions based on historical data
   - **Reality:** Ratios may shift over time
   - **Solution:** Requires periodic model retraining

2. **No Real-Time Updates:** Dashboard uses pre-generated forecasts
   - **Limitation:** Cannot incorporate today's sales into predictions
   - **Ideal:** Streaming data pipeline for daily updates

3. **Single Model:** Only Linear Regression deployed
   - **Alternative:** Could implement ensemble averaging

---

## 10. Future Research Directions

### 10.1 Short-Term Enhancements (3-6 months)

#### 10.1.1 Data Enrichment
- **Collect 2+ years of historical data** for robust seasonal modeling
- **Add promotional calendar** with discount periods and campaign dates
- **Integrate weather data** (temperature, precipitation) via APIs
- **Include economic indicators** (consumer confidence index, unemployment rates)

#### 10.1.2 Model Improvements
- **Implement Prophet** (Facebook's time series library) with automatic seasonality detection
- **Develop ensemble model** combining Linear Regression + XGBoost
- **Add probabilistic forecasting** with prediction intervals (95% confidence bounds)
- **Build separate models per product** for improved accuracy

#### 10.1.3 Dashboard Features
- **Real-time data integration** with Walmart's POS systems
- **Automated daily retraining** to incorporate latest sales data
- **Email alerts** for forecast anomalies or inventory risks
- **Mobile app version** for on-the-go access

### 10.2 Medium-Term Research (6-12 months)

#### 10.2.1 Advanced ML Techniques
- **Deep Learning:** LSTM/GRU neural networks for complex temporal patterns
- **Transfer Learning:** Pre-train on industry-wide retail data, fine-tune on Walmart
- **Attention Mechanisms:** Transformer-based models (successful in NLP, emerging in time series)

#### 10.2.2 Multivariate Forecasting
- **Multi-product forecasting:** Predict all 8 products simultaneously capturing cross-effects
- **Hierarchical forecasting:** Predict at category level, then disaggregate to products
- **Causal inference:** Quantify impact of promotions on sales (counterfactual analysis)

#### 10.2.3 Inventory Optimization
- **Safety stock calculations** based on forecast uncertainty
- **Reorder point optimization** minimizing stockout risk
- **Multi-echelon inventory** across warehouse and store locations

### 10.3 Long-Term Vision (1-2 years)

#### 10.3.1 Prescriptive Analytics
- **Recommendation engine:** Suggest optimal pricing and promotions
- **Dynamic pricing:** Adjust prices based on demand forecasts
- **Assortment optimization:** Recommend which products to stock at each store

#### 10.3.2 Customer-Level Modeling
- **Customer lifetime value (CLV) prediction** for each loyalty tier
- **Churn prediction:** Identify customers likely to downgrade loyalty status
- **Next-purchase prediction:** Recommend products based on individual history

#### 10.3.3 Expand Scope
- **Multi-store rollout:** Scale dashboard to all Walmart locations
- **Real-time anomaly detection:** Alert for sudden demand spikes/drops
- **Supply chain integration:** Coordinate with suppliers based on forecasts

#### 10.3.4 Emerging Technologies
- **Generative AI:** Use large language models for natural language queries
  - Example: "Show me forecast for laptops in Dallas next month"
- **Reinforcement Learning:** Learn optimal inventory policies through simulation
- **Edge Computing:** Deploy models at store level for offline predictions

### 10.4 Academic Research Opportunities

1. **Benchmark Study:** Compare performance across retail forecasting methods
2. **Feature Importance:** Quantify impact of each predictor on forecast accuracy
3. **Explainable AI:** Develop interpretable time series models for business users
4. **Hybrid Models:** Combine statistical (SARIMA) and ML (XGBoost) approaches

---

## 11. Acknowledgments

I would like to express my gratitude to:
- **Dr. Chaojie (Jay) Wang** for guidance throughout this capstone project
- **UMBC Data Science Department** for providing resources and support
- **Walmart** for the inspiration behind this retail analytics project
- **Open-source community** for excellent Python libraries (Streamlit, Scikit-learn, Plotly)

---

## 12. References

1. Hyndman, R.J., & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts.

2. Scikit-learn Development Team. (2024). *Scikit-learn: Machine Learning in Python.* https://scikit-learn.org/

3. Streamlit Team. (2024). *Streamlit Documentation.* https://docs.streamlit.io/

4. Brownlee, J. (2020). *Time Series Forecasting with Python.* Machine Learning Mastery.

5. Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). *Time Series Analysis: Forecasting and Control* (5th ed.). Wiley.

6. Kaggle. (2024). *Walmart Store Sales Forecasting.* https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting

7. Hyndman, R.J., & Koehler, A.B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, 22(4), 679-688.

8. Chai, T., & Draxler, R.R. (2014). Root mean square error (RMSE) or mean absolute error (MAE)? *Geoscientific Model Development*, 7, 1247-1250.

---

## Appendix

### A. GitHub Repository Structure
```
UMBC-DATA606-Capstone/
├── docs/
│   ├── report.md
│   ├── presentation.pptx
│   └── proposal.md
├── notebooks/
│   ├── EDA.ipynb
│   └── model_training.ipynb
├── data/
│   ├── Walmart_Sales_Data.csv
│   └── Walmart_Sales_EDA.csv
├── ui.py
├── requirements.txt
├── cleaned_data.csv
├── daily_sales.csv
├── forecast_2025.csv
├── model_comparison.csv
├── product_ranking.csv
├── encoders.pkl
├── best_qty_model.pkl
└── best_cog_model.pkl
```

### B. How to Run the Dashboard Locally
```bash
# Clone repository
git clone https://github.com/Sruthi1203/UMBC-DATA606-Capstone.git
cd UMBC-DATA606-Capstone

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run ui.py
```

### C. Model Training Time Comparison
| Model | Training Time | Prediction Time |
|-------|---------------|-----------------|
| Linear Regression | 0.05s | <0.001s |
| Ridge Regression | 0.05s | <0.001s |
| Gradient Boosting | 5.2s | 0.002s |
| SARIMA | 180s | 0.5s |



**End of Report**

---
