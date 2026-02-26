import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Executive E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# Header
# =========================
st.title("📊 Executive E-Commerce Sales Dashboard")
st.markdown("Analisis performa bisnis berdasarkan data transaksi")

st.markdown("---")

# =========================
# Load Data
# =========================
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(__file__)
    DATA_PATH = os.path.join(BASE_DIR, "main_data.csv")

    df = pd.read_csv(DATA_PATH)

    # Bersihkan nama kolom (anti error spasi & huruf besar)
    df.columns = df.columns.str.strip().str.lower()

    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['year_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    return df

df = load_data()

# =========================
# Sidebar Filter
# =========================
st.sidebar.header("📌 Filter Data")

selected_month = st.sidebar.multiselect(
    "Pilih Bulan",
    options=sorted(df['year_month'].unique()),
    default=sorted(df['year_month'].unique())
)

filtered_df = df[df['year_month'].isin(selected_month)]

# =========================
# KPI Section
# =========================
total_revenue = filtered_df['revenue'].sum()
total_orders = filtered_df['order_id'].nunique()
aov = total_revenue / total_orders if total_orders > 0 else 0

st.subheader("📈 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"R$ {total_revenue:,.0f}")
col2.metric("🛒 Total Orders", f"{total_orders:,}")
col3.metric("📦 Average Order Value", f"R$ {aov:,.2f}")

st.markdown("---")

# =========================
# Monthly Revenue Analysis
# =========================
monthly_sales = (
    filtered_df.groupby('year_month')['revenue']
    .sum()
    .reset_index()
)

peak_month = monthly_sales.loc[monthly_sales['revenue'].idxmax()]
peak_value = peak_month['revenue']
peak_label = peak_month['year_month']

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📅 Monthly Revenue Trend")

    fig1, ax1 = plt.subplots(figsize=(6,4))
    ax1.plot(monthly_sales['year_month'], monthly_sales['revenue'])
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue")

    # tampilkan tick setiap 2 bulan agar tidak padat
    ax1.set_xticks(range(0, len(monthly_sales), 2))
    ax1.set_xticklabels(monthly_sales['year_month'][::2], rotation=45)

    st.pyplot(fig1)

with col_right:
    st.subheader("🏆 Top 10 Categories by Revenue")

    top_categories = (
        filtered_df.groupby('product_category_name_english')['revenue']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(6,4))
    top_categories.sort_values().plot(kind='barh', ax=ax2)
    ax2.set_xlabel("Revenue")
    st.pyplot(fig2)

st.markdown("---")

# =========================
# Executive Insight Section
# =========================

top_category = top_categories.idxmax()

st.info(f"""
### 📌 Key Business Insights

• Revenue menunjukkan tren pertumbuhan yang konsisten dengan pola musiman yang jelas.  
• Puncak revenue terjadi pada **{peak_label}** dengan total sebesar **R$ {peak_value:,.0f}**.  
• Kategori dengan kontribusi revenue tertinggi adalah **{top_category}**.  
• Strategi optimalisasi promosi pada periode high season berpotensi meningkatkan profit secara signifikan.  
• Penurunan pada bulan terakhir kemungkinan disebabkan oleh data yang belum lengkap, sehingga perlu interpretasi yang hati-hati.
""")

# =========================
# Footer
# =========================
st.markdown("---")
st.markdown(
    """
    <center>
    <small>
    Executive Dashboard - Proyek Analisis Data Dicoding<br>
    Developed using Streamlit & Python
    </small>
    </center>
    """,
    unsafe_allow_html=True
)


