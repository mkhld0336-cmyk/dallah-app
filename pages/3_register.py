import streamlit as st
import json, os
from datetime import datetime

SUBS_FILE = "marsad_subscribers.json"

st.title(":material/person_add: انضم كتاجر في مرصد")
st.write("سجل بياناتك لنتمكن من توصيل طلبات الجملة إليك بأسرع وقت.")

with st.form("sub_form"):
    store_name = st.text_input("اسم المتجر / المطعم:")
    owner_name = st.text_input("اسم المالك:")
    phone = st.text_input("رقم الجوال:")
    location = st.text_input("الموقع (الحي / المدينة):")
    
    if st.form_submit_button("إرسال طلب الاشتراك", type="primary"):
        if store_name and phone:
            subs = []
            if os.path.exists(SUBS_FILE):
                with open(SUBS_FILE, 'r', encoding='utf-8') as f: subs = json.load(f)
            subs.append({"store": store_name, "owner": owner_name, "phone": phone, "location": location, "date": datetime.now().strftime("%Y-%m-%d")})
            with open(SUBS_FILE, 'w', encoding='utf-8') as f: json.dump(subs, f, ensure_ascii=False)
            st.success("✅ تم استلام طلبك! سيتواصل معك فريق مرصد قريباً.")
        else:
            st.error("⚠️ يرجى إدخال اسم المتجر ورقم الجوال.")
