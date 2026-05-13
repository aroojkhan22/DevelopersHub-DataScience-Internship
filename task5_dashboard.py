import pandas as pd
import streamlit as st
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Global Superstore Dashboard",
    layout="wide"
)

# Dashboard title
st.title("Global Superstore Business Dashboard")

# Dashboard description
st.markdown("""
## Dashboard Overview

This interactive dashboard analyzes:
- Sales performance
- Profit trends
- Customer performance
- Regional insights
""")

# Load dataset
df = pd.read_csv("Global_Superstore2.csv", encoding='latin1')

# Dataset preview
st.subheader("Dataset Preview")

st.dataframe(df.head())

# =========================
# Sidebar Filters
# =========================

st.sidebar.header("Dashboard Filters")

# Region filter
region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

# Category filter
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Sub-Category filter
subcategory_filter = st.sidebar.multiselect(
    "Select Sub-Category",
    options=df['Sub-Category'].unique(),
    default=df['Sub-Category'].unique()
)

# Apply filters
filtered_df = df[
    (df['Region'].isin(region_filter)) &
    (df['Category'].isin(category_filter)) &
    (df['Sub-Category'].isin(subcategory_filter))
]

# Show filtered dataset
st.subheader("Filtered Dataset")

st.dataframe(filtered_df)

# =========================
# KPI Section
# =========================

st.subheader("Key Performance Indicators")

total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order ID'].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", total_orders)

# =========================
# Sales by Category
# =========================

st.subheader("Sales by Category")

sales_by_category = filtered_df.groupby('Category')['Sales'].sum().reset_index()

fig1 = px.bar(
    sales_by_category,
    x='Category',
    y='Sales',
    title='Sales by Category'
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# Profit by Region
# =========================

st.subheader("Profit by Region")

profit_by_region = filtered_df.groupby('Region')['Profit'].sum().reset_index()

fig2 = px.pie(
    profit_by_region,
    names='Region',
    values='Profit',
    title='Profit Distribution by Region'
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# Top 5 Customers
# =========================

st.subheader("Top 5 Customers by Sales")

top_customers = (
    filtered_df.groupby('Customer Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

fig3 = px.bar(
    top_customers,
    x='Customer Name',
    y='Sales',
    title='Top 5 Customers by Sales'
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# Sales Trend Over Time
# =========================

st.subheader("Sales Trend Over Time")

filtered_df['Order Date'] = pd.to_datetime(
    filtered_df['Order Date'],
    dayfirst=True,
    errors='coerce'
)

sales_trend = (
    filtered_df.groupby('Order Date')['Sales']
    .sum()
    .reset_index()
)

fig4 = px.line(
    sales_trend,
    x='Order Date',
    y='Sales',
    title='Sales Trend Over Time'
)

st.plotly_chart(fig4, use_container_width=True)