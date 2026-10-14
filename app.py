import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import urllib.parse

st.set_page_config(page_title="AUREI KALOS - Luxury AI Fashion Atelier", layout="centered", page_icon="✨")

st.markdown("""
<style>
.stApp { background-color: #0e1117; }
h1 { color: gold; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.title("✨ AUREI KALOS")
st.markdown("<h3 style='text-align:center; color:#aaa;'>Luxury AI Fashion Atelier</h3>", unsafe_allow_html=True)

prompt = st.text_area("Enter your design prompt", placeholder="Elegant golden evening gown, African luxury, flowing silk, runway...")
style = st.selectbox("Style", ["Luxury Gold", "Afro Futurism", "Haute Couture", "Bridal Elegance", "Street Luxury"])

ref = st.file_uploader("Upload reference (optional)", type=["jpg","png","jpeg"])

if st.button("GENERATE AUREI DESIGN", use_container_width=True):
    if not prompt:
        st.warning("Boss, enter a design first!")
    else:
        full_prompt = f"{prompt}, {style} style, luxury fashion photography, ultra detailed, 8k, haute couture, African luxury model"
        encoded = urllib.parse.quote(full_prompt)
        
        # FREE AI GENERATOR - NO KEY NEEDED
        image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true&enhance=true"
        
        with st.spinner("Aurei Atelier is designing your luxury piece... ✨"):
            try:
                response = requests.get(image_url, timeout=30)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    st.image(img, caption=f"AUREI KALOS: {prompt}", use_column_width=True)
                    st.success("Design Generated! Save it boss!")
                    
                    # Download button
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button("📥 DOWNLOAD LUXURY DESIGN", buf.getvalue(), file_name="aurei_kalos_design.png", mime="image/png", use_container_width=True)
                else:
                    st.error(f"Atelier busy, retry! Code {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}. Try again boss!")

st.markdown("---")
st.caption("LIVE on FREE Streamlit • AUREI KALOS Luxury Atelier • Made in Lagos 🇳🇬")
