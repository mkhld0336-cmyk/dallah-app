import streamlit as st
import time

# ==========================================
# 1. إعدادات الصفحة والتصميم (Light Mode)
# ==========================================
st.set_page_config(page_title="مرصد | Marsad", page_icon="🦅", layout="wide")

# تصميم CSS نظيف واحترافي (يحاكي الصور)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Cairo', sans-serif; 
        direction: rtl; 
        text-align: right;
    }
    .stApp { 
        background-color: #F8FAFC; 
        color: #0F172A;
    }
    
    /* تصميم البطاقات */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        border-color: #3B82F6 !important;
    }
    
    /* العناوين */
    h1, h2, h3 { color: #1E293B !important; font-weight: 800 !important; }
    
    /* الأزرار */
    .stButton>button { 
        background-color: #3B82F6 !important; 
        color: white !important; 
        font-weight: bold !important; 
        border-radius: 8px !important; 
        border: none !important;
        padding: 10px 24px !important;
        transition: 0.2s !important;
    }
    .stButton>button:hover {
        background-color: #2563EB !important;
    }
    
    /* تنسيق أزرار الكمية */
    .qty-btn {
        background-color: #F1F5F9;
        color: #1E293B;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
    }
    
    /* الفاتورة */
    .invoice-box {
        background-color: #F1F5F9;
        padding: 20px;
        border-radius: 10px;
        border-right: 4px solid #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. إدارة الحالة (Session State)
# ==========================================
if "stage" not in st.session_state:
    st.session_state.stage = "categories"
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "quantity" not in st.session_state:
    st.session_state.quantity = 1
if "phone" not in st.session_state:
    st.session_state.phone = ""
if "payment_method" not in st.session_state:
    st.session_state.payment_method = "full"

# بيانات تجريبية للمنتجات (سنستبدلها ببياناتك قريباً)
PRODUCTS = {
    "cafe": [
        {"id": 1, "name": "أكواب قهوة ورقية", "desc": "عبوة توريد - 1 كرتون", "min": 1, "price": 145.00, "img": "https://images.unsplash.com/photo-1611162458324-aae1eb4129a4?auto=format&fit=crop&w=400&q=80"},
        {"id": 2, "name": "حليب مبخر (أبوقوس)", "desc": "عبوة توريد - 24 حبة", "min": 1, "price": 180.00, "img": "https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=400&q=80"}
    ],
    "restaurant": [
        {"id": 3, "name": "زيت قلي نخيل", "desc": "عبوة توريد - 18 لتر", "min": 1, "price": 112.50, "img": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=400&q=80"},
        {"id": 4, "name": "أرز بسمتي الشفاء", "desc": "عبوة توريد - 4.5 كجم", "min": 1, "price": 25.99, "img": "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=400&q=80"}
    ],
    "grocery": [
        {"id": 5, "name": "مياه نوفا", "desc": "كرتون 40x330 مل", "min": 1, "price": 14.99, "img": "https://images.unsplash.com/photo-1523362628745-0c100150b504?auto=format&fit=crop&w=400&q=80"},
        {"id": 6, "name": "بيض فقيه", "desc": "طبق 30 حبة", "min": 1, "price": 13.99, "img": "https://images.unsplash.com/photo-1506976785307-8732e854ad03?auto=format&fit=crop&w=400&q=80"}
    ]
}

# ==========================================
# 3. بناء الطبقات (UI)
# ==========================================

# --- الطبقة الأولى: الأقسام ---
if st.session_state.stage == "categories":
    st.title("🦅 منصة مرصد")
    st.write("اختر قطاعك للبدء في تسوق احتياجاتك بالجملة.")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>☕</h2>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>المقاهي</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>أكواب ومستلزمات</p>", unsafe_allow_html=True)
            if st.button("تصفح المقاهي", key="cat_cafe", use_container_width=True):
                st.session_state.stage = "products"
                st.session_state.category = "cafe"
                st.rerun()
    with col2:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🍽️</h2>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>المطاعم</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>مواد تشغيل</p>", unsafe_allow_html=True)
            if st.button("تصفح المطاعم", key="cat_rest", use_container_width=True):
                st.session_state.stage = "products"
                st.session_state.category = "restaurant"
                st.rerun()
    with col3:
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center;'>🛒</h2>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>البقالات</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray;'>احتياجات يومية</p>", unsafe_allow_html=True)
            if st.button("تصفح البقالات", key="cat_groc", use_container_width=True):
                st.session_state.stage = "products"
                st.session_state.category = "grocery"
                st.rerun()

# --- الطبقة الثانية: المنتجات ---
elif st.session_state.stage == "products":
    if st.button("🔙 العودة للأقسام"):
        st.session_state.stage = "categories"
        st.rerun()
        
    st.title("المنتجات المتاحة")
    st.divider()
    
    cat = st.session_state.category
    cols = st.columns(3)
    for idx, prod in enumerate(PRODUCTS[cat]):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(prod["img"], use_container_width=True)
                st.markdown(f"### {prod['name']}")
                st.markdown(f"<p style='color: gray; font-size: 0.9em;'>{prod['desc']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 0.9em;'>الحد الأدنى: {prod['min']} كرتون</p>", unsafe_allow_html=True)
                
                # أزرار الكمية
                q_col1, q_col2, q_col3 = st.columns([1, 2, 1])
                with q_col1:
                    if st.button("−", key=f"minus_{prod['id']}"):
                        if st.session_state.quantity > prod['min']:
                            st.session_state.quantity -= 1
                            st.rerun()
                with q_col2:
                    st.markdown(f"<h4 style='text-align: center; margin: 0;'>{st.session_state.quantity}</h4>", unsafe_allow_html=True)
                with q_col3:
                    if st.button("+", key=f"plus_{prod['id']}"):
                        st.session_state.quantity += 1
                        st.rerun()
                
                if st.button("اطلب الآن", key=f"order_{prod['id']}", use_container_width=True, type="primary"):
                    st.session_state.selected_product = prod
                    st.session_state.stage = "otp"
                    st.rerun()
                
                st.caption("اعرف تفاصيل طلبك بعد التحقق")

# --- الطبقة الثالثة: التحقق OTP ---
elif st.session_state.stage == "otp":
    if st.button("🔙 العودة للمنتجات"):
        st.session_state.stage = "products"
        st.rerun()
        
    st.title("التحقق من الحساب")
    st.write("أدخل رقم جوالك لإظهار تفاصيل الطلب ومتابعة الشراء.")
    st.divider()
    
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center;'>📱</h3>", unsafe_allow_html=True)
        phone = st.text_input("رقم الجوال السعودي", placeholder="05X XXX XXXX")
        
        if st.button("إرسال رمز التحقق", use_container_width=True, type="primary"):
            if len(phone) >= 10:
                st.session_state.phone = phone
                st.session_state.stage = "otp_verify"
                st.rerun()
            else:
                st.error("أدخل رقم جوال صحيح")
                
    st.caption("تحقق آمن وواضح. يُستخدم رقمك للتحقق من الحساب ومتابعة الطلب.")

# --- الطبقة الثالثة (ب): إدخال رمز التحقق ---
elif st.session_state.stage == "otp_verify":
    st.title("رمز التحقق")
    st.write(f"تم إرسال الرمز إلى {st.session_state.phone}")
    
    with st.container(border=True):
        otp = st.text_input("أدخل رمز التحقق (للتجربة: 1234)", type="password")
        if st.button("تأكيد الرمز", use_container_width=True, type="primary"):
            if otp == "1234":
                st.session_state.stage = "invoice"
                st.rerun()
            else:
                st.error("رمز غير صحيح. جرب 1234")

# --- الطبقة الرابعة: الفاتورة والدفع ---
elif st.session_state.stage == "invoice":
    prod = st.session_state.selected_product
    qty = st.session_state.quantity
    subtotal = prod['price'] * qty
    vat = subtotal * 0.15
    total = subtotal + vat
    
    st.title("ملخص الطلب")
    st.success("✅ تم التحقق من الحساب")
    st.divider()
    
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(prod["img"], use_container_width=True)
        with col2:
            st.markdown(f"### {prod['name']}")
            st.markdown(f"**الكمية:** {qty} كرتون")
            st.markdown(f"**سعر الوحدة:** `{prod['price']:.2f} ر.س`")
            
        st.divider()
        
        st.markdown(f"**الإجمالي قبل الضريبة:** {subtotal:.2f} ر.س")
        st.markdown(f"**ضريبة القيمة المضافة (15%):** {vat:.2f} ر.س")
        st.markdown(f"**التوصيل:** حسب الوجهة")
        st.markdown(f"<h3 style='color: #3B82F6;'>الإجمالي النهائي: {total:.2f} ر.س</h3>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("اختر طريقة الدفع")
        
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            if st.button("دفع كامل", use_container_width=True, type="primary" if st.session_state.payment_method == "full" else "secondary"):
                st.session_state.payment_method = "full"
                st.rerun()
        with col_p2:
            if st.button("عند الاستلام", use_container_width=True, type="primary" if st.session_state.payment_method == "cod" else "secondary"):
                st.session_state.payment_method = "cod"
                st.rerun()
        with col_p3:
            if st.button("عربون 20%", use_container_width=True, type="primary" if st.session_state.payment_method == "deposit" else "secondary"):
                st.session_state.payment_method = "deposit"
                st.rerun()
                
        st.divider()
        
        # عرض تفاصيل الدفع المختار
        if st.session_state.payment_method == "full":
            st.info(f"سيتم سداد كامل المبلغ: **{total:.2f} ر.س**")
        elif st.session_state.payment_method == "cod":
            st.info(f"سيتم الدفع عند الاستلام: **{total:.2f} ر.س**")
        elif st.session_state.payment_method == "deposit":
            deposit = total * 0.20
            remaining = total - deposit
            st.info(f"العربون المطلوب الآن: **{deposit:.2f} ر.س**\n\nالمبلغ المتبقي: **{remaining:.2f} ر.س**")

        if st.button("تأكيد الطلب النهائي", use_container_width=True, type="primary"):
            st.balloons()
            st.success("🎉 تم استلام طلبك بنجاح! سيتواصل معك فريق مرصد قريباً.")
            if st.button("العودة للرئيسية"):
                st.session_state.clear()
                st.rerun()
