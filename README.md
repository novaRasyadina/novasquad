# Proyek Analisis Data: E-Commerce Public Dataset (Olist)

## Deskripsi Proyek

Proyek ini menganalisis E-Commerce Public Dataset milik Olist, sebuah marketplace di Brasil. Analisis dilakukan untuk menjawab dua pertanyaan bisnis berikut:

1. Kategori produk apa yang memberikan kontribusi pendapatan tertinggi dan terendah pada periode 2017-2018?
2. Bagaimana pengaruh keterlambatan pengiriman terhadap skor ulasan pelanggan pada periode 2017-2018?

Selain itu, proyek ini memuat analisis lanjutan berupa geospatial analysis dan RFM analysis (Recency, Frequency, Monetary), serta pengelompokan keterlambatan menggunakan teknik binning.

## Struktur Direktori

```
submission
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
├── data
│   └── (dataset E-Commerce Public Dataset)
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

- `dashboard/` berisi file dashboard Streamlit dan data hasil olahan (`main_data.csv`).
- `data/` berisi dataset asli.
- `notebook.ipynb` berisi seluruh proses analisis data, mulai dari gathering data sampai conclusion.
- `requirements.txt` berisi daftar library yang dibutuhkan.
- `url.txt` berisi tautan dashboard yang sudah dideploy.

## Setup Environment

Pastikan Python sudah terpasang, lalu jalankan perintah berikut di folder utama proyek:

```
pip install -r requirements.txt
```

## Menjalankan Dashboard

Dari folder utama proyek, jalankan:

```
streamlit run dashboard/dashboard.py
```

Jika perintah `streamlit` tidak dikenali, gunakan:

```
python -m streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka di browser pada alamat `http://localhost:8501`.

## Dashboard Online

Dashboard yang sudah dideploy dapat diakses melalui tautan yang tertera pada file `url.txt`.

## Sumber Data

E-Commerce Public Dataset (Olist), tersedia di Kaggle: Brazilian E-Commerce Public Dataset by Olist.