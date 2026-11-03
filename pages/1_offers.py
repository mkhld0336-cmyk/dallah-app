import streamlit as st
import pandas as pd
import os, json
from datetime import datetime

CSV_PATH = "Marsad_Final_Categorized.csv"
ORDERS_FILE = "marsad_orders.json"

@st.cache_data
def load_products():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df = df.rename(columns={'اسم_الصورة': 'image', 'اسم_المنتج': 'name', 'السعر': 'price', 'القسم': 'category'})
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
        return df
    return pd.DataFrame()

st.title(":material/local_offer: مستودع العروض الحصرية")
st.caption("منصة مرصد - توريد ذكي وسريع للمطاعم والمتاجر في المملكة")

df = load_products()

if not df.empty:
    st.subheader("ملخص السوق اليوم", anchor=False)
    c1, c2, c3 = st.columns(3)
    c1.metric(label="المنتجات المتاحة", value=f"{len(df)} صنف")
    c2.metric(label="متوسط وقت التوصيل", value="4 ساعات", delta="-30 دقيقة")
    c3.metric(label="الحد الأدنى للطلب", value="250 ر.س", delta="مرن")
    
    st.divider()
    st.subheader("الأصناف المتوفرة للتوريد الفوري", anchor=False)

    for index, row in df.iterrows():
        with st.container(border=True):
            col_info, col_action = st.columns([3, 1], vertical_alignment="center")
            with col_info:
                st.markdown(f"### {row.get('name', 'منتج')}")
                sub_c1, sub_c2 = st.columns(2)
                with sub_c1:
                    st.markdown(f":material/category: **التصنيف:** {row.get('category', 'عام')}")
                with sub_c2:
                    st.markdown(f":material/payments: **السعر:** `{row.get('price', 0):.2f} ر.س`")
            with col_action:
                with st.expander("اطلب الآن"):
                    with st.form(f"form_{index}"):
                        phone = st.text_input("رقم الجوال:", key=f"phone_{index}")
                        if st.form_submit_button("تأكيد الطلب", type="primary"):
                            if phone:
                                orders = []
                                if os.path.exists(ORDERS_FILE):
                                    with open(ORDERS_FILE, 'r', encoding='utf-8') as f: orders = json.load(f)
                                orders.append({"product": row.get('name'), "price": row.get('price'), "phone": phone, "status": "تم الاستلام", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                                with open(ORDERS_FILE, 'w', encoding='utf-8') as f: json.dump(orders, f, ensure_ascii=False)
                                st.success("تم الطلب!")
                            else:
                                st.error("أدخل الجوال")
else:
    st.warning("ملف البيانات غير موجود.")
