# -*- coding: utf-8 -*-
"""dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1deEgDcOknc3BvzLtJbvlbGiL4YRIsQ-W
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install streamlit seaborn matplotlib pandas

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Analisis E-Commerce", layout="wide")

# Judul Dashboard
st.title("Dashboard Analisis E-Commerce")
st.write("""
    Dashboard ini memberikan gambaran tentang analisis data e-commerce berdasarkan beberapa pertanyaan utama.
    Berikut adalah analisis tentang kategori produk, tren penjualan, tingkat kepuasan pelanggan, dan daerah yang paling aktif bertransaksi.
""")

# Load Data
@st.cache
def load_data():
    return pd.read_csv("dashboard/main_data.csv")  
data = load_data()

# Sidebar untuk filter interaktif
st.sidebar.header("Filter Data")
selected_category = st.sidebar.selectbox("Pilih Kategori Produk:", data['product_category_name'].unique())
selected_state = st.sidebar.selectbox("Pilih Negara Bagian:", data['customer_state'].unique())
selected_year = st.sidebar.slider("Pilih Tahun Transaksi:", min_value=int(data['order_year'].min()), max_value=int(data['order_year'].max()), value=int(data['order_year'].max()))

# Filter Data Berdasarkan Pilihan
filtered_data = data[(data['product_category_name'] == selected_category) &
                     (data['customer_state'] == selected_state) & 
                     (data['order_year'] == selected_year)]

# Menampilkan Tabel Data yang Sudah Difilter
st.write(f"Data untuk kategori: **{selected_category}**, negara bagian: **{selected_state}**, tahun: **{selected_year}**")
st.dataframe(filtered_data)

# Plot 1: Kategori Produk Paling Populer dan Paling Tidak Diminati
st.subheader("Kategori Produk Paling Populer dan Paling Tidak Diminati")

category_popularity = data.groupby('product_category_name')['order_id'].count().sort_values(ascending=False).reset_index()
category_popularity.columns = ['product_category_name', 'transaction_count']

# Visualisasi 5 Produk Paling Populer dan Paling Tidak Diminati
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

# Visualisasi 5 Produk Paling Populer
sns.barplot(data=category_popularity.head(5), x='transaction_count', y='product_category_name', palette='Blues_d', ax=ax[0])
ax[0].set_title('5 Kategori Produk Paling Populer Berdasarkan Jumlah Transaksi')
ax[0].set_xlabel('Jumlah Transaksi')
ax[0].set_ylabel('Kategori Produk')

# Visualisasi 5 Produk Paling Tidak Diminati (Dimulai dari yang Terendah)
sns.barplot(data=category_popularity.tail(5).sort_values(by='transaction_count', ascending=True),
            x='transaction_count', y='product_category_name', palette='Blues_d', ax=ax[1])
ax[1].set_title('5 Kategori Produk Paling Tidak Diminati Berdasarkan Jumlah Transaksi')
ax[1].set_xlabel('Jumlah Transaksi')
ax[1].set_ylabel('Kategori Produk')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position('right')
ax[1].yaxis.tick_right()

plt.tight_layout()
st.pyplot(plt)

# Plot 2: Tren Penjualan E-Commerce dari Waktu ke Waktu
# Tambahkan subtitle pada dashboard
st.subheader("Tren Penjualan E-Commerce dari Waktu ke Waktu")

# Pastikan order_purchase_timestamp berbentuk datetime
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'], errors='coerce')

# Tampilkan kolom untuk debugging
st.write(data.columns)

# Buat kolom 'month_year'
data['month_year'] = data['order_purchase_timestamp'].dt.to_period('M')

# Hitung jumlah transaksi bulanan
monthly_sales = data.groupby('month_year')['order_id'].count().reset_index()
monthly_sales.columns = ['month_year', 'transaction_count']

# Konversi 'month_year' ke datetime untuk visualisasi
monthly_sales['month_year'] = monthly_sales['month_year'].astype(str)
monthly_sales['month_year'] = pd.to_datetime(monthly_sales['month_year'], format='%Y-%m')

# Visualisasi
plt.figure(figsize=(16, 6))
sns.lineplot(data=monthly_sales, x='month_year', y='transaction_count', marker='o', color='blue')
plt.title('Tren Penjualan E-Commerce dari Waktu ke Waktu')
plt.xlabel('Bulan-Tahun')
plt.ylabel('Jumlah Transaksi')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# Tampilkan visualisasi di Streamlit
st.pyplot(plt)

# Plot 3: Tingkat Kepuasan Pelanggan pada Tahun Terakhir
st.subheader(f"Tingkat Kepuasan Pelanggan pada Tahun {selected_year}")
review_distribution = data[data['order_year'] == selected_year].groupby('review_score')['order_id'].count().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=review_distribution, x='review_score', y='order_id', palette='Blues_d')
plt.title(f"Distribusi Skor Ulasan di Tahun {selected_year}", fontsize=14)
plt.xlabel("Skor Ulasan")
plt.ylabel("Jumlah")
st.pyplot(plt)

# Plot 4: Daerah Paling Aktif Bertransaksi di E-Commerce
st.subheader("Daerah Paling Aktif Bertransaksi")
state_activity = data.groupby('customer_state')['customer_id'].nunique().sort_values(ascending=False).reset_index()
state_activity.columns = ['customer_state', 'unique_customers']
plt.figure(figsize=(10, 6))
sns.barplot(data=state_activity.head(10), x='unique_customers', y='customer_state', palette='Blues_d')
plt.title("10 Daerah Paling Aktif Bertransaksi di E-Commerce", fontsize=14)
plt.xlabel("Jumlah Pelanggan Unik")
plt.ylabel("Negara Bagian")
st.pyplot(plt)

# Insight RFM Analysis
st.subheader("Segmentasi Pelanggan Berdasarkan RFM")
rfm_summary = pd.DataFrame({
    'Rata-Rata Recency': [data['recency'].mean()],
    'Rata-Rata Frequency': [data['frequency'].mean()],
    'Rata-Rata Monetary': [data['monetary'].mean()]
})
st.write(rfm_summary)

st.write("### Terima kasih telah menggunakan dashboard ini!")
st.write("Nanangsr")
