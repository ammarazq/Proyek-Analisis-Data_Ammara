import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Fungsi untuk menyiapkan dataframe berdasarkan berat produk dari dataset produk
def create_byweight_df(products_df):
    byweight_df = products_df.groupby(by="product_id").agg({
        "product_weight_g": "max"  # Mengambil berat maksimum untuk setiap produk
    }).reset_index()
    byweight_df.rename(columns={"product_weight_g": "max_product_weight_g"}, inplace=True)
    
    return byweight_df

# Fungsi untuk menyiapkan dataframe berdasarkan kota dan menghitung jumlah penjual dari dataset penjual
def create_byseller_city_df(sellers_df):
    byseller_city_df = sellers_df.groupby("seller_city").seller_id.nunique().reset_index()
    byseller_city_df.rename(columns={
        "seller_id": "seller_count"
    }, inplace=True)
    
    # Mengurutkan kota berdasarkan jumlah penjual terbanyak
    byseller_city_df = byseller_city_df.sort_values(by="seller_count", ascending=False)
    
    return byseller_city_df


# Load dataset produk dan penjual
products_df = pd.read_csv("products_dataset.csv")
sellers_df = pd.read_csv("sellers_dataset.csv")


# Menyiapkan dataframe untuk produk terberat dan kota dengan seller terbanyak
byweight_df = create_byweight_df(products_df)
byseller_city_df = create_byseller_city_df(sellers_df)

# Menampilkan produk dengan berat terbesar
st.header('Dashboard Produk dan Seller')
st.subheader('Top 5 Produk Terberat')

# Plotting produk terberat
top_heavy_products = byweight_df.sort_values(by="max_product_weight_g", ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="max_product_weight_g", 
    x="product_id",
    data=top_heavy_products,
    palette="Blues_d"
)
ax.set_title("Top 5 Produk Terberat", fontsize=15)
ax.set_xlabel("Product ID")
ax.set_ylabel("Weight (g)")
plt.xticks(rotation=45)
st.pyplot(fig)

# Menampilkan kota dengan seller terbanyak
st.subheader('Top 5 Kota dengan Seller Terbanyak')
# Plotting kota dengan seller terbanyak
top_seller_cities = byseller_city_df.head(5)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    y="seller_count", 
    x="seller_city",
    data=top_seller_cities,
    palette="Blues_d"
)
ax.set_title("Top 5 Kota dengan Seller Terbanyak", fontsize=15)
ax.set_xlabel("City")
ax.set_ylabel("Seller Count")
st.pyplot(fig)

st.caption('By: Ammara Desma Marzooqa')
