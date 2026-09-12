import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
engine = create_engine(f"postgresql://postgres:{db_password}@localhost:5432/ytanalytics")

st.set_page_config(page_title="YouTube Trending Analytics", layout="wide", page_icon="📊")

# ---------- Sidebar ----------
with st.sidebar:
    st.title("📊 About")
    st.markdown("""
    A data pipeline and analytics dashboard built on **375K+ trending YouTube videos**
    across 9 countries, combining a bulk Kaggle dataset with live YouTube Data API pulls.

    **Stack:** Python, Pandas, PostgreSQL, Streamlit, Plotly

    Built by JAMER
    """)
    st.divider()
    countries = pd.read_sql("SELECT DISTINCT country FROM videos ORDER BY country", engine)["country"].tolist()
    selected_countries = st.multiselect("Filter by country", countries, default=countries)

country_filter = "'" + "','".join(selected_countries) + "'" if selected_countries else "''"

# ---------- Header + KPIs ----------
st.title("YouTube Trending Video Analytics")

kpi_query = f"""
    SELECT COUNT(*) AS total_videos, COUNT(DISTINCT video_id) AS unique_videos,
           ROUND(AVG(engagement_rate)::numeric, 4) AS avg_engagement,
           ROUND(AVG(views)::numeric, 0) AS avg_views
    FROM videos WHERE country IN ({country_filter})
"""
kpis = pd.read_sql(kpi_query, engine).iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", f"{int(kpis['total_videos']):,}")
col2.metric("Unique Videos", f"{int(kpis['unique_videos']):,}")
col3.metric("Avg Engagement Rate", f"{float(kpis['avg_engagement'])*100:.2f}%")
col4.metric("Avg Views", f"{int(kpis['avg_views']):,}")

st.divider()

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🎬 By Category", "🌍 By Country", "🔎 Raw Data"])

with tab1:
    st.subheader("Views vs Engagement Rate by Category")
    scatter_df = pd.read_sql(f"""
        SELECT category_name, ROUND(AVG(engagement_rate)::numeric, 4) AS avg_engagement,
               ROUND(AVG(views)::numeric, 0) AS avg_views, COUNT(*) AS video_count
        FROM videos WHERE country IN ({country_filter})
        GROUP BY category_name
    """, engine)
    fig = px.scatter(
        scatter_df, x="avg_views", y="avg_engagement", size="video_count",
        color="category_name", hover_name="category_name",
        labels={"avg_views": "Average Views", "avg_engagement": "Average Engagement Rate"},
        title="Reach vs Engagement — bigger bubbles = more videos in that category"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Niche categories with fewer, smaller-reach videos tend to cluster higher on engagement rate, while mass-appeal categories trade reach for engagement.")

    st.subheader("Engagement Rate Trend Over Time")
    trend_df = pd.read_sql(f"""
        SELECT trending_date, ROUND(AVG(engagement_rate)::numeric, 4) AS avg_engagement
        FROM videos WHERE country IN ({country_filter}) AND trending_date IS NOT NULL
        GROUP BY trending_date ORDER BY trending_date
    """, engine)
    fig2 = px.line(trend_df, x="trending_date", y="avg_engagement", title="Average Engagement Rate Over Time")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Top Categories by Engagement Rate")
    cat_df = pd.read_sql(f"""
        SELECT category_name, ROUND(AVG(engagement_rate)::numeric, 4) AS avg_engagement, COUNT(*) AS video_count
        FROM videos WHERE country IN ({country_filter})
        GROUP BY category_name ORDER BY avg_engagement DESC LIMIT 10
    """, engine)
    fig3 = px.bar(cat_df, x="category_name", y="avg_engagement", color="avg_engagement",
                  color_continuous_scale="Blues", title="Top 10 Categories by Avg Engagement Rate")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Top Categories by Average Views")
    views_df = pd.read_sql(f"""
        SELECT category_name, ROUND(AVG(views)::numeric, 0) AS avg_views
        FROM videos WHERE country IN ({country_filter})
        GROUP BY category_name ORDER BY avg_views DESC LIMIT 10
    """, engine)
    fig4 = px.bar(views_df, x="category_name", y="avg_views", color="avg_views",
                  color_continuous_scale="Oranges", title="Top 10 Categories by Avg Views")
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.subheader("Engagement Rate by Country")
    country_df = pd.read_sql(f"""
        SELECT country, ROUND(AVG(engagement_rate)::numeric, 4) AS avg_engagement,
               ROUND(AVG(views)::numeric, 0) AS avg_views
        FROM videos WHERE country IN ({country_filter})
        GROUP BY country ORDER BY avg_engagement DESC
    """, engine)
    fig5 = px.bar(country_df, x="country", y="avg_engagement", color="avg_engagement",
                  color_continuous_scale="Greens", title="Average Engagement Rate by Country")
    st.plotly_chart(fig5, use_container_width=True)
    st.dataframe(country_df, use_container_width=True)

with tab4:
    st.subheader("Raw Data Sample")
    raw_df = pd.read_sql(f"""
        SELECT video_id, title, channel_title, category_name, country, views, likes, engagement_rate
        FROM videos WHERE country IN ({country_filter})
        ORDER BY views DESC LIMIT 200
    """, engine)
    st.dataframe(raw_df, use_container_width=True)