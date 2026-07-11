import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, timedelta
import plotly.express as px


# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Monitoring Prospek Nasabah KUR/KPR",
    page_icon="🏦",
    layout="wide"
)


# =====================================================
# CSS STYLE
# =====================================================

st.markdown("""
<style>

.main {
    background-color:#f7f9fc;
}


/* HEADER */

.title-box {

    background:
    linear-gradient(
        90deg,
        #003D79,
        #F58220
    );

    padding:25px;
    border-radius:15px;
    color:white;

    margin-bottom:20px;
}


.title-box h1 {

    color:white !important;
    font-size:32px;
    margin-bottom:5px;

}


.title-box p {

    color:white !important;
    font-size:16px;

}



/* CARD */

.info-card {

    background:white;
    padding:20px;
    border-radius:15px;

    border:
    1px solid #e5e7eb;

    box-shadow:
    0px 3px 10px rgba(0,0,0,0.08);

}


/* KPI CARD */

div[data-testid="stMetric"] {

    background:white;

    padding:20px;

    border-radius:15px;

    border:
    1px solid #e5e7eb;

    box-shadow:
    0px 3px 10px rgba(0,0,0,0.08);

}


div[data-testid="stMetricValue"] {

    color:#003D79 !important;

    font-size:30px !important;

    font-weight:800;

}


div[data-testid="stMetricLabel"] {

    color:#374151 !important;

    font-weight:600;

}



/* SECTION TITLE */

.section-title {

    font-size:23px;

    font-weight:700;

    color:#003D79;

}



/* BTN LOGO */

.btn-logo-box {

    background:white;

    padding:15px;

    border-radius:12px;

    border-left:
    6px solid #F58220;

}



.btn-logo-text {

    color:#003D79;

    font-size:28px;

    font-weight:800;

}


.btn-logo-subtitle {

    color:#F58220;

    font-size:13px;

    font-weight:600;

}


</style>

""",
unsafe_allow_html=True)



# =====================================================
# PATH FILE
# =====================================================

DATA_DIR = Path("data")

DATA_FILE = DATA_DIR / "prospek_nasabah.csv"


ASSETS_DIR = Path("assets")

LOGO_PATH = ASSETS_DIR / "logo_btn.png"



# =====================================================
# MASTER DATA
# =====================================================


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


PRODUK_LIST = [

    "KUR",
    "KPR"

]


STATUS_LIST = [

    "Dihubungi",
    "Merespons",
    "Berminat",
    "Disurvei",
    "Terealisasi"

]



# =====================================================
# DATA DUMMY
# =====================================================


