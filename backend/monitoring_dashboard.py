import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set default values
default_reaction_type = "dislike"
default_start_date = datetime.now() - timedelta(days=30)
default_end_date = datetime.now()

# Streamlit UI
st.title("Gus Meta Reaction Monitoring Dashboard")

# Dropdown for selecting reaction type
reaction_type = st.selectbox(
    "Select Reaction Type:",
    options=["like", "dislike", "regenerate"],
    index=1  # default is "dislike"
)

# Input for selecting start date
start_date = st.date_input(
    "Select Start Date:",
    value=default_start_date.date()
)

# Input for selecting end date
end_date = st.date_input(
    "Select End Date:",
    value=default_end_date.date()
)

# Dropdown for selecting plot type
plot_type = st.selectbox(
    "Select Plot Type:",
    options=['Scatter', "Line"]
)

# Make sure end date is after start date
if start_date > end_date:
    st.error("End Date must be after Start Date.")
    st.stop()

# Convert dates to string format with time component
start_date_str = datetime.combine(start_date, datetime.min.time()).strftime("%Y-%m-%d %H:%M:%S")
end_date_str = datetime.combine(end_date, datetime.max.time()).strftime("%Y-%m-%d %H:%M:%S")

# Function to fetch reaction data from the FastAPI backend
def fetch_reaction_data(reaction_type, start_date, end_date):
    url = f"http://localhost:8000/all-reactions"
    params = {
        "reaction_type": reaction_type,
        "start_datetime": start_date,
        "end_datetime": end_date
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data['reactions']
    else:
        st.error("Failed to fetch data from the API.")
        return None

# Fetch the data from FastAPI
reactions = fetch_reaction_data(reaction_type, start_date_str, end_date_str)

def create_plot(df, plot_type):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if plot_type == "Scatter":
        ax.scatter(df.index, df['count'])
    else:  # Line plot
        ax.plot(df.index, df['count'])
    
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Reaksi')
    ax.set_title(f'{reaction_type.capitalize()} Reactions over Time')
    
    # Mengatur format tanggal pada sumbu x
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    
    # Merotasi label sumbu x untuk keterbacaan yang lebih baik
    plt.xticks(rotation=45, ha='right')
    
    # Mengatur tata letak agar tidak terpotong
    plt.tight_layout()
    
    return fig



# Jika ada data reaksi, proses dan tampilkan
if reactions is not None and len(reactions) > 0:
    # Konversi list reaksi menjadi DataFrame
    df = pd.DataFrame(reactions)
    
    # Konversi kolom 'created_at' menjadi datetime
    df['created_at'] = pd.to_datetime(df['created_at'])
    
    # Kelompokkan reaksi berdasarkan tanggal (tanpa komponen waktu)
    df_grouped = df.groupby(df['created_at'].dt.date).size().reset_index(name='count')
    
    # Ubah nama kolom untuk kejelasan
    df_grouped.rename(columns={'created_at': 'Date'}, inplace=True)
    
    # Konversi kolom 'Date' menjadi datetime
    df_grouped['Date'] = pd.to_datetime(df_grouped['Date'])
    
    # Urutkan berdasarkan tanggal
    df_grouped.sort_values('Date', inplace=True)
    
    # Atur 'Date' sebagai indeks
    df_grouped.set_index('Date', inplace=True)

    # Buat plot menggunakan Matplotlib
    fig = create_plot(df_grouped, plot_type)
    
    # Tampilkan plot menggunakan Streamlit
    st.pyplot(fig)
else:
    st.warning("Tidak ada reaksi yang ditemukan untuk kriteria yang dipilih.")