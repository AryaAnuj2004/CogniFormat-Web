import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import base64
import json
from PIL import Image
from datetime import datetime
import re
import socket
import dns.resolver
from email_validator import validate_email, EmailNotValidError

# Paths
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
SCREENSHOTS_DIR = os.path.join(ASSETS_DIR, "screenshots")
DOWNLOADS_DIR = os.path.join(ASSETS_DIR, "downloads")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
EXE_PATH = os.path.join(DOWNLOADS_DIR, "CogniFormat_Setup.exe")
LEADS_FILE = os.path.join(DATA_DIR, "leads.csv")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo_black.png")

# Base64 helper for local logo
def get_base64_image(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

logo_b64 = get_base64_image(LOGO_PATH)
logo_icon = Image.open(LOGO_PATH) if os.path.exists(LOGO_PATH) else None

# Screenshots Metadata for Modern Slider UI
SCREENSHOTS_METADATA = [
    {
        "filename": "Starter.png",
        "title": "Main Application Window Loading",
        "badge": "Main Loading Screen",
        "desc": "First look at the main application window as it initializes with a smooth fade-in transition."
    },
    {
        "filename": "Dark Mode.png",
        "title": "Sleek High-Contrast Dark Theme",
        "badge": "Dark-Interface",
        "desc": "Modern dark mode engineered for comfortable low-light editing and reduced eye fatigue."
    },
    {
        "filename": "Light Mode.png",
        "title": "Clean High-Clarity Light Theme",
        "badge": "Light-Interface",
        "desc": "Vibrant light interface designed for daytime productivity, clear contrast, and crisp visual hierarchy."
    },
    {
        "filename": "Enhance.png",
        "title": "AI Image Enhancer & Upscaler",
        "badge": "AI-Image-Enhancer",
        "desc": "Super-resolution neural model upscaling low-res photos into high-definition crisp images offline."
    },
    {
        "filename": "BG Remove.png",
        "title": "AI Background Remover and Editor",
        "badge": "AI-Image-Background-Remover",
        "desc": "Extract subjects, products, or logos automatically with clean transparent background output."
    },
    {
        "filename": "Trim Video.png",
        "title": "Visual Video Trimmer & Converter",
        "badge": "Video Studio",
        "desc": "Precision video editing with dual timestamp sliders, format re-encoding, and aspect ratio reframing."
    },
    {
        "filename": "Trim Audio.png",
        "title": "Precision Audio Trimmer & Merger",
        "badge": "Audio Studio",
        "desc": "Waveform timeline preview to clip unwanted audio sections, join tracks, and adjust bitrate quality."
    },
    {
        "filename": "ChatBot.png",
        "title": "CogniBot — Offline AI Assistant",
        "badge": "AI Assistant",
        "desc": "In-app offline assistant providing instant guidance on format options and app tools without sending data online."
    }
]

@st.cache_data
def get_all_screenshots_data():
    data = []
    for item in SCREENSHOTS_METADATA:
        file_path = os.path.join(SCREENSHOTS_DIR, item["filename"])
        b64 = get_base64_image(file_path)
        if b64:
            data.append({
                "title": item["title"],
                "badge": item["badge"],
                "desc": item["desc"],
                "src": f"data:image/png;base64,{b64}"
            })
    return data

def render_modern_screenshot_slider(slider_id="hero_slider", viewport_height=320, frame_height=520):
    screenshots = get_all_screenshots_data()
    if not screenshots:
        st.warning("no screenshot images found.")
        return

    json_data = json.dumps(screenshots)
    
    slider_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            background: transparent;
            color: #f8fafc;
            user-select: none;
            overflow: hidden;
        }}
        
        .slider-container {{
            background: linear-gradient(145deg, #0f172a, #1e293b);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 16px;
            padding: 14px;
            box-shadow: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 100%;
            margin: 2px 2px 6px 2px;
        }}
        
        .slider-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            background: rgba(15, 23, 42, 0.6);
            padding: 8px 12px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        
        .header-info {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            overflow: hidden;
        }}
        
        .title-row {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .badge {{
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: #ffffff;
            font-size: 0.68rem;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }}
        
        .slide-title {{
            font-size: 0.95rem;
            font-weight: 700;
            color: #ffffff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .slide-desc {{
            font-size: 0.8rem;
            color: #94a3b8;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .controls-top {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;
        }}
        
        .counter-pill {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 3px 8px;
            border-radius: 20px;
            font-size: 0.72rem;
            font-weight: 700;
            color: #38bdf8;
            white-space: nowrap;
        }}
        
        .autoplay-btn {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #cbd5e1;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .autoplay-btn:hover {{
            background: rgba(59, 130, 246, 0.3);
            color: #ffffff;
            border-color: #3b82f6;
        }}
    
        .viewport {{
            position: relative;
            width: 100%;
            height: {viewport_height}px;
            background: #020617;
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        
        .slide-img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            transition: opacity 0.35s ease, transform 0.35s ease;
            opacity: 1;
        }}
        
        .nav-arrow {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 36px;
            height: 36px;
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.25s ease;
            z-index: 10;
        }}
        
        .nav-arrow:hover {{
            background: #2563eb;
            border-color: #60a5fa;
            transform: translateY(-50%) scale(1.1);
            box-shadow: 0 0 12px rgba(37, 99, 235, 0.6);
        }}
        
        .nav-prev {{ left: 10px; }}
        .nav-next {{ right: 10px; }}
        
        .thumbnail-ribbon {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 2px 2px 4px 2px;
            scroll-behavior: smooth;
        }}
        
        .thumbnail-ribbon::-webkit-scrollbar {{
            height: 4px;
        }}
        .thumbnail-ribbon::-webkit-scrollbar-thumb {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
        }}
        
        .thumb-card {{
            flex: 0 0 76px;
            height: 48px;
            border-radius: 6px;
            overflow: hidden;
            cursor: pointer;
            border: 2px solid transparent;
            opacity: 0.6;
            transition: all 0.25s ease;
            background: #020617;
            position: relative;
        }}
        
        .thumb-card img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .thumb-card:hover {{
            opacity: 0.9;
            transform: translateY(-2px);
        }}
        
        .thumb-card.active {{
            border-color: #38bdf8;
            opacity: 1;
            transform: translateY(-2px);
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
        }}
    
        .dots-bar {{
            display: flex;
            justify-content: center;
            gap: 5px;
        }}
        
        .dot {{
            width: 7px;
            height: 7px;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.25);
            cursor: pointer;
            transition: all 0.25s ease;
        }}
        
        .dot.active {{
            width: 18px;
            background: #38bdf8;
            border-radius: 4px;
        }}
    </style>
    </head>
    <body>
    
    <div class="slider-container" id="{slider_id}">
        <div class="slider-header">
            <div class="header-info">
                <div class="title-row">
                    <span class="badge" id="{slider_id}_badge">BADGE</span>
                    <span class="slide-title" id="{slider_id}_title">Title</span>
                </div>
                <div class="slide-desc" id="{slider_id}_desc">Description</div>
            </div>
            <div class="controls-top">
                <div class="counter-pill" id="{slider_id}_counter">1 / 8</div>
                <button class="autoplay-btn" id="{slider_id}_playbtn" onclick="toggleAutoplay()">
                    <span id="{slider_id}_playicon">⏸</span> Pause
                </button>
            </div>
        </div>
        
        <div class="viewport" id="{slider_id}_viewport">
            <button class="nav-arrow nav-prev" onclick="prevSlide()">❮</button>
            <img class="slide-img" id="{slider_id}_img" src="" alt="Screenshot">
            <button class="nav-arrow nav-next" onclick="nextSlide()">❯</button>
        </div>
        
        <div class="thumbnail-ribbon" id="{slider_id}_thumbs"></div>
        
        <div class="dots-bar" id="{slider_id}_dots"></div>
    </div>
    
    <script>
        const slidesData = {json_data};
        let currentIndex = 0;
        let autoplayTimer = null;
        let isPlaying = true;
        
        const sliderId = "{slider_id}";
        const badgeEl = document.getElementById(sliderId + "_badge");
        const titleEl = document.getElementById(sliderId + "_title");
        const descEl = document.getElementById(sliderId + "_desc");
        const counterEl = document.getElementById(sliderId + "_counter");
        const imgEl = document.getElementById(sliderId + "_img");
        const thumbsEl = document.getElementById(sliderId + "_thumbs");
        const dotsEl = document.getElementById(sliderId + "_dots");
        const playBtnEl = document.getElementById(sliderId + "_playbtn");
    
        function initSlider() {{
            thumbsEl.innerHTML = "";
            dotsEl.innerHTML = "";
            
            slidesData.forEach((slide, idx) => {{
                const thumb = document.createElement("div");
                thumb.className = "thumb-card" + (idx === 0 ? " active" : "");
                thumb.onclick = () => goToSlide(idx);
                const tImg = document.createElement("img");
                tImg.src = slide.src;
                thumb.appendChild(tImg);
                thumbsEl.appendChild(thumb);
                
                const dot = document.createElement("div");
                dot.className = "dot" + (idx === 0 ? " active" : "");
                dot.onclick = () => goToSlide(idx);
                dotsEl.appendChild(dot);
            }});
            
            renderSlide(0);
            startAutoplay();
        }}
        
        function renderSlide(idx) {{
            currentIndex = idx;
            const slide = slidesData[idx];
            
            imgEl.style.opacity = "0.3";
            imgEl.style.transform = "scale(0.98)";
            
            setTimeout(() => {{
                imgEl.src = slide.src;
                badgeEl.innerText = slide.badge;
                titleEl.innerText = slide.title;
                descEl.innerText = slide.desc;
                counterEl.innerText = (idx + 1) + " / " + slidesData.length;
                
                imgEl.style.opacity = "1";
                imgEl.style.transform = "scale(1)";
            }}, 90);
            
            const thumbs = thumbsEl.querySelectorAll(".thumb-card");
            thumbs.forEach((t, i) => {{
                if (i === idx) {{
                    t.classList.add("active");
                    const scrollPos = t.offsetLeft - (thumbsEl.clientWidth / 2) + (t.clientWidth / 2);
                    thumbsEl.scrollTo({{ left: scrollPos, behavior: 'smooth' }});
                }} else {{
                    t.classList.remove("active");
                }}
            }});
            
            const dots = dotsEl.querySelectorAll(".dot");
            dots.forEach((d, i) => {{
                d.className = "dot" + (i === idx ? " active" : "");
            }});
        }}
        
        function goToSlide(idx) {{
            renderSlide(idx);
            resetAutoplay();
        }}
        
        function nextSlide() {{
            let next = (currentIndex + 1) % slidesData.length;
            goToSlide(next);
        }}
        
        function prevSlide() {{
            let prev = (currentIndex - 1 + slidesData.length) % slidesData.length;
            goToSlide(prev);
        }}
        
        function startAutoplay() {{
            if (autoplayTimer) clearInterval(autoplayTimer);
            autoplayTimer = setInterval(() => {{
                let next = (currentIndex + 1) % slidesData.length;
                renderSlide(next);
            }}, 4000);
            isPlaying = true;
            playBtnEl.style.background = "rgba(255, 255, 255, 0.1)";
            playBtnEl.innerHTML = '<span>⏸</span> Pause';
        }}
        
        function stopAutoplay() {{
            if (autoplayTimer) clearInterval(autoplayTimer);
            isPlaying = false;
            playBtnEl.style.background = "rgba(59, 130, 246, 0.4)";
            playBtnEl.innerHTML = '<span>▶</span> Play';
        }}
        
        function toggleAutoplay() {{
            if (isPlaying) {{
                stopAutoplay();
            }} else {{
                startAutoplay();
            }}
        }}
        
        function resetAutoplay() {{
            if (isPlaying) {{
                startAutoplay();
            }}
        }}
        
        document.addEventListener("keydown", (e) => {{
            if (e.key === "ArrowRight") nextSlide();
            if (e.key === "ArrowLeft") prevSlide();
        }});

        let touchStartX = 0;
        const viewport = document.getElementById(sliderId + "_viewport");
        viewport.addEventListener("touchstart", (e) => {{
            touchStartX = e.changedTouches[0].screenX;
        }}, {{ passive: true }});
        
        viewport.addEventListener("touchend", (e) => {{
            let touchEndX = e.changedTouches[0].screenX;
            if (touchStartX - touchEndX > 40) nextSlide();
            if (touchEndX - touchStartX > 40) prevSlide();
        }}, {{ passive: true }});
        
        window.onload = initSlider;
    </script>
    </body>
    </html>
    """
    components.html(slider_html, height=frame_height, scrolling=False)

# Set Page Config
st.set_page_config(
    page_title="CogniFormat — All-in-One File Converter and AI Enhancer",
    page_icon=logo_icon,
    layout="wide",
    initial_sidebar_state="collapsed"
)

os.makedirs(DATA_DIR, exist_ok=True)

# List of known disposable / temporary email domain providers
DISPOSABLE_DOMAINS = {
    'mailinator.com', 'tempmail.com', '10minutemail.com', 'trashmail.com', 
    'yopmail.com', 'guerrillamail.com', 'dispostable.com', 'fakeinbox.com',
    'sharklasers.com', 'getnada.com', 'disposable.com'
}

def validate_authorized_email(email: str):
    """
    Strict Email Domain Validation:
    1. Checks email structure and syntax using email_validator.
    2. Filters out temporary / disposable email domain providers.
    3. Filters out fake numeric-only domain prefixes.
    4. Performs authoritative DNS MX (Mail Exchange) record resolution.
    """
    if not email or not email.strip():
        return False, "Please enter an email address."
        
    email_str = email.strip().lower()
    
    try:
        # Validate syntax & check deliverability
        valid_info = validate_email(email_str, check_deliverability=True)
        domain = valid_info.domain.lower()
        
        # Check disposable domain blacklists
        if domain in DISPOSABLE_DOMAINS:
            return False, "Temporary / disposable email domains are not authorized."
            
        # Reject numeric domain prefixes (e.g. 123.com)
        domain_prefix = domain.split('.')[0]
        if domain_prefix.isdigit():
            return False, f"The domain '{domain}' is not an authorized email domain."
            
        # DNS MX record check for active mail servers
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            if len(mx_records) > 0:
                return True, valid_info.normalized
        except Exception:
            return False, f"The domain '{domain}' has no active authorized mail servers (MX)."
            
        return True, valid_info.normalized
    except EmailNotValidError as err:
        return False, f"Unauthorized email: {str(err)}"
        
    return False, "Unauthorized email domain."

# Custom CSS for Premium Design & Vibrant Colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
        color: #0f172a;
    }
    
    /* Permanently Hide Streamlit Hamburger Menu, Header, Toolbar, & Footer */
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }
    
    header, header[data-testid="stHeader"], [data-testid="stHeader"] {
        visibility: hidden !important;
        display: none !important;
        height: 0px !important;
        min-height: 0px !important;
    }

    [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        visibility: hidden !important;
        display: none !important;
    }

    footer, footer[data-testid="stFooter"] {
        visibility: hidden !important;
        display: none !important;
    }

    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
        width: 0px !important;
    }
    
    [data-testid="collapsedControl"], button[kind="header"] {
        display: none !important;
    }

    /* Page Background */
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1140px;
    }

    /* Brand Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 1.5rem;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    
    .brand-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0084ff;
        letter-spacing: -0.3px;
    }

    .version-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .dot-active {
        width: 6px;
        height: 6px;
        background-color: #2563eb;
        border-radius: 50%;
        display: inline-block;
    }

    /* Vibrant Hero Banner Box */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #1e1b4b 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2.8rem 2rem;
        text-align: center;
        color: #ffffff;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
        position: relative;
        overflow: hidden;
    }

    .hero-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 30px;
        background: rgba(37, 99, 235, 0.25);
        border: 1px solid rgba(96, 165, 250, 0.4);
        color: #93c5fd;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .hero-h1 {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.9rem;
        line-height: 1.2;
        letter-spacing: -0.8px;
    }

    .hero-sub {
        font-size: 1.05rem;
        color: #94a3b8;
        max-width: 780px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }

    .hero-highlights {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 1.4rem;
        margin-top: 1rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-size: 0.88rem;
        color: #cbd5e1;
        font-weight: 500;
    }

    /* Key Highlights Grid Cards */
    .section-header {
        text-align: center;
        margin: 2.4rem 0 1.4rem 0;
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.5px;
    }

    .section-desc {
        font-size: 0.92rem;
        color: #64748b;
        margin-top: 4px;
    }

    .highlight-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.3rem;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }

    .highlight-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border-color: #cbd5e1;
    }

    .highlight-title {
        font-size: 1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.4rem;
    }

    .highlight-text {
        font-size: 0.84rem;
        color: #64748b;
        line-height: 1.5;
    }

    /* Studio Tabs Container */
    .studio-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 0.8rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }

    .feature-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 0.9rem;
    }

    .feature-bullet {
        background: #eff6ff;
        color: #2563eb;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        flex-shrink: 0;
        margin-top: 2px;
    }

    .feature-text-title {
        font-size: 0.92rem;
        font-weight: 700;
        color: #0f172a;
    }

    .feature-text-desc {
        font-size: 0.83rem;
        color: #64748b;
        line-height: 1.4;
    }

    /* Form & Download Box */
    [data-testid="stForm"], div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-top: 1.8rem !important;
        margin-bottom: 1.8rem !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04) !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"]:nth-child(2) {
        border-left: 1px solid #e2e8f0 !important;
        padding-left: 1.5rem !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"]:nth-child(2) [data-testid="stDownloadButton"],
    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="column"]:nth-child(2) [data-testid="stLinkButton"] {
        margin-left: 0 !important;
        width: 100% !important;
    }

    .download-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
    }

    .card-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.3rem;
    }

    .card-sub {
        font-size: 0.88rem;
        color: #64748b;
        margin-bottom: 1.2rem;
    }

    .notice-locked {
        padding: 12px 16px;
        border-radius: 10px;
        background: #fffbeb;
        border: 1px solid #fde68a;
        color: #b45309;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1rem;
    }

    .notice-unlocked {
        padding: 12px 16px;
        border-radius: 10px;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #15803d;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1rem;
    }

    /* System Requirements Table Styling */
    .sys-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        margin-top: 1rem;
        font-size: 0.88rem;
    }

    .sys-table th {
        background: #f8fafc;
        color: #334155;
        font-weight: 700;
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
    }

    .sys-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #f1f5f9;
        color: #475569;
    }

    .sys-table tr:last-child td {
        border-bottom: none;
    }

    .sys-table tr:nth-child(even) {
        background-color: #ffffff;
    }

    .sys-table tr:nth-child(odd) {
        background-color: #fafafa;
    }

    /* Installation Steps Cards */
    .step-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        height: 100%;
    }

    .step-num {
        display: inline-block;
        width: 28px;
        height: 28px;
        border-radius: 8px;
        background: #2563eb;
        color: white;
        text-align: center;
        line-height: 28px;
        font-weight: 800;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }

    .step-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.3rem;
    }

    .step-desc {
        font-size: 0.82rem;
        color: #64748b;
        line-height: 1.4;
    }

    /* Vibrant Buttons Override */
    .stButton>button {
        border-radius: 10px;
        padding: 0.65rem 1.2rem;
        font-size: 0.92rem;
        font-weight: 700;
        background: #2563eb;
        color: white;
        border: none;
        width: 100%;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }

    .stButton>button:hover {
        background: #1d4ed8;
    }

    .stDownloadButton>button {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 700;
        background: #16a34a;
        color: white;
        border: none;
        width: 100%;
        box-shadow: 0 4px 14px rgba(22, 163, 74, 0.25);
    }

    .stDownloadButton>button:hover {
        background: #15803d;
    }
</style>
""", unsafe_allow_html=True)

