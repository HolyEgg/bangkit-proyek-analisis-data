import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px
import seaborn as sea
import streamlit as st
import matplotlib.pyplot as plt

# memberi warna template
px.defaults.template = 'plotly_dark'
px.defaults.color_continuous_scale = 'reds'

#load data
@st.cache_resource
def load_data():
    dataframe_hour = pd.read_csv("https://raw.githubusercontent.com/HolyEgg/bangkit-proyek-analisis-data/main/data/hour.csv")
    return dataframe_hour

dataframe_hour = load_data()

#Judul
st.title("Sewa Sepeda Dashboard")

#Sidebar
img = Image.open('../asset/sepeda.png')
st.sidebar.image(img)

st.sidebar.title("Sewa Sepeda")

st.sidebar.subheader("Seputar Data Ini")

# Menunjukkan Dataset
if st.sidebar.checkbox("Menunjukkan Dataset"):
    st.subheader("Data Mentah")
    st.write(dataframe_hour)
    
# Deskripsi Data    
if st.sidebar.checkbox("Menunjukkan Deskripsi Data"):
    st.subheader('Deskripsi Data')
    st.markdown("""
        - **instant**: record index
        - **dteday**: date
        - **season**: season(1.springer, 2.summer, 3.fall, 4.winter)
        - **yr**: year (0: 2011, 1:2012)
        - **mnth**: month (1 to 12)
        - **hr**: hour (0 to 23)
        - **holiday**: weather day is holiday or not
        - **weekday**: day of the week
        - **workingday**: if day is neither weekend nor holiday is 1, otherwise is 0.
        - **weathersit**:
            1. Clear, Few clouds, Partly cloudy, Partly cloudy
            2. Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
            3. Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
            4. Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
        - **temp**: Normalized temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-8, t_max=+39 (only in hourly scale)
        - **atemp**: Normalized feeling temperature in Celsius. The values are derived via (t-t_min)/(t_max-t_min), t_min=-16, t_max=+50 (only in hourly scale)
        - **hum**: Normalized humidity. The values are divided to 100 (max)
        - **windspeed**: Normalized wind speed. The values are divided to 67 (max)
        - **casual**: count of casual users
        - **registered**: count of registered users
        - **cnt**: count of total rental bikes including both casual and registered
        """)

    
# Menunjukkan summary statistics
if st.sidebar.checkbox("Menunjukkan Summary Statistics"):
    st.subheader("Summary Statistics")
    st.write(dataframe_hour.describe())
    
# Sidebar
st.sidebar.title("Membuat Boxplot")
x_variable = st.sidebar.selectbox("Pilih Variabel X", ['season', 'yr', 'mnth', 'weathersit', 'weekday', 'cnt'])
y_variable = st.sidebar.selectbox("Pilih Variabel Y", ['cnt', 'yr', 'mnth', 'weathersit', 'weekday', 'season'])

# Membuat diagram boxplot
st.subheader('Diagram Boxplot')
st.write(f"Diagram Boxplot untuk Variabel {x_variable} dan {y_variable}")
fig, ax = plt.subplots()
sea.boxplot(data=dataframe_hour, x=x_variable, y=y_variable, ax=ax)
st.pyplot(fig)


st.sidebar.subheader("Pertanyaan")
# Pertanyaan 1
if st.sidebar.checkbox("Pertanyaan 1"):
    st.subheader("Pertanyaan 1 : berapakah rata-rata jumlah sewa perbulan di tahun depan?")
    
    # Menghitung rata-rata jumlah cnt untuk setiap bulan dalam setiap tahun
    average_cnt = dataframe_hour.groupby(['yr', 'mnth'])['cnt'].mean()

    # Menentukan tahun terakhir dalam dataset
    last_year = dataframe_hour['yr'].max()

    # Membuat prediksi untuk tahun-tahun berikutnya
    future_predictions = []
    for year in range(last_year, last_year + 1):  # Prediksi untuk 1 tahun ke depan
        for month in range(1, 13):
            predicted_cnt = average_cnt[(last_year, month)]
            future_predictions.append({'yr': year, 'mnth': month, 'predicted_cnt': predicted_cnt})

    # Membuat dataframe untuk hasil prediksi
    predicted_df = pd.DataFrame(future_predictions)

    # Menampilkan hasil prediksi
    st.write("Hasil Prediksi:")
    st.write(predicted_df)

    # Menampilkan hasil prediksi dengan Plotly Express
    st.write("Grafik Prediksi:")
    fig = px.line(predicted_df, x='mnth', y='predicted_cnt', color='yr',
                labels={'mnth': 'Month', 'predicted_cnt': 'Predicted Count', 'yr': 'Year'},
                title='Predicted Count of Bike Rentals for Future Years')
    st.plotly_chart(fig)

# Pertanyaan 2  
if st.sidebar.checkbox("Pertanyaan 2"):
    st.subheader("Pertanyaan 2 : kelompokkan berapa rata rata jumlah sewa sepeda setiap jam? dan yang mana saja jam dengan rata rata jumlah sewanya termasuk kelas HIGH?")
    
    # Mengelompokkan data berdasarkan jam dan menghitung rata-rata jumlah sewa sepeda
    hourly_avg_cnt = dataframe_hour.groupby('hr')['cnt'].mean().reset_index()

    # Membuat diagram garis menggunakan Plotly Express
    st.write("Mean Count of Bike Rentals per Hour:")
    fig = px.line(hourly_avg_cnt, x='hr', y='cnt', 
                labels={'hr': 'Hour', 'cnt': 'Mean Count'},
                title='Mean Count of Bike Rentals per Hour')
    st.plotly_chart(fig)

    # Menambahkan kolom cluster berdasarkan rata-rata jumlah sewa
    hourly_avg_cnt['cluster'] = pd.cut(hourly_avg_cnt['cnt'], bins=3, labels=['low', 'medium', 'high'])

    # Menampilkan data hasil pengelompokan
    st.write("Data Hasil Pengelompokan:")
    st.write(hourly_avg_cnt)

    # Filter data untuk clustering "high"
    high_cluster_hours = hourly_avg_cnt[hourly_avg_cnt['cluster'] == 'high']

    # Menampilkan hasil
    st.write("\nJam dengan jumlah sewa sepeda tertinggi (clustering 'high'):")
    st.write(high_cluster_hours)
