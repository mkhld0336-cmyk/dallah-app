
import streamlit as st
import pandas as pd
from pathlib import Path
import html
import re

st.set_page_config(page_title="مرصد | مشتريات أعمالك", page_icon="🛒", layout="wide", initial_sidebar_state="collapsed")
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "Marsad_Valid_Products.csv"

st.markdown('''<style>@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800;900&display=swap'); html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; } .stApp { background: #F8FAFC; } .marsad-header { display: flex; justify-content: space-between; background: #FFF; border-radius: 18px; padding: 15px; margin-bottom: 24px; } .brand { color: #123B2D; font-size: 27px; font-weight: 900; } .hero { background: linear-gradient(120deg, #123B2D, #1D5A42); color: white; padding: 35px; border-radius: 22px; margin-bottom: 25px; } .category-card { background: white; border: 1px solid #E5EBEF; border-radius: 18px; padding: 23px; text-align: center; } .product-hidden-price { background: #F3F6F4; color: #557363; border-radius: 8px; padding: 7px; text-align: center; margin: 8px 0; } div.stButton > button { background: #174B35; color: #FFF; border-radius: 11px; font-weight: 800; width: 100%; }</style>''', unsafe_allow_html=True)

@st.cache_data
def load_products():
    if not CSV_FILE.exists(): return pd.DataFrame()
    df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")
    df["اسم المنتج"] = df["اسم المنتج"].fillna("").astype(str).str.strip()
    df["السعر"] = pd.to_numeric(df["السعر"].astype(str).str.replace(",", ".", regex=False), errors="coerce").fillna(0)
    def extract_old(notes):
        m = re.search(r"(?:السابق|قبل)\s*[:]?\s*(\d+(?:[.,]\d+)?)", str(notes))
        return float(m.group(1).replace(",", ".")) if m else None
    df["السعر القديم"] = df["ملاحظات"].apply(extract_old)
    def normalize(c):
        c = str(c).lower()
        if "بقال" in c: return "بقالة"
        if "رقمي" in c or "بطاق" in c: return "بطاقة رقمية"
        return "أخرى"
    df["القسم"] = df["القطاع"].apply(normalize)
    return df[df["السعر"] > 0].reset_index(drop=True)

products = load_products()

if "screen" not in st.session_state: st.session_state.screen = "home"
if "category" not in st.session_state: st.session_state.category = "بقالة"
if "sel" not in st.session_state: st.session_state.sel = None
if "otp_ok" not in st.session_state: st.session_state.otp_ok = False

def go(s): st.session_state.screen = s; st.rerun()

st.markdown('<div class="marsad-header"><div class="brand">مرصد</div></div>', unsafe_allow_html=True)

if st.session_state.screen == "home":
    st.markdown('<div class="hero"><h1>مشتريات أعمالك، بوضوح أكبر</h1><p>اختر القسم، واعرف تفاصيل طلبك بعد التحقق.</p></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, cat in zip(cols, ["بقالة", "بطاقة رقمية", "أخرى"]):
        with col:
            st.markdown(f'<div class="category-card"><h3>{cat}</h3></div>', unsafe_allow_html=True)
            if st.button("استعراض القسم", key=f"c_{cat}"):
                st.session_state.category = cat; go("products")

elif st.session_state.screen == "products":
    if st.button("← عودة للرئيسية"): go("home")
    st.subheader(st.session_state.category)
    cat_df = products[products["القسم"] == st.session_state.category]
    st.write(f"عدد المنتجات: {len(cat_df)}")
    
    for i in range(0, len(cat_df), 3):
        cols = st.columns(3)
        for col, (idx, row) in zip(cols, cat_df.iloc[i:i+3].iterrows()):
            with col:
                with st.container(border=True):
                    st.write(f"**{row['اسم المنتج']}**")
                    st.markdown('<div class="product-hidden-price">اعرف السعر بعد التحقق</div>', unsafe_allow_html=True)
                    if st.button("اطلب الآن", key=f"o_{idx}"):
                        st.session_state.sel = idx
                        st.session_state.otp_ok = False
                        go("verify")

elif st.session_state.screen == "verify":
    if st.button("← عودة"): go("products")
    st.subheader("التحقق من الحساب")
    phone = st.text_input("رقم الجوال", placeholder="+9665XXXXXXXX")
    if not st.session_state.otp_ok:
        if st.button("إرسال رمز التحقق"):
            if re.fullmatch(r"\+9665\d{8}", phone.strip()):
                st.success("الرمز التجريبي هو 1234")
            else:
                st.error("رقم غير صحيح")
        otp = st.text_input("رمز التحقق", type="password")
        if st.button("تأكيد"):
            if otp == "1234":
                st.session_state.otp_ok = True; go("invoice")
            else: st.error("رمز خاطئ")
    else:
        if st.button("متابعة للفاتورة"): go("invoice")

elif st.session_state.screen == "invoice":
    if st.session_state.sel is None or not st.session_state.otp_ok: go("home")
    prod = products.iloc[st.session_state.sel]
    
    st.subheader("ملخص الطلب")
    st.write(f"المنتج: **{prod['اسم المنتج']}**")
    
    qty = st.number_input("الكمية", min_value=1, value=1)
    unit_price = prod['السعر']
    total = unit_price * qty * 1.15
    
    st.write(f"سعر الوحدة: {unit_price} ر.س")
    st.write(f"الإجمالي شامل 15% ضريبة: {total:.2f} ر.س")
    
    if pd.notna(prod['السعر القديم']):
        st.markdown(f"~~السعر القديم: {prod['السعر القديم']} ر.س~~")
        saving = (prod['السعر القديم'] - unit_price) * qty
        st.success(f"🏷️ وفرت {saving:.2f} ر.س!")

    st.write("### طريقة الدفع")
    st.radio("اختر", ["دفع كامل", "عند الاستلام", "عربون 20%"])
    
    if st.button("تأكيد الطلب النهائي", type="primary"):
        st.success("تم استلام طلبك بنجاح! 🎉")
        if st.button("العودة للرئيسية"):
            st.session_state.screen = "home"; st.session_state.sel = None; st.rerun()
