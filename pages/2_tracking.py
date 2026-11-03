import streamlit as st
import json, os

ORDERS_FILE = "marsad_orders.json"

st.title(":material/local_shipping: تتبع طلبك")
phone = st.text_input("أدخل رقم جوالك لمتابعة طلبك:")

if phone:
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f: orders = json.load(f)
        my_orders = [o for o in orders if str(o.get("phone")) == phone]
        
        if my_orders:
            latest = my_orders[-1]
            st.info(f"**الطلب:** {latest['product']}\n\n**الحالة:** {latest['status']}")
            progress = {"تم الاستلام": 25, "قيد التجهيز": 50, "في الطريق": 75, "تم التسليم": 100}
            st.progress(progress.get(latest['status'], 25) / 100)
        else:
            st.warning("لا توجد طلبات مسجلة بهذا الرقم.")
