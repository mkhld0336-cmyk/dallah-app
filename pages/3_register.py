
import streamlit as st
import json, os
from datetime import datetime

st.markdown("""
<style>
html, body, [data-testid="stSidebarNav"] { direction: RTL; text-align: right; }
</style>
""", unsafe_import_code=True)

st.title(":material/person_add: انضم كتاجر في مرصد")
st.caption("سجل بيانات متجرك أو مطعمك للانضمام إلى شبكة مرصد للتوريد الذكي")

SUBS_FILE = "marsad_subscribers.json"

with st.container(border=True):
    st.subheader("بيانات المتجر / المطعم", anchor=False)
    
    with st.form("sub_form"):
        col1, col2 = st.columns(2)
        with col1:
            store_name = st.text_input("اسم المتجر / المطعم *")
            owner_name = st.text_input("اسم المالك")
        with col2:
            phone = st.text_input("رقم الجوال *", placeholder="05xxxxxxxx")
            location = st.text_input("الموقع (الحي / المدينة)")
        
        st.markdown(":material/info: الحقول التي تحمل (*) إلزامية.")
        
        if st.form_submit_button("إرسال طلب الاشتراك", type="primary", use_container_width=True):
            if store_name and phone:
                if phone.startswith("05") and len(phone) == 10:
                    subs = []
                    if os.path.exists(SUBS_FILE):
                        with open(SUBS_FILE, "r", encoding="utf-8") as f:
                            subs = json.load(f)
                    subs.append({
                        "store": store_name,
                        "owner": owner_name,
                        "phone": phone,
                        "location": location,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    with open(SUBS_FILE, "w", encoding="utf-8") as f:
                        json.dump(subs, f, ensure_ascii=False)
                    st.success("✅ تم استلام طلبك! سيتواصل معك فريق مرصد خلال 24 ساعة.")
                else:
                    st.error("⚠️ رقم الجوال يجب أن يبدأ بـ 05 ويكون 10 أرقام.")
            else:
                st.error("⚠️ يرجى إدخال اسم المتجر ورقم الجوال.")
