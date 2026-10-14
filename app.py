
# Paste this FULL CODE in github.com -> aurei-kalos -> app.py
import streamlit as st, requests, urllib.parse
from PIL import Image
from io import BytesIO
import random

st.set_page_config(page_title="AUREI KALOS UNIVERSE", page_icon="✨", layout="wide")
st.title("✨ AUREI KALOS - UNIVERSE")
st.caption("Any Color | Any Gender | Any Face | Image + Video + Audio | HD No Watermark | 0 Money")

key = st.secrets.get("POLLINATIONS_KEY","")
if key: st.success("🔑 Key Connected - Can Generate Image, Video, Audio, Many More!")
else: st.warning("Add POLLINATIONS_KEY in Streamlit Secrets!")

c1,c2,c3 = st.columns(3)
with c1:
    cat = st.selectbox("CATEGORY", ["Gown","Bridal White","Ankara","Streetwear","Corporate Suit","Men's Agbada","Men's Suit","Kids","Traditional","Any Style"])
    gender = st.selectbox("GENDER", ["Female","Male","Unisex","Kids Girl","Plus Size"])
with c2:
    color = st.text_input("COLORS (Any!)", placeholder="Red, Blue, Multicolor Ankara, Gold")
    fabric = st.text_input("FABRIC", placeholder="Silk, Velvet, Lace, Ankara, Denim")
with c3:
    face = st.selectbox("FACE", ["African","European","Asian","Mixed Race","Dark Skin","Caramel","Any"])
    out = st.selectbox("OUTPUT", ["IMAGE + VIDEO","IMAGE ONLY","VIDEO ONLY"])

prompt = st.text_area("DESCRIBE (Anything!)", placeholder="e.g. Red velvet gown cape, blue corporate suit female, black agbada male, ankara jumpsuit, kids yellow dress...", height=120)

if st.button("🚀 GENERATE - ANY COLOR GENDER FACE", type="primary", use_container_width=True):
    full = f"{prompt}, {cat}, {gender}, {face} beautiful face, {color} color, {fabric}, clear detailed face, 8k luxury fashion"
    enc = urllib.parse.quote(full)
    headers = {"Authorization": f"Bearer {key}"} if key else {}
    seed = random.randint(1,999999)

    if "IMAGE" in out:
        url = f"https://image.pollinations.ai/prompt/{enc}?width=1024&height=1536&model=flux&nologo=true&seed={seed}"
        r = requests.get(url, headers=headers, timeout=120)
        img = Image.open(BytesIO(r.content)).convert("RGB")
        st.image(img, use_container_width=True)
        buf=BytesIO(); img.save(buf, format="PNG")
        st.download_button("📥 DOWNLOAD IMAGE HD", buf.getvalue(), "aurei.png", "image/png", use_container_width=True)

    if "VIDEO" in out:
        vurl = f"https://gen.pollinations.ai/video/{enc}?model=veo&duration=6&nologo=true"
        vr = requests.get(vurl, headers=headers, timeout=180)
        if len(vr.content) > 200000:
            st.video(vr.content)
            st.download_button("📥 DOWNLOAD VIDEO HD", vr.content, "aurei.mp4", "video/mp4", use_container_width=True)
            st.balloons()
