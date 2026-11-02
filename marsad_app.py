import streamlit as st
import pandas as pd
import os
import json
import time
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="مرصد | Marsad", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; background-color: #0b0f19; color: #f3f4f6; }
    .marquee-container { background: linear-gradient(90deg, rgba(212,175,55,0.1), rgba(0,242,254,0.1)); border-bottom: 1px solid rgba(212,175,55,0.3); overflow: hidden; white-space: nowrap; padding: 10px 0; font-weight: 600; color: #fbbf24; }
    .marquee-text { display: inline-block; animation: marquee 25s linear infinite; }
    @keyframes marquee { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .glass-card { background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 16px; padding: 20px; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(135deg, #d4af37 0%, #aa771c 100%); color: white; border: none; border-radius: 50px; padding: 10px 24px; font-weight: 700; width: 100%; }
</style>
<div class="marquee-container"><div class="marquee-text">✨ النسخة التجريبية (Beta) - منصة مرصد تتجهز للانطلاق العالمي أبو محمد 👑</div></div>
""", unsafe_allow_html=True)

# مسار الملفات (نسخة Streamlit Cloud)
CSV_PATH = "Marsad_Final_Categorized.csv"
IMAGES_DIR = "Marsad_Images"
ORDERS_PATH = "marsad_orders.json"

# دالة تحميل البيانات
@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df.rename(columns={'اسم_المنتج':'name', 'السعر':'price', 'القسم':'category', 'اسم_الصورة':'image'}, inplace=True)
        return df
    return pd.DataFrame({"name": ["منتج تجريبي"], "price": [0], "category": ["عام"], "image": [""]})

df = load_data()

st.sidebar.markdown("<h2 style='text-align: center; color: #d4af37;'>💎 منصة مرصد</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("اختر القسم:", ["🏪 واجهة المتجر", "📊 لوحة التحكم", "💬 الشات الفاخر"])

if app_mode == "🏪 واجهة المتجر":
    st.markdown("<h1 style='text-align: center; color: #00f2fe;'>سوق النخبة - مرصد بريميوم</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, row in df.iterrows():
        col = cols[idx % 3]
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: #fbbf24;">{row['name']}</h3>
                <p style="color: #00f2fe; font-size: 1.2rem; font-weight: bold;">السعر: {row['price']} ر.س</p>
                <p style="color: #9ca3af;">القسم: {row['category']}</p>
            </div>
            """, unsafe_allow_html=True)

elif app_mode == "📊 لوحة التحكم":
    st.markdown("<h1 style='color: #d4af37;'>لوحة تحكم المشرف</h1>", unsafe_allow_html=True)
    st.info("هذه الصفحة مخصصة للمشرف. جاري تطوير الصلاحيات الكاملة...")

elif app_mode == "💬 الشات الفاخر":
    st.markdown("<h1 style='color: #00f2fe;'>الدردشة الحية</h1>", unsafe_allow_html=True)
    st.info("جاري ربط الدردشة بالخادم...")
