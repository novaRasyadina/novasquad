import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set(style="darkgrid")
st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")

pertanyaan_1 = (
    "Kategori produk apa saja yang memiliki jumlah pendapatan dari harga barang tanpa ongkos kirim "
    "tertinggi dan terendah pada pesanan delivered selama tahun 2017-2018, sebagai dasar penentuan "
    "prioritas stok dan anggaran promosi?"
)
pertanyaan_2 = (
    "Bagaimana perbedaan rata-rata skor ulasan antara pesanan yang tiba tepat waktu dan yang tiba terlambat, "
    "serta pada keterlambatan berapa hari skor ulasan mulai menurun tajam, pada pesanan delivered selama "
    "tahun 2017-2018, sebagai dasar penentuan batas keterlambatan untuk peningkatan kinerja tim logistik?"
)


@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "main_data.csv")
    df = pd.read_csv(path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df


def format_ribuan(angka):
    # pemisah ribuan pakai titik
    return f"{angka:,.0f}".replace(",", ".")


def format_koma(angka, digit=2):
    return f"{angka:.{digit}f}".replace(".", ",")


main_data = load_data()

# sidebar
min_date = main_data["order_purchase_timestamp"].min().date()
max_date = main_data["order_purchase_timestamp"].max().date()

with st.sidebar:
    st.header("E-Commerce")
    date_range = st.date_input(
        "Rentang tanggal pembelian",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    st.caption("Pilih 1 Januari 2017 sampai 31 Agustus 2018 untuk periode analisis 2017-2018.")

# kalau baru satu tanggal yang dipilih, pakai rentang penuh dulu
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

df = main_data[
    (main_data["order_purchase_timestamp"].dt.date >= start_date)
    & (main_data["order_purchase_timestamp"].dt.date <= end_date)
].copy()

if df.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
    st.stop()

# satu baris per pesanan
orders = df.drop_duplicates(subset="order_id").copy()

# judul dan ringkasan
st.title("Dashboard Analisis Data E-Commerce")
st.write(
    "Dashboard ini menjawab dua pertanyaan bisnis, yaitu kategori produk dengan pendapatan "
    "tertinggi dan terendah, serta perbedaan skor ulasan antara pesanan tepat waktu dan terlambat. "
    "Ada juga analisis lanjutan berupa geospatial dan RFM."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pendapatan", "BRL " + format_ribuan(df["price"].sum()))
col2.metric("Jumlah Pesanan", format_ribuan(orders["order_id"].nunique()))
col3.metric("Rata-rata Skor Ulasan", format_koma(orders["review_score"].mean()))
persen_telat = (orders["delay_days"].dropna() > 0).mean() * 100
col4.metric("Pesanan Terlambat", format_koma(persen_telat) + "%")

# pertanyaan 1
st.header("Pertanyaan 1")
st.write(pertanyaan_1)

revenue = (
    df.groupby("category", as_index=False)["price"]
    .sum()
    .rename(columns={"price": "revenue"})
    .sort_values("revenue", ascending=False)
)
top5 = revenue.head(5)
bottom5 = revenue.tail(5).sort_values("revenue")

fig, ax = plt.subplots(1, 2, figsize=(18, 6))

sns.barplot(data=top5, x="revenue", y="category", color="#3b78b5", ax=ax[0])
ax[0].set_title("5 Kategori dengan Pendapatan Tertinggi", fontsize=14)
ax[0].set_xlabel("Total pendapatan (BRL)")
ax[0].set_ylabel("")

sns.barplot(data=bottom5, x="revenue", y="category", color="#c0504d", ax=ax[1])
ax[1].set_title("5 Kategori dengan Pendapatan Terendah", fontsize=14)
ax[1].set_xlabel("Total pendapatan (BRL)")
ax[1].set_ylabel("")

plt.tight_layout()
st.pyplot(fig)

share_top5 = top5["revenue"].sum() / revenue["revenue"].sum() * 100
st.write(
    f"Kategori {top5.iloc[0]['category']} menyumbang pendapatan terbesar, yaitu "
    f"BRL {format_ribuan(top5.iloc[0]['revenue'])}. Lima kategori teratas menyumbang "
    f"sekitar {format_koma(share_top5, 1)}% dari total pendapatan. Kategori dengan pendapatan "
    f"paling rendah adalah {bottom5.iloc[0]['category']} "
    f"(BRL {format_ribuan(bottom5.iloc[0]['revenue'])})."
)

# pertanyaan 2
st.header("Pertanyaan 2")
st.write(pertanyaan_2)

delay_df = orders.dropna(subset=["delay_days", "review_score"]).copy()
delay_df["is_negative"] = delay_df["review_score"] <= 2

bins = [-float("inf"), -7, 0, 3, 7, 14, float("inf")]
labels = ["Lebih awal >7 hari", "Lebih awal 0-7 hari", "Telat 0-3 hari",
          "Telat 3-7 hari", "Telat 7-14 hari", "Telat >14 hari"]
delay_df["kelompok"] = pd.cut(delay_df["delay_days"], bins=bins, labels=labels)

ringkasan = (
    delay_df.groupby("kelompok", observed=True)
    .agg(
        rata_skor=("review_score", "mean"),
        persen_buruk=("is_negative", lambda x: x.mean() * 100),
    )
    .reset_index()
)

fig, ax = plt.subplots(1, 2, figsize=(18, 6))

sns.barplot(data=ringkasan, x="kelompok", y="rata_skor", color="#5b9b5b", ax=ax[0])
ax[0].set_title("Rata-rata Skor Ulasan per Kelompok Keterlambatan", fontsize=14)
ax[0].set_xlabel("")
ax[0].set_ylabel("Rata-rata skor ulasan (1-5)")
ax[0].set_ylim(0, 5)
ax[0].tick_params(axis="x", rotation=20)
for c in ax[0].containers:
    ax[0].bar_label(c, fmt="%.2f", padding=3)

sns.barplot(data=ringkasan, x="kelompok", y="persen_buruk", color="#c0504d", ax=ax[1])
ax[1].set_title("Persentase Ulasan Buruk (Skor 1-2) per Kelompok", fontsize=14)
ax[1].set_xlabel("")
ax[1].set_ylabel("Ulasan buruk (%)")
ax[1].set_ylim(0, 100)
ax[1].tick_params(axis="x", rotation=20)
for c in ax[1].containers:
    ax[1].bar_label(c, fmt="%.1f%%", padding=3)

plt.tight_layout()
st.pyplot(fig)

skor_tepat = delay_df.loc[delay_df["delay_days"] <= 0, "review_score"].mean()
skor_telat = delay_df.loc[delay_df["delay_days"] > 0, "review_score"].mean()
teks = (
    f"Pesanan yang tiba tepat waktu memiliki rata-rata skor {format_koma(skor_tepat)}, "
    f"sedangkan pesanan yang terlambat hanya {format_koma(skor_telat)}."
)
selisih = ringkasan["rata_skor"].diff()
if selisih.notna().any():
    kelompok_turun = ringkasan.loc[selisih.idxmin(), "kelompok"]
    teks += f" Penurunan skor paling besar terjadi pada kelompok {kelompok_turun}."
st.write(teks)

# geospatial
st.header("Analisis Lanjutan: Geospatial")

kiri, kanan = st.columns(2)

with kiri:
    state_df = (
        delay_df.assign(telat=delay_df["delay_days"] > 0)
        .groupby("customer_state")
        .agg(persen_telat=("telat", "mean"), jumlah_pesanan=("order_id", "count"))
        .reset_index()
    )
    state_df["persen_telat"] = state_df["persen_telat"] * 100
    state_df = state_df[state_df["jumlah_pesanan"] >= 300]
    state_top = state_df.sort_values("persen_telat", ascending=False).head(10)

    if state_top.empty:
        st.info("Tidak ada negara bagian dengan minimal 300 pesanan pada rentang tanggal ini.")
    else:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(data=state_top, x="persen_telat", y="customer_state", color="#e08a2c", ax=ax)
        ax.set_title("10 Negara Bagian dengan Persentase Keterlambatan Tertinggi", fontsize=13)
        ax.set_xlabel("Pesanan terlambat (%)")
        ax.set_ylabel("Negara bagian")
        st.pyplot(fig)
        st.caption("Hanya negara bagian dengan minimal 300 pesanan.")

with kanan:
    st.write("Sebaran lokasi pelanggan dengan pesanan terlambat")
    map_df = (
        orders[orders["delay_days"] > 0]
        .dropna(subset=["lat", "lng"])
        .rename(columns={"lng": "lon"})[["lat", "lon"]]
    )
    st.map(map_df)

# rfm
st.header("Analisis Lanjutan: RFM")

ref_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)
rfm = (
    orders.groupby("customer_unique_id")
    .agg(
        terakhir_beli=("order_purchase_timestamp", "max"),
        frequency=("order_id", "nunique"),
        monetary=("payment_value", "sum"),
    )
    .reset_index()
)
rfm["recency"] = (ref_date - rfm["terakhir_beli"]).dt.days
rfm["id_singkat"] = rfm["customer_unique_id"].str[:8]

c1, c2, c3 = st.columns(3)
c1.metric("Rata-rata Recency", f"{rfm['recency'].mean():.0f} hari")
c2.metric("Rata-rata Frequency", format_koma(rfm["frequency"].mean()))
c3.metric("Rata-rata Monetary", "BRL " + format_koma(rfm["monetary"].mean()))

fig, ax = plt.subplots(1, 3, figsize=(20, 6))
warna = "#72bcd4"

sns.barplot(data=rfm.sort_values("recency").head(5), x="recency", y="id_singkat", color=warna, ax=ax[0])
ax[0].set_title("Recency Terbaik (hari)", fontsize=13)

sns.barplot(data=rfm.sort_values("frequency", ascending=False).head(5), x="frequency", y="id_singkat", color=warna, ax=ax[1])
ax[1].set_title("Frequency Tertinggi (transaksi)", fontsize=13)

sns.barplot(data=rfm.sort_values("monetary", ascending=False).head(5), x="monetary", y="id_singkat", color=warna, ax=ax[2])
ax[2].set_title("Monetary Tertinggi (BRL)", fontsize=13)

for a in ax:
    a.set_xlabel("")
    a.set_ylabel("ID pelanggan")
    a.tick_params(axis="y", labelsize=9)

plt.tight_layout()
st.pyplot(fig)

persen_repeat = (rfm["frequency"] > 1).mean() * 100
st.write(
    f"Hanya sekitar {format_koma(persen_repeat, 1)}% pelanggan yang berbelanja lebih dari satu kali, "
    "sehingga masih ada peluang untuk meningkatkan retensi pelanggan."
)

st.caption("Sumber data: E-Commerce Public Dataset")