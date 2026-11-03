import streamlit as st
import json, os
import pandas as pd

ORDERS_FILE = "marsad_orders.json"
SUBS_FILE = "marsad_subscribers.json"

st.title(":material/admin_panel_settings: لوحة التحكم الإدارية")
auth = st.text_input("أدخل كود الإدارة للدخول:", type="password")

if auth == "1990":
    st.success("مرحباً بك يا مدير المنصة")
    tab1, tab2 = st.tabs(["📦 الطلبات", "🤝 طلبات الاشتراك"])
    
    with tab1:
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, 'r', encoding='utf-8') as f: orders = json.load(f)
            if orders:
                for i, o in enumerate(reversed(orders)):
                    idx = len(orders) - 1 - i
                    with st.expander(f"{o['product']} | {o['phone']} | {o['status']}"):
                        c1, c2, c3 = st.columns(3)
                        if c1.button("تجهيز", key=f"p_{idx}"): 
                            orders[idx]['status']="قيد التجهيز"
                            with open(ORDERS_FILE, 'w', encoding='utf-8') as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
                        if c2.button("توصيل", key=f"w_{idx}"): 
                            orders[idx]['status']="في الطريق"
                            with open(ORDERS_FILE, 'w', encoding='utf-8') as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
                        if c3.button("تم التسليم", key=f"d_{idx}"): 
                            orders[idx]['status']="تم التسليم"
                            with open(ORDERS_FILE, 'w', encoding='utf-8') as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
            else: st.info("لا توجد طلبات.")
            
    with tab2:
        if os.path.exists(SUBS_FILE):
            with open(SUBS_FILE, 'r', encoding='utf-8') as f: subs = json.load(f)
            if subs:
                st.dataframe(pd.DataFrame(subs), use_container_width=True)
            else: st.info("لا توجد طلبات اشتراك.")
            
elif auth != "":
    st.error("❌ كود غير صحيح")
