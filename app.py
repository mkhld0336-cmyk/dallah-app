import streamlit as st
import os

st.set_page_config(
    page_title="مرصد | Marsad B2B",
    page_icon=":material/storefront:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [data-testid="stSidebarNav"] {
    direction: RTL;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

offers_page = st.Page("pages/1_offers.py", title="العروض المتاحة", icon=":material/local_offer:")
tracking_page = st.Page("pages/2_tracking.py", title="تتبع الطلبات", icon=":material/local_shipping:")
register_page = st.Page("pages/3_register.py", title="تسجيل تاجر جديد", icon=":material/person_add:")
admin_page = st.Page("pages/4_admin.py", title="لوحة التحكم الإدارية", icon=":material/admin_panel_settings:")

pg = st.navigation({
    "بوابة التاجر": [offers_page, tracking_page, register_page],
    "الإدارة الداخلية": [admin_page],
})

pg.run()
