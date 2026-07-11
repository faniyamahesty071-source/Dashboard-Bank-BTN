import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, timedelta
import plotly.express as px



# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(

    page_title="BTN Monitoring Prospek KUR/KPR",

    page_icon="🏦",

    layout="wide",

    initial_sidebar_state="expanded"

)





# =====================================================
# CORPORATE BTN STYLE
# =====================================================


st.markdown("""

<style>


/* =================================================
GLOBAL STYLE
================================================= */


html, body, [class*="css"] {


    font-family:

    "Segoe UI",

    Arial,

    sans-serif;


}



/* mengikuti tema streamlit */

.main {


    background-color:

    var(--background-color);


}





/* =================================================
HEADER CORPORATE
================================================= */


.title-box {


    background:

    linear-gradient(

        135deg,

        #003B71,

        #005BAB

    );


    padding:

    30px 35px;


    border-radius:

    18px;


    margin-bottom:

    25px;


    box-shadow:

    0 8px 25px rgba(0,0,0,0.15);


}



.title-box h1 {


    color:white !important;


    font-size:

    32px;


    font-weight:

    800;


    margin-bottom:

    8px;


}



.title-box p {


    color:

    rgba(255,255,255,0.9)

    !important;


    font-size:

    16px;


}






/* =================================================
SECTION TITLE
================================================= */


.section-title {


    color:

    #005BAB !important;


    font-size:

    24px;


    font-weight:

    750;


}







/* =================================================
CARD
================================================= */


.info-card {


    background:

    var(--secondary-background-color);


    padding:

    24px;


    border-radius:

    16px;


    border:

    1px solid rgba(128,128,128,0.25);


    box-shadow:

    0 5px 18px rgba(0,0,0,0.08);


}



.info-card h3 {


    color:

    #005BAB !important;


}



.info-card p {


    color:

    var(--text-color)

    !important;


}







/* =================================================
KPI CARD
================================================= */


div[data-testid="metric-container"] {


    background:

    var(--secondary-background-color);


    border-radius:

    16px;


    padding:

    18px;


    border:

    1px solid rgba(128,128,128,0.25);


    box-shadow:

    0 5px 18px rgba(0,0,0,0.08);


}





div[data-testid="stMetricLabel"] {


    color:

    var(--text-color)

    !important;


    font-weight:

    600;


}





div[data-testid="stMetricValue"] {


    color:

    #005BAB

    !important;


    font-size:

    30px !important;


    font-weight:

    800 !important;


}







/* =================================================
SIDEBAR CORPORATE
================================================= */


section[data-testid="stSidebar"] {


    background:

    linear-gradient(

        180deg,

        #003B71,

        #001F3F

    );


}



section[data-testid="stSidebar"] * {


    color:white !important;


}





section[data-testid="stSidebar"] button {


    background:

    #F58220 !important;


    color:white !important;


    border-radius:

    10px;


    border:none;


    font-weight:

    700;


}








/* =================================================
BUTTON
================================================= */


.stButton button {


    background:

    linear-gradient(

        90deg,

        #005BAB,

        #003B71

    );


    color:white;


    border-radius:

    10px;


    border:none;


    font-weight:

    600;


}



.stButton button:hover {


    background:

    #F58220;


    color:white;


}






/* =================================================
DOWNLOAD BUTTON
================================================= */


.stDownloadButton button {


    background:

    #F58220 !important;


    color:white !important;


    border-radius:

    10px;


    font-weight:

    700;


}







/* =================================================
TABLE
================================================= */


div[data-testid="stDataFrame"] {


    border-radius:

    15px;


    overflow:hidden;


}





</style>


""",

unsafe_allow_html=True

)







# =====================================================
# FILE PATH
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
# DATA DUMMY NASABAH
# =====================================================


