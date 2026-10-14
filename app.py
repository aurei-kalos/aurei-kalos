import streamlit as st
import requests
import urllib.parse
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AUREI KALOS PRO", page_icon="✨")
st.title("✨ AUREI KALOS - PRO")
st.caption("HD Face, No Watermark")

prompt = st.text_area("Prompt", "Elegant golden evening gown, African luxury supermodel, clear face, runway")

if st.button("GENERATE HD DESIGN", use_container_width=True):
    if not prompt:
        st.warning("Enter prompt boss!")
    else:
        enhanced = f"{prompt}, clear face, sharp focus face, beautiful symmetrical face, detailed eyes, flawless skin, high detail, 8k, ultra sharp, professional fashion photography"
        encoded = urllib.parse.quote(enhanced)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1280&model=flux&enhance=true&nologo=true&seed=12345"
        
        with st.spinner("Creating HD..."):
            try:
                resp = requests.get(url, timeout=60)
                img = Image.open(BytesIO(resp.content)).convert("RGB")
                # Remove watermark area
                w, h = img.size
                img = img.crop((0, 0, w, h-40))
                st.image(img, use_column_width=True)
                buf = BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 DOWNLOAD HD (No Watermark)", buf.getvalue(), "aurei_hd.png", "image/png", use_container_width=True)
                st.success("HD Clear Face! No Watermark!")
            except Exception as e:
                st.error(f"Error: {e}")
