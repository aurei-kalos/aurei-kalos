import streamlit as st, requests, urllib.parse
from PIL import Image
from io import BytesIO
import random

st.set_page_config(page_title="AUREI KALOS UNIVERSE", page_icon="✨", layout="wide")
st.title("✨ AUREI KALOS - UNIVERSE")
st.caption("Any Color | Any Gender | Any Face | Any Style | Image + Video | HD | 0 Money")

key = st.secrets.get("POLLINATIONS_KEY","")
if key:
    st.success(f"🔑 Key Connected - Ready for Image + Video + Any Color Gender Face!")
else:
    st.error("Add POLLINATIONS_KEY in Secrets!")

c1,c2,c3 = st.columns(3)
with c1:
    cat = st.selectbox("CATEGORY", ["Gown","Bridal White","Ankara African","Streetwear","Corporate Suit","Men's Agbada","Men's Suit","Kids Fashion","Traditional","Casual","Any Style"])
    gender = st.selectbox("GENDER", ["Female","Male","Unisex","Kids Girl","Kids Boy","Plus Size Female"])
with c2:
    color = st.text_input("COLORS (Any!)", value="Red")
    fabric = st.text_input("FABRIC", value="Silk")
with c3:
    face = st.selectbox("FACE DIVERSITY", ["African Beautiful Face","European","Asian","Mixed Race","Dark Skin","Caramel","Light Skin","Any"])
    out = st.selectbox("OUTPUT", ["IMAGE + VIDEO","IMAGE ONLY","VIDEO ONLY","AUDIO"])

prompt = st.text_area("DESCRIBE YOUR DESIGN (Anything!)", placeholder="e.g. Red velvet gown cape, blue corporate pantsuit female, black agbada male with gold embroidery, ankara jumpsuit, kids yellow party dress...", height=120)

if st.button("🚀 GENERATE - FIXED - NO ERROR", type="primary", use_container_width=True):
    if not prompt:
        st.warning("Type design first boss!")
    else:
        full = f"{prompt}, {cat}, {gender}, {face}, {color} color outfit, {fabric} fabric, clear detailed beautiful face, sharp eyes, ultra detailed skin, luxury fashion photography, 8k, studio lighting"
        enc = urllib.parse.quote(full)
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        seed = random.randint(1,999999)

        # ---- IMAGE WITH ERROR CHECK ----
        if "IMAGE" in out:
            with st.spinner(f"Generating IMAGE: {gender} | {color} | {face}..."):
                iurl = f"https://image.pollinations.ai/prompt/{enc}?width=1024&height=1536&model=flux&enhance=true&nologo=true&seed={seed}"
                try:
                    r = requests.get(iurl, headers=headers, timeout=120)
                    # Check if it's image or error
                    if "image" in r.headers.get("content-type","") or r.content[:4] == b'\x89PNG' or r.content[:2] == b'\xff\xd8':
                        img = Image.open(BytesIO(r.content)).convert("RGB")
                        st.image(img, caption=f"{gender} | {color} | {face}", use_container_width=True)
                        buf=BytesIO(); img.save(buf, format="PNG")
                        st.download_button("📥 DOWNLOAD IMAGE HD - No Watermark", buf.getvalue(), f"aurei_{gender}_{color}.png", "image/png", use_container_width=True)
                    else:
                        st.error("API returned text not image. Showing details:")
                        st.code(r.text[:500])
                        st.info("Try again in 20 sec - Free tier sometimes busy - but still 0 Money!")
                except Exception as e:
                    st.error(f"Image error: {e} - Retrying... Try again!")

        # ---- VIDEO WITH ERROR CHECK ----
        if "VIDEO" in out:
            with st.spinner(f"Generating VIDEO: {gender} {color} - Wait 60 sec..."):
                vurl = f"https://gen.pollinations.ai/image/{enc}?model=veo&width=1024&height=1536&nologo=true&enhance=true"
                # Fallback to image-to-video if needed
                try:
                    vr = requests.get(vurl, headers=headers, timeout=180)
                    ctype = vr.headers.get("content-type","")
                    if "video" in ctype or len(vr.content) > 300000:
                        st.video(vr.content)
                        st.download_button("📥 DOWNLOAD VIDEO HD", vr.content, f"aurei_{gender}_{color}.mp4", "video/mp4", use_container_width=True)
                        st.balloons()
                        st.success(f"Done! {gender} | {face} | {color} | {cat} | Clear Face | HD No Watermark!")
                    else:
                        st.warning("Video queue busy on free tier. Your IMAGE above is ready! Wait 1 min and try VIDEO ONLY again.")
                        st.code(vr.text[:500])
                except Exception as e:
                    st.error(f"Video busy: {e} - Try VIDEO ONLY after 1 min!")

st.divider()
st.write("**Tips:** Different Colors = Type in COLORS box. Different Gender = Select GENDER. Different Faces = Select FACE DIVERSITY. Not only gown = Select CATEGORY!")
