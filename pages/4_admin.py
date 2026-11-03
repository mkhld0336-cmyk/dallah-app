
import streamlit as st
import json, os
import pandas as pd

st.markdown("""<style>html, body, [data-testid="stSidebarNav"] {direction: RTL; text-align: right;}</style>""", unsafe_allow_html=True)

st.title("🔐 لوحة التحكم الإدارية الداخلية")
st.caption("خاصة بموظفي العمليات والدعم اللوجستي لمنصة مرصد")

ORDERS_FILE = "marsad_orders.json"
SUBS_FILE = "marsad_subscribers.json"

if "admin_auth" not in st.session_state:
    st.session_state.admin_auth = False

if not st.session_state.admin_auth:
    with st.container(border=True):
        st.subheader("التحقق من الهوية الرقمية", anchor=False)
        access_code = st.text_input("أدخل كود الدخول للإدارة", type="password", placeholder="••••")
        if st.button("تسجيل الدخول", type="primary", use_container_width=True):
            if access_code == "1990":
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("❌ كود الدخول غير صحيح!")
else:
    if st.sidebar.button("🚪 تسجيل الخروج", use_container_width=True):
        st.session_state.admin_auth = False
        st.rerun()
    
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f: orders = json.load(f)
    
    subs = []
    if os.path.exists(SUBS_FILE):
        with open(SUBS_FILE, "r", encoding="utf-8") as f: subs = json.load(f)
    
    pending = sum(1 for o in orders if o.get("status") == "تم الاستلام")
    in_transit = sum(1 for o in orders if o.get("status") == "في الطريق")
    delivered = sum(1 for o in orders if o.get("status") == "تم التسليم")
    total_value = sum(float(o.get("price", 0)) for o in orders)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي الطلبات", f"{len(orders)}", delta=f"{pending} معلق")
    c2.metric("في الطريق", f"{in_transit}", delta="قيد التوصيل")
    c3.metric("تم التسليم", f"{delivered}", delta="مكتمل")
    c4.metric("حجم المبيعات", f"{total_value:.0f} ر.س")
    
    st.divider()
    
    tab1, tab2 = st.tabs([f"📦 الطلبات ({len(orders)})", f"🤝 طلبات الاشتراك ({len(subs)})"])
    
    with tab1:
        if orders:
            for i, o in enumerate(reversed(orders)):
                idx = len(orders) - 1 - i
                status = o.get("status", "تم الاستلام")
                icon = {"تم الاستلام": "🆕", "قيد التجهيز": "⚙️", "في الطريق": "🚚", "تم التسليم": "✅"}.get(status, "•")
                
                with st.container(border=True):
                    col_det, col_ops = st.columns([3, 1], vertical_alignment="center")
                    with col_det:
                        st.markdown(f"### {icon} {o.get('product', '')}")
                        st.markdown(f"📱 **الجوال:** `{o.get('phone', '')}` | 💰 **القيمة:** `{o.get('price', 0)} ر.س`")
                        st.markdown(f"🕐 **التاريخ:** {o.get('date', '')} | 🚦 **الحالة:** `{status}`")
                    with col_ops:
                        if st.button("⚙️ تجهيز", key=f"p_{idx}", use_container_width=True):
                            orders[idx]["status"] = "قيد التجهيز"
                            with open(ORDERS_FILE, "w", encoding="utf-8") as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
                        if st.button("🚚 توصيل", key=f"w_{idx}", use_container_width=True):
                            orders[idx]["status"] = "في الطريق"
                            with open(ORDERS_FILE, "w", encoding="utf-8") as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
                        if st.button("✅ تسليم", key=f"d_{idx}", use_container_width=True, type="primary"):
                            orders[idx]["status"] = "تم التسليم"
                            with open(ORDERS_FILE, "w", encoding="utf-8") as f: json.dump(orders, f, ensure_ascii=False)
                            st.rerun()
        else:
            st.info("📭 لا توجد طلبات حتى الآن.")
    
    with tab2:
        if subs:
            df = pd.DataFrame(subs)
            df.columns = ["المتجر", "المالك", "الجوال", "البريد", "المدينة", "الحي", "العنوان", "التاريخ"]
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("📥 تحميل قائمة المشتركين (CSV)", data=csv,
                              file_name=f"marsad_subs_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                              mime="text/csv", use_container_width=True)
        else:
            st.info("📭 لا توجد طلبات اشتراك حتى الآن.")
