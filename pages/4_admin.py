
import streamlit as st
import json, os
import pandas as pd

st.markdown("""
<style>
html, body, [data-testid="stSidebarNav"] { direction: RTL; text-align: right; }
</style>
""", unsafe_import_code=True)

st.title(":material/admin_panel_settings: لوحة التحكم الإدارية")
st.caption("إدارة الطلبات والاشتراكات - محمية بكود إدارة")

ORDERS_FILE = "marsad_orders.json"
SUBS_FILE = "marsad_subscribers.json"

auth = st.text_input("أدخل كود الإدارة للدخول:", type="password")

if auth == "1990":
    st.success("مرحباً بك يا مدير المنصة")
    
    tab1, tab2 = st.tabs(["📦 الطلبات الحالية", "🤝 طلبات الاشتراك"])
    
    with tab1:
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                orders = json.load(f)
            
            if orders:
                st.markdown(f"**:material/analytics: إجمالي الطلبات: {len(orders)}**")
                
                for i, o in enumerate(reversed(orders)):
                    idx = len(orders) - 1 - i
                    status = o.get("status", "تم الاستلام")
                    icon = {"تم الاستلام": "🆕", "قيد التجهيز": "⚙️", "في الطريق": "🚚", "تم التسليم": "✅"}.get(status, "•")
                    
                    with st.expander(f"{icon} {o.get('product')} | {o.get('phone')} | {status}"):
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.markdown(f":material/payments: **السعر:** {o.get('price')} ر.س")
                        with c2:
                            st.markdown(f":material/schedule: **التاريخ:** {o.get('date', '')}")
                        with c3:
                            st.markdown(f":material/flag: **الحالة:** {status}")
                        
                        st.markdown("**تحديث الحالة:**")
                        btn1, btn2, btn3 = st.columns(3)
                        if btn1.button("⚙️ قيد التجهيز", key=f"p_{idx}", use_container_width=True):
                            orders[idx]["status"] = "قيد التجهيز"
                            with open(ORDERS_FILE, "w", encoding="utf-8") as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
                        if btn2.button("🚚 في الطريق", key=f"w_{idx}", use_container_width=True):
                            orders[idx]["status"] = "في الطريق"
                            with open(ORDERS_FILE, "w", encoding="utf-8") as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
                        if btn3.button("✅ تم التسليم", key=f"d_{idx}", use_container_width=True):
                            orders[idx]["status"] = "تم التسليم"
                            with open(ORDERS_FILE, "w", encoding="utf-8") as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
            else:
                st.info(":material/inbox: لا توجد طلبات حتى الآن.")
        else:
            st.info(":material/inbox: لا توجد طلبات حتى الآن.")
    
    with tab2:
        if os.path.exists(SUBS_FILE):
            with open(SUBS_FILE, "r", encoding="utf-8") as f:
                subs = json.load(f)
            
            if subs:
                st.markdown(f"**:material/people: إجمالي المشتركين: {len(subs)}**")
                df = pd.DataFrame(subs)
                df.columns = ["اسم المتجر", "المالك", "الجوال", "الموقع", "التاريخ"]
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                csv = df.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    label="📥 تحميل قائمة المشتركين (CSV)",
                    data=csv,
                    file_name=f"marsad_subscribers_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.info(":material/inbox: لا توجد طلبات اشتراك حتى الآن.")
        else:
            st.info(":material/inbox: لا توجد طلبات اشتراك حتى الآن.")
            
elif auth != "":
    st.error("❌ كود الإدارة غير صحيح. حاول مرة أخرى.")
else:
    st.info("🔒 هذه الصفحة محمية. أدخل الكود للوصول إلى لوحة التحكم.")