def get_dummy_data():


    today = date.today()



    data = [


        [
            "Andi Prasetyo",
            "081234567801",
            "Kelurahan Payaman Kecamatan Nganjuk",
            "KUR",
            "Dihubungi",
            "Prospek hasil WA blast usaha toko kelontong"
        ],


        [
            "Siti Rahayu",
            "081234567802",
            "Perum Kertosono Kecamatan Kertosono",
            "KPR",
            "Merespons",
            "Meminta simulasi cicilan rumah subsidi"
        ],


        [
            "Budi Santoso",
            "081234567803",
            "Desa Warujayeng Kecamatan Tanjunganom",
            "KUR",
            "Berminat",
            "Membutuhkan tambahan modal usaha"
        ],


        [
            "Dewi Lestari",
            "081234567804",
            "Desa Sukomoro Kecamatan Sukomoro",
            "KUR",
            "Disurvei",
            "Survei usaha sembako"
        ],


        [
            "Agus Firmansyah",
            "081234567805",
            "Kelurahan Mangundikaran Kecamatan Nganjuk",
            "KPR",
            "Terealisasi",
            "Dokumen pengajuan telah lengkap"
        ],


        [
            "Rina Wulandari",
            "081234567806",
            "Desa Loceret Kecamatan Loceret",
            "KUR",
            "Dihubungi",
            "Pemilik usaha laundry rumahan"
        ],


        [
            "Eko Purnomo",
            "081234567807",
            "Desa Berbek Kecamatan Berbek",
            "KUR",
            "Merespons",
            "Menanyakan plafon pinjaman"
        ],


        [
            "Fitri Handayani",
            "081234567808",
            "Desa Bagor Kecamatan Bagor",
            "KPR",
            "Berminat",
            "Tertarik rumah pertama"
        ],


        [
            "Hendra Wijaya",
            "081234567809",
            "Desa Baron Kecamatan Baron",
            "KUR",
            "Disurvei",
            "Survei usaha bengkel"
        ],


        [
            "Lina Safitri",
            "081234567810",
            "Desa Prambon Kecamatan Prambon",
            "KUR",
            "Terealisasi",
            "Pembiayaan usaha berhasil"
        ]

    ]




    dummy=[]



    for i in range(1,31):


        item=data[(i-1) % len(data)]



        dummy.append(


            {

                "ID":i,


                "Tanggal":

                str(

                    today -

                    timedelta(

                        days=(30-i)//2

                    )

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

            }


        )


    return dummy







# =====================================================
# DATABASE MANAGEMENT
# =====================================================



def init_data():


    DATA_DIR.mkdir(

        exist_ok=True

    )



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



    df=pd.read_csv(


        DATA_FILE,


        dtype=str


    )



    df=df.fillna("")



    for col in COLUMNS:


        if col not in df.columns:


            df[col]=""




    return df[COLUMNS]








def save_data(df):


    DATA_DIR.mkdir(

        exist_ok=True

    )


    df.to_csv(

        DATA_FILE,

        index=False

    )







def reset_dummy_data():


    df_dummy=pd.DataFrame(

        get_dummy_data(),

        columns=COLUMNS

    )


    save_data(df_dummy)







def get_next_id(df):


    if df.empty:


        return 1



    angka=pd.to_numeric(

        df["ID"],

        errors="coerce"

    )



    if angka.isna().all():


        return 1



    return int(

        angka.max()

    )+1








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


        hasil=(

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






    # FILTER PRODUK

    if produk!="Semua":


        result=result[

            result["Produk Diminati"]

            ==

            produk

        ]






    # FILTER STATUS

    if status!="Semua":


        result=result[

            result["Status Follow Up"]

            ==

            status

        ]







    # FILTER PERIODE

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








    # SEARCH

    if keyword.strip()!="":



        keyword=keyword.lower()



        result=result[



            result["Nama Calon Nasabah"]

            .str.lower()

            .str.contains(

                keyword,

                na=False

            )



            |



            result["Nomor HP"]

            .str.lower()

            .str.contains(

                keyword,

                na=False

            )



            |



            result["Alamat"]

            .str.lower()

            .str.contains(

                keyword,

                na=False

            )



            |



            result["Produk Diminati"]

            .str.lower()

            .str.contains(

                keyword,

                na=False

            )



            |



            result["Status Follow Up"]

            .str.lower()

            .str.contains(

                keyword,

                na=False

            )


        ]





    return result







# =====================================================
# LOAD DATA UTAMA
# =====================================================


df = load_data()
# =====================================================
# SIDEBAR CORPORATE
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

"""

## Monitoring System


"""

)





menu = st.sidebar.radio(

    "Menu Utama",

    [

        "Beranda",

        "Data Entry",

        "Dashboard"

    ]

)





st.sidebar.divider()





if st.sidebar.button(

    "🔄 Reset Data Dummy"

):


    reset_dummy_data()


    st.sidebar.success(

        "Data berhasil diperbarui"

    )





st.sidebar.markdown(

"""

---

### Informasi Sistem


Dashboard ini digunakan untuk:

✓ Monitoring prospek nasabah

✓ Evaluasi follow up marketing

✓ Analisis produk KUR/KPR

✓ Monitoring wilayah prospek


---

**BTN Digital Monitoring System**

"""

)








# =====================================================
# HALAMAN BERANDA
# =====================================================



if menu=="Beranda":



    st.markdown(

    """

    <div class="title-box">


        <h1>

        Dashboard Monitoring Prospek Nasabah KUR/KPR

        </h1>


        <p>

        Sistem digital monitoring aktivitas pemasaran dan progres calon nasabah.

        </p>


    </div>


    """,

    unsafe_allow_html=True

    )






    st.markdown(

    """

    <div class="section-title">

    Overview Sistem

    </div>


    """,

    unsafe_allow_html=True

    )






    st.markdown(

    """

    <div class="info-card">


    Dashboard Monitoring Prospek Nasabah KUR/KPR

    merupakan sistem informasi untuk membantu proses

    pencatatan, pemantauan, dan evaluasi calon nasabah.


    <br><br>


    Sistem ini mendukung aktivitas marketing melalui

    pengelolaan data:


    <br><br>


    • Data calon nasabah

    <br>

    • Produk yang diminati

    <br>

    • Status follow up

    <br>

    • Wilayah prospek

    <br>

    • Perkembangan proses pengajuan


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

        📋 Data Entry Prospek

        </h3>



        <p>


        Digunakan untuk mencatat data

        calon nasabah dari kegiatan marketing,

        WA blast, dan aktivitas pemasaran.


        </p>



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



        <p>


        Menampilkan informasi strategis

        terkait jumlah prospek, status follow up,

        produk, tren waktu, dan wilayah.


        </p>



        </div>


        """,

        unsafe_allow_html=True

        )








    st.markdown("---")





    st.markdown(

    "### Ringkasan Data Saat Ini"

    )





    total=len(df)



    kur=int(

        (

            df["Produk Diminati"]

            ==

            "KUR"

        ).sum()

    )



    kpr=int(

        (

            df["Produk Diminati"]

            ==

            "KPR"

        ).sum()

    )



    realisasi=count_status(

        df,

        "Terealisasi"

    )








    c1,c2,c3,c4=st.columns(4)





    c1.metric(

        "Total Prospek",

        total

    )





    c2.metric(

        "Prospek KUR",

        kur

    )





    c3.metric(

        "Prospek KPR",

        kpr

    )





    c4.metric(

        "Terealisasi",

        realisasi

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

        Input dan pengelolaan data calon nasabah KUR/KPR.

        </p>


    </div>


    """,

    unsafe_allow_html=True

    )







    st.markdown(

        "### Tambah Data Prospek"

    )







    with st.form(

        "form_input_nasabah",

        clear_on_submit=True

    ):



        col1,col2=st.columns(2)





        with col1:


            nama = st.text_input(

                "Nama Calon Nasabah"

            )


            nomor_hp = st.text_input(

                "Nomor HP"

            )


            produk = st.selectbox(

                "Produk Diminati",

                PRODUK_LIST

            )





        with col2:


            alamat = st.text_area(

                "Alamat"

            )


            status = st.selectbox(

                "Status Follow Up",

                STATUS_LIST

            )






        keterangan = st.text_area(

            "Keterangan"

        )






        submit = st.form_submit_button(

            "💾 Simpan Data Prospek"

        )







        if submit:



            if nama.strip()=="":


                st.warning(

                    "Nama calon nasabah wajib diisi"

                )



            elif nomor_hp.strip()=="":


                st.warning(

                    "Nomor HP wajib diisi"

                )



            elif alamat.strip()=="":


                st.warning(

                    "Alamat wajib diisi"

                )



            else:



                data_baru = {


                    "ID":

                    get_next_id(df),



                    "Tanggal":

                    str(date.today()),



                    "Nama Calon Nasabah":

                    nama.strip(),



                    "Nomor HP":

                    nomor_hp.strip(),



                    "Alamat":

                    alamat.strip(),



                    "Produk Diminati":

                    produk,



                    "Status Follow Up":

                    status,



                    "Keterangan":

                    keterangan.strip()


                }




                df = pd.concat(

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

                    "Data prospek berhasil disimpan"

                )








    st.divider()







    st.markdown(

        "### Monitoring Data Prospek"

    )






    f1,f2,f3,f4 = st.columns(

        [1,1,1,2]

    )






    with f1:


        produk_filter = st.selectbox(

            "Filter Produk",

            ["Semua"]+PRODUK_LIST,

            key="filter_produk_entry"

        )





    with f2:


        status_filter = st.selectbox(

            "Filter Status",

            ["Semua"]+STATUS_LIST,

            key="filter_status_entry"

        )






    with f3:


        periode_filter = st.selectbox(

            "Filter Periode",

            [

                "Semua",

                "Hari ini",

                "7 hari terakhir",

                "Bulan ini"

            ],

            key="filter_periode_entry"

        )






    with f4:


        keyword = st.text_input(

            "Pencarian Data",

            placeholder=

            "Nama / HP / Produk / Status",

            key="search_entry"

        )








    filtered_data = filter_data(

        df,

        produk_filter,

        status_filter,

        periode_filter,

        keyword

    )






    st.caption(

        f"Menampilkan {len(filtered_data)} dari {len(df)} data"

    )







    st.dataframe(

        filtered_data,

        use_container_width=True,

        hide_index=True

    )








    csv_data = (

        filtered_data

        .to_csv(index=False)

        .encode("utf-8")

    )






    st.download_button(

        label="⬇️ Download Data CSV",

        data=csv_data,

        file_name="data_prospek_nasabah.csv",

        mime="text/csv"

    )







    st.divider()







    st.markdown(

        "### Hapus Data Prospek"

    )






    col_delete1,col_delete2 = st.columns(

        [3,1]

    )






    with col_delete1:


        delete_id = st.text_input(

            "Masukkan ID Data"

        )






    with col_delete2:


        st.write("")

        st.write("")



        delete_button = st.button(

            "🗑️ Hapus"

        )






    if delete_button:



        if delete_id in df["ID"].astype(str).tolist():



            df = df[

                df["ID"].astype(str)

                !=

                delete_id

            ]



            save_data(df)



            st.success(

                "Data berhasil dihapus"

            )



            st.rerun()





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



        # =================================================
        # FILTER DASHBOARD
        # =================================================


        st.markdown(

            "### Filter Monitoring"

        )





        col1,col2,col3,col4 = st.columns(

            [1,1,1,2]

        )






        with col1:


            produk_dashboard = st.selectbox(

                "Produk",

                ["Semua"] + PRODUK_LIST,

                key="dashboard_produk"

            )






        with col2:


            status_dashboard = st.selectbox(

                "Status Follow Up",

                ["Semua"] + STATUS_LIST,

                key="dashboard_status"

            )






        with col3:


            periode_dashboard = st.selectbox(

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


            search_dashboard = st.text_input(

                "Pencarian",

                placeholder=

                "Cari nama / nomor HP / alamat",

                key="dashboard_search"

            )







        dashboard_df = filter_data(

            df,

            produk_dashboard,

            status_dashboard,

            periode_dashboard,

            search_dashboard

        )







        st.caption(

            f"Menampilkan {len(dashboard_df)} dari {len(df)} total prospek"

        )







        # =================================================
        # KPI MONITORING
        # =================================================


        st.markdown(

            "### Ringkasan Monitoring"

        )





        k1,k2,k3,k4,k5,k6 = st.columns(6)





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

                "Tidak ada data yang sesuai filter"

            )






        else:





            chart_df = dashboard_df.copy()



            chart_df["Tanggal"] = pd.to_datetime(

                chart_df["Tanggal"],

                errors="coerce"

            )




            chart_df["Kecamatan"] = chart_df[

                "Alamat"

            ].apply(

                extract_kecamatan

            )







            # =================================================
            # GRAFIK 1
            # STATUS FOLLOW UP
            # =================================================



            st.markdown(

                "### 1. Jumlah Prospek Berdasarkan Status Follow Up"

            )





            status_chart = (

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






            fig_status = px.bar(

                status_chart,

                x="Status Follow Up",

                y="Jumlah",

                text="Jumlah",

                title="Monitoring Tahapan Follow Up"

            )






            fig_status.update_traces(

                textposition="outside"

            )





            fig_status.update_layout(

                height=420,

                template="plotly_white",

                showlegend=False

            )





            st.plotly_chart(

                fig_status,

                use_container_width=True

            )









            # =================================================
            # GRAFIK 2 DAN 3
            # =================================================



            col_a,col_b = st.columns(2)






            with col_a:



                st.markdown(

                    "### 2. Persentase Produk Diminati"

                )





                produk_chart = (

                    chart_df

                    .groupby(

                        "Produk Diminati"

                    )

                    .size()

                    .reset_index(

                        name="Jumlah"

                    )

                )






                fig_produk = px.pie(

                    produk_chart,

                    names="Produk Diminati",

                    values="Jumlah",

                    hole=0.45,

                    title="Komposisi Produk KUR dan KPR"

                )





                fig_produk.update_layout(

                    height=420

                )





                st.plotly_chart(

                    fig_produk,

                    use_container_width=True

                )








            with col_b:



                st.markdown(

                    "### 3. Tren Input Prospek Berdasarkan Tanggal"

                )






                trend_chart = (

                    chart_df

                    .dropna(

                        subset=["Tanggal"]

                    )

                    .groupby(

                        "Tanggal"

                    )

                    .size()

                    .reset_index(

                        name="Jumlah Prospek"

                    )

                    .sort_values(

                        "Tanggal"

                    )

                )






                fig_trend = px.line(

                    trend_chart,

                    x="Tanggal",

                    y="Jumlah Prospek",

                    markers=True,

                    title="Perkembangan Input Prospek"

                )






                fig_trend.update_layout(

                    height=420

                )





                st.plotly_chart(

                    fig_trend,

                    use_container_width=True

                )









            # =================================================
            # GRAFIK 4
            # KECAMATAN
            # =================================================



            st.markdown(

                "### 4. Sebaran Prospek Berdasarkan Kecamatan"

            )






            kecamatan_chart = (

                chart_df

                .groupby(

                    "Kecamatan"

                )

                .size()

                .reset_index(

                    name="Jumlah Prospek"

                )

                .sort_values(

                    "Jumlah Prospek",

                    ascending=False

                )

            )







            fig_kecamatan = px.bar(

                kecamatan_chart,

                x="Kecamatan",

                y="Jumlah Prospek",

                text="Jumlah Prospek",

                title="Distribusi Wilayah Prospek"

            )







            fig_kecamatan.update_traces(

                textposition="outside"

            )






            fig_kecamatan.update_layout(

                height=450,

                template="plotly_white"

            )






            st.plotly_chart(

                fig_kecamatan,

                use_container_width=True

            )









            # =================================================
            # TABEL MONITORING
            # =================================================



            st.divider()





            st.markdown(

                "### Tabel Monitoring Prospek"

            )






            table_df = chart_df.copy()





            table_df["Tanggal"] = (

                table_df["Tanggal"]

                .dt.strftime("%d-%m-%Y")

            )







            st.dataframe(

                table_df,

                use_container_width=True,

                hide_index=True

            )







            download_file = (

                table_df

                .to_csv(index=False)

                .encode("utf-8")

            )







            st.download_button(

                label="⬇️ Download Dashboard Report",

                data=download_file,

                file_name=

                "dashboard_monitoring_prospek_btn.csv",

                mime="text/csv"

            )
