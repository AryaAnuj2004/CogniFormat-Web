# CogniFormat Web — Official Landing Page & Download Portal

[![Windows Version](https://img.shields.io/badge/Windows-v1.0.0-blue.svg)](https://github.com/AryaAnuj2004/CogniFormat-Web)
[![Streamlit App](https://img.shields.io/badge/Built%20With-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**CogniFormat Web** is the official web application and download portal for **CogniFormat Desktop** — an all-in-one, 100% offline, privacy-first AI media converter, document processor, and image enhancer for Windows.

This web application built with Streamlit serves as the distribution platform for CogniFormat Desktop. It features strict lead capture validation (using syntax checks, disposable domain filtering, and real-time DNS MX record resolution), dynamic installer download gating, and a rich interactive showcase of CogniFormat's power studios.

---

## 🌟 Key Web Portal Features

- 🔒 **Gated Download & Lead Capture**: Secure download unlock system that requires authorized user verification.
- ✉️ **Strict Real-Time Email Validation**:
  - **Syntax & Deliverability Check**: Powered by `email-validator`.
  - **Disposable Domain Filtering**: Blocks temporary email services like Mailinator, 10MinuteMail, Yopmail, etc.
  - **Numeric Prefix Filtering**: Rejects fake numeric domain prefixes.
  - **Authoritative DNS MX Resolution**: Performs live Mail Exchange (MX) DNS queries via `dnspython` to verify domain authenticity.
- 📊 **Lead Data Tracking**: Automatically stores verified user registrations in `data/leads.csv`.
- 🎨 **Premium Aesthetic & Custom Design**: Custom CSS styling with Google Fonts (*Plus Jakarta Sans* and *Inter*), smooth gradients, card hover animations, and hidden default Streamlit chrome.
- 🖼️ **Visual Workspace Gallery**: Interactive before/after workspace previews and high-speed batch queue manager screenshots.
- 💻 **System Requirements & Setup Guide**: Built-in interactive guides for quick onboarding.

---

## 🚀 CogniFormat Desktop Overview

CogniFormat Desktop is a hardware-accelerated, zero-subscription desktop software packed with 6 powerful studios running 100% locally on your PC:

| Studio | Core Capabilities |
| :--- | :--- |
| 🖼️ **Image Studio & AI Enhancer** | AI Background Removal, AI Image Upscaling, AI Deblurring, side-by-side split view, format conversion (JPG, PNG, WEBP, BMP), crop/rotate, Images-to-PDF. |
| 🎬 **Video Studio & Smart Framing** | Format conversion & compression (MP4, MKV, AVI, MOV, WEBM, GIF), next-gen codecs (H.264, H.265/HEVC, VP9, AV1), visual trimming, smart aspect ratio reframing (16:9 to 9:16 for Reels/Shorts), AI focus tracking. |
| 📄 **PDF & Document Studio** | Merge, split, compress PDFs, extract embedded images/pages, visual page organizer (reorder, rotate, delete), convert Office docs (DOCX, XLSX, PPTX, TXT, HTML, EPUB) to PDF. |
| 🎵 **Audio Converter & Editor** | Convert formats (MP3, WAV, AAC, M4A, FLAC, OGG), join audio tracks, precision waveform timeline trimmer. |
| 🤖 **CogniBot AI Assistant** | 100% local, offline AI assistant for in-app help and format guidance without external API keys. |
| ⚡ **UI & Workflow** | Global quick search (`Ctrl + K`), background queue manager, system tray notifications, dark/light themes. |

---

## 🛠️ Project Structure

```text
CogniFormat Web/
├── app.py                  # Main Streamlit Web Application
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules for virtualenvs, leads, and binaries
├── assets/                 # App logos, brand assets, and screenshots
│   ├── logo_black.png
│   ├── screenshots/
│   │   ├── dashboard.jpg
│   │   └── batch.jpg
│   └── downloads/          # Local setup executable target directory
│       └── CogniFormat_Setup.exe (ignored in git)
└── data/                   # Generated leads CSV store
    └── leads.csv (ignored in git)
```

---

## 💻 Installation & Running Locally

### Prerequisites

- Python 3.9 or higher
- Git

### Quickstart Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AryaAnuj2004/CogniFormat-Web.git
   cd CogniFormat-Web
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Web Portal:**
   ```bash
   streamlit run app.py
   ```

   The app will open automatically in your browser at `http://localhost:8501`.

---

## ⚙️ Environment Variables

Optional environment variables can be configured:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SETUP_EXE_URL` | Fallback external direct download URL for `CogniFormat_Setup.exe` if the file is hosted on cloud storage instead of local disk `assets/downloads/`. | `""` |

---

## 📄 Dependencies

- **`streamlit`** — Interactive web interface framework
- **`pandas`** — Data manipulation and leads tracking
- **`pillow`** — Image loading and header branding
- **`email-validator`** — Email syntax verification
- **`dnspython`** — Live DNS MX record checking

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📬 Contact & Support

For feedback, support, or inquiries regarding CogniFormat:
- Repository: [AryaAnuj2004/CogniFormat-Web](https://github.com/AryaAnuj2004/CogniFormat-Web)