# Save Lead Function (New entry if Name or Email is different)
def save_lead(name: str, email: str):
    clean_name = name.strip()
    clean_email = email.strip().lower()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if os.path.exists(LEADS_FILE) and os.path.getsize(LEADS_FILE) > 0:
        try:
            df = pd.read_csv(LEADS_FILE)
            if not {'Timestamp', 'Name', 'Email'}.issubset(df.columns):
                df = pd.DataFrame(columns=["Timestamp", "Name", "Email"])
        except Exception:
            df = pd.DataFrame(columns=["Timestamp", "Name", "Email"])
    else:
        df = pd.DataFrame(columns=["Timestamp", "Name", "Email"])
    
    df['Name_Clean'] = df['Name'].astype(str).str.strip().str.lower()
    df['Email_Clean'] = df['Email'].astype(str).str.strip().str.lower()
    
    # Check if exact (Name, Email) combination already exists
    match_mask = (df['Name_Clean'] == clean_name.lower()) & (df['Email_Clean'] == clean_email)
    
    if match_mask.any():
        idx = df[match_mask].index[0]
        df.loc[idx, 'Timestamp'] = now_str
        df.loc[idx, 'Name'] = clean_name
        df.loc[idx, 'Email'] = clean_email
    else:
        new_row = pd.DataFrame([{
            "Timestamp": now_str,
            "Name": clean_name,
            "Email": clean_email
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    
    df = df.drop(columns=['Name_Clean', 'Email_Clean'])
    df.to_csv(LEADS_FILE, index=False)

# Session State
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ==================== BRAND NAVIGATION BAR ====================
logo_icon_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 38px; border-radius: 8px; object-fit: contain; vertical-align: middle;">' if logo_b64 else ''

st.markdown(f"""
<div class="top-nav">
    <div style="display: flex; align-items: center; gap: 12px;">
        {logo_icon_html}
        <span class="brand-title">CogniFormat</span>
    </div>
    <div class="version-pill">
        <span class="dot-active"></span> Windows v1.0 Official Release
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== HERO SECTION ====================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">100% Offline & Private AI Desktop App</div>
    <div class="hero-h1">The Ultimate 100% Offline AI Media & Document Converter</div>
    <div class="hero-sub">
        Convert, compress, upscale, edit, and organize your images, videos, audio, and PDF documents locally on your PC. No file size limits. No subscriptions. 100% private.
    </div>
    <div class="hero-highlights">
        <span>Fast 1-Click Setup</span>
        <span>•</span>
        <span>100% Free & Safe</span>
        <span>•</span>
        <span>Works 100% Offline</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== MAIN SECTION: DOWNLOAD GATE ====================
st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
with st.container(border=True):
    dl_col_left, dl_col_right = st.columns([1, 1])

    with dl_col_left:
        st.markdown("""
            <div class="card-title">Registration & Verification</div>
            <div class="card-sub">Enter your full name and authorized email to activate installer download link</div>
        """, unsafe_allow_html=True)
        
        with st.form("download_form"):
            name_val = st.text_input("Name", value=st.session_state.user_name, placeholder="Enter your full name")
            email_val = st.text_input("Authorized Email Address", value=st.session_state.user_email, placeholder="name@domain.com")
            submit_btn = st.form_submit_button("Unlock Installer Download")
            
            if submit_btn:
                if not name_val.strip():
                    st.error("Please enter your name.")
                else:
                    is_valid, res_msg = validate_authorized_email(email_val)
                    if not is_valid:
                        st.error(f"{res_msg}")
                    else:
                        save_lead(name_val, res_msg)
                        st.session_state.unlocked = True
                        st.session_state.user_name = name_val
                        st.session_state.user_email = res_msg
                        st.toast("Authorized Email Verified!", icon="✅")

    with dl_col_right:
        if not st.session_state.unlocked:
            st.markdown("""
            <div style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div class="card-title" style="margin-bottom: 0;">Download CogniFormat for Windows</div>
                        <span style="background: #fffbeb; border: 1px solid #fde68a; color: #b45309; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px;">🔒 Locked</span>
                    </div>
                    <div class="card-sub">EXE Installer — Version 1.0 (Windows 10/11 64-bit)</div>
                    <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; padding: 14px; margin: 12px 0; font-size: 0.84rem; color: #475569; line-height: 1.6;">
                        <div style="font-weight: 700; color: #0f172a; margin-bottom: 4px;">Activation Steps:</div>
                        1. Enter your name and authorized email on the left.<br>
                        2. Automatically verifies your domain configuration.<br>
                        3. Your Windows installer download button appears right here!
                    </div>
                </div>
                <div class="notice-locked" style="margin-top: 8px;">
                    Enter an authorized email address on the left to activate your free download link.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div class="card-title" style="margin-bottom: 0;">Download CogniFormat for Windows</div>
                        <span style="background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px;">🔓 Unlocked</span>
                    </div>
                    <div class="card-sub">EXE Installer — Version 1.0 (Windows 10/11 64-bit)</div>
                    <div class="notice-unlocked" style="margin-top: 4px;">
                        Authorized email verified for <b>{st.session_state.user_name}</b> ({st.session_state.user_email}). Click below to download your 1-click installer.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            SETUP_EXE_URL = os.getenv("SETUP_EXE_URL", "").strip()

            if os.path.exists(EXE_PATH):
                with open(EXE_PATH, "rb") as f:
                    bytes_data = f.read()
                st.download_button(
                    label="Download CogniFormat_Setup.exe (v1.0)",
                    data=bytes_data,
                    file_name="CogniFormat_Setup.exe",
                    mime="application/octet-stream",
                    use_container_width=True
                )
            elif SETUP_EXE_URL:
                st.link_button("Download CogniFormat_Setup.exe (v1.0)", SETUP_EXE_URL, use_container_width=True)
            else:
                st.error("Installer executable file missing from assets directory.")

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

# ==================== KEY HIGHLIGHTS SECTION ====================
st.markdown("""
<div class="section-header">
    <div class="section-title">Why Choose CogniFormat?</div>
    <div class="section-desc">Empowering creators, professionals, and privacy-conscious users with local AI tools</div>
</div>
""", unsafe_allow_html=True)

h_col1, h_col2, h_col3 = st.columns(3)

with h_col1:
    st.markdown("""
    <div class="highlight-card">
        <div class="highlight-title">100% Private & Local Processing</div>
        <div class="highlight-text">All conversions, background removals, and AI upscaling happen right on your computer. Your files never get uploaded to cloud servers or shared with third parties.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="highlight-card">
        <div class="highlight-title">Hardware Accelerated Speed</div>
        <div class="highlight-text">Powered by multi-core CPU optimization and embedded FFmpeg/PyMuPDF, ensuring lightning-fast media rendering and document extraction.</div>
    </div>
    """, unsafe_allow_html=True)

with h_col2:
    st.markdown("""
    <div class="highlight-card">
        <div class="highlight-title">Zero File Size Limits</div>
        <div class="highlight-text">Unlike web-based converters that cap file sizes or charge monthly fees, CogniFormat offers unlimited batch processing for files of any size without subscriptions.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="highlight-card">
        <div class="highlight-title">Sleek & Modern UI</div>
        <div class="highlight-text">Elegant dark and light themes, dynamic split-screen before/after visual previews, interactive timeline trimmers, and a built-in offline AI helper.</div>
    </div>
    """, unsafe_allow_html=True)

with h_col3:
    st.markdown("""
    <div class="highlight-card" style="grid-row: span 2;">
        <div class="highlight-title">Built-in Local AI Engine</div>
        <div class="highlight-text">
            Powerful AI image processing that runs entirely on your device, with no internet connection required.
        </div>
        <div style="margin-top:12px; padding:10px; background:#eff6ff; border: 1px solid #bfdbfe; border-radius:8px; font-size:0.8rem; color:#1d4ed8; line-height:1.6;">
            • AI Background Removal with high-quality edge detection<br>
            • AI Image Upscaling for sharper, higher-resolution images<br>
            • AI Image Deblurring to recover details from blurry photos<br>
            • Private & Offline processing with no image uploads
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

# ==================== APPLICATION SCREENSHOTS GALLERY ====================
st.markdown("""
<div class="section-header">
    <div class="section-title">Application Screenshots Showcase</div>
    <div class="section-desc">Interactive visual tour of CogniFormat Desktop, dark & light themes, and local AI tools</div>
</div>
""", unsafe_allow_html=True)

render_modern_screenshot_slider(slider_id="full_gallery_slider", viewport_height=420, frame_height=610)

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

# ==================== DETAILED FEATURE BREAKDOWN ====================
st.markdown("""
<div class="section-header">
    <div class="section-title">Detailed Feature Breakdown</div>
    <div class="section-desc">Explore the 6 power studios built inside CogniFormat Desktop</div>
</div>
""", unsafe_allow_html=True)

tab_img, tab_vid, tab_pdf, tab_aud, tab_bot, tab_ui = st.tabs([
    "Image Studio",
    "Video Studio",
    "PDF & Document Studio",
    "Audio Converter",
    "CogniBot AI",
    "UI & Workflow"
])

with tab_img:
    st.markdown("""
    <div class="studio-box">
        <h4 style="margin-top:0; color:#0f172a; font-weight:700;">Image Studio & Local AI Tools</h4>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Universal Image Format Conversion</div>
                    <div class="feature-text-desc">Convert single images or entire folders between JPG, PNG, WEBP, BMP, and more with quality sliders.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">AI Image Enhancer (Upscaling)</div>
                    <div class="feature-text-desc">Enhance low-res images into ultra-sharp high-definition photos (powered by local AI models).</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">AI Image Deblurring</div>
                    <div class="feature-text-desc">Remove camera shake and lens blur automatically using the Deblurring AI neural model.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">1-Click AI Background Removal</div>
                    <div class="feature-text-desc">Instantly extract portrait subjects, products, or logos with transparent background generation.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Background Color Replacement</div>
                    <div class="feature-text-desc">Replace extracted backgrounds with solid colors, custom canvas dimensions, or custom hex color codes.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Interactive Crop & Rotate</div>
                    <div class="feature-text-desc">Precise crop bounds, rotation controls, and visual ratio locked adjustments.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Side-by-Side Comparison View</div>
                    <div class="feature-text-desc">Compare your original vs modified photo in real-time with an interactive slider.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Batch Images-to-PDF</div>
                    <div class="feature-text-desc">Combine dozens of images into a single formatted PDF document in seconds.</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab_vid:
    st.markdown("""
    <div class="studio-box">
        <h4 style="margin-top:0; color:#0f172a; font-weight:700;">Video Studio & Smart AI Focus Framing</h4>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Video Converter & Compression</div>
                    <div class="feature-text-desc">Convert between MP4, MKV, AVI, MOV, WEBM, and animated GIF formats while dramatically reducing file sizes without losing quality.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Next-Gen Codec Controls</div>
                    <div class="feature-text-desc">Full support for H.264, H.265/HEVC, VP9, and AV1 video encoding.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Visual Video Trimming</div>
                    <div class="feature-text-desc">Interactive video player with dual sliders to trim and cut videos down to exact millisecond timestamps.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Orientation & Aspect Ratio Converter</div>
                    <div class="feature-text-desc">Rotate vertical videos or reframe 16:9 landscape videos into 9:16 vertical videos tailored for TikTok, Instagram Reels, and YouTube Shorts.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Smart Background Blur Padding</div>
                    <div class="feature-text-desc">Automatically fill letterbox borders with stylish blurred video backgrounds.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Smart AI Focus Mode (Object Tracking)</div>
                    <div class="feature-text-desc">Track moving people, pets, or objects in a video. CogniFormat automatically centers the camera crop on your selected target throughout the video.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Audio Track Replacement & Overlay</div>
                    <div class="feature-text-desc">Remove original video audio, attach custom background music, or adjust soundtrack audio offsets.</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab_pdf:
    st.markdown("""
    <div class="studio-box">
        <h4 style="margin-top:0; color:#0f172a; font-weight:700;">PDF & Document Management Studio</h4>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Merge PDF Documents</div>
                    <div class="feature-text-desc">Combine multiple PDF files into one clean document with custom page ordering.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Split PDF Files</div>
                    <div class="feature-text-desc">Extract individual pages or define page ranges (e.g., pages 1–3, 5, 8–12).</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">PDF File Compression</div>
                    <div class="feature-text-desc">Shrink bloated PDF sizes with customizable resolution and quality presets.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">PDF Image Extraction</div>
                    <div class="feature-text-desc">Save every embedded image or render full PDF pages as high-resolution image files (PNG, JPG, WEBP).</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Visual PDF Page Organizer</div>
                    <div class="feature-text-desc">Grid view of document pages—reorder pages via keyboard or buttons, rotate individual pages, and delete unwanted pages before export.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Office Document Conversion</div>
                    <div class="feature-text-desc">Convert Word documents (DOCX), Excel spreadsheets (XLSX), PowerPoint presentations (PPTX), Text (TXT), HTML, and EPUB files into standard PDF files.</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab_aud:
    st.markdown("""
    <div class="studio-box">
        <h4 style="margin-top:0; color:#0f172a; font-weight:700;">Audio Converter & Editor</h4>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Audio Format Conversion</div>
                    <div class="feature-text-desc">Convert audio files between MP3, WAV, AAC, M4A, FLAC, and OGG formats with custom bitrate settings.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Audio Track Merger</div>
                    <div class="feature-text-desc">Join multiple songs, voice recordings, or audio clips into a single continuous track.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Precision Audio Trimmer</div>
                    <div class="feature-text-desc">Waveform timeline preview with start/end time markers to clip unwanted audio sections.</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab_bot:
    st.markdown("""
    <div class="studio-box">
        <h4 style="margin-top:0; color:#0f172a; font-weight:700;">CogniBot — Offline AI Assistant</h4>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Instant In-App Chat</div>
                    <div class="feature-text-desc">Built-in offline AI helper to answer questions about supported formats, optimal quality settings, or application navigation.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">100% Local Intelligence</div>
                    <div class="feature-text-desc">Works completely offline without requiring API keys or internet access.</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab_ui:
    st.markdown("""
    <div class="studio-box">
        <h4 style="margin-top:0; color:#0f172a; font-weight:700;">User Interface & Workflow Enhancements</h4>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px;">
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Global Quick Search (Ctrl + K)</div>
                    <div class="feature-text-desc">Instantly search and jump to any converter tool, tab, or settings option.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Background Queue Manager</div>
                    <div class="feature-text-desc">Batch process long queues of files while continuing to work; pause, resume, or cancel jobs at any time.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Recent Activity Log</div>
                    <div class="feature-text-desc">Quickly locate and open converted files or open destination folders with one click.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Dark & Light Themes</div>
                    <div class="feature-text-desc">Auto-adapts to Windows title bar themes with a customizable dark/light look.</div>
                </div>
            </div>
            <div class="feature-item">
                <div class="feature-bullet">✓</div>
                <div>
                    <div class="feature-text-title">Windows System Tray & Notifications</div>
                    <div class="feature-text-desc">Stay updated with desktop toast notifications when long render tasks finish.</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

# ==================== SYSTEM REQUIREMENTS ====================
st.markdown("""
<div class="section-header">
    <div class="section-title">System Requirements</div>
    <div class="section-desc">Optimized for maximum speed on standard and high-performance Windows PCs</div>
</div>

<table class="sys-table">
    <thead>
        <tr>
            <th>Specification</th>
            <th>Minimum Requirement</th>
            <th>Recommended Specification</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><b>Operating System</b></td>
            <td>Windows 10 (64-bit)</td>
            <td>Windows 11 (64-bit)</td>
        </tr>
        <tr>
            <td><b>Processor (CPU)</b></td>
            <td>Intel Core i3 / AMD Ryzen 3</td>
            <td>Intel Core i5/i7 / AMD Ryzen 5/7 (Multi-core)</td>
        </tr>
        <tr>
            <td><b>System Memory (RAM)</b></td>
            <td>4 GB RAM</td>
            <td>8 GB RAM or higher</td>
        </tr>
        <tr>
            <td><b>Disk Space</b></td>
            <td>500 MB free storage</td>
            <td>2 GB free storage (for local AI models & cache)</td>
        </tr>
        <tr>
            <td><b>Graphics (GPU)</b></td>
            <td>Standard Integrated Graphics</td>
            <td>Dedicated GPU / High-Performance Integrated</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

# ==================== INSTALLATION GUIDE ====================
st.markdown("""
<div class="section-header">
    <div class="section-title">Setup & Installation</div>
    <div class="section-desc">Get CogniFormat up and running on your PC in less than a minute</div>
</div>
""", unsafe_allow_html=True)

i_col1, i_col2, i_col3, i_col4 = st.columns(4)

with i_col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-num">1</div>
        <div class="step-title">Download Setup</div>
        <div class="step-desc">Click the Download button above to get the official <code>CogniFormat_Setup.exe</code> installer file.</div>
    </div>
    """, unsafe_allow_html=True)

with i_col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-num">2</div>
        <div class="step-title">Run Installer</div>
        <div class="step-desc">Double-click the setup file to launch the rapid 1-click Windows installation wizard.</div>
    </div>
    """, unsafe_allow_html=True)

with i_col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-num">3</div>
        <div class="step-title">Auto Config</div>
        <div class="step-desc">The installer configures embedded FFmpeg and local neural models automatically.</div>
    </div>
    """, unsafe_allow_html=True)

with i_col4:
    st.markdown("""
    <div class="step-card">
        <div class="step-num">4</div>
        <div class="step-title">Launch & Convert</div>
        <div class="step-desc">Open CogniFormat from your Desktop or Start Menu and convert unlimited files offline!</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

# ==================== FREQUENTLY ASKED QUESTIONS (FAQ) ====================
st.markdown("""
<div class="section-header">
    <div class="section-title">Frequently Asked Questions</div>
    <div class="section-desc">Everything you need to know about CogniFormat Desktop</div>
</div>
""", unsafe_allow_html=True)

with st.expander("Is CogniFormat completely free?"):
    st.write("Yes! CogniFormat is 100% free to download and use with zero hidden subscriptions, premium paywalls, or feature limits.")

with st.expander("Does CogniFormat require an internet connection?"):
    st.write("No. All video rendering, image conversions, PDF processing, AI upscaling, and background removal models run locally on your device offline. Although you have to be connected to the internet to download the installer. After installation, no internet connection is required.")

with st.expander("Is my privacy safe when converting sensitive documents?"):
    st.write("Absolutely. Because no files leave your computer, your private documents, financial reports, personal photos, and videos stay completely confidential on your machine.")

with st.expander("Are there any file size limits or watermarks?"):
    st.write("None at all. You can convert 4K/8K videos, multi-gigabyte document archives, or thousands of high-res photos without any watermarks or artificial limits.")

with st.expander("How does the AI Background Removal and Upscaling work?"):
    st.write("CogniFormat includes embedded neural network models running via Deep Learning Runtime on your CPU/GPU, producing professional results without cloud APIs.")

st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("""
<hr style="border: 0; height: 1px; background: #e2e8f0; margin-bottom: 1.5rem;">
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding-bottom: 1rem;">
    <p style="margin-bottom: 4px;"><b>CogniFormat Desktop</b> • Version 1.0 — Official Web Release</p>
    <p style="margin-bottom: 0;">100% Private Local Processing • Built for Windows 10 & 11 (64-bit) • © CogniFormat</p>
</div>
""", unsafe_allow_html=True)
