import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="YouTube Trending Analytics", layout="wide")
st.title("📊 YouTube Trending Video Analytics")

db_password = os.getenv("DB_PASSWORD")
engine = create_engine(f"postgresql://postgres:{db_password}@localhost:5432/ytanalytics")

# Load aggregated data
categories_df = pd.read_sql("""
SELECT category_name, Round(AVG(engagement_rate)::numeric, 4) AS avg_engagement, COUNT(*) AS video_count
FROM videos
GROUP BY category_name
ORDER BY avg_engagement DESC
LIMIT 10""", engine)

country_df = pd.read_sql("""
SELECT country, Round(AVG(engagement_rate)::numeric, 4) AS avg_engagement, COUNT(*) AS video_count
FROM videos
GROUP BY country
ORDER BY avg_engagement DESC """, engine)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Categories by Engagement Rate")
    st.bar_chart(categories_df.set_index('category_name')['avg_engagement'])

with col2:
    st.subheader("Average Engagement Rate by Country")
    st.bar_chart(country_df.set_index('country')['avg_engagement'])

st.subheader("Raw Data")
st.dataframe(categories_df)
st.dataframe(country_df)