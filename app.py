import streamlit as st
import pandas as pd
from pathlib import Path
import html
import re

# =========================================================
# إعداد التطبيق
# =========================================================

st.set_page_config(
    page_title="مرصد | مشتريات أعمالك",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "Marsad_Valid_Products.csv"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded');

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
    font-family: 'Cairo', sans-serif !important;
    direction: rtl;
}
.stApp { background: #F8FAFC; color: #172033; }
header[data-testid="stHeader"] { background: #F8FAFC; }
.block-container { max-width: 1180px; padding-top: 1.5rem; padding-bottom: 3rem; }
h1, h2, h3, p, label, span, div { font-family: 'Cairo', sans-serif; }

.marsad-header {
    display: flex; align-items: center; justify-content: space-between;
    background: #FFFFFF; border: 1px solid #E8EDF2;
    border-radius: 18px; padding: 15px 22px; margin-bottom: 24px;
}
.brand { color: #123B2D; font-size: 27px; font-weight: 900; }
.brand-sub { color: #7B8794; font-size: 12px; }
.header-tag { background: #EAF3EE; color: #17563D; padding: 7px 13px; border-radius: 30px; font-size: 12px; font-weight: 700; }

.hero { background: linear-gradient(120deg, #123B2D, #1D5A42); color: white; padding: 35px; border-radius: 22px; margin-bottom: 25px; }
.hero h1 { font-size: 30px; font-weight: 900; margin: 0 0 8px 0; }
.hero p { color: #D6E6DD; margin: 0; font-size: 14px; }

.section-title { font-size: 21px; font-weight: 900; color: #172033; margin: 20px 0 15px 0; }

.category-card { background: white; border: 1px solid #E5EBEF; border-radius: 18px; padding: 23px 17px; min-height: 145px; text-align: center; }
.category-icon { font-family: 'Material Symbols Rounded'; font-size: 35px; color: #1B6045; margin-bottom: 8px; }
.category-name { color: #172033; font-size: 17px; font-weight: 900; }
.category-desc { color: #87919B; font-size: 12px; margin-top: 5px; }

/* تعديلات الكارت عشان تطلع بشكل صحيح */
div[data-testid="stVerticalBlockBorderWrapper"] { background: #FFFFFF !important; border-radius: 16px !important; border: 1px solid #E7ECF0 !important; padding: 15px !important; transition: all 0.3s; }
div[data-testid="stVerticalBlockBorderWrapper"]:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.05); transform: translateY(-3px); }

.product-name { font-size: 14px; font-weight: 800; color: #172033; line-height: 1.8; min-height: 48px; }
.product-note { color: #8A949E; font-size: 11px; min-height: 22px; }
.product-hidden-price { background: #F3F6F4; color: #557363; border-radius: 8px; padding: 7px; font-size: 11px; text-align: center; margin: 8px 0; }

.digital-banner { background: linear-gradient(120deg, #172B28, #263E35); border-radius: 20px; padding: 25px; color: #FFFFFF; margin-bottom: 20px; }
.digital-banner h2 { color: #E7C77B; font-weight: 900; }
.digital-banner p { color: #D4DED8; font-size: 13px; }

.info-card { background: #FFFFFF; border: 1px solid #E7ECF0; border-radius: 16px; padding: 20px; margin-bottom: 15px; }
.step-label { color: #1D6548; font-size: 12px; font-weight: 800; margin-bottom: 8px; }
.invoice-total { background: #123B2D; color: #FFFFFF; border-radius: 15px; padding: 20px; margin: 15px 0; }
.invoice-total small { color: #D6E6DD; }
.invoice-total strong { font-size: 27px; font-weight: 900; }
.receipt-code { background: #F2F5F2; border: 1px dashed #6C927B; border-radius: 13px; padding: 20px; text-align: center; color: #174B35; font-size: 22px; font-weight: 900; letter-spacing: 2px; direction: ltr; }

.saving-badge { display: inline-block; background: #E5F4E9; color: #17633B; padding: 6px 12px; border-radius: 20px; font-size: 13px; font-weight: 900; margin: 8px 0; }
.old-price { color: #8A949E; text-decoration: line-through; font-size: 14px; }
.muted { color: #89939D; font-size: 12px; }

div.stButton > button { background: #174B35; color: #FFFFFF; border: 0; border-radius: 11px; min-height: 43px; font-family: 'Cairo', sans-serif; font-weight: 800; width: 100%; }
div.stButton > button:hover { background: #236448; color: white; border: 0; }
div[data-testid="stTextInput"] input { border-radius: 10px; text-align: right; font-family: 'Cairo', sans-serif; }
div[data-testid="stNumberInput"] input { text-align: center; }
hr { border-color: #E8EDF0; }
[data-testid="stRadio"] label { font-weight: 700; }

@media (max-width: 700px) {
    .block-container { padding: 1rem 0.8rem 2rem 0.8rem; }
    .hero { padding: 24px 18px; }
    .hero h1 { font-size: 23px; }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# قراءة CSV بالأعمدة العربية
# =========================================================

@st.cache_data
def load_products():
    if not CSV_FILE.exists():
        return pd.DataFrame()

    df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")

    required_columns = ["اسم المنتج", "السعر", "القطاع", "ملاحظات", "الصورة"]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError("الأعمدة التالية غير موجودة في الملف: " + "، ".join(missing))

    df["اسم المنتج"] = df["اسم المنتج"].fillna("").astype(str).str.strip()
    df["القطاع"] = df["القطاع"].fillna("").astype(str).str.strip()
    df["ملاحظات"] = df["ملاحظات"].fillna("").astype(str).str.strip()
    df["الصورة"] = df["الصورة"].fillna("").astype(str).str.strip()

    df["السعر"] = pd.to_numeric(df["السعر"].astype(str).str.replace(",", ".", regex=False), errors="coerce").fillna(0)

    # استخراج السعر السابق من الملاحظات
    old_price_pattern = re.compile(
        r"(?:السعر\s*(?:السابق|قبل\s*العرض|الأصلي|قبل\s*الخصم))\s*[:：\-]?\s*([0-9]+(?:[.,][0-9]{1,2})?)",
        flags=re.IGNORECASE
    )

    def extract_old_price(notes):
        match = old_price_pattern.search(str(notes))
        if not match: return None
        try: return float(match.group(1).replace(",", "."))
        except (ValueError, AttributeError): return None

    df["السعر القديم"] = df["ملاحظات"].apply(extract_old_price)

    def normalize_category(value):
        value = str(value).strip().lower()
        if "بقال" in value or "grocery" in value: return "بقالة"
        if "رقمي" in value or "بطاق" in value or "digital" in value: return "بطاقة رقمية"
        return "أخرى"

    df["القسم"] = df["القطاع"].apply(normalize_category)

    df = df[(df["اسم المنتج"] != "") & (df["السعر"] > 0)].copy()
    return df.reset_index(drop=True)


try:
    products = load_products()
    data_error = None
except Exception as exc:
    products = pd.DataFrame()
    data_error = str(exc)


# =========================================================
# حالة التطبيق والتنقل
# =========================================================

DEFAULTS = {
    "screen": "home", "category": "بقالة", "selected_product": None,
    "quantity": 1, "phone": "", "otp_sent": False, "otp_verified": False,
    "payment_method": "دفع كامل", "order_confirmed": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

def go(screen):
    st.session_state.screen = screen
    st.rerun()

def reset_order():
    st.session_state.selected_product = None
    st.session_state.quantity = 1
    st.session_state.otp_sent = False
    st.session_state.otp_verified = False
    st.session_state.order_confirmed = False
    st.session_state.payment_method = "دفع كامل"

def money(value):
    return f"{value:,.2f} ر.س"

def safe_image_path(filename):
    if not filename: return None
    filename = str(filename).strip()
    if not filename: return None
    candidate = Path(filename)
    possible_paths = [
        BASE_DIR / candidate,
        BASE_DIR / "images" / candidate.name,
        BASE_DIR / "assets" / candidate.name,
        BASE_DIR / "assets" / "images" / candidate.name,
    ]
    for path in possible_paths:
        try:
            resolved = path.resolve()
            if resolved.is_relative_to(BASE_DIR.resolve()) and resolved.is_file():
                return resolved
        except (OSError, ValueError):
            continue
    return None

def get_selected_product():
    index = st.session_state.selected_product
    if index is None: return None
    if index < 0 or index >= len(products): return None
    return products.iloc[index]


# =========================================================
# رأس التطبيق ومعالجة الأخطاء
# =========================================================

st.markdown("""
<div class="marsad-header">
    <div>
        <div class="brand">مرصد</div>
        <div class="brand-sub">منصة مشتريات الأعمال</div>
    </div>
    <div class="header-tag">مشتريات أعمالك بوضوح أكبر</div>
</div>
""", unsafe_allow_html=True)

if data_error:
    st.error(f"تعذر قراءة ملف المنتجات: {data_error}")
    st.stop()

if products.empty:
    st.error("لم يتم العثور على منتجات صالحة. تأكد من وجود Marsad_Valid_Products.csv بجانب app.py وأن عمود السعر يحتوي على أسعار صحيحة.")
    st.stop()


# =========================================================
# الصفحة الرئيسية
# =========================================================

if st.session_state.screen == "home":
    st.markdown("""
    <div class="hero">
        <h1>مشتريات أعمالك، بوضوح أكبر</h1>
        <p>اختر القسم، حدّد احتياجك، واعرف تفاصيل طلبك بعد التحقق.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">تصفح الأقسام</div>', unsafe_allow_html=True)

    categories = [
        {"name": "بقالة", "icon": "local_grocery_store", "desc": "منتجات واحتياجات المتاجر"},
        {"name": "بطاقة رقمية", "icon": "card_giftcard", "desc": "بطاقات رقمية وشحن"},
        {"name": "أخرى", "icon": "inventory_2", "desc": "منتجات وخيارات إضافية"},
    ]

    cols = st.columns(3)
    for col, item in zip(cols, categories):
        count = int((products["القسم"] == item["name"]).sum())
        with col:
            st.markdown(f"""
            <div class="category-card">
                <div class="category-icon">{item['icon']}</div>
                <div class="category-name">{item['name']}</div>
                <div class="category-desc">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"{count} منتج")
            if st.button("استعراض القسم", key=f"cat_{item['name']}"):
                st.session_state.category = item["name"]
                go("products")

    st.markdown("---")
    st.markdown('<p class="muted">مرصد — مشتريات الأعمال بطريقة أوضح.</p>', unsafe_allow_html=True)


# =========================================================
# صفحة المنتجات
# =========================================================

elif st.session_state.screen == "products":
    category = st.session_state.category

    if st.button("← العودة للرئيسية", key="back_home"):
        go("home")

    st.markdown(f'<div class="section-title">{html.escape(category)}</div>', unsafe_allow_html=True)

    if category == "بطاقة رقمية":
        st.markdown("""
        <div class="digital-banner">
            <h2>البطاقات الرقمية</h2>
            <p>اختر البطاقة المناسبة. تظهر تفاصيل الطلب بعد التحقق.</p>
        </div>
        """, unsafe_allow_html=True)

    category_products = products[products["القسم"] == category].copy()
    st.caption(f"عدد المنتجات: {len(category_products)}")

    search = st.text_input("ابحث عن منتج", placeholder="اكتب اسم المنتج...")
    if search.strip():
        category_products = category_products[
            category_products["اسم المنتج"].str.contains(re.escape(search.strip()), case=False, na=False)
        ]

    if category_products.empty:
        st.info("لا توجد منتجات مطابقة للبحث.")
    else:
        for start in range(0, len(category_products), 3):
            row = category_products.iloc[start:start + 3]
            cols = st.columns(3)

            for col, (original_index, product) in zip(cols, row.iterrows()):
                with col:
                    # 🔥 استخدمنا st.container بدلاً من div عشان الشكل يطلع مظبوط
                    with st.container(border=True):
                        image_path = safe_image_path(product["الصورة"])
                        if image_path:
                            st.image(str(image_path), use_container_width=True)
                        else:
                            st.markdown("""
                            <div style="height:130px; background:#F1F4F2; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#799084; font-size:42px;">▧</div>
                            """, unsafe_allow_html=True)

                        st.markdown(f'<div class="product-name">{html.escape(product["اسم المنتج"])}</div>', unsafe_allow_html=True)
                        st.markdown('<div class="product-note">متاح للطلب</div>', unsafe_allow_html=True)
                        st.markdown('<div class="product-hidden-price">اعرف تفاصيل طلبك بعد التحقق</div>', unsafe_allow_html=True)

                        if st.button("اطلب الآن", key=f"order_{original_index}"):
                            st.session_state.selected_product = int(original_index)
                            st.session_state.quantity = 1
                            st.session_state.otp_sent = False
                            st.session_state.otp_verified = False
                            st.session_state.order_confirmed = False
                            go("verify")


# =========================================================
# التحقق من رقم الجوال ورمز OTP
# =========================================================

elif st.session_state.screen == "verify":
    product = get_selected_product()

    if product is None:
        st.warning("لم يتم اختيار منتج.")
        if st.button("العودة للرئيسية"): go("home")
    else:
        if st.button("← العودة للمنتجات"): go("products")

        st.markdown("""
        <div class="section-title">تحقق للمتابعة</div>
        <div class="info-card">
            <div class="step-label">خطوة التحقق</div>
            <h3>تحقق من رقم جوالك</h3>
            <p class="muted">أدخل رقم الجوال للانتقال إلى تفاصيل طلبك.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**المنتج المختار:** {html.escape(product['اسم المنتج'])}")

        st.session_state.phone = st.text_input("رقم الجوال", value=st.session_state.phone, placeholder="+9665XXXXXXXX", help="أدخل رقم الجوال بصيغة +966")

        if not st.session_state.otp_verified:
            if st.button("إرسال رمز التحقق"):
                phone = st.session_state.phone.strip()
                if not re.fullmatch(r"\+9665\d{8}", phone):
                    st.error("أدخل رقم جوال سعودي بصيغة +9665XXXXXXXX.")
                else:
                    st.session_state.otp_sent = True
                    st.success("رمز التحقق التجريبي هو 1234.")

            if st.session_state.otp_sent:
                otp = st.text_input("رمز التحقق", max_chars=4, placeholder="أدخل 1234")
                if st.button("تحقق والمتابعة"):
                    if otp.strip() == "1234":
                        st.session_state.otp_verified = True
                        go("invoice")
                    else:
                        st.error("رمز التحقق غير صحيح.")
        else:
            st.success("تم التحقق من رقم الجوال.")
            if st.button("متابعة إلى الفاتورة"): go("invoice")


# =========================================================
# الفاتورة
# =========================================================

elif st.session_state.screen == "invoice":
    product = get_selected_product()

    if product is None or not st.session_state.otp_verified:
        st.warning("يرجى إكمال اختيار المنتج والتحقق أولاً.")
        if st.button("العودة للرئيسية"): go("home")
    else:
        st.markdown("""
        <div class="section-title">ملخص الطلب</div>
        <div class="step-label">تم التحقق ✓</div>
        """, unsafe_allow_html=True)

        image_path = safe_image_path(product["الصورة"])
        col1, col2 = st.columns([1, 3])

        with col1:
            if image_path:
                st.image(str(image_path), use_container_width=True)
            else:
                st.markdown("📦")

        with col2:
            st.markdown(f"**{html.escape(product['اسم المنتج'])}**")
            st.markdown('<span class="muted">تفاصيل المنتج والكمية</span>', unsafe_allow_html=True)

        st.markdown("---")

        quantity = st.number_input("الكمية", min_value=1, max_value=999, value=int(st.session_state.quantity), step=1)
        st.session_state.quantity = int(quantity)

        unit_price = float(product["السعر"])
        old_unit_price = product["السعر القديم"]

        subtotal = unit_price * quantity
        tax = subtotal * 0.15
        total = subtotal + tax

        valid_old_price = (pd.notna(old_unit_price) and old_unit_price is not None and float(old_unit_price) > unit_price)

        st.markdown("### تفاصيل الفاتورة")

        if valid_old_price:
            old_unit_price = float(old_unit_price)
            old_subtotal = old_unit_price * quantity
            saving = old_subtotal - subtotal

            st.markdown(f'<div class="old-price">السعر السابق للوحدة: {money(old_unit_price)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="saving-badge">وفر {money(saving)}</div>', unsafe_allow_html=True)

        invoice_rows = [
            ("سعر الوحدة", money(unit_price)),
            ("الكمية", str(quantity)),
            ("الإجمالي", money(subtotal)),
            ("ضريبة القيمة المضافة 15%", money(tax)),
        ]

        for label, value in invoice_rows:
            left, right = st.columns([2, 1])
            left.write(label)
            right.markdown(f"<div style='text-align:left;font-weight:800'>{value}</div>", unsafe_allow_html=True)

        st.markdown('<div class="muted">التوصيل: يحدد عند تأكيد الطلب</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="invoice-total">
            <small>الإجمالي شامل ضريبة القيمة المضافة 15%</small><br>
            <strong>{money(total)}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### طريقة الدفع")
        payment_options = ["دفع كامل", "عند الاستلام", "عربون 20%"]
        payment_method = st.radio("اختر طريقة الدفع", payment_options, index=payment_options.index(st.session_state.payment_method))
        st.session_state.payment_method = payment_method

        if payment_method == "دفع كامل":
            amount_due = total
            payment_description = "المبلغ المطلوب حالياً"
        elif payment_method == "عربون 20%":
            amount_due = total * 0.20
            payment_description = "العربون المطلوب حالياً"
        else:
            amount_due = 0
            payment_description = "الدفع عند الاستلام"

        st.info(f"{payment_description}: {money(amount_due) if amount_due else 'لا يوجد مبلغ مقدم'}")
        st.caption("رسوم التوصيل غير محتسبة هنا، وتحدد عند تأكيد الطلب.")

        if st.button("تأكيد الطلب"):
            st.session_state.order_confirmed = True
            go("receipt")


# =========================================================
# شاشة الاستلام
# =========================================================

elif st.session_state.screen == "receipt":
    product = get_selected_product()

    if product is None or not st.session_state.order_confirmed:
        st.warning("لا يوجد طلب مؤكد.")
        if st.button("العودة للرئيسية"):
            reset_order()
            go("home")
    else:
        st.markdown("""
        <div class="hero">
            <h1>تم استلام طلبك</h1>
            <p>شكراً لاختيارك مرصد. نعمل على تجهيز طلبك.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### تفاصيل الطلب")
        st.markdown(f"**المنتج:** {html.escape(product['اسم المنتج'])}")
        st.markdown(f"**الكمية:** {st.session_state.quantity}")
        st.markdown(f"**طريقة الدفع:** {st.session_state.payment_method}")

        if product["القسم"] == "بطاقة رقمية":
            st.markdown("### رمز البطاقة التجريبي")
            st.markdown('<div class="receipt-code">XXXX-XXXX-XXXX-YYYY</div>', unsafe_allow_html=True)
            st.warning("هذا رمز تجريبي للعرض فقط، وليس بطاقة فعلية ولا يمكن استخدامه للشحن أو التفعيل.")
            st.markdown("""
            **تعليمات التفعيل التجريبية:**
            1. افتح التطبيق أو المتجر الخاص بالبطاقة.
            2. اختر استرداد أو تفعيل الرمز.
            3. أدخل الرمز بعد استلام البطاقة الفعلية.
            """)
        else:
            st.markdown("""
            <div class="info-card">
                <div class="step-label">حالة الطلب</div>
                <h3>قيد التجهيز</h3>
                <p class="muted">سيتم تجهيز المنتجات ومتابعة حالة الطلب.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("العودة للرئيسية"):
            reset_order()
            go("home")

st.markdown("""
<div style="text-align:center; color:#9AA4AD; font-size:11px; padding-top:25px;">
    مرصد © — مشتريات أعمالك، بوضوح أكبر
</div>
""", unsafe_allow_html=True)