def get_dummy_data():

    today = date.today()


    data = [

        [
            "Andi Prasetyo",
            "08XX-0000-1001",
            "Jl Ahmad Yani Kecamatan Nganjuk",
            "KUR",
            "Dihubungi",
            "Prospek hasil WA blast usaha toko"
        ],


        [
            "Siti Rahayu",
            "08XX-0000-1002",
            "Perum Kertosono Kecamatan Kertosono",
            "KPR",
            "Merespons",
            "Menanyakan simulasi cicilan"
        ],


        [
            "Budi Santoso",
            "08XX-0000-1003",
            "Desa Warujayeng Kecamatan Tanjunganom",
            "KUR",
            "Berminat",
            "Membutuhkan tambahan modal usaha"
        ],


        [
            "Dewi Lestari",
            "08XX-0000-1004",
            "Desa Sukomoro Kecamatan Sukomoro",
            "KUR",
            "Disurvei",
            "Survei usaha sembako"
        ],


        [
            "Agus Firmansyah",
            "08XX-0000-1005",
            "Kelurahan Mangundikaran Kecamatan Nganjuk",
            "KPR",
            "Terealisasi",
            "Pengajuan KPR selesai"
        ]

    ]


    # Tambahkan data berulang agar dashboard terlihat

    dummy=[]


    for i in range(1,31):

        item=data[(i-1)%len(data)]


        dummy.append({

            "ID":i,

            "Tanggal":
            str(
                today -
                timedelta(days=(30-i)//2)
            ),


            "Nama Calon Nasabah":
            item[0],


            "Nomor HP":
            item[1],


            "Alamat":
            item[2],


            "Produk Diminati":
            item[3],


            "Status Follow Up":
            item[4],


            "Keterangan":
            item[5]

        })


    return dummy
# =====================================================
# FUNGSI DATABASE
# =====================================================


def init_data():

    DATA_DIR.mkdir(exist_ok=True)


    if not DATA_FILE.exists():

        df_dummy = pd.DataFrame(
            get_dummy_data(),
            columns=COLUMNS
        )

        df_dummy.to_csv(
            DATA_FILE,
            index=False
        )



def load_data():

    init_data()


    df = pd.read_csv(
        DATA_FILE,
        dtype=str
    )


    df = df.fillna("")


    for col in COLUMNS:

        if col not in df.columns:

            df[col]=""



    df = df[COLUMNS]


    return df





def save_data(df):

    DATA_DIR.mkdir(exist_ok=True)

    df.to_csv(
        DATA_FILE,
        index=False
    )





def reset_dummy_data():

    df_dummy = pd.DataFrame(
        get_dummy_data(),
        columns=COLUMNS
    )


    save_data(df_dummy)





def get_next_id(df):

    if df.empty:

        return 1


    angka = pd.to_numeric(
        df["ID"],
        errors="coerce"
    )


    if angka.isna().all():

        return 1


    return int(
        angka.max()
    ) + 1






# =====================================================
# FUNGSI MONITORING
# =====================================================


def count_status(df,status):

    if df.empty:

        return 0


    return int(
        (
            df["Status Follow Up"]
            ==
            status
        ).sum()
    )





def extract_kecamatan(alamat):

    if pd.isna(alamat):

        return "Tidak diketahui"



    alamat=str(alamat)



    if "Kecamatan" in alamat:

        hasil = (
            alamat
            .split("Kecamatan")[1]
            .split(",")[0]
            .strip()
        )


        if hasil:

            return hasil



    return "Tidak diketahui"







def filter_data(
        df,
        produk,
        status,
        periode,
        keyword
):


    result=df.copy()



    if produk!="Semua":

        result=result[
            result["Produk Diminati"]
            ==
            produk
        ]



    if status!="Semua":

        result=result[
            result["Status Follow Up"]
            ==
            status
        ]



    if periode!="Semua":


        tanggal=pd.to_datetime(
            result["Tanggal"],
            errors="coerce"
        )


        sekarang=pd.to_datetime(
            date.today()
        )


        if periode=="Hari ini":

            result=result[
                tanggal.dt.date
                ==
                date.today()
            ]



        elif periode=="7 hari terakhir":

            result=result[
                tanggal >=
                sekarang -
                timedelta(days=7)
            ]



        elif periode=="Bulan ini":

            result=result[
                (
                    tanggal.dt.month
                    ==
                    sekarang.month
                )
                &
                (
                    tanggal.dt.year
                    ==
                    sekarang.year
                )
            ]





    if keyword.strip()!="":


        keyword=keyword.lower()



        result=result[

            result["Nama Calon Nasabah"]
            .str.lower()
            .str.contains(keyword,na=False)

            |

            result["Nomor HP"]
            .str.lower()
            .str.contains(keyword,na=False)

            |

            result["Alamat"]
            .str.lower()
            .str.contains(keyword,na=False)

            |

            result["Produk Diminati"]
            .str.lower()
            .str.contains(keyword,na=False)

            |

            result["Status Follow Up"]
            .str.lower()
            .str.contains(keyword,na=False)

        ]



    return result







# =====================================================
# LOAD DATA AWAL
# =====================================================


df = load_data()





# =====================================================
# SIDEBAR
# =====================================================


if LOGO_PATH.exists():

    st.sidebar.image(
        str(LOGO_PATH),
        width=170
    )


else:


    st.sidebar.markdown(
    """

    <div class="btn-logo-box">

    <div class="btn-logo-text">
    BANK BTN
    </div>

    <div class="btn-logo-subtitle">
    Monitoring Prospek KUR/KPR
    </div>

    </div>

    """,
    unsafe_allow_html=True
    )





st.sidebar.markdown(
"## Menu"
)



menu = st.sidebar.radio(

    "Pilih Halaman",

    [

        "Beranda",

        "Data Entry",

        "Dashboard"

    ]

)





st.sidebar.divider()



if st.sidebar.button(
    "📥 Reset Data Dummy"
):

    reset_dummy_data()

    st.success(
        "Data berhasil direset"
    )




st.sidebar.info(

"""

Dashboard monitoring prospek

KUR/KPR untuk membantu

pencatatan dan evaluasi

proses pemasaran nasabah.

"""

)
# =====================================================
# HALAMAN BERANDA
# =====================================================


if menu == "Beranda":


    st.markdown(
    """

    <div class="title-box">

    <h1>
    Monitoring Prospek Nasabah KUR/KPR
    </h1>

    <p>
    Sistem pencatatan dan monitoring progres calon nasabah secara digital.
    </p>

    </div>

    """,
    unsafe_allow_html=True
    )



    st.markdown(
    """
    <div class="section-title">
    Tentang Dashboard
    </div>
    """,
    unsafe_allow_html=True
    )



    st.markdown(
    """

    <div class="info-card">

    Dashboard ini digunakan untuk melakukan pencatatan,
    pemantauan, dan evaluasi prospek nasabah KUR/KPR.

    Data yang dikelola meliputi:

    <br><br>

    • Nama calon nasabah

    <br>
    • Nomor HP

    <br>
    • Wilayah

    <br>
    • Produk diminati

    <br>
    • Status follow up

    <br>
    • Keterangan proses marketing


    </div>

    """,
    unsafe_allow_html=True
    )



    st.markdown("---")



    col1,col2=st.columns(2)



    with col1:


        st.markdown(

        """

        <div class="info-card">

        <h3>
        📌 Data Entry Prospek
        </h3>


        Form digunakan untuk mencatat

        data calon nasabah dari kegiatan

        marketing dan WA blast.


        </div>

        """,

        unsafe_allow_html=True

        )



    with col2:


        st.markdown(

        """

        <div class="info-card">

        <h3>
        📊 Dashboard Monitoring
        </h3>


        Menampilkan informasi penting

        terkait jumlah prospek,

        progres follow up,

        produk,

        waktu,

        dan wilayah.


        </div>

        """,

        unsafe_allow_html=True

        )





    st.markdown("---")



    st.markdown(
    "### Ringkasan Data"
    )



    a,b,c,d=st.columns(4)



    a.metric(
        "Total Prospek",
        len(df)
    )


    b.metric(
        "Prospek KUR",
        int(
            (
                df["Produk Diminati"]
                ==
                "KUR"
            ).sum()
        )
    )



    c.metric(
        "Prospek KPR",
        int(
            (
                df["Produk Diminati"]
                ==
                "KPR"
            ).sum()
        )
    )



    d.metric(
        "Terealisasi",
        count_status(
            df,
            "Terealisasi"
        )
    )







# =====================================================
# HALAMAN DATA ENTRY
# =====================================================


elif menu=="Data Entry":



    st.markdown(

    """

    <div class="title-box">

    <h1>
    Form Data Entry Prospek Nasabah
    </h1>

    <p>
    Input data calon nasabah hasil marketing.
    </p>

    </div>

    """,

    unsafe_allow_html=True

    )





    st.markdown(
    "### Tambah Data Prospek"
    )




    with st.form(
        "form_input",
        clear_on_submit=True
    ):



        col1,col2=st.columns(2)



        with col1:


            nama=st.text_input(
                "Nama Calon Nasabah"
            )


            hp=st.text_input(
                "Nomor HP"
            )


            produk=st.selectbox(

                "Produk Diminati",

                PRODUK_LIST

            )



        with col2:


            alamat=st.text_area(
                "Alamat"
            )


            status=st.selectbox(

                "Status Follow Up",

                STATUS_LIST

            )



        keterangan=st.text_area(
            "Keterangan"
        )



        simpan=st.form_submit_button(
            "💾 Simpan Data"
        )



        if simpan:



            if nama.strip()=="":


                st.warning(
                    "Nama wajib diisi"
                )


            elif hp.strip()=="":


                st.warning(
                    "Nomor HP wajib diisi"
                )



            else:



                data_baru={


                    "ID":
                    get_next_id(df),


                    "Tanggal":
                    str(date.today()),


                    "Nama Calon Nasabah":
                    nama,


                    "Nomor HP":
                    hp,


                    "Alamat":
                    alamat,


                    "Produk Diminati":
                    produk,


                    "Status Follow Up":
                    status,


                    "Keterangan":
                    keterangan

                }



                df=pd.concat(

                    [

                        df,

                        pd.DataFrame(
                            [data_baru]
                        )

                    ],

                    ignore_index=True

                )



                save_data(df)



                st.success(
                    "Data berhasil disimpan"
                )





    st.divider()



    st.markdown(
    "### Monitoring Data"
    )



    f1,f2,f3,f4=st.columns(
        [1,1,1,2]
    )



    with f1:


        produk_filter=st.selectbox(

            "Produk",

            ["Semua"]+PRODUK_LIST,

            key="entry_produk"

        )



    with f2:


        status_filter=st.selectbox(

            "Status",

            ["Semua"]+STATUS_LIST,

            key="entry_status"

        )



    with f3:


        periode_filter=st.selectbox(

            "Periode",

            [

                "Semua",

                "Hari ini",

                "7 hari terakhir",

                "Bulan ini"

            ],

            key="entry_periode"

        )



    with f4:


        keyword=st.text_input(

            "Pencarian",

            key="entry_search"

        )





    tampil=filter_data(

        df,

        produk_filter,

        status_filter,

        periode_filter,

        keyword

    )



    st.caption(

        f"Menampilkan {len(tampil)} dari {len(df)} data"

    )



    st.dataframe(

        tampil,

        use_container_width=True

    )



    csv=tampil.to_csv(
        index=False
    ).encode(
        "utf-8"
    )



    st.download_button(

        "⬇️ Download CSV",

        csv,

        "data_prospek.csv",

        "text/csv"

    )



    st.divider()



    st.markdown(
    "### Hapus Data"
    )



    hapus_id=st.text_input(
        "Masukkan ID Data"
    )


    if st.button(
        "🗑️ Hapus"
    ):


        if hapus_id in df["ID"].astype(str).tolist():


            df=df[
                df["ID"].astype(str)
                !=
                hapus_id
            ]


            save_data(df)


            st.success(
                "Data berhasil dihapus"
            )


        else:


            st.error(
                "ID tidak ditemukan"
            )
# =====================================================
# HALAMAN DASHBOARD
# =====================================================


elif menu=="Dashboard":


    st.markdown(

    """

    <div class="title-box">

    <h1>
    Dashboard Monitoring Prospek Nasabah KUR/KPR
    </h1>


    <p>
    Monitoring performa prospek berdasarkan status,
    produk, waktu, dan wilayah.
    </p>


    </div>

    """,

    unsafe_allow_html=True

    )





    if df.empty:


        st.info(
            "Belum ada data tersedia"
        )


    else:



        # =============================================
        # FILTER DASHBOARD
        # =============================================


        st.markdown(
            "### Filter Dashboard"
        )



        col1,col2,col3,col4=st.columns(
            [1,1,1,2]
        )



        with col1:


            produk_dash=st.selectbox(

                "Produk",

                ["Semua"]+PRODUK_LIST,

                key="dashboard_produk"

            )



        with col2:


            status_dash=st.selectbox(

                "Status",

                ["Semua"]+STATUS_LIST,

                key="dashboard_status"

            )



        with col3:


            periode_dash=st.selectbox(

                "Periode",

                [

                    "Semua",

                    "Hari ini",

                    "7 hari terakhir",

                    "Bulan ini"

                ],

                key="dashboard_periode"

            )



        with col4:


            search_dash=st.text_input(

                "Pencarian",

                placeholder=
                "Cari nama / HP / alamat",

                key="dashboard_search"

            )







        dashboard_df=filter_data(

            df,

            produk_dash,

            status_dash,

            periode_dash,

            search_dash

        )





        st.caption(

            f"Data tampil : {len(dashboard_df)} dari {len(df)} total prospek"

        )





        # =============================================
        # KPI CARD
        # =============================================


        st.markdown(
            "### Ringkasan Monitoring"
        )



        k1,k2,k3,k4,k5,k6=st.columns(6)



        k1.metric(

            "Total Prospek",

            len(dashboard_df)

        )



        k2.metric(

            "Dihubungi",

            count_status(
                dashboard_df,
                "Dihubungi"
            )

        )



        k3.metric(

            "Merespons",

            count_status(
                dashboard_df,
                "Merespons"
            )

        )



        k4.metric(

            "Berminat",

            count_status(
                dashboard_df,
                "Berminat"
            )

        )



        k5.metric(

            "Disurvei",

            count_status(
                dashboard_df,
                "Disurvei"
            )

        )



        k6.metric(

            "Terealisasi",

            count_status(
                dashboard_df,
                "Terealisasi"
            )

        )





        st.divider()





        if dashboard_df.empty:


            st.warning(
                "Tidak ada data sesuai filter"
            )



        else:



            chart_df=dashboard_df.copy()



            chart_df["Tanggal"]=pd.to_datetime(

                chart_df["Tanggal"],

                errors="coerce"

            )



            chart_df["Kecamatan"]=chart_df[

                "Alamat"

            ].apply(
                extract_kecamatan
            )





            # =============================================
            # GRAFIK 1
            # =============================================


            st.markdown(
                "### 1. Jumlah Prospek Berdasarkan Status Follow Up"
            )


            status_chart=(

                chart_df

                .groupby(
                    "Status Follow Up"
                )

                .size()

                .reindex(
                    STATUS_LIST,
                    fill_value=0
                )

                .reset_index(
                    name="Jumlah"
                )

            )



            fig1=px.bar(

                status_chart,

                x="Status Follow Up",

                y="Jumlah",

                text="Jumlah",

                title=
                "Jumlah Prospek Berdasarkan Status Follow Up"

            )



            fig1.update_traces(

                textposition="outside"

            )


            st.plotly_chart(

                fig1,

                use_container_width=True

            )







            # =============================================
            # GRAFIK 2
            # =============================================


            st.markdown(
                "### 2. Persentase Produk Diminati"
            )



            col_a,col_b=st.columns(2)



            with col_a:



                produk_chart=(

                    chart_df

                    .groupby(
                        "Produk Diminati"
                    )

                    .size()

                    .reset_index(
                        name="Jumlah"
                    )

                )



                fig2=px.pie(

                    produk_chart,

                    names=
                    "Produk Diminati",

                    values=
                    "Jumlah",

                    hole=0.4,

                    title=
                    "Komposisi Produk KUR dan KPR"

                )



                st.plotly_chart(

                    fig2,

                    use_container_width=True

                )






            # =============================================
            # GRAFIK 3
            # =============================================


            with col_b:



                trend=(

                    chart_df

                    .dropna(
                        subset=["Tanggal"]
                    )

                    .groupby(
                        "Tanggal"
                    )

                    .size()

                    .reset_index(
                        name="Jumlah"
                    )

                    .sort_values(
                        "Tanggal"
                    )

                )



                fig3=px.line(

                    trend,

                    x="Tanggal",

                    y="Jumlah",

                    markers=True,

                    title=
                    "Tren Input Prospek"

                )



                st.plotly_chart(

                    fig3,

                    use_container_width=True

                )







            # =============================================
            # GRAFIK 4
            # =============================================


            st.markdown(
                "### 4. Sebaran Prospek Berdasarkan Kecamatan"
            )



            kec_chart=(

                chart_df

                .groupby(
                    "Kecamatan"
                )

                .size()

                .reset_index(
                    name="Jumlah"
                )

                .sort_values(

                    "Jumlah",

                    ascending=False

                )

            )



            fig4=px.bar(

                kec_chart,

                x="Kecamatan",

                y="Jumlah",

                text="Jumlah",

                title=
                "Sebaran Prospek per Kecamatan"

            )



            fig4.update_traces(

                textposition="outside"

            )



            st.plotly_chart(

                fig4,

                use_container_width=True

            )







            # =============================================
            # TABEL MONITORING
            # =============================================


            st.divider()



            st.markdown(

                "### Tabel Monitoring Prospek"

            )



            chart_df_display=chart_df.copy()



            chart_df_display["Tanggal"]=(

                chart_df_display["Tanggal"]

                .dt.strftime("%d-%m-%Y")

            )



            st.dataframe(

                chart_df_display,

                use_container_width=True

            )




            csv_dashboard=(

                chart_df_display

                .to_csv(
                    index=False
                )

                .encode("utf-8")

            )



            st.download_button(

                "⬇️ Download Data Dashboard",

                csv_dashboard,

                "dashboard_monitoring_prospek.csv",

                "text/csv"

            )
