
import streamlit as st
import json, os
from datetime import datetime

st.markdown("""
<style>
html, body, [data-testid="stSidebarNav"] { direction: RTL; text-align: right; }
</style>
""", unsafe_import_code=True)

st.title("🚚 مركز تتبع الشحنات والطلبات")
st.caption("أدخل رقم الجوال المسجل لمتابعة حالة طلبات التوريد الحالية والمكتملة")

ORDERS_FILE = "marsad_orders.json"
phone_number = st.text_input("رقم الجوال الخاص بالمتجر/المطعم", placeholder="05xxxxxxxx", max_chars=10)

if phone_number:
    if phone_number.startswith("05") and len(phone_number) == 10:
        orders = []
        if os.path.exists(ORDERS_FILE):
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                orders = json.load(f)

        my_orders = [o for o in orders if str(o.get("phone")) == phone_number]

        if my_orders:
            st.success(f"تم العثور على {len(my_orders)} طلب مرتبط بهذا الرقم.")

            for order in reversed(my_orders):
                status = order.get("status", "تم الاستلام")
                status_map = {"تم الاستلام": 1, "قيد التجهيز": 2, "في الطريق": 3, "تم التسليم": 4}
                current_stage = status_map.get(status, 1)

                with st.container(border=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**المنتج:** {order.get('product', '')}")
                    with col2:
                        st.markdown(f"**التاريخ:** {order.get('date', '')}")
                    with col3:
                        st.markdown(f"**السعر:** `{order.get('price', 0)} ر.س`")

                    st.subheader("مرحلة التوصيل الحالية", anchor=False)
                    progress_percentage = (current_stage - 1) / 3
                    st.progress(progress_percentage)

                    step_cols = st.columns(4)
                    with step_cols[0]:
                        st.markdown(":material/fact_check: **تم تأكيد الطلب**")
                        st.caption("تم مراجعة الأصناف")
                    with step_cols[1]:
                        st.markdown(":material/inventory_2: **جاري التجهيز**")
                        st.caption("في مستودع مرصد")
                    with step_cols[2]:
                        if current_stage == 3:
                            st.markdown(":material/local_shipping: **خرج للتوصيل** :orange[[نشط]]")
                            st.caption("السائق في الطريق")
                        else:
                            st.markdown(":material/local_shipping: خرج للتوصيل")
                            st.caption("انتظار")
                    with step_cols[3]:
                        if current_stage == 4:
                            st.markdown(":material/check_box: **تم التسليم** :green[[مكتمل]]")
                        else:
                            st.markdown(":material/check_box: تم التسليم")
                            st.caption("في موقع المتجر")

                    if current_stage >= 3 and current_stage < 4:
                        st.info("معلومات السائق: كابتن أحمد - 0500000000 - مركبة مبردة")
                    st.divider()
        else:
            st.warning("لا توجد طلبات مسجلة بهذا الرقم. تأكد من الرقم أو اطلب الآن من صفحة العروض.")
    else:
        st.error("صيغة رقم الجوال غير صحيحة، يرجى كتابة 10 أرقام تبدأ بـ 05.")
else:
    st.info("يرجى كتابة رقم الجوال بالأعلى ليتم استدعاء بيانات شحنتك فوراً.")
