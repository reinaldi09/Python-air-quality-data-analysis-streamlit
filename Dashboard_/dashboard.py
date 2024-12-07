import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# Load data polusi udara
# data = pd.read_csv("all_data.csv")

data = pd.read_csv("./Dashboard_/all_data.csv")

# Konversi kolom 'datetime' ke datetime dan atur sebagai indeks
data['datetime'] = pd.to_datetime(data['datetime'])
data.set_index('datetime', inplace=True)

# Sidebar untuk filter data berdasarkan rentang waktu
with st.sidebar:
    # st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.image("./Python-air-quality-data-analysis-streamlit/Assets/datt.webp")
    start_date, end_date = st.date_input(
        "Pilih rentang waktu:",
        [data.index.min().date(), data.index.max().date()]
    )

# Filter data sesuai rentang waktu
filtered_data = data.loc[start_date:end_date]

# --- 1. Tren PM2.5 dan PM10 sepanjang tahun ---
st.header("Tren PM2.5 dan PM10 Sepanjang Tahun")

fig, ax = plt.subplots(figsize=(14, 6))
sns.lineplot(data=filtered_data[['PM2.5', 'PM10']], palette='muted', ax=ax)
ax.set_title("Tren PM2.5 dan PM10", fontsize=16)
ax.set_ylabel("Konsentrasi (µg/m³)")
ax.set_xlabel("Tanggal")
st.pyplot(fig)

st.markdown("Grafik menunjukkan tren musiman dari PM2.5 dan PM10 sepanjang tahun.")

# --- 2. Hubungan NO2 dan SO2 dengan Suhu ---
st.header("Hubungan Antara Konsentrasi NO2 dan SO2 dengan Suhu")

fig, ax = plt.subplots(1, 2, figsize=(16, 6))
sns.scatterplot(x='TEMP', y='NO2', data=filtered_data, ax=ax[0], color='orange')
ax[0].set_title("NO2 vs Suhu")
ax[0].set_xlabel("Suhu (°C)")
ax[0].set_ylabel("Konsentrasi NO2 (µg/m³)")

sns.scatterplot(x='TEMP', y='SO2', data=filtered_data, ax=ax[1], color='purple')
ax[1].set_title("SO2 vs Suhu")
ax[1].set_xlabel("Suhu (°C)")
ax[1].set_ylabel("Konsentrasi SO2 (µg/m³)")

st.pyplot(fig)
st.markdown("Hubungan antara NO2 dan SO2 dengan suhu dapat membantu memahami bagaimana polutan ini bereaksi terhadap perubahan suhu.")

# --- 3. Hubungan Kecepatan Angin dan Polutan ---
st.header("Hubungan Antara Kecepatan Angin dan Polutan")

fig, ax = plt.subplots(1, 3, figsize=(20, 6))
sns.scatterplot(x='WSPM', y='PM2.5', data=filtered_data, ax=ax[0], color='blue')
ax[0].set_title("PM2.5 vs Kecepatan Angin")
sns.scatterplot(x='WSPM', y='PM10', data=filtered_data, ax=ax[1], color='green')
ax[1].set_title("PM10 vs Kecepatan Angin")
sns.scatterplot(x='WSPM', y='CO', data=filtered_data, ax=ax[2], color='red')
ax[2].set_title("CO vs Kecepatan Angin")

st.pyplot(fig)
st.markdown("Grafik di atas menunjukkan hubungan antara kecepatan angin dan polutan seperti PM2.5, PM10, dan CO.")

# --- 4. Clustering Manual untuk PM2.5 ---
def categorize_pm25(value):
    if value <= 50:
        return 'Low'
    elif 50 < value <= 100:
        return 'Moderate'
    else:
        return 'High'

filtered_data['PM2.5_Category'] = filtered_data['PM2.5'].apply(categorize_pm25)
colors = {'Low': 'green', 'Moderate': 'orange', 'High': 'red'}

st.header("Clustering Manual untuk PM2.5")
fig, ax = plt.subplots(figsize=(10, 6))
for category, color in colors.items():
    subset = filtered_data[filtered_data['PM2.5_Category'] == category]
    ax.scatter(subset['PM2.5'], subset['PM10'], label=category, color=color, alpha=0.6)
ax.set_title('Scatter Plot of PM2.5 vs PM10 with Categories')
ax.set_xlabel('PM2.5')
ax.set_ylabel('PM10')
ax.legend(title='PM2.5 Category')
st.pyplot(fig)

st.markdown("Scatter plot menunjukkan hubungan PM2.5 dan PM10 berdasarkan kategori PM2.5.")

# --- 5. Clustering Manual untuk NO2 ---
def cluster_NO2(value):
    if value <= 30:
        return 'Rendah'
    elif 30 < value <= 80:
        return 'Sedang'
    else:
        return 'Tinggi'

filtered_data['NO2_Cluster'] = filtered_data['NO2'].apply(cluster_NO2)

st.header("Clustering Manual untuk NO2")
fig, ax = plt.subplots(1, 2, figsize=(16, 6))
sns.countplot(data=filtered_data, x='NO2_Cluster', order=['Rendah', 'Sedang', 'Tinggi'], palette='coolwarm', ax=ax[0])
ax[0].set_title('Distribusi Clustering Manual NO2')
sns.boxplot(data=filtered_data, x='NO2_Cluster', y='NO2', order=['Rendah', 'Sedang', 'Tinggi'], palette='coolwarm', ax=ax[1])
ax[1].set_title('Distribusi Nilai NO2 Berdasarkan Cluster')
st.pyplot(fig)

st.markdown("Distribusi nilai NO2 berdasarkan cluster membantu memahami pola konsentrasi NO2.")
