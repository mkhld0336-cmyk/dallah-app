import streamlit as st
import pandas as pd
import time
import os

st.set_page_config(page_title="مرصد | Marsad", page_icon="🦅", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
.stApp { background-color: #F8FAFC; color: #0F172A; }
h1, h2, h3 { color: #1E293B !important; font-weight: 800 !important; }
.hero-banner { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-radius: 16px; padding: 40px 30px; color: white; text-align: center; margin-bottom: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.15); }
.hero-banner h1 { color: #FFD700 !important; font-size: 2.2rem; margin: 0; }
.hero-banner p { color: #CBD5E1; font-size: 1.1rem; margin-top: 10px; }
div[data-testid="stVerticalBlockBorderWrapper"] { background: #ffffff !important; border: 1px solid #E2E8F0 !important; border-radius: 16px !important; padding: 20px !important; transition: all 0.3s ease !important; }
div[data-testid="stVerticalBlockBorderWrapper"]:hover { box-shadow: 0 12px 24px rgba(0,0,0,0.08) !important; transform: translateY(-3px) !important; }
.price-tag { font-size: 1.5rem; font-weight: 900; color: #10B981; margin: 10px 0; }
.card-region { color: #64748B; font-size: 0.9rem; }
.code-box { background: #0F172A; color: #FFD700; padding: 24px; border-radius: 12px; font-size: 1.6rem; font-weight: 900; text-align: center; letter-spacing: 4px; font-family: monospace; margin: 15px 0; }
.qty-display { text-align: center; font-size: 1.5rem; font-weight: 900; padding: 5px; }
.stButton>button { background-color: #3B82F6 !important; color: white !important; font-weight: bold !important; border-radius: 10px !important; border: none !important; padding: 10px !important; }
.stButton>button:hover { background-color: #2563EB !important; }
</style>
""", unsafe_allow_html=True)

# ============ STATE ============
if "page" not in st.session_state: st.session_state.page = "home"
if "category" not in st.session_state: st.session_state.category = None
if "selected" not in st.session_state: st.session_state.selected = None
if "quantity" not in st.session_state: st.session_state.quantity = 1
if "payment" not in st.session_state: st.session_state.payment = "دفع كامل"

# ============ LOAD DATA ============
@st.cache_data
def load_data():
    if os.path.exists("Marsad_Valid_Products.csv"):
        df = pd.read_csv("Marsad_Valid_Products.csv")
        df.columns = ["name", "price", "category", "notes", "image"]
        return df
    return pd.DataFrame()

df = load_data()

# ============ HOME ============
if st.session_state.page == "home":
    st.markdown("<h1 style='text-align:center;'>🦅 منصة مرصد</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748B; font-size:1.1rem;'>منصة التوريد الذكية للمتاجر والمطاعم والمقاهي</p>", unsafe_allow_html=True)
    st.divider()
    st.subheader("اختر قطاعك")
    
    cols = st.columns(3)
    cats = [("🛒", "البقالة", "grocery"), ("💳", "البطاقات الرقمية", "digital"), ("📦", "أخرى", "other")]
    
    for i, (icon, name, key) in enumerate(cats):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"<h2 style='text-align:center; font-size:2.5rem;'>{icon}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align:center;'>{name}</h3>", unsafe_allow_html=True)
                if st.button(f"اكتشف {name}", key=f"cat_{key}", use_container_width=True, type="primary"):
                    st.session_state.category = key
                    st.session_state.page = "products"
                    st.rerun()

# ============ PRODUCTS ============
elif st.session_state.page == "products":
    if st.button("🔙 العودة للأقسام"):
        st.session_state.page = "home"
        st.rerun()
        
    cat = st.session_state.category
    cat_map = {"grocery": "بقالة", "digital": "بطاقة رقمية", "other": "أخرى"}
    cat_name = cat_map.get(cat, "بقالة")
    
    if cat == "digital":
        st.markdown("""
        <div class="hero-banner">
            <h1>قسم البطاقات الرقمية</h1>
            <p>عالمك الرقمي.. أقرب إليك</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.title(cat_name)
    
    st.divider()
    
    filtered_df = df[df['category'] == cat_name]
    
    if filtered_df.empty:
        st.warning("لا توجد منتجات في هذا القسم حالياً.")
    else:
        cols = st.columns(3)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            with cols[idx % 3]:
                with st.container(border=True):
                    st.markdown(f"<h3>{row['name']}</h3>", unsafe_allow_html=True)
                    st.caption(f"ملاحظات: {row['notes']}")
                    if cat == "digital":
                        st.markdown(f"<div class='card-region'>المنطقة: السعودية</div>", unsafe_allow_html=True)
                    
                    # هنا نضع السعر في الفاتورة لاحقاً، لكن لا نعرضه هنا
                    if st.button("اطلب الآن", key=f"ord_{idx}", use_container_width=True, type="primary"):
                        st.session_state.selected = row.to_dict()
                        st.session_state.page = "otp"
                        st.rerun()
                    st.caption("اعرف تفاصيل طلبك بعد التحقق")

# ============ OTP ============
elif st.session_state.page == "otp":
    if st.button("🔙 العودة للمنتجات"):
        st.session_state.page = "products"
        st.rerun()
    st.title("التحقق من الحساب")
    with st.container(border=True):
        phone = st.text_input("رقم الجوال السعودي", placeholder="05X XXX XXXX")
        if st.button("إرسال رمز التحقق", use_container_width=True, type="primary"):
            if len(phone) >= 10:
                st.session_state.phone = phone
                st.session_state.page = "otp_verify"
                st.rerun()
            else:
                st.error("⚠️ أدخل رقم جوال صحيح")

# ============ OTP VERIFY ============
elif st.session_state.page == "otp_verify":
    st.title("رمز التحقق")
    with st.container(border=True):
        otp = st.text_input("أدخل الرمز (للتجربة: 1234)", type="password")
        if st.button("تأكيد", use_container_width=True, type="primary"):
            if otp == "1234":
                st.session_state.page = "invoice"
                st.rerun()
            else:
                st.error("⚠️ رمز غير صحيح")

# ============ INVOICE ============
elif st.session_state.page == "invoice":
    prod = st.session_state.selected
    price = float(prod['price'])
    vat = price * 0.15
    total = price + vat
    
    st.title("ملخص الطلب")
    st.success("✅ تم التحقق")
    st.divider()
    
    with st.container(border=True):
        st.markdown(f"### {prod['name']}")
        st.markdown(f"**سعر الوحدة:** `{price:.2f} ر.س`")
        st.markdown(f"**ضريبة القيمة المضافة (15%):** `{vat:.2f} ر.س`")
        st.markdown(f"<div class='price-tag'>الإجمالي النهائي: {total:.2f} ر.س</div>", unsafe_allow_html=True)
        st.divider()
        st.subheader("اختر طريقة الدفع")
        
        c1, c2, c3 = st.columns(3)
        if c1.button("دفع كامل", use_container_width=True): st.session_state.payment = "دفع كامل"
        if c2.button("عند الاستلام", use_container_width=True): st.session_state.payment = "عند الاستلام"
        if c3.button("عربون 20%", use_container_width=True): st.session_state.payment = "عربون 20%"
        
        st.info(f"طريقة الدفع المختارة: **{st.session_state.payment}**")
        
        if st.button("تأكيد الطلب النهائي", use_container_width=True, type="primary"):
            st.session_state.page = "delivery"
            st.rerun()

# ============ DELIVERY ============
elif st.session_state.page == "delivery":
    prod = st.session_state.selected
    st.title("🎉 تم الطلب بنجاح")
    st.balloons()
    
    with st.container(border=True):
        st.markdown(f"### {prod['name']}")
        st.markdown(f"**رقم الطلب:** `MR-{int(time.time())}`")
        
        if prod['category'] == "بطاقة رقمية":
            st.divider()
            st.markdown("<div class='code-box'>XXXX-XXXX-XXXX-YYYY</div>", unsafe_allow_html=True)
            st.caption("⚠️ رمز تجريبي (Demo).")
        else:
            st.info("📦 سيتواصل معك فريق الميدان لتوصيل الطلب.")
        
        if st.button("العودة للرئيسية", use_container_width=True):
            st.session_state.clear()
            st.rerun()
