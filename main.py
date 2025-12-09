import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

class RobotAnalisis:
    def __init__(self, uploaded_file):
        try:
            self.df = pd.read_csv(uploaded_file, encoding='latin-1')
            self.df['Order Date'] = pd.to_datetime(self.df['Order Date'], errors='coerce')
        except Exception as e:
            st.error(f"❌ Data gagal dimuat: {e}")

    def cek_kesehatan_data(self):
        st.subheader("🏥 Cek Kesehatan Data")
        missing = self.df.isnull().sum()
        if missing.sum() == 0:
            st.success("✨ Data bersih! Tidak ada nilai kosong (NaN).")
        else:
            st.warning("⚠️ Ditemukan data kosong.")
            st.write(missing[missing > 0])

    def ringkasan_bisnis(self):
        st.subheader("💰 Ringkasan Bisnis")
        total_sales = self.df['Sales'].sum()
        total_profit = self.df['Profit'].sum()
        margin = (total_profit / total_sales) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Penjualan", f"${total_sales:,.2f}")
        col2.metric("Total Profit", f"${total_profit:,.2f}")
        col3.metric("Margin Keuntungan", f"{margin:.2f}%")

    def analisis_strategi(self):
        st.subheader("📊 Performa per Kategori")
        hasil = self.df.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
        st.dataframe(hasil, use_container_width=True) 

    def visualisasi_data(self):
        st.subheader("📈 Tren Penjualan Bulanan")

        # Set index ke tanggal
        df_waktu = self.df.set_index('Order Date')
        
        # --- PERBAIKAN 1: Ganti 'M' jadi 'ME' ---
        tren_bulanan = df_waktu['Sales'].resample('ME').sum()

        # --- PERBAIKAN 2: Teknik Gambar Khusus Streamlit ---
        # Kita harus membuat objek 'fig' (kanvas) dan 'ax' (kuas)
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Menggambar di atas 'ax'
        ax.plot(tren_bulanan.index, tren_bulanan.values, marker='o', linestyle='-', color='teal')
        ax.set_title('Tren Penjualan Bulanan Superstore')
        ax.set_xlabel('Waktu')
        ax.set_ylabel('Penjualan ($)')
        ax.grid(True, linestyle='--', alpha=0.5)

        # Jangan pakai plt.show(), tapi pakai st.pyplot(fig)
        st.pyplot(fig)

# --- MAIN PROGRAM ---
st.set_page_config(page_title="Robot Analisis Toko", layout="wide")
st.title("🤖 Robot Analisis Data Toko")

st.sidebar.header("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload file CSV di sini", type=["csv"])

if uploaded_file is not None:
    robot = RobotAnalisis(uploaded_file)
    
    # Jalankan Metode
    robot.cek_kesehatan_data()
    st.markdown("---")
    robot.ringkasan_bisnis()
    st.markdown("---")
    robot.analisis_strategi()
    st.markdown("---")
    robot.visualisasi_data()
else:

    st.info("👋 Silakan upload file CSV di sidebar untuk memulai.")
