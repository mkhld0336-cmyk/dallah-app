
import streamlit as st
import json, os
from datetime import datetime

st.markdown("""<style>html, body, [data-testid="stSidebarNav"] {direction: RTL; text-align: right;}</style>""", unsafe_allow_html=True)

st.title("🤝 انضم إلى شبكة مرصد كتاجر")
st.caption("سجل بيانات منشأتك الآن وابدأ في استقبال عروض التوريد بأسعار تنافسية")

SUBS_FILE = "marsad_subscribers.json"

with st.container(border=True):
    st.subheader("📝 نموذج تسجيل منشأة جديدة", anchor=False)
    
    col1, col2 = st.columns(2)
    with col1:
        shop_name = st.text_input("اسم المتجر / المطعم / المقهى *", placeholder="مثال: شركة مذاق القهوة المحدودة")
        manager_name = st.text_input("اسم المسؤول عن المشتريات", placeholder="الاسم الثنائي")
    with col2:
        phone = st.text_input("رقم جوال التواصل التجاري *", placeholder="05xxxxxxxx", max_chars=10)
        email = st.text_input("البريد الإلكتروني التجاري (اختياري)", placeholder="info@yourcompany.com")
    
    st.divider()
    st.markdown("📍 **تفاصيل الموقع الجغرافي والشحن**")
    
    col_geo1, col_geo2 = st.columns(2)
    with col_geo1:
        city = st.selectbox("المدينة", ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "القصيم", "أخرى"])
    with col_geo2:
        district = st.text_input("الحي", placeholder="مثال: حي الصحافة")
    
    address_details = st.text_area("تفاصيل العنوان ورقم المبنى", placeholder="اكتب تفاصيل العنوان أو رابط خرائط جوجل بدقة")
    
    agree = st.checkbox("أوافق على شروط وأحكام منصة مرصد للتوريد وسياسة الخصوصية.")

if st.button("تقديم طلب الاشتراك والاعتماد", type="primary", use_container_width=True, icon="assignment_turned_in"):
    if not shop_name or not phone or not address_details:
        st.error("⚠️ يرجى ملء الحقول الأساسية (اسم المتجر، الجوال، وتفاصيل العنوان).")
    elif not phone.startswith("05") or len(phone) != 10:
        st.error("⚠️ يرجى إدخال رقم جوال سعودي صحيح 10 أرقام يبدأ بـ 05.")
    elif not agree:
        st.warning("⚠️ يجب الموافقة على شروط الخدمة.")
    else:
        subs = []
        if os.path.exists(SUBS_FILE):
            with open(SUBS_FILE, "r", encoding="utf-8") as f:
                subs = json.load(f)
        subs.append({
            "store": shop_name, "owner": manager_name, "phone": phone,
            "email": email, "city": city, "district": district,
            "address": address_details, "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        with open(SUBS_FILE, "w", encoding="utf-8") as f:
            json.dump(subs, f, ensure_ascii=False, indent=2)
        st.balloons()
        st.success(f"🎉 تم استلام طلبك بنجاح لمتجر **{shop_name}**! سيتواصل معك فريق مرصد خلال 24 ساعة.")
