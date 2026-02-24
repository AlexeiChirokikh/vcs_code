import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="DataViz Pro", page_icon="📊", layout="wide")

# --- CUSTOM CSS FOR MODERN LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child { background-color: #00d4ff; color: white; border-radius: 10px; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR / DATA GENERATION ---
with st.sidebar:
    st.title("📂 Data Controls")
    if st.button("Generate Sample Data"):
        n_rows = 1000
        categories = ['Electronics', 'Home Decor', 'Fitness', 'Software', 'Books']
        regions = ['North America', 'Europe', 'Asia', 'LATAM']
        data = {
            'Order_Date': [datetime(2025, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)],
            'Category': np.random.choice(categories, n_rows),
            'Region': np.random.choice(regions, n_rows),
            'Sales_USD': np.random.uniform(20.0, 500.0, n_rows).round(2),
            'Quantity': np.random.randint(1, 10, n_rows)
        }
        df_sample = pd.DataFrame(data)
        st.session_state['df'] = df_sample
        st.success("Sample Data Loaded!")

    uploaded_file = st.file_uploader("Or Upload your CSV", type="csv")
    if uploaded_file:
        st.session_state['df'] = pd.read_csv(uploaded_file)

# --- MAIN DASHBOARD ---
st.title("📊 Business Intelligence Dashboard")
st.markdown("---")

if 'df' in st.session_state:
    df = st.session_state['df']
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

    # 1. KEY METRICS ROW
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${df['Sales_USD'].sum():,.2f}")
    col2.metric("Total Orders", f"{len(df):,}")
    col3.metric("Avg Order Value", f"${df['Sales_USD'].mean():.2f}")
    col4.metric("Top Region", df['Region'].mode()[0])

    st.markdown("---")

    # 2. CHARTS ROW 1
    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.subheader("📈 Sales Trend")
        df_trend = df.groupby('Order_Date')['Sales_USD'].sum().reset_index()
        fig_line = px.line(df_trend, x='Order_Date', y='Sales_USD', template="plotly_dark", color_discrete_sequence=['#00D4FF'])
        st.plotly_chart(fig_line, use_container_width=True)

    with right_chart:
        st.subheader("🍕 Revenue by Category")
        fig_pie = px.pie(df, values='Sales_USD', names='Category', hole=0.5, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # 3. CHARTS ROW 2
    left_chart_2, right_chart_2 = st.columns(2)

    with left_chart_2:
        st.subheader("🌎 Regional Performance")
        fig_bar = px.bar(df, x='Region', y='Sales_USD', color='Category', barmode='group', template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)

    with right_chart_2:
        st.subheader("🎯 Sales vs Quantity Correlation")
        fig_scatter = px.scatter(df, x='Quantity', y='Sales_USD', color='Region', size='Sales_USD', template="plotly_dark")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 4. RAW DATA TABLE
    with st.expander("🔍 View Raw Data Table"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("👈 Please upload a file or click 'Generate Sample Data' in the sidebar to begin.")

