import streamlit as st
import pandas as pd
import os
import json
import time
from datetime import datetime
from PIL import Image, ImageDraw

# ==========================================
# 1. إعدادات الصفحة والتصميم
# ==========================================
st.set_page_config(page_title="مرصد - سوق النخبة", page_icon="👑", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; }
    .stApp { background-color: #0e1117; background-image: radial-gradient(circle at 15% 50%, rgba(0, 255, 255, 0.08), transparent 25%), radial-gradient(circle at 85% 30%, rgba(255, 0, 255, 0.08), transparent 25%); }
    .neon-text { color: #fff; text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff, 0 0 20px #00ffff; text-align: center; font-weight: bold; margin-bottom: 20px; }
    [data-testid="stVerticalBlockBorderWrapper"] { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(10px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 15px !important; padding: 15px !important; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important; transition: transform 0.3s ease !important; }
    [data-testid="stVerticalBlockBorderWrapper"]:hover { transform: translateY(-5px) !important; border: 1px solid rgba(0, 255, 255, 0.3) !important; }
    .product-title { color: #ffd700; font-size: 1.2rem; font-weight: bold; margin-top: 10px; }
    .product-price { color: #00ffff; font-size: 1.1rem; font-weight: bold; }
    .product-category { color: #a0a0a0; font-size: 0.9rem; }
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(90deg, #00ffff, #ff00ff); color: white; font-weight: bold; border: none; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='neon-text'>👑 سوق النخبة - مرصد بريميوم</h1>", unsafe_allow_html=True)

# ==========================================
# 2. المسارات ودوال مساعدة
# ==========================================
CSV_PATH = "Marsad_Final_Categorized.csv"
IMAGES_DIR = "Marsad_Images"
ORDERS_FILE = "marsad_orders.json"

@st.cache_data
def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df.rename(columns={'اسم_الصورة': 'image_filename', 'اسم_المنتج': 'product_name', 'السعر': 'price', 'القسم': 'category'}, inplace=True)
        return df
    return pd.DataFrame()

df_market = load_data()

@st.cache_data
def add_watermark(img_path):
    try:
        img = Image.open(img_path).convert("RGBA")
        txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        d.text((20, 20), "MARSAD PREMIUM", fill=(212, 175, 55, 180))
        return Image.alpha_composite(img, txt).convert("RGB")
    except:
        return None

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)

# ==========================================
# 3. الشريط الجانبي (الصلاحيات والتتبع)
# ==========================================
with st.sidebar:
    st.header("لوحة التحكم ⚙️")
    user_role = "تاجر"
    auth_code = st.text_input("كود الدخول (للمشرفين فقط):", type="password")
    
    # 👇 تمت إضافة رقم اليمني هنا (الفريق صار 3 مشرفين)
    if auth_code == "1990":
        user_role = "المدير 👑"
        st.success(f"مرحباً بك يا {user_role}")
    elif auth_code in ["0511344046", "0582239230"]:
        user_role = "المشرف 🛡️"
        st.success(f"مرحباً بك يا {user_role}")
    elif auth_code != "":
        st.error("كود الدخول غير صحيح! ❌")

    st.markdown("---")
    
    # قسم التتبع للتاجر
    if user_role == "تاجر":
        st.subheader("📍 تتبع طلبك")
        track_phone = st.text_input("أدخل رقم جوالك لمتابعة الطلب:")
        if track_phone:
            orders = load_orders()
            user_orders = [o for o in orders if o.get("phone") == track_phone]
            if user_orders:
                latest_order = user_orders[-1]
                status = latest_order.get("status", "تم الاستلام")
                st.info(f"**الطلب:** {latest_order['product_name']}\n\n**الحالة:** {status}")
                
                progress_map = {"تم الاستلام": 25, "قيد التجهيز": 50, "في الطريق": 75, "تم التسليم": 100}
                st.progress(progress_map.get(status, 25) / 100)
                
                st.write("🗺️ **مسار التوصيل:**")
                map_data = pd.DataFrame({'lat': [24.7136, 24.7200], 'lon': [46.6753, 46.6800]})
                st.map(map_data, zoom=13)
            else:
                st.warning("لا توجد طلبات مسجلة برقم الجوال هذا.")

# ==========================================
# 4. عرض المنتجات (للتاجر فقط)
# ==========================================
if user_role == "تاجر":
    if not df_market.empty:
        cols = st.columns(3)
        for index, row in df_market.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    img_name = row.get('image_filename', '')
                    img_path = os.path.join(IMAGES_DIR, str(img_name))
                    
                    if os.path.exists(img_path):
                        wm_img = add_watermark(img_path)
                        if wm_img: st.image(wm_img, use_container_width=True)
                        else: st.image(img_path, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x200?text=No+Image", use_container_width=True)

                    st.markdown(f"<div class='product-title'>{row.get('product_name', 'منتج')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='product-price'>السعر: {row.get('price', '0')} ر.س</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='product-category'>القسم: {row.get('category', 'عام')}</div>", unsafe_allow_html=True)

                    with st.expander("🛒 اطلب الآن"):
                        order_phone = st.text_input("رقم جوالك (للتتبع):", key=f"phone_{index}")
                        if st.button(f"تأكيد الطلب", key=f"order_{index}"):
                            if order_phone:
                                new_order = {
                                    "product_name": row.get('product_name', 'منتج'),
                                    "price": row.get('price', '0'),
                                    "phone": order_phone,
                                    "status": "تم الاستلام",
                                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                }
                                orders = load_orders()
                                orders.append(new_order)
                                save_orders(orders)
                                st.success("✅ تم إرسال الطلب! تتبع طلبك من الشريط الجانبي.")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("⚠️ يرجى إدخال رقم الجوال أولاً.")

# ==========================================
# 5. لوحة تحكم المشرف / المدير (لإدارة الطلبات)
# ==========================================
if user_role in ["المشرف 🛡️", "المدير 👑"]:
    st.markdown("---")
    st.subheader(f"⚡ إدارة الطلبات الميدانية - {user_role}")
    orders = load_orders()
    
    if orders:
        for i, order in enumerate(orders):
            with st.expander(f"طلب: {order['product_name']} | الجوال: {order['phone']} | الحالة: {order['status']}"):
                st.write(f"**السعر:** {order['price']} ر.س")
                st.write(f"**التاريخ:** {order['date']}")
                
                col1, col2, col3 = st.columns(3)
                if col1.button("قيد التجهيز", key=f"proc_{i}"):
                    orders[i]["status"] = "قيد التجهيز"
                    save_orders(orders)
                    st.rerun()
                if col2.button("في الطريق", key=f"way_{i}"):
                    orders[i]["status"] = "في الطريق"
                    save_orders(orders)
                    st.rerun()
                if col3.button("تم التسليم", key=f"done_{i}"):
                    orders[i]["status"] = "تم التسليم"
                    save_orders(orders)
                    st.rerun()
    else:
        st.info("لا توجد طلبات حالياً.")
