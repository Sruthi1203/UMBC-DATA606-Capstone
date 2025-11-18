import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import calendar

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Walmart Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0071ce;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .loyalty-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc220;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333 !important;
    }
    .loyalty-card h4 {
        color: #0071ce !important;
        margin: 0;
    }
    .loyalty-card p {
        color: #333 !important;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cleaned_data.csv")
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        
        daily_sales = pd.read_csv("daily_sales.csv")
        daily_sales["transaction_date"] = pd.to_datetime(daily_sales["transaction_date"])
        
        forecast = pd.read_csv("forecast_2025.csv")
        forecast["transaction_date"] = pd.to_datetime(forecast["transaction_date"])
        
        product_ranking = pd.read_csv("product_ranking.csv")
        model_comparison = pd.read_csv("model_comparison.csv")
        product_ratios = pd.read_csv("product_ratios.csv")
        
        try:
            store_ratios = pd.read_csv("store_ratios.csv")
        except:
            store_ratios = None
            
        try:
            loyalty_analysis = pd.read_csv("loyalty_analysis.csv")
        except:
            loyalty_analysis = None
        
        return df, daily_sales, forecast, product_ranking, model_comparison, product_ratios, store_ratios, loyalty_analysis
    
    except FileNotFoundError as e:
        st.error(f"Missing file: {e}")
        st.stop()

df, daily_sales, forecast, product_ranking, model_comparison, product_ratios, store_ratios, loyalty_analysis = load_data()

has_store = 'store_location' in df.columns and store_ratios is not None
has_loyalty = loyalty_analysis is not None

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/b/b1/Walmart_logo_%282008%29.svg", width=200)
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Quick Prediction",
     "Overview",
     "Customer Analytics",
     "Model Performance",
     "Data Explorer"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"""
**Data Period**  
{df['transaction_date'].min().strftime('%b %d, %Y')} to  
{df['transaction_date'].max().strftime('%b %d, %Y')}

**Products:** {df['product_name'].nunique()}  
**Transactions:** {len(df):,}
""")

