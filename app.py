import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Judul & Konfigurasi
st.set_page_config(page_title="Dashboard Tracer Study", layout="wide")
st.title("📊 Dashboard Monitoring Tracer Study FEB Unisba")

# 2. Load Data (Otomatis deteksi perubahan file)
@st.cache_data
def load_data():
    return pd.read_csv("Data_Tracer_2023.csv") # Sesuaikan path file Anda

df = load_data()

# 3. Sidebar untuk Filter
st.sidebar.header("Filter Data")
jurusan = st.sidebar.multiselect("Pilih Jurusan", options=df['jurusan'].unique())

# 4. Visualisasi Utama
col1, col2 = st.columns(2)

with col1:
    st.subheader("Status Lulusan")
    status_counts = df['a16. Bagaimana status Saudara saat ini?'].value_counts()
    fig1 = px.pie(values=status_counts, names=status_counts.index, hole=0.3)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Relevansi Studi vs Pekerjaan")
    # Logika untuk menghitung seberapa erat hubungan
    rel_counts = df['b13. Seberapa erat hubungan?'].value_counts()
    fig2 = px.bar(x=rel_counts.index, y=rel_counts.values)
    st.plotly_chart(fig2, use_container_width=True)

# 5. Tabel Monitoring Live
st.subheader("Data Alumni Terbaru")
st.dataframe(df)
