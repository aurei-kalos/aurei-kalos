import streamlit as st, requests, urllib.parse, numpy as np, imageio
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AUREI KALOS PRO", page_icon="✨")
st.title("✨ AUREI KALOS - PRO")
st.caption("Luxury Atelier - HD Face, No Watermark")

prompt = st.text_area("Prompt", "Elegant golden evening gown, African luxury supermodel, runway")
style = st.selectbox("Style", ["Luxury Gold", "Runway Video", "Couture"])
mode = st.radio("Mode", ["📸 Image HD", "🎬 Video HD"])

def generate_image(full_prompt):
    # NEW PROMPT ENGINEERING FOR CLEAR FACE
    enhanced_prompt = f"{full_prompt}, (clear face, sharp focus face, beautiful symmetrical face, detailed eyes, flawless skin, high detail face), luxury fashion photography, 8k, ultra sharp, model face in focus, professional makeup"
    encoded = urllib.parse.quote(enhanced_prompt)
    # Use Flux model - better faces + no watermark param
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1280&model=flux&enhance=true&nologo=true&nofeed=true&private=true&seed={np.random.randint(999999)}"
    resp = requests.get(url, timeout=60)
    img = Image.open(BytesIO(resp.content)).convert("RGB")
    
    # AUTO REMOVE WATERMARK - Crop bottom right watermark area
    w, h = img.size
    # Remove bottom 60px where watermark sits, then resize back
    img_no_wm = img.crop((0, 0, w, h-70)) 
    img_no_wm = img_no_wm.resize((w, h), Image.LANCZOS)
    
    return img_no_wm

if st.button("GENERATE AUREI DESIGN", use_container_width=True):
    if not prompt:
        st.warning("Enter prompt!")
    else:
        full = f"{prompt}, {style}"
        with st.spinner("Atelier creating HD luxury design... ✨"):
            try:
                img = generate_image(full)
                if mode == "📸 Image HD":
                    st.image(img, use_column_width=True, caption="AUREI KALOS - HD No Watermark")
                    buf = BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button("📥 DOWNLOAD HD (No Watermark)", buf.getvalue(), "aurei_hd.png", "image/png", use_container_width=True)
                else:
                    st.image(img, caption="HD Design")
                    with st.spinner("Creating HD runway video..."):
                        frames = []
                        w, h = img.size
                        for i in range(60):
                            zoom = 1.0 + i*0.005
                            crop_w, crop_h = int(w/zoom), int(h/zoom)
                            left = int((w-crop_w)/2)
                            top = int((h-crop_h)/2)
                            frame = img.crop((left, top, left+crop_w, top+crop_h)).resize((1024,1280))
                            frames.append(np.array(frame))
                        path = "/tmp/aurei_hd.mp4"
                        imageio.mimsave(path, frames, fps=12, macro_block_size=1)
                        st.video(path)
                        with open(path, "rb") as f:
                            st.download_button("📥 DOWNLOAD HD VIDEO", f.read(), "aurei_hd_video.mp4", "video/mp4", use_container_width=True)
                st.success("HD Generated! No watermark! Clear face!")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("PRO Version: HD Face + No Watermark + Video")