if page == "Quick Prediction":
    st.markdown('<h1 class="main-header">Sales Prediction Tool</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="prediction-box">
    <h3>Generate Custom Sales Forecast</h3>
    <p>Select product, location, and forecast period (Jan-Sep 2025)</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'show_prediction' not in st.session_state:
        st.session_state.show_prediction = False
    if 'last_product' not in st.session_state:
        st.session_state.last_product = None
    if 'last_store' not in st.session_state:
        st.session_state.last_store = None
    if 'last_months' not in st.session_state:
        st.session_state.last_months = 3
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Configuration")
        
        selected_product = st.selectbox(
            "Select Product:",
            options=sorted(df['product_name'].unique()),
            key='product_select'
        )
        
        if has_store:
            selected_store = st.selectbox(
                "Select Store Location:",
                options=sorted(df['store_location'].unique()),
                key='store_select'
            )
        else:
            selected_store = None
            st.info("Store location not available")
        
        st.write("**Forecast Period (2025):**")
        
        month_options = {
            "January only (1 month)": 1,
            "January - February (2 months)": 2,
            "January - March (Q1 - 3 months)": 3,
            "January - April (4 months)": 4,
            "January - May (5 months)": 5,
            "January - June (H1 - 6 months)": 6,
            "January - July (7 months)": 7,
            "January - August (8 months)": 8,
            "January - September (Full 9 months)": 9
        }
        
        selected_period = st.selectbox(
            "Select forecast period:",
            options=list(month_options.keys()),
            index=2,
            key='period_select'
        )
        
        forecast_months = month_options[selected_period]
        
        st.markdown("---")
        st.write("**Scenario Adjustment (Promotion Period):**")
        demand_multiplier = st.slider(
            "Adjust forecast by percentage:",
            min_value=50,
            max_value=200,
            value=100,
            step=10,
            help="100% = baseline forecast, 150% = optimistic scenario"
        ) / 100.0
        
        if demand_multiplier != 1.0:
            st.caption(f"Showing {demand_multiplier*100:.0f}% scenario")
        
        if st.button("Generate Prediction", type="primary", use_container_width=True):
            st.session_state.show_prediction = True
            st.session_state.last_product = selected_product
            st.session_state.last_store = selected_store
            st.session_state.last_months = forecast_months
            st.session_state.last_multiplier = demand_multiplier
    
    with col2:
        st.subheader("Historical Performance")
        product_hist = df[df['product_name'] == selected_product]
        
        col_a, col_b = st.columns(2)
        col_a.metric("Total Sales", f"${product_hist['cost_of_goods'].sum():,.0f}")
        col_b.metric("Units Sold", f"{product_hist['quantity_sold'].sum():,}")
        
        col_c, col_d = st.columns(2)
        col_c.metric("Avg Price", f"${product_hist['cost_of_goods'].mean():.2f}")
        col_d.metric("Transactions", f"{len(product_hist):,}")
        
        monthly_hist = product_hist.groupby(
            product_hist['transaction_date'].dt.to_period('M')
        )['cost_of_goods'].sum().reset_index()
        monthly_hist['transaction_date'] = monthly_hist['transaction_date'].dt.to_timestamp()
        
        if len(monthly_hist) > 0:
            fig = px.line(monthly_hist, x='transaction_date', y='cost_of_goods',
                         title=f'Historical Trend - {selected_product}')
            fig.update_traces(line_color='#0071ce', line_width=2)
            fig.update_layout(height=250, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.show_prediction:
        st.markdown("---")
        
        pred_product = st.session_state.last_product
        pred_store = st.session_state.last_store
        pred_months = st.session_state.last_months
        pred_multiplier = st.session_state.last_multiplier
        
        st.subheader(f"Forecast: {pred_product}")
        
        caption_parts = [f"{calendar.month_name[1]} - {calendar.month_name[pred_months]} 2025"]
        if pred_store:
            caption_parts.append(f"Store: {pred_store}")
        if pred_multiplier != 1.0:
            caption_parts.append(f"{pred_multiplier*100:.0f}% scenario")
        
        st.caption(" | ".join(caption_parts))
        
        product_ratio_row = product_ratios[product_ratios['product_name'] == pred_product]
        
        if len(product_ratio_row) > 0:
            qty_ratio = product_ratio_row['qty_ratio'].values[0]
            cog_ratio = product_ratio_row['cog_ratio'].values[0]
            
            start_date = datetime(2025, 1, 1)
            
            if pred_months == 12:
                end_date = datetime(2025, 12, 31)
            else:
                year = 2025
                month = pred_months
                last_day = calendar.monthrange(year, month)[1]
                end_date = datetime(year, month, last_day)
            
            future_dates = pd.date_range(start=start_date, end=end_date, freq='D')
            
            daily_avg_qty = daily_sales['quantity_sold'].tail(30).mean()
            daily_avg_cog = daily_sales['cost_of_goods'].tail(30).mean()
            
            pred_df = pd.DataFrame({
                'date': future_dates,
                'predicted_quantity': daily_avg_qty * qty_ratio * pred_multiplier,
                'predicted_revenue': daily_avg_cog * cog_ratio * pred_multiplier
            })
            
            if pred_store and store_ratios is not None:
                store_ratio_row = store_ratios[store_ratios['store_location'] == pred_store]
                if len(store_ratio_row) > 0:
                    store_ratio = store_ratio_row['cog_ratio'].values[0]
                    pred_df['predicted_revenue'] *= store_ratio
                    pred_df['predicted_quantity'] *= store_ratio
            
            pred_df['day_of_week'] = pred_df['date'].dt.dayofweek
            pred_df['is_weekend'] = pred_df['day_of_week'].isin([5, 6])
            pred_df.loc[pred_df['is_weekend'], 'predicted_revenue'] *= 1.2
            pred_df.loc[pred_df['is_weekend'], 'predicted_quantity'] *= 1.2
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Units", f"{pred_df['predicted_quantity'].sum():,.0f}")
            col2.metric("Total Revenue", f"${pred_df['predicted_revenue'].sum():,.2f}")
            col3.metric("Daily Avg", f"${pred_df['predicted_revenue'].mean():.2f}")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=pred_df['date'],
                y=pred_df['predicted_revenue'],
                mode='lines',
                name='Revenue',
                line=dict(color='#0071ce', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 113, 206, 0.2)'
            ))
            fig.update_layout(
                title=f"Daily Revenue Forecast ({pred_months} months)",
                xaxis_title="Date",
                yaxis_title="Revenue ($)",
                height=400,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            pred_df['month'] = pred_df['date'].dt.month
            pred_df['month_name'] = pred_df['date'].dt.strftime('%B %Y')
            monthly_summary = pred_df.groupby('month_name').agg({
                'predicted_quantity': 'sum',
                'predicted_revenue': 'sum'
            }).reset_index()
            
            st.subheader("Monthly Breakdown")
            st.dataframe(
                monthly_summary.style.format({
                    'predicted_quantity': '{:,.0f}',
                    'predicted_revenue': '${:,.2f}'
                }),
                column_config={
                    'month_name': 'Month',
                    'predicted_quantity': 'Units',
                    'predicted_revenue': 'Revenue'
                },
                hide_index=True,
                use_container_width=True
            )
            
            csv = pred_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Forecast",
                data=csv,
                file_name=f"forecast_{pred_product}_{pred_months}months_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

elif page == "Overview":
    st.markdown('<h1 class="main-header">Business Overview</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = df["cost_of_goods"].sum()
    total_qty = df["quantity_sold"].sum()
    total_txn = len(df)
    avg_txn = df["cost_of_goods"].mean()
    
    with col1:
        st.metric("Total Revenue", f"${total_sales:,.0f}")
    with col2:
        st.metric("Units Sold", f"{total_qty:,}")
    with col3:
        st.metric("Transactions", f"{total_txn:,}")
    with col4:
        st.metric("Avg Transaction", f"${avg_txn:.2f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Category")
        category_sales = df.groupby("category")["cost_of_goods"].sum().reset_index()
        fig = px.pie(
            category_sales,
            values="cost_of_goods",
            names="category",
            color_discrete_sequence=['#0071ce', '#ffc220'],
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=350, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Products")
        top5 = product_ranking.head(5)
        fig = px.bar(
            top5,
            x="total_revenue",
            y="product_name",
            orientation="h",
            color="total_revenue",
            color_continuous_scale="Blues",
            text="total_revenue"
        )
        fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
        fig.update_yaxes(categoryorder="total ascending")
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("Sales Trend")
    
    trend_view = st.radio("View by:", ["Monthly", "Weekly", "Daily"], horizontal=True)
    
    if trend_view == "Monthly":
        trend_data = df.groupby(df["transaction_date"].dt.to_period("M")).agg({
            "cost_of_goods": "sum",
            "quantity_sold": "sum"
        }).reset_index()
        trend_data["transaction_date"] = trend_data["transaction_date"].dt.to_timestamp()
        x_label = "Month"
    elif trend_view == "Weekly":
        trend_data = df.groupby(pd.Grouper(key='transaction_date', freq='W')).agg({
            "cost_of_goods": "sum",
            "quantity_sold": "sum"
        }).reset_index()
        x_label = "Week"
    else:
        trend_data = daily_sales[['transaction_date', 'cost_of_goods', 'quantity_sold']].copy()
        x_label = "Date"
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Revenue ($)", "Units Sold"))
    
    fig.add_trace(
        go.Scatter(
            x=trend_data["transaction_date"],
            y=trend_data["cost_of_goods"],
            mode="lines+markers",
            name="Revenue",
            line=dict(color="#0071ce", width=2),
            marker=dict(size=6)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=trend_data["transaction_date"],
            y=trend_data["quantity_sold"],
            mode="lines+markers",
            name="Units",
            line=dict(color="#ffc220", width=2),
            marker=dict(size=6)
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(title_text=x_label, row=1, col=1)
    fig.update_xaxes(title_text=x_label, row=1, col=2)
    fig.update_layout(height=400, showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Complete Product Rankings")
    
    st.dataframe(
        product_ranking.style.format({
            'total_quantity': '{:,}',
            'total_revenue': '${:,.2f}',
            'transaction_count': '{:,}'
        }),
        column_config={
            'rank': 'Rank',
            'product_name': 'Product',
            'total_quantity': 'Units',
            'total_revenue': 'Revenue',
            'transaction_count': 'Transactions'
        },
        hide_index=True,
        use_container_width=True
    )

elif page == "Customer Analytics":
    st.markdown('<h1 class="main-header">Customer Loyalty Analysis</h1>', unsafe_allow_html=True)
    
    if has_loyalty:
        # -------------------------------------------
        # Loyalty Program Overview
        # -------------------------------------------
        st.subheader("Loyalty Program Overview")
        
        total_customers = loyalty_analysis['transaction_count'].sum()
        total_loyalty_revenue = loyalty_analysis['total_cog'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Loyalty Members", f"{total_customers:,}")
        col2.metric("Loyalty Revenue", f"${total_loyalty_revenue:,.2f}")
        col3.metric("Loyalty Levels", f"{len(loyalty_analysis)}")
        
        st.markdown("---")
        
        # -------------------------------------------
        # Revenue by Loyalty Level
        # -------------------------------------------
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Revenue by Loyalty Level")
            
            fig = px.bar(
                loyalty_analysis.sort_values('total_cog', ascending=False),
                x='loyalty_level',
                y='total_cog',
                color='loyalty_level',
                text='total_cog',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_title="Loyalty Level",
                yaxis_title="Revenue ($)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")

        # -------------------------------------------
        # Horizontal Key Metrics Layout
        # -------------------------------------------
        st.subheader("Key Metrics by Loyalty Level")

        # Create horizontal columns dynamically for each loyalty level
        cols = st.columns(len(loyalty_analysis))

        for idx, (_, row) in enumerate(loyalty_analysis.sort_values('total_cog', ascending=False).iterrows()):
            pct = (row['total_cog'] / total_loyalty_revenue) * 100
            
            with cols[idx]:
                st.markdown(f"""
                <div class="loyalty-card" style="
                    background-color:#f9f9f9;
                    padding:15px;
                    border-radius:12px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.1);
                    text-align:center;
                    margin-bottom:10px;">
                    <h4 style="color:#004b87;">{row['loyalty_level']}</h4>
                    <p><strong>Revenue:</strong> ${row['total_cog']:,.0f} ({pct:.1f}%)</p>
                    <p><strong>Members:</strong> {row['transaction_count']:,}</p>
                    <p><strong>Avg/Member:</strong> ${row['avg_transaction_value']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # -------------------------------------------
        # Distribution Visuals
        # -------------------------------------------
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Transaction Distribution")
            fig = px.pie(
                loyalty_analysis,
                values='transaction_count',
                names='loyalty_level',
                title='Transactions by Loyalty Level',
                color_discrete_sequence=px.colors.sequential.Teal
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Average Transaction Value")
            fig = px.bar(
                loyalty_analysis.sort_values('avg_transaction_value', ascending=False),
                x='loyalty_level',
                y='avg_transaction_value',
                color='avg_transaction_value',
                color_continuous_scale='Greens',
                text='avg_transaction_value'
            )
            fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # -------------------------------------------
        # Actionable Insights
        # -------------------------------------------
        st.markdown("---")
        st.subheader("Actionable Insights")
        
        lowest_loyalty = loyalty_analysis.loc[loyalty_analysis['total_cog'].idxmin()]
        highest_loyalty = loyalty_analysis.loc[loyalty_analysis['total_cog'].idxmax()]
        lowest_avg = loyalty_analysis.loc[loyalty_analysis['avg_transaction_value'].idxmin()]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.error(f"""
            **Growth Opportunity**
            
            **{lowest_loyalty['loyalty_level']}**
            
            Lowest revenue: ${lowest_loyalty['total_cog']:,.0f}
            
            **Actions:**
            - Launch targeted email campaign  
            - Offer upgrade incentives  
            - Personalized product bundles  
            - Limited-time promotions
            """)
        
        with col2:
            st.success(f"""
            **Top Performers**
            
            **{highest_loyalty['loyalty_level']}**
            
            Highest revenue: ${highest_loyalty['total_cog']:,.0f}
            
            **Actions:**
            - Maintain exclusive benefits  
            - VIP early product access  
            - Dedicated support line  
            - Special anniversary rewards
            """)
        
        with col3:
            st.warning(f"""
            **Engagement Focus**
            
            **{lowest_avg['loyalty_level']}**
            
            Lowest avg: ${lowest_avg['avg_transaction_value']:.2f}
            
            **Actions:**
            - Cross-sell campaigns  
            - Bundle discounts  
            - Loyalty points multiplier  
            - Free shipping threshold
            """)
        
        # -------------------------------------------
        # Detailed Comparison Table
        # -------------------------------------------
        st.subheader("Detailed Comparison")
        
        comparison_df = loyalty_analysis.copy().sort_values('total_cog', ascending=False)
        
        st.dataframe(
            comparison_df.style.format({
                'total_quantity': '{:,}',
                'total_cog': '${:,.2f}',
                'transaction_count': '{:,}',
                'avg_transaction_value': '${:.2f}',
                'pct_of_total': '{:.1f}%'
            }).background_gradient(subset=['total_cog'], cmap='RdYlGn'),
            column_config={
                'loyalty_level': 'Loyalty Level',
                'total_quantity': 'Total Units',
                'total_cog': 'Total Revenue',
                'transaction_count': 'Transactions',
                'avg_transaction_value': 'Avg Value',
                'pct_of_total': '% of Total'
            },
            hide_index=True,
            use_container_width=True
        )
    
    else:
        st.warning("Customer loyalty data not available in your dataset.")


elif page == "Model Performance":
    st.markdown('<h1 class="main-header">Model Performance Analysis</h1>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.subheader("Model Comparison Results")
    
    display_df = model_comparison.copy()
    
    st.dataframe(
        display_df.style.format({
            'MAE_Quantity': '{:.4f}',
            'MAPE_Quantity': '{:.2f}%',
            'R2_Quantity': '{:.4f}',
            'MAE_COG': '{:.2f}',
            'MAPE_COG': '{:.2f}%',
            'R2_COG': '{:.4f}'
        }).background_gradient(subset=['MAE_COG'], cmap='RdYlGn_r'),
        use_container_width=True
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("MAE Comparison")
        fig = px.bar(
            model_comparison,
            x='Model',
            y='MAE_COG',
            color='MAE_COG',
            color_continuous_scale='RdYlGn_r',
            text='MAE_COG',
            title='Mean Absolute Error - Cost of Goods'
        )
        fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("MAPE Comparison")
        
        mape_df = model_comparison[model_comparison['MAPE_COG'].notna()].copy()
        
        fig = px.bar(
            mape_df,
            x='Model',
            y='MAPE_COG',
            color='MAPE_COG',
            color_continuous_scale='Reds_r',
            text='MAPE_COG',
            title='Mean Absolute Percentage Error'
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    best_model_idx = model_comparison['MAE_COG'].idxmin()
    best_model = model_comparison.loc[best_model_idx]
    
    st.success(f"""
    ### Best Performing Model: {best_model['Model']}
    
    **Performance Metrics:**
    - **MAE:** ${best_model['MAE_COG']:.2f} (Average error in dollars)
    - **MAPE:** {best_model['MAPE_COG']:.2f}% (Percentage error)
    - **R-Squared:** {best_model['R2_COG']:.4f} (Variance)
    
    This model is used for all forecasts in the prediction tool.
    """)
    
    st.markdown("---")
elif page == "Data Explorer":
    st.markdown('<h1 class="main-header">Data Explorer</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Transactions", "Forecast Data", "Product Rankings"])
    
    with tab1:
        st.subheader("Transaction Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.multiselect(
                "Category:",
                df['category'].unique().tolist(),
                default=df['category'].unique().tolist()
            )
        
        with col2:
            product_filter = st.multiselect(
                "Product:",
                df['product_name'].unique().tolist(),
                default=df['product_name'].unique().tolist()
            )
        
        with col3:
            date_range = st.date_input(
                "Date Range:",
                value=(df['transaction_date'].min().date(), df['transaction_date'].max().date())
            )
        
        filtered_df = df[
            (df['category'].isin(category_filter)) &
            (df['product_name'].isin(product_filter)) &
            (df['transaction_date'] >= pd.Timestamp(date_range[0])) &
            (df['transaction_date'] <= pd.Timestamp(date_range[1]))
        ].copy()
        
        st.write(f"Showing {len(filtered_df):,} of {len(df):,} transactions")
        
        display_cols = ['transaction_date', 'product_name', 'category', 'quantity_sold', 'cost_of_goods']
        if has_store:
            display_cols.insert(3, 'store_location')
        
        st.dataframe(
            filtered_df[display_cols].sort_values('transaction_date', ascending=False).head(100),
            use_container_width=True
        )
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${filtered_df['cost_of_goods'].sum():,.2f}")
        col2.metric("Total Units", f"{filtered_df['quantity_sold'].sum():,}")
        col3.metric("Transactions", f"{len(filtered_df):,}")
        
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("2025 Forecast Data")
        
        view_type = st.radio("View:", ["Daily", "Monthly"], horizontal=True)
        
        if view_type == "Daily":
            st.dataframe(
                forecast[['transaction_date', 'predicted_quantity', 'predicted_cog']].head(100),
                use_container_width=True
            )
            st.caption(f"Showing first 100 of {len(forecast)} days")
        else:
            monthly_forecast = forecast.groupby(
                forecast['transaction_date'].dt.to_period('M')
            ).agg({
                'predicted_quantity': 'sum',
                'predicted_cog': 'sum'
            }).reset_index()
            monthly_forecast['Month'] = monthly_forecast['transaction_date'].dt.strftime('%B %Y')
            
            st.dataframe(
                monthly_forecast[['Month', 'predicted_quantity', 'predicted_cog']],
                use_container_width=True
            )
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Units", f"{forecast['predicted_quantity'].sum():,.0f}")
        col2.metric("Total Revenue", f"${forecast['predicted_cog'].sum():,.2f}")
        col3.metric("Daily Avg", f"${forecast['predicted_cog'].mean():.2f}")
        
        csv = forecast.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Forecast",
            data=csv,
            file_name=f"forecast_2025.csv",
            mime="text/csv"
        )
    
    with tab3:
        st.subheader("Product Rankings")
        
        st.dataframe(product_ranking, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(product_ranking, x='product_name', y='total_revenue',
                        title='Revenue by Product')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(product_ranking, x='product_name', y='total_quantity',
                        title='Units by Product')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
