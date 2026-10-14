import streamlit as st
from PIL import Image

st.set_page_config(page_title="AUREI KALOS", page_icon="✨", layout="centered")

st.markdown("<h1 style='text-align:center;color:#d4af37'>✨ AUREI KALOS ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Luxury AI Fashion Atelier</p>", unsafe_allow_html=True)

prompt = st.text_area("Enter your design prompt", placeholder="Elegant golden evening gown, African luxury...")
style = st.selectbox("Style", ["Luxury Gold", "Royal Silk", "Afro Couture", "Minimal Chic", "Bridal Divine"])
uploaded = st.file_uploader("Upload reference (optional)", type=["jpg","png","jpeg"])

if st.button("GENERATE AUREI DESIGN"):
    if not prompt:
        st.warning("Boss, enter prompt first!")
    else:
        st.success(f"Prompt: {prompt} | Style: {style}")
        if uploaded:
            st.image(Image.open(uploaded), use_container_width=True)
        st.info("LIVE on FREE Streamlit! Never Paused like Hugging Face. Ready for AI model.")
