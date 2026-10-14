import streamlit as st
import requests
import urllib.parse
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AUREI KALOS", page_icon="✨")
st.title("✨ AUREI KALOS")
st.caption("HD - No Watermark - Clear Face")

prompt = st.text_area("WRITE YOUR PROMPT", placeholder="Golden gown, African queen, luxury, clear face...")
style = st.selectbox("Style", ["Luxury Gold", "Haute Couture", "Bridal", "Royal", "Afro Futurism"])
mode = st.selectbox("Type", ["IMAGE", "VIDEO"])

ref = st.file_uploader("Upload Reference (optional)", type=["jpg","jpeg","png"])
if ref:
    st.image(Image.open(ref), width=250)

if st.button("GENERATE", type="primary", use_container_width=True):
    if not prompt:
        st.warning("Write prompt!")
    else:
        full = f"{prompt}, {style}, clear face, sharp face, beautiful eyes, luxury, 8k"
        enc = urllib.parse.quote(full)
        
        if mode == "IMAGE":
            url = f"https://image.pollinations.ai/prompt/{enc}?width=1024&height=1280&model=flux&nologo=true"
            r = requests.get(url, timeout=60)
            img = Image.open(BytesIO(r.content)).convert("RGB")
            w,h = img.size
            img = img.crop((0,0,w,h-50))
            st.image(img, use_column_width=True)
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.download_button("DOWNLOAD HD", buf.getvalue(), "aurei.png", "image/png", use_container_width=True)
            st.success("Done - No Watermark!")
        else:
            vurl = f"https://gen.pollinations.ai/video/{enc}?duration=5&nologo=true"
            try:
                vr = requests.get(vurl, timeout=120)
                ctype = vr.headers.get("content-type","")
                if "video" in ctype:
                    st.video(vr.content)
                    st.download_button("DOWNLOAD VIDEO", vr.content, "aurei.mp4", "video/mp4", use_container_width=True)
                else:
                    st.info("Video API busy - showing IMAGE instead. Use IMAGE mode for now - no watermark!")
                    url = f"https://image.pollinations.ai/prompt/{enc}?width=1024&height=1280&model=flux&nologo=true"
                    r = requests.get(url, timeout=60)
                    img = Image.open(BytesIO(r.content)).convert("RGB")
                    w,h = img.size
                    img = img.crop((0,0,w,h-50))
                    st.image(img, use_column_width=True)
                    st.success("Image generated - No Watermark!")
            except Exception as e:
                st.error(f"Retry: {e}")
