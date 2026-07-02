import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, timedelta
import plotly.express as px
import plotly.graph_objects as go

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Monitoring Prospek Nasabah KUR/KPR",
    page_icon="🏦",
    layout="wide"
)

# =========================
# STYLE CSS
# =========================
st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .title-box {
        background: linear-gradient(90deg, #003D79, #F58220);
        padding: 24px;
        border-radius: 14px;
        color: white !important;
        margin-bottom: 20px;
    }

    .title-box h1 {
        margin: 0;
        font-size: 30px;
        color: white !important;
    }

    .title-box p {
        margin-top: 8px;
        font-size: 16px;
        color: white !important;
    }

    .info-card {
        background-color: #ffffff;
        color: #1f2937 !important;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e4e8f0;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 16px;
    }

    .info-card h1,
    .info-card h2,
    .info-card h3,
    .info-card h4,
    .info-card p,
    .info-card b {
        color: #1f2937 !important;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #005BAB !important;
        margin-bottom: 8px;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e4e8f0;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] div,
    div[data-testid="stMetric"] p,
    div[data-testid="stMetric"] span {
        color: #1f2937 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #003D79 !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #374151 !important;
        font-weight: 600 !important;
    }

    .btn-logo-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 14px;
        border-left: 6px solid #F58220;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 18px;
    }

    .btn-logo-text {
        font-size: 28px;
        font-weight: 800;
        color: #003D79 !important;
        letter-spacing: 1px;
        margin-bottom: 0px;
    }

    .btn-logo-subtitle {
        font-size: 13px;
        color: #F58220 !important;
        font-weight: 600;
        margin-top: -4px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# PATH FILE
# =========================
DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "prospek_nasabah.csv"

ASSETS_DIR = Path("assets")
LOGO_PATH = ASSETS_DIR / "logo_btn.png"

# =========================
# MASTER DATA
# =========================
COLUMNS = [
    "ID",
    "Tanggal",
    "Nama Calon Nasabah",
    "Nomor HP",
    "Alamat",
    "Produk Diminati",
    "Status Follow Up",
    "Keterangan"
]

PRODUK_LIST = ["KUR", "KPR"]

STATUS_LIST = [
    "Dihubungi",
    "Merespons",
    "Berminat",
    "Disurvei",
    "Terealisasi"
]

# =========================
# DATA DUMMY
# =========================
def get_dummy_data():
    today = date.today()

    data = [
        ["Andi Prasetyo", "08XX-0000-1001", "Jl. Ahmad Yani, Kelurahan Payaman, Kecamatan Nganjuk", "KUR", "Dihubungi", "Prospek hasil WA blast, memiliki usaha toko kelontong."],
        ["Siti Rahayu", "08XX-0000-1002", "Perum Kertosono Residence, Kecamatan Kertosono, Kabupaten Nganjuk", "KPR", "Merespons", "Menanyakan simulasi cicilan rumah subsidi."],
        ["Budi Santoso", "08XX-0000-1003", "Desa Warujayeng, Kecamatan Tanjunganom, Kabupaten Nganjuk", "KUR", "Berminat", "Membutuhkan tambahan modal untuk usaha warung makan."],
        ["Dewi Lestari", "08XX-0000-1004", "Desa Sukomoro, Kecamatan Sukomoro, Kabupaten Nganjuk", "KUR", "Disurvei", "Sudah dijadwalkan survei usaha sembako."],
        ["Agus Firmansyah", "08XX-0000-1005", "Kelurahan Mangundikaran, Kecamatan Nganjuk, Kabupaten Nganjuk", "KPR", "Terealisasi", "Berkas pengajuan KPR telah lengkap dan diproses."],
        ["Rina Wulandari", "08XX-0000-1006", "Desa Loceret, Kecamatan Loceret, Kabupaten Nganjuk", "KUR", "Dihubungi", "Calon nasabah memiliki usaha laundry rumahan."],
        ["Eko Purnomo", "08XX-0000-1007", "Desa Berbek, Kecamatan Berbek, Kabupaten Nganjuk", "KUR", "Merespons", "Meminta penjelasan plafon pinjaman KUR."],
        ["Fitri Handayani", "08XX-0000-1008", "Desa Bagor, Kecamatan Bagor, Kabupaten Nganjuk", "KPR", "Berminat", "Tertarik pembiayaan rumah pertama."],
        ["Hendra Wijaya", "08XX-0000-1009", "Desa Baron, Kecamatan Baron, Kabupaten Nganjuk", "KUR", "Disurvei", "Survei usaha bengkel motor kecil."],
        ["Lina Safitri", "08XX-0000-1010", "Desa Prambon, Kecamatan Prambon, Kabupaten Nganjuk", "KUR", "Terealisasi", "Pengajuan modal usaha frozen food terealisasi."],
        ["M. Arif Setiawan", "08XX-0000-1011", "Desa Rejoso, Kecamatan Rejoso, Kabupaten Nganjuk", "KUR", "Dihubungi", "Prospek dari daftar pelaku UMKM wilayah Rejoso."],
        ["Nur Aini", "08XX-0000-1012", "Desa Gondang, Kecamatan Gondang, Kabupaten Nganjuk", "KPR", "Merespons", "Menanyakan syarat pengajuan KPR untuk karyawan swasta."],
        ["Wahyu Nugroho", "08XX-0000-1013", "Desa Pacekulon, Kecamatan Pace, Kabupaten Nganjuk", "KUR", "Berminat", "Membutuhkan modal untuk pengembangan usaha pertanian."],
        ["Sri Utami", "08XX-0000-1014", "Desa Patianrowo, Kecamatan Patianrowo, Kabupaten Nganjuk", "KUR", "Disurvei", "Survei usaha toko pakaian."],
        ["Yoga Saputra", "08XX-0000-1015", "Desa Ngluyu, Kecamatan Ngluyu, Kabupaten Nganjuk", "KPR", "Terealisasi", "Pengajuan KPR disetujui berdasarkan kelengkapan dokumen."],
        ["Dian Permatasari", "08XX-0000-1016", "Kelurahan Kartoharjo, Kecamatan Nganjuk, Kabupaten Nganjuk", "KUR", "Dihubungi", "Calon nasabah memiliki usaha jajanan pasar."],
        ["Rizky Maulana", "08XX-0000-1017", "Desa Ngronggot, Kecamatan Ngronggot, Kabupaten Nganjuk", "KUR", "Merespons", "Menanyakan angsuran dan tenor KUR."],
        ["Maya Sulastri", "08XX-0000-1018", "Desa Lengkong, Kecamatan Lengkong, Kabupaten Nganjuk", "KPR", "Berminat", "Berminat KPR rumah sederhana area Nganjuk."],
        ["Teguh Prabowo", "08XX-0000-1019", "Desa Wilangan, Kecamatan Wilangan, Kabupaten Nganjuk", "KUR", "Disurvei", "Survei usaha penggilingan kecil."],
        ["Indah Kurnia", "08XX-0000-1020", "Desa Sawahan, Kecamatan Sawahan, Kabupaten Nganjuk", "KUR", "Terealisasi", "Pembiayaan usaha katering rumahan terealisasi."],
        ["Fajar Ramadhan", "08XX-0000-1021", "Kelurahan Kauman, Kecamatan Nganjuk, Kabupaten Nganjuk", "KPR", "Dihubungi", "Prospek dari kegiatan pemasaran digital."],
        ["Ani Mulyani", "08XX-0000-1022", "Desa Jatikalen, Kecamatan Jatikalen, Kabupaten Nganjuk", "KUR", "Merespons", "Merespons WA blast dan meminta informasi persyaratan."],
        ["Bayu Kurniawan", "08XX-0000-1023", "Desa Ngetos, Kecamatan Ngetos, Kabupaten Nganjuk", "KUR", "Berminat", "Tertarik KUR untuk tambahan modal toko pupuk."],
        ["Citra Melati", "08XX-0000-1024", "Desa Brebek, Kecamatan Ngronggot, Kabupaten Nganjuk", "KPR", "Disurvei", "Sudah dilakukan survei awal untuk pengajuan KPR."],
        ["Galih Pratama", "08XX-0000-1025", "Desa Candirejo, Kecamatan Loceret, Kabupaten Nganjuk", "KUR", "Terealisasi", "Pengajuan KUR untuk usaha konter pulsa terealisasi."],
        ["Novi Anggraini", "08XX-0000-1026", "Desa Kedungrejo, Kecamatan Tanjunganom, Kabupaten Nganjuk", "KUR", "Dihubungi", "Calon nasabah dari daftar UMKM makanan ringan."],
        ["Dimas Arya", "08XX-0000-1027", "Desa Sambiroto, Kecamatan Baron, Kabupaten Nganjuk", "KPR", "Merespons", "Menanyakan DP dan tenor pembiayaan rumah."],
        ["Putri Maharani", "08XX-0000-1028", "Desa Tempuran, Kecamatan Ngluyu, Kabupaten Nganjuk", "KUR", "Berminat", "Berminat mengajukan KUR untuk usaha salon kecil."],
        ["Ilham Fauzi", "08XX-0000-1029", "Desa Rowomarto, Kecamatan Patianrowo, Kabupaten Nganjuk", "KUR", "Disurvei", "Survei usaha toko bahan bangunan."],
        ["Ratna Dewi", "08XX-0000-1030", "Kelurahan Ganungkidul, Kecamatan Nganjuk, Kabupaten Nganjuk", "KPR", "Terealisasi", "Pengajuan KPR dinyatakan layak proses."]
    ]

    dummy_data = []

    for index, item in enumerate(data, start=1):
        tanggal = today - timedelta(days=(30 - index) // 2)

        dummy_data.append({
            "ID": index,
            "Tanggal": str(tanggal),
            "Nama Calon Nasabah": item[0],
            "Nomor HP": item[1],
            "Alamat": item[2],
            "Produk Diminati": item[3],
            "Status Follow Up": item[4],
            "Keterangan": item[5]
        })

    return dummy_data

# =========================
# FUNGSI BANTUAN
# =========================
def init_data():
    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        df_dummy = pd.DataFrame(get_dummy_data(), columns=COLUMNS)
        df_dummy.to_csv(DATA_FILE, index=False)


def load_data():
    init_data()

    df = pd.read_csv(DATA_FILE, dtype=str)
    df = df.fillna("")

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[COLUMNS]
    return df


def save_data(df):
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(DATA_FILE, index=False)


def reset_dummy_data():
    df_dummy = pd.DataFrame(get_dummy_data(), columns=COLUMNS)
    save_data(df_dummy)


def get_next_id(df):
    if df.empty:
        return 1

    id_numeric = pd.to_numeric(df["ID"], errors="coerce")

    if id_numeric.isna().all():
        return 1

    return int(id_numeric.max()) + 1


def count_status(df, status_name):
    if df.empty:
        return 0

    return int((df["Status Follow Up"] == status_name).sum())


def extract_kecamatan(alamat):
    if pd.isna(alamat) or str(alamat).strip() == "":
        return "Tidak diketahui"

    alamat = str(alamat)

    if "Kecamatan" in alamat:
        bagian = alamat.split("Kecamatan", 1)[1]
        hasil = bagian.split(",")[0].strip()
        return hasil if hasil else "Tidak diketahui"

    return "Tidak diketahui"


def filter_data(df, produk_filter, status_filter, periode_filter, keyword):
    filtered_df = df.copy()

    if filtered_df.empty:
        return filtered_df

    if produk_filter != "Semua":
        filtered_df = filtered_df[filtered_df["Produk Diminati"] == produk_filter]

    if status_filter != "Semua":
        filtered_df = filtered_df[filtered_df["Status Follow Up"] == status_filter]

    if periode_filter != "Semua":
        tanggal_series = pd.to_datetime(filtered_df["Tanggal"], errors="coerce")
        today = pd.to_datetime(date.today())

        if periode_filter == "Hari ini":
            filtered_df = filtered_df[tanggal_series.dt.date == date.today()]

        elif periode_filter == "7 hari terakhir":
            batas_awal = today - timedelta(days=7)
            filtered_df = filtered_df[tanggal_series >= batas_awal]

        elif periode_filter == "Bulan ini":
            filtered_df = filtered_df[
                (tanggal_series.dt.month == today.month) &
                (tanggal_series.dt.year == today.year)
            ]

    if keyword.strip() != "":
        keyword_lower = keyword.lower()

        filtered_df = filtered_df[
            filtered_df["Nama Calon Nasabah"].str.lower().str.contains(keyword_lower, na=False) |
            filtered_df["Nomor HP"].str.lower().str.contains(keyword_lower, na=False) |
            filtered_df["Alamat"].str.lower().str.contains(keyword_lower, na=False) |
            filtered_df["Produk Diminati"].str.lower().str.contains(keyword_lower, na=False) |
            filtered_df["Status Follow Up"].str.lower().str.contains(keyword_lower, na=False) |
            filtered_df["Keterangan"].str.lower().str.contains(keyword_lower, na=False)
        ]

    return filtered_df


# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# SIDEBAR
# =========================
if LOGO_PATH.exists():
    st.sidebar.image(str(LOGO_PATH), width=170)
else:
    st.sidebar.markdown("""
    <div class="btn-logo-box">
        <div class="btn-logo-text">BANK BTN</div>
        <div class="btn-logo-subtitle">Prospek Nasabah KUR/KPR</div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("### Navigasi")

menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Beranda", "Data Entry", "Dashboard"]
)

st.sidebar.markdown("---")

if st.sidebar.button("📥 Muat / Reset Data"):
    reset_dummy_data()
    st.success("Data berhasil dimuat. Silakan refresh halaman jika tabel belum berubah.")

st.sidebar.info(
    "Website ini digunakan untuk pencatatan dan monitoring prospek nasabah KUR/KPR "
    "hasil WA blast dan kegiatan marketing."
)

# =========================
# HALAMAN BERANDA
# =========================
if menu == "Beranda":
    st.markdown("""
    <div class="title-box">
        <h1>Monitoring Prospek Nasabah KUR/KPR</h1>
        <p>Sistem pencatatan dan pemantauan progres pemasaran calon nasabah secara digital.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Deskripsi Website</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        Website ini dirancang untuk membantu proses pencatatan prospek calon nasabah 
        yang diperoleh dari kegiatan WA blast dan marketing. Data yang dicatat meliputi 
        nama calon nasabah, nomor HP, alamat, produk yang diminati, status follow up, serta keterangan tambahan.
        <br><br>
        Melalui dashboard, pengguna dapat melihat jumlah calon nasabah yang sudah dihubungi, 
        merespons, berminat, disurvei, hingga terealisasi. Dengan demikian, proses monitoring 
        pemasaran dapat dilakukan secara lebih terstruktur dan berbasis data.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>📌 Luaran 1: Form Data Entry</h3>
            <p><b>Form Data Entry Prospek Nasabah KUR/KPR</b></p>
            <p>Berisi pencatatan data calon nasabah, nomor HP, alamat, produk diminati, status follow up, dan keterangan.</p>
            <p><b>Manfaat:</b> Membantu pencatatan prospek hasil WA blast dan marketing.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>📌 Luaran 2: Dashboard</h3>
            <p><b>Dashboard Monitoring Prospek Nasabah KUR/KPR</b></p>
            <p>Berisi visualisasi monitoring prospek nasabah KUR/KPR berdasarkan status, produk, wilayah, dan waktu.</p>
            <p><b>Manfaat:</b> Membantu monitoring progres pemasaran secara cepat dan berbasis data.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Ringkasan Data Saat Ini")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    col_m1.metric("Total Prospek", len(df))
    col_m2.metric("Prospek KUR", int((df["Produk Diminati"] == "KUR").sum()) if not df.empty else 0)
    col_m3.metric("Prospek KPR", int((df["Produk Diminati"] == "KPR").sum()) if not df.empty else 0)
    col_m4.metric("Terealisasi", count_status(df, "Terealisasi"))

# =========================
# HALAMAN DATA ENTRY
# =========================
elif menu == "Data Entry":
    st.markdown("""
    <div class="title-box">
        <h1>Form Data Entry Prospek Nasabah KUR/KPR</h1>
        <p>Input data calon nasabah hasil WA blast dan kegiatan marketing.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Tambah Data Prospek")

    with st.form("form_data_entry", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            nama = st.text_input("Nama Calon Nasabah")
            nomor_hp = st.text_input("Nomor HP")
            produk = st.selectbox("Produk Diminati", PRODUK_LIST)

        with col2:
            alamat = st.text_area("Alamat")
            status = st.selectbox("Status Follow Up", STATUS_LIST)

        keterangan = st.text_area("Keterangan")

        submit = st.form_submit_button("💾 Simpan Data")

        if submit:
            if nama.strip() == "":
                st.warning("Nama calon nasabah wajib diisi.")
            elif nomor_hp.strip() == "":
                st.warning("Nomor HP wajib diisi.")
            elif alamat.strip() == "":
                st.warning("Alamat wajib diisi.")
            else:
                new_data = {
                    "ID": get_next_id(df),
                    "Tanggal": str(date.today()),
                    "Nama Calon Nasabah": nama.strip(),
                    "Nomor HP": nomor_hp.strip(),
                    "Alamat": alamat.strip(),
                    "Produk Diminati": produk,
                    "Status Follow Up": status,
                    "Keterangan": keterangan.strip()
                }

                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                save_data(df)
                st.success("Data prospek berhasil disimpan. Silakan refresh halaman jika data belum muncul.")

    st.markdown("---")
    st.markdown("### Filter Data Prospek Nasabah")

    if df.empty:
        st.info("Belum ada data yang tersimpan.")
    else:
        col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([1, 1, 1.2, 1.8])

        with col_filter1:
            filter_produk = st.selectbox(
                "Filter Produk",
                ["Semua"] + PRODUK_LIST,
                key="filter_produk_data_entry"
            )

        with col_filter2:
            filter_status = st.selectbox(
                "Filter Status",
                ["Semua"] + STATUS_LIST,
                key="filter_status_data_entry"
            )

        with col_filter3:
            filter_periode = st.selectbox(
                "Filter Periode",
                ["Semua", "Hari ini", "7 hari terakhir", "Bulan ini"],
                key="filter_periode_data_entry"
            )

        with col_filter4:
            keyword = st.text_input(
                "Cari Data",
                placeholder="Cari nama, nomor HP, alamat, produk, status, atau keterangan",
                key="keyword_data_entry"
            )

        filtered_df = filter_data(
            df,
            filter_produk,
            filter_status,
            filter_periode,
            keyword
        )

        st.caption(
            f"Total seluruh data: {len(df)} | "
            f"Total data ditampilkan setelah filter: {len(filtered_df)}"
        )

        st.dataframe(filtered_df, use_container_width=True)

        csv_download = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Data Hasil Filter",
            data=csv_download,
            file_name="data_prospek_nasabah_btn.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.markdown("### Hapus Data Prospek")

        col_hapus1, col_hapus2 = st.columns([2, 1])

        with col_hapus1:
            hapus_id = st.text_input(
                "Masukkan ID data yang ingin dihapus",
                placeholder="Contoh: 1"
            )

        with col_hapus2:
            st.write("")
            st.write("")
            tombol_hapus = st.button("🗑️ Hapus Data")

        if tombol_hapus:
            if hapus_id.strip() == "":
                st.warning("Masukkan ID terlebih dahulu.")
            elif hapus_id.strip() not in df["ID"].astype(str).tolist():
                st.error("ID tidak ditemukan.")
            else:
                df = df[df["ID"].astype(str) != hapus_id.strip()]
                save_data(df)
                st.success("Data berhasil dihapus. Silakan refresh halaman jika data belum berubah.")

# =========================
# HALAMAN DASHBOARD
# =========================
elif menu == "Dashboard":
    st.markdown("""
    <div class="title-box">
        <h1>Dashboard Monitoring Prospek Nasabah KUR/KPR</h1>
        <p>Visualisasi progres pemasaran calon nasabah berdasarkan status follow up, produk, wilayah, dan tren data.</p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("Belum ada data untuk ditampilkan pada dashboard.")
    else:
        st.markdown("### Filter Dashboard")

        col_filter1, col_filter2, col_filter3, col_filter4 = st.columns([1, 1, 1.2, 1.8])

        with col_filter1:
            dashboard_produk = st.selectbox(
                "Pilih Produk",
                ["Semua"] + PRODUK_LIST,
                key="filter_produk_dashboard"
            )

        with col_filter2:
            dashboard_status = st.selectbox(
                "Pilih Status",
                ["Semua"] + STATUS_LIST,
                key="filter_status_dashboard"
            )

        with col_filter3:
            dashboard_periode = st.selectbox(
                "Pilih Periode",
                ["Semua", "Hari ini", "7 hari terakhir", "Bulan ini"],
                key="filter_periode_dashboard"
            )

        with col_filter4:
            dashboard_keyword = st.text_input(
                "Cari Data",
                placeholder="Cari nama, nomor HP, alamat, produk, status, atau keterangan",
                key="keyword_dashboard"
            )

        dashboard_df = filter_data(
            df,
            dashboard_produk,
            dashboard_status,
            dashboard_periode,
            dashboard_keyword
        )

        st.caption(
            f"Total seluruh data: {len(df)} | "
            f"Total data ditampilkan setelah filter: {len(dashboard_df)}"
        )

        st.markdown("### Ringkasan Monitoring")

        m1, m2, m3, m4, m5 = st.columns(5)

        m1.metric("Dihubungi", count_status(dashboard_df, "Dihubungi"))
        m2.metric("Merespons", count_status(dashboard_df, "Merespons"))
        m3.metric("Berminat", count_status(dashboard_df, "Berminat"))
        m4.metric("Disurvei", count_status(dashboard_df, "Disurvei"))
        m5.metric("Terealisasi", count_status(dashboard_df, "Terealisasi"))

        st.markdown("---")

        if dashboard_df.empty:
            st.warning("Tidak ada data yang sesuai dengan filter.")
        else:
            chart_df = dashboard_df.copy()
            chart_df["Tanggal"] = pd.to_datetime(chart_df["Tanggal"], errors="coerce")
            chart_df["Kecamatan"] = chart_df["Alamat"].apply(extract_kecamatan)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 1. Jumlah Prospek Berdasarkan Status Follow Up")

                status_count = (
                    chart_df.groupby("Status Follow Up")
                    .size()
                    .reindex(STATUS_LIST, fill_value=0)
                    .reset_index(name="Jumlah")
                )

                fig_status = px.bar(
                    status_count,
                    x="Status Follow Up",
                    y="Jumlah",
                    text="Jumlah",
                    color="Status Follow Up",
                    title="Jumlah Prospek Berdasarkan Status Follow Up"
                )

                fig_status.update_traces(textposition="outside")
                fig_status.update_layout(
                    showlegend=False,
                    yaxis_title="Jumlah Prospek",
                    xaxis_title="Status Follow Up"
                )

                st.plotly_chart(fig_status, use_container_width=True)

            with col2:
                st.markdown("### 2. Persentase Produk Diminati")

                produk_count = (
                    chart_df.groupby("Produk Diminati")
                    .size()
                    .reindex(PRODUK_LIST, fill_value=0)
                    .reset_index(name="Jumlah")
                )

                fig_produk = px.pie(
                    produk_count,
                    values="Jumlah",
                    names="Produk Diminati",
                    hole=0.35,
                    title="Persentase Produk KUR dan KPR"
                )

                st.plotly_chart(fig_produk, use_container_width=True)

            st.markdown("---")

            col3, col4 = st.columns(2)

            with col3:
                st.markdown("### 3. Tren Input Prospek Berdasarkan Tanggal")

                tren_df = (
                    chart_df.dropna(subset=["Tanggal"])
                    .groupby("Tanggal")
                    .size()
                    .reset_index(name="Jumlah Prospek")
                    .sort_values("Tanggal")
                )

                fig_tren = px.line(
                    tren_df,
                    x="Tanggal",
                    y="Jumlah Prospek",
                    markers=True,
                    title="Tren Jumlah Prospek Masuk per Tanggal"
                )

                fig_tren.update_layout(
                    yaxis_title="Jumlah Prospek",
                    xaxis_title="Tanggal"
                )

                st.plotly_chart(fig_tren, use_container_width=True)

            with col4:
                st.markdown("### 4. Sebaran Prospek Berdasarkan Kecamatan")

                kecamatan_count = (
                    chart_df.groupby("Kecamatan")
                    .size()
                    .reset_index(name="Jumlah Prospek")
                    .sort_values(by="Jumlah Prospek", ascending=False)
                )

                fig_kec = px.bar(
                    kecamatan_count,
                    x="Kecamatan",
                    y="Jumlah Prospek",
                    text="Jumlah Prospek",
                    title="Sebaran Prospek per Kecamatan"
                )

                fig_kec.update_traces(textposition="outside")
                fig_kec.update_layout(
                    yaxis_title="Jumlah Prospek",
                    xaxis_title="Kecamatan"
                )

                st.plotly_chart(fig_kec, use_container_width=True)

            st.markdown("---")

            col5, col6 = st.columns(2)

            with col5:
                st.markdown("### 5. Perbandingan Status Follow Up per Produk")

                produk_status = (
                    chart_df.groupby(["Produk Diminati", "Status Follow Up"])
                    .size()
                    .reset_index(name="Jumlah")
                )

                fig_produk_status = px.bar(
                    produk_status,
                    x="Produk Diminati",
                    y="Jumlah",
                    color="Status Follow Up",
                    barmode="group",
                    text="Jumlah",
                    title="Perbandingan Status Follow Up pada Produk KUR dan KPR"
                )

                fig_produk_status.update_traces(textposition="outside")
                fig_produk_status.update_layout(
                    yaxis_title="Jumlah Prospek",
                    xaxis_title="Produk Diminati"
                )

                st.plotly_chart(fig_produk_status, use_container_width=True)

            with col6:
                st.markdown("### 6. Funnel Progres Prospek Nasabah")

                funnel_count = (
                    chart_df.groupby("Status Follow Up")
                    .size()
                    .reindex(STATUS_LIST, fill_value=0)
                    .reset_index(name="Jumlah")
                )

                fig_funnel = px.funnel(
                    funnel_count,
                    x="Jumlah",
                    y="Status Follow Up",
                    title="Alur Progres dari Dihubungi sampai Terealisasi"
                )

                st.plotly_chart(fig_funnel, use_container_width=True)

            st.markdown("---")

            col7, col8 = st.columns(2)

            with col7:
                st.markdown("### 7. Heatmap Produk dan Status Follow Up")

                heatmap_data = pd.crosstab(
                    chart_df["Status Follow Up"],
                    chart_df["Produk Diminati"]
                )

                heatmap_data = heatmap_data.reindex(
                    index=STATUS_LIST,
                    columns=PRODUK_LIST,
                    fill_value=0
                )

                fig_heatmap = go.Figure(
                    data=go.Heatmap(
                        z=heatmap_data.values,
                        x=heatmap_data.columns,
                        y=heatmap_data.index,
                        colorscale="Blues"
                    )
                )

                fig_heatmap.update_layout(
                    title="Heatmap Produk dan Status Follow Up",
                    xaxis_title="Produk Diminati",
                    yaxis_title="Status Follow Up"
                )

                st.plotly_chart(fig_heatmap, use_container_width=True)

            with col8:
                st.markdown("### 8. Komposisi Produk per Kecamatan")

                kec_produk = (
                    chart_df.groupby(["Kecamatan", "Produk Diminati"])
                    .size()
                    .reset_index(name="Jumlah")
                )

                fig_kec_produk = px.bar(
                    kec_produk,
                    x="Kecamatan",
                    y="Jumlah",
                    color="Produk Diminati",
                    text="Jumlah",
                    title="Komposisi Minat Produk KUR/KPR per Kecamatan"
                )

                fig_kec_produk.update_traces(textposition="outside")
                fig_kec_produk.update_layout(
                    yaxis_title="Jumlah Prospek",
                    xaxis_title="Kecamatan"
                )

                st.plotly_chart(fig_kec_produk, use_container_width=True)

            st.markdown("---")

            col9, col10 = st.columns(2)

            with col9:
                st.markdown("### 9. Distribusi Prospek Berdasarkan Hari")

                hari_df = chart_df.dropna(subset=["Tanggal"]).copy()
                hari_df["Hari"] = hari_df["Tanggal"].dt.day_name()

                urutan_hari = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday"
                ]

                hari_count = (
                    hari_df.groupby("Hari")
                    .size()
                    .reindex(urutan_hari, fill_value=0)
                    .reset_index(name="Jumlah Prospek")
                )

                fig_hari = px.bar(
                    hari_count,
                    x="Hari",
                    y="Jumlah Prospek",
                    text="Jumlah Prospek",
                    title="Distribusi Prospek Berdasarkan Hari"
                )

                fig_hari.update_traces(textposition="outside")
                fig_hari.update_layout(
                    yaxis_title="Jumlah Prospek",
                    xaxis_title="Hari"
                )

                st.plotly_chart(fig_hari, use_container_width=True)

            with col10:
                st.markdown("### 10. Distribusi Produk dan Status Follow Up")

                sunburst_df = (
                    chart_df.groupby(["Produk Diminati", "Status Follow Up"])
                    .size()
                    .reset_index(name="Jumlah")
                )

                fig_sunburst = px.sunburst(
                    sunburst_df,
                    path=["Produk Diminati", "Status Follow Up"],
                    values="Jumlah",
                    title="Distribusi Produk dan Status Follow Up"
                )

                st.plotly_chart(fig_sunburst, use_container_width=True)

            st.markdown("---")
            st.markdown("### Tabel Monitoring Prospek")

            st.dataframe(chart_df, use_container_width=True)

            csv_dashboard = chart_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download Data Dashboard",
                data=csv_dashboard,
                file_name="dashboard_monitoring_prospek_btn.csv",
                mime="text/csv"
            )
