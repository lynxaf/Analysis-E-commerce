import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set(style='darkgrid')


df = pd.read_csv("all_data.csv")


df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])


min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()

with st.sidebar:
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


filtered_df = df[
    (df['order_purchase_timestamp'].dt.date >= start_date) &
    (df['order_purchase_timestamp'].dt.date <= end_date)
]

product_sales = filtered_df.groupby('product_category_name')['order_id'].count().sort_values(ascending=False)


filtered_df['order_purchase_month'] = filtered_df['order_purchase_timestamp'].dt.month
monthly_sales = filtered_df.groupby('order_purchase_month')['order_id'].count()


st.title("Dashboard Penjualan E-Commerce :shopping_trolley:")
st.caption("Dibuat oleh Mukhlishah Afdhaliyah")


st.header("Produk Terpopuler")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=product_sales.head(10).index, y=product_sales.head(10).values, ax=ax1)
ax1.set_title('10 Produk Paling Digemari')
ax1.set_ylabel('Jumlah Penjualan')
ax1.set_xlabel('Kategori Produk')
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)


st.header("Produk Kurang Populer")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x=product_sales.tail(10).index, y=product_sales.tail(10).values, ax=ax2)
ax2.set_title('10 Produk Paling Sedikit Digemari')
ax2.set_ylabel('Jumlah Penjualan')
ax2.set_xlabel('Kategori Produk')
ax2.tick_params(axis='x', rotation=90)
st.pyplot(fig2)

st.header("Tren Penjualan Bulanan")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, ax=ax3, marker='o')
ax3.set_xlabel('Bulan')
ax3.set_ylabel('Jumlah Penjualan')
ax3.set_title('Tren Penjualan Bulanan')
ax3.set_xticks(range(1, 13))
st.pyplot(fig3)
