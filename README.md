# Dashboard Analisis Data E-Commerce

Proyek ini menganalisis E-Commerce Public Dataset untuk menjawab dua pertanyaan bisnis, lalu menampilkan hasilnya dalam dashboard Streamlit. Selain itu, proyek ini memuat analisis lanjutan berupa geospatial analysis dan RFM analysis, serta pengelompokan keterlambatan dengan teknik binning.

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

## Setup Environment - Anaconda

```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```
pip install -r requirements.txt
```

## Run Streamlit App

Jalankan perintah berikut dari folder utama proyek (folder yang berisi folder `dashboard`):

```
streamlit run dashboard/dashboard.py
```

Jika perintah `streamlit` tidak dikenali, gunakan:

```
python -m streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka di browser pada alamat `http://localhost:8501`.

## Dashboard Online

Tautan dashboard yang sudah dideploy tertulis pada berkas `url.txt`.

## Catatan

Folder `data` hanya disertakan pada berkas ZIP submission karena ukuran dataset terlalu besar untuk diunggah ke GitHub.
