import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Monitoring Tracer Study", layout="wide")
st.title("📊 Dashboard Monitoring Tracer Study FEB Unisba")

# 1. Load Data
@st.cache_data
def load_data():
    # Pastikan nama file sesuai dengan yang ada di folder Anda
    df = pd.read_csv("Data TS 2023.xlsx - Sheet1.csv")
    return df

try:
    df = load_data()
    
    # 2. Pembersihan & Pemetaan Data (Mapping)
    rating_map = {"Sangat Tinggi": 4, "Tinggi": 3, "Sedang": 2, "Rendah": 1, "Sangat Rendah": 0}
    
    def clean_and_map(val):
        if pd.isna(val) or not isinstance(val, str): return np.nan
        return rating_map.get(val.strip(), np.nan)

    # Identifikasi kolom kompetensi (sesuaikan dengan nama kolom di CSV Anda)
    # Contoh: mengasumsikan kolom kompetensi mengandung teks 'Tinggi' atau pola tertentu
    f1_cols = [c for c in df.columns if c.startswith("f1")] 
    
    # 3. Sidebar Filter
    st.sidebar.header("Filter")
    pilihan_jurusan = st.sidebar.multiselect("Pilih Jurusan", options=df['jurusan'].unique())
    
    if pilihan_jurusan:
        df = df[df['jurusan'].isin(pilihan_jurusan)]

    # 4. Visualisasi
    st.subheader("Analisis Status Lulusan")
    status_counts = df['a16. Bagaimana status Saudara saat ini?'].value_counts()
    fig1 = px.pie(values=status_counts, names=status_counts.index, hole=0.3)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Relevansi Studi vs Pekerjaan")
    # Menggunakan kolom dari data yang ada di file
    rel_col = 'b13. Seberapa erat hubungan antara bidang studi yang Saudara pelajari selama kuliah dengan pekerjaan Saudara?'
    if rel_col in df.columns:
        rel_counts = df[rel_col].value_counts()
        fig2 = px.bar(x=rel_counts.index, y=rel_counts.values, color=rel_counts.index)
        st.plotly_chart(fig2, use_container_width=True)
    
    # 5. Tabel Data
    st.subheader("Data Alumni Terbaru")
    st.dataframe(df)

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat dashboard: {e}")
    st.write("Pastikan file CSV berada di folder yang sama dengan app.py")
