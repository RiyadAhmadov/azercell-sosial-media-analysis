import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import base64
import io

st.set_page_config(page_title="🚀Ana Səhifə", layout="centered")

st.sidebar.image(r"azercell/azercell_app/azercell_telecom_llc_logo.png", use_container_width = True, width = 5)

data_ins = pd.read_excel(r'azercell/azercell_app/azercell_instagram_comments.xlsx')
data_face_image = pd.read_excel(r'azercell/azercell_app/azercell_facebook_image_comments.xlsx')
data_face_video = pd.read_excel(r'azercell/azercell_app/azercell_facebook_video_comments.xlsx')
data_face = pd.concat([data_face_image,data_face_video]) 

data_ins.columns = ['Hesab Adı','Rəy','Postun Paylaşılma Tarixi','Postun Paylaşılma Saatı','Rəyin Yazılma Tarixi','Paylaşımın Məzmunu','Rəy Bəyənmə','Paylaşım Bəyənmə','Paylaşım']
data_face.columns = ['Hesab Adı','Rəy','Rəyin Yazılma Tarixi','Paylaşım']

data_ins['Postun Paylaşılma Saatı'] = pd.to_datetime(data_ins['Postun Paylaşılma Saatı']).dt.strftime('%H:%M:%S')
data_face['Rəyin Yazılma Tarixi'] = pd.to_datetime(data_face['Rəyin Yazılma Tarixi']).dt.date

st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img src="https://seeklogo.com/images/A/azercell-logo-119FFF6347-seeklogo.com.png" width="80">
        <h1 style="margin-left: 10px;">Azercell Telecom LLC - Sosial Şəbəkə Rəylərinin Analizi</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("📋 Layihə Haqqında")
st.markdown("""
Bu layihə, müştəri rəylərinin analizi vasitəsilə Azercell Telecom LLC-nin xidmətlərindəki çatışmazlıqları və inkişaf ehtiyaclarını müəyyən etməyə yönəlib.
""")

st.subheader("📊 Verilənlər Haqqında (Dataset)")

st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img style="margin-left: 4.5px;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Instagram_logo_2022.svg/1024px-Instagram_logo_2022.svg.png" width="27">
        <a href="https://www.instagram.com/azercell/?hl=en" target="_blank" style="text-decoration: none; color: white;">
            <h3 style="margin-left: 10px; margin-bottom: 0px; line-height: 1.8; display: inline; font-size: 26px; font-weight: 600;">Azercell Telecom LLC - Instagram</h3>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("""
Layihədə istifadə olunan məlumat aşağıdakı sütunları əhatə edir:
- **Hesab Adı**: Rəyin yazıldığı istifadəçi adı.
- **Rəy**: İstifadəçinin yazdığı rəy mətni.
- **Postun Paylaşılma Tarixi**: Postun paylaşıldığı tarix.
- **Postun Paylaşılma Saatı**: Postun paylaşıldığı saat.
- **Rəyin Yazılma Tarixi**: Rəyin yazıldığı tarix.
- **Paylaşımın Məzmunu**: Paylaşımın məzmunu.
- **Rəy Bəyənmə**: Rəyin aldığı bəyənmə sayı.
- **Paylaşım Bəyənmə**: Paylaşımın aldığı bəyənmə sayı.
- **Paylaşım**: Paylaşımın linki və ya URL-si.
""")

st.write("🔍 **Verilənlərə Baxış:**")
st.dataframe(data_ins.head())

st.markdown("---")

st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <img style="margin-left: 4.5px;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/2023_Facebook_icon.svg/768px-2023_Facebook_icon.svg.png" width="27">
        <a href="https://www.facebook.com/azercell/?hl=en" target="_blank" style="text-decoration: none; color: white;">
            <h1 style="margin-left: 10px; margin-bottom: 0px; line-height: 1.8; display: inline; font-size: 26px; font-weight: 600;">Azercell Telecom LLC - Facebook</h1>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""\n
Layihədə istifadə olunan məlumat aşağıdakı sütunları əhatə edir:
- **Hesab Adı**: Rəyin yazıldığı istifadəçi adı.
- **Rəy**: İstifadəçinin yazdığı rəy mətni.
- **Rəyin Yazılma Tarixi**: Rəyin yazıldığı tarix.
- **Paylaşım**: Paylaşımın linki və ya URL-si.
""")

st.write("🔍 **Verilənlərə Baxış:**")
st.dataframe(data_face.head())

st.markdown("---")

st.subheader("🎯 Layihənin Məqsədi")
st.markdown("""
- **Problemin Təsviri**: Müştəri rəyləri əsasında Azercell Telecom LLC-nin xidmət keyfiyyətini və müştəri məmnuniyyətini təhlil etmək.  
- **Hədəf**: Sosial şəbəkələrdəki istifadəçi rəylərini analiz edərək xidmətin zəif və güclü tərəflərini müəyyənləşdirmək.
""")

st.subheader("🌟 Layihənin Faydaları")
st.markdown("""
- **Müştərilər üçün üstünlüklər**: Şirkətin xidmət keyfiyyəti haqqında daha dolğun məlumat əldə etməyə kömək edir.  
- **Şirkət üçün üstünlüklər**: Müştəri məmnuniyyətini artırmaq üçün xidmət sahəsində inkişaf istiqamətlərini müəyyənləşdirməyə imkan yaradır.  
- **Sektor üçün üstünlüklər**: Telekommunikasiya sahəsində daha məlumatlı və müştəri yönümlü qərarların qəbul edilməsini təmin edir.
""")

st.markdown("---")
st.write("📥 **İnstagram Sosial Şəbəkə Müştəri Rəyləri Məlumatını Yükləyin:**")

col1, col2 = st.columns(2)

ins_data_excel = io.BytesIO()
data_ins.to_excel(ins_data_excel, index=False)
ins_data_excel.seek(0)

ins_data_csv = io.BytesIO()
data_ins.to_csv(ins_data_csv, index=False)
ins_data_csv.seek(0)

with col1:
    st.download_button(
        label="📊 Excel Faylını Yüklə",
        data=ins_data_excel,
        file_name='azercell_instagram_comments.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

with col2:
    st.download_button(
        label="📄 CSV Faylını Yüklə",
        data=ins_data_csv,
        file_name='azercell_instagram_comments.csv',
        mime='text/csv'
    )


st.markdown("---")
st.write("📥 **Facebook Sosial Şəbəkə Müştəri Rəyləri Məlumatını Yükləyin:**")

col3, col4 = st.columns(2)

face_data_excel = io.BytesIO()
data_face.to_excel(face_data_excel, index=False)
face_data_excel.seek(0)

face_data_csv = io.BytesIO()
data_face.to_csv(face_data_csv, index=False)
face_data_csv.seek(0)

with col3:
    st.download_button(
        label="📊 Excel Faylını Yüklə",
        data=face_data_excel,
        file_name='azercell_facebook_comments.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
with col4:
    st.download_button(
        label="📄 CSV Faylını Yüklə",
        data=face_data_csv,
        file_name='azercell_facebook_comments.csv',
        mime='text/csv'
    )


st.markdown("---")
st.write("💡 Daha ətraflı məlumat üçün layihə sənədlərinə baxın və ya əlaqə saxlayın.")
st.write("📧 Email: [riyadehmedov03@gmail.com](mailto:riyadehmedov03@gmail.com)")
st.write("📞 Telefon: +994 55 551-98-18")

# ✅Done
