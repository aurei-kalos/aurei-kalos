import streamlit as st
import requests
import urllib.parse
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AUREI KALOS", page_icon="✨")
st.title("✨ AUREI KALOS")
st.caption("Full Body Gown + Clear Face - No Watermark")

prompt = st.text_area("WRITE YOUR PROMPT", placeholder="Full body African queen, golden mermaid gown, luxury...")
style = st.selectbox("Style", ["Luxury Gold", "Haute Couture", "Bridal", "Royal"])
mode = st.selectbox("Type", ["FULL BODY + CLEAR FACE", "CLOSE-UP FACE (Ultra Clear)"])

ref = st.file_uploader("Upload Reference", type=["jpg","jpeg","png"])
if ref:
    st.image(Image.open(ref), width=250)

if st.button("GENERATE", type="primary", use_container_width=True):
    if not prompt:
        st.warning("Write prompt!")
    else:
        if mode == "FULL BODY + CLEAR FACE":
            full = f"{prompt}, {style}, full body portrait, full length gown, beautiful clear face, ultra detailed face, sharp focus on face, symmetrical face, detailed eyes, flawless skin, face in focus, luxury fashion photography, 8k, ultra detailed face and dress"
        else:
            full = f"{prompt}, {style}, close-up portrait, beautiful clear face, ultra detailed face, sharp focus, symmetrical face, detailed eyes, flawless skin, 8k"
            
        enc = urllib.parse.quote(full)
        url = f"https://image.pollinations.ai/prompt/{enc}?width=1024&height=1536&model=flux&enhance=true&nologo=true&private=true"
        
        with st.spinner("Generating luxury with clear face..."):
            r = requests.get(url, timeout=90)
            img = Image.open(BytesIO(r.content)).convert("RGB")
            w,h = img.size
            img = img.crop((0,0,w,h-50))
            st.image(img, use_column_width=True)
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.download_button("DOWNLOAD HD - No Watermark", buf.getvalue(), "aurei_clear_face.png", "image/png", use_container_width=True)
            st.success("Done! Full body + Clear Face!")
