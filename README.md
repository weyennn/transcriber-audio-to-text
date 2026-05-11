# Whisper Transcriber

Web app transkripsi audio berbasis [OpenAI Whisper](https://github.com/openai/whisper) dan [Streamlit](https://streamlit.io). Upload file audio, pilih model dan bahasa, dapatkan transkrip dalam format TXT, JSON, atau SRT.

---

## Features

- Multi-file upload sekaligus
- Audio preview sebelum transkripsi
- Pilihan model: tiny / base / small / medium / turbo / large
- Auto-detect bahasa atau pilih manual (Indonesia, English, Jawa, Sunda, Melayu)
- Mode **transcribe** (pertahankan bahasa asli) atau **translate** (output English)
- Stats hasil: jumlah kata, karakter, segmen, durasi
- Export transkrip ke **TXT**, **JSON** (dengan timestamp), **SRT** (subtitle)
- GPU support otomatis jika tersedia

## Model Guide

| Model     | Kecepatan | Akurasi | VRAM   |
|-----------|-----------|---------|--------|
| tiny      | ████      | ▪       | ~1 GB  |
| base      | ███       | ██      | ~1 GB  |
| small     | ██        | ███     | ~2 GB  |
| medium    | █         | ████    | ~5 GB  |
| **turbo** | ███       | ████    | ~6 GB  |
| large     | ▪         | █████   | ~10 GB |

Rekomendasi: **turbo** — keseimbangan terbaik antara kecepatan dan akurasi.

---

## Prerequisites

### System dependency: ffmpeg

Whisper membutuhkan `ffmpeg` yang terinstall di sistem.

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows
# Download dari https://ffmpeg.org/download.html dan tambahkan ke PATH
```

### Python 3.8+

---

## Installation

```bash
git clone https://github.com/weyennn/transcriber-audio-to-text.git
cd transcriber-audio-to-text
pip install -r requirements.txt
```

---

## Usage

```bash
streamlit run whisper_app.py
```

Buka `http://localhost:8501` di browser.

---

## Format Output

| Format | Isi |
|--------|-----|
| TXT    | Teks bersih tanpa timestamp |
| JSON   | Teks + array segmen dengan `start`, `end`, `text` |
| SRT    | File subtitle siap pakai di video editor |

---

## Credits

**Ian**  
Magister Ilmu Komputer, Universitas Gadjah Mada
