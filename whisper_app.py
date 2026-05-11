# -*- coding: utf-8 -*-
"""
Whisper Transcription App — Streamlit Version

Run with:
    streamlit run whisper_app.py
"""

import streamlit as st
import whisper
import torch
import json
import os
import tempfile
from pathlib import Path

# ─────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Whisper Transcriber",
    page_icon="🎙️",
    layout="wide",
)

# ─────────────────────────────────────────────
#  Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

    .stApp { background: #f5f7fa; color: #1a1d27; }

    h1 {
        font-family: 'IBM Plex Mono', monospace;
        color: #1a1d27;
        font-size: 1.75rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        font-family: 'IBM Plex Mono', monospace;
        color: #2d3148;
        font-weight: 500;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e8eaf2;
    }

    /* Primary button */
    .stButton > button {
        background: #009e82;
        color: #ffffff;
        font-weight: 700;
        border: none;
        border-radius: 6px;
        padding: 0.65rem 1.5rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.88rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.18s ease;
    }
    .stButton > button:hover {
        background: #008a71;
        box-shadow: 0 4px 16px rgba(0, 158, 130, 0.2);
        transform: translateY(-1px);
    }

    /* Download buttons */
    [data-testid="stDownloadButton"] > button {
        background: transparent;
        color: #009e82;
        border: 1px solid #009e8240;
        border-radius: 6px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.82rem;
        letter-spacing: 0.5px;
        transition: all 0.18s ease;
        width: 100%;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: #009e8210;
        border-color: #009e8280;
    }

    /* Transcript box */
    .transcript-box {
        background: #ffffff;
        border: 1px solid #e4e7f0;
        border-radius: 10px;
        padding: 1.4rem 1.8rem;
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.95rem;
        line-height: 1.85;
        white-space: pre-wrap;
        max-height: 420px;
        overflow-y: auto;
        color: #2d3148;
    }
    .transcript-box::-webkit-scrollbar { width: 4px; }
    .transcript-box::-webkit-scrollbar-track { background: transparent; }
    .transcript-box::-webkit-scrollbar-thumb { background: #d0d4e4; border-radius: 2px; }

    /* Segment list */
    .segment-table {
        border: 1px solid #e4e7f0;
        border-radius: 10px;
        overflow: hidden;
        max-height: 420px;
        overflow-y: auto;
        background: #ffffff;
    }
    .segment-table::-webkit-scrollbar { width: 4px; }
    .segment-table::-webkit-scrollbar-track { background: transparent; }
    .segment-table::-webkit-scrollbar-thumb { background: #d0d4e4; border-radius: 2px; }
    .segment-row {
        display: flex;
        gap: 1.2rem;
        padding: 0.6rem 1.2rem;
        border-bottom: 1px solid #f0f2f8;
        font-size: 0.87rem;
        transition: background 0.12s;
    }
    .segment-row:last-child { border-bottom: none; }
    .segment-row:hover { background: #f5f7fc; }
    .seg-time {
        font-family: 'IBM Plex Mono', monospace;
        color: #009e82;
        min-width: 148px;
        flex-shrink: 0;
        font-size: 0.8rem;
        padding-top: 2px;
    }

    /* Info pills */
    .info-pill {
        display: inline-block;
        background: #eef0f8;
        border: 1px solid #e0e3f0;
        border-radius: 4px;
        padding: 0.2rem 0.7rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.73rem;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
        color: #8890a8;
        letter-spacing: 0.3px;
    }
    .info-pill span { color: #009e82; font-weight: 500; }

    /* Device badge */
    .badge-gpu {
        display: inline-block;
        background: #009e8214;
        border: 1px solid #009e8240;
        color: #009e82;
        border-radius: 4px;
        padding: 0.2rem 0.7rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.73rem;
        letter-spacing: 0.5px;
    }
    .badge-cpu {
        display: inline-block;
        background: #e8760014;
        border: 1px solid #e8760040;
        color: #c46200;
        border-radius: 4px;
        padding: 0.2rem 0.7rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.73rem;
        letter-spacing: 0.5px;
    }

    /* Section label */
    .label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        color: #b0b8cc;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin-bottom: 0.7rem;
    }

    /* File header */
    .file-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.9rem;
        color: #b0b8cc;
        padding: 0.8rem 0 0.6rem;
        border-bottom: 1px solid #e4e7f0;
        margin-bottom: 1rem;
    }
    .file-header span { color: #1a1d27; }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
    }
    .empty-state p { font-size: 0.85rem; color: #b0b8cc; margin: 0; }
    .empty-state small { font-size: 0.75rem; color: #cdd0dc; }

    /* Model comparison table */
    .model-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.78rem;
    }
    .model-table th {
        color: #b0b8cc;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-size: 0.68rem;
        padding: 0.4rem 0.4rem;
        border-bottom: 1px solid #e8eaf2;
        text-align: left;
        font-weight: 400;
    }
    .model-table td {
        padding: 0.32rem 0.4rem;
        color: #b0b8cc;
        border-bottom: 1px solid #f5f7fa;
    }
    .model-table tr.active td { color: #1a1d27; }
    .bar-fill {
        display: inline-block;
        height: 5px;
        width: 9px;
        border-radius: 2px;
        background: #009e82;
        margin-right: 2px;
        vertical-align: middle;
    }
    .bar-empty {
        display: inline-block;
        height: 5px;
        width: 9px;
        border-radius: 2px;
        background: #dde0ea;
        margin-right: 2px;
        vertical-align: middle;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #e4e7f0;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: #b0b8cc;
        padding: 0.5rem 1.2rem;
        border-radius: 0;
        letter-spacing: 0.3px;
    }
    .stTabs [aria-selected="true"] {
        color: #009e82 !important;
        border-bottom: 2px solid #009e82;
        background: transparent !important;
    }

    hr { border-color: #e4e7f0 !important; margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def format_time(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


def srt_time(seconds: float) -> str:
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(segments: list) -> str:
    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{srt_time(seg['start'])} --> {srt_time(seg['end'])}")
        lines.append(seg["text"])
        lines.append("")
    return "\n".join(lines)


def bars(level: int, total: int = 5) -> str:
    return "".join(
        f'<span class="bar-fill"></span>' if i < level else f'<span class="bar-empty"></span>'
        for i in range(total)
    )


@st.cache_resource(show_spinner=False)
def load_model(model_size: str):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return whisper.load_model(model_size, device=device), device


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Configuration")

    model_size = st.selectbox(
        "Model",
        ["tiny", "base", "small", "medium", "turbo", "large"],
        index=4,
        help="turbo = recommended — fast + accurate",
    )

    language_map = {
        "Auto-detect": None,
        "Indonesia": "id",
        "English": "en",
        "Jawa": "jw",
        "Sunda": "su",
        "Melayu": "ms",
    }
    lang_label = st.selectbox("Language", list(language_map.keys()), index=1)
    language = language_map[lang_label]

    task = st.radio(
        "Task",
        ["transcribe", "translate"],
        help="translate: output in English regardless of source language",
    )

    st.markdown("---")
    st.markdown('<div class="label">Model Comparison</div>', unsafe_allow_html=True)

    model_specs = {
        "tiny":   (4, 1),
        "base":   (3, 2),
        "small":  (3, 3),
        "medium": (2, 4),
        "turbo":  (4, 4),
        "large":  (1, 5),
    }

    rows = ""
    for name, (spd, acc) in model_specs.items():
        active = ' class="active"' if name == model_size else ""
        marker = "→ " if name == model_size else "&nbsp;&nbsp; "
        rows += (
            f"<tr{active}>"
            f"<td>{marker}{name}</td>"
            f"<td>{bars(spd)}</td>"
            f"<td>{bars(acc)}</td>"
            f"</tr>"
        )

    st.markdown(
        f"""<table class="model-table">
            <thead><tr><th>Model</th><th>Speed</th><th>Accuracy</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown('<div class="label">Output Formats</div>', unsafe_allow_html=True)
    st.markdown(
        """<div style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#555;line-height:2.2;">
        TXT &nbsp;&nbsp;&nbsp; Plain text<br>
        JSON &nbsp;&nbsp; With timestamps<br>
        SRT &nbsp;&nbsp;&nbsp; Subtitle file
        </div>""",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  Main area
# ─────────────────────────────────────────────
st.markdown("# Whisper Transcriber")
st.markdown(
    '<p style="color:#9ca3b8;margin-top:-0.8rem;margin-bottom:1.4rem;font-size:0.88rem;">'
    "Upload audio &nbsp;·&nbsp; Get transcript &nbsp;·&nbsp; Export TXT / JSON / SRT"
    "</p>",
    unsafe_allow_html=True,
)

is_gpu = torch.cuda.is_available()
badge_class = "badge-gpu" if is_gpu else "badge-cpu"
device_label = "GPU" if is_gpu else "CPU"

st.markdown(
    f'<span class="info-pill">model: <span>{model_size}</span></span>'
    f'<span class="info-pill">lang: <span>{lang_label.lower()}</span></span>'
    f'<span class="info-pill">task: <span>{task}</span></span>'
    f'<span class="{badge_class}">{device_label}</span>',
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload audio files",
    type=["mp3", "wav", "m4a", "flac", "ogg", "aac", "wma", "mp4", "webm"],
    accept_multiple_files=True,
)

if uploaded_files:
    st.markdown("<br>", unsafe_allow_html=True)

    # Audio preview — shown immediately after upload
    for uploaded_file in uploaded_files:
        st.markdown(
            f'<div class="file-header">/ <span>{uploaded_file.name}</span></div>',
            unsafe_allow_html=True,
        )
        st.audio(uploaded_file)

    st.markdown("<br>", unsafe_allow_html=True)

    n = len(uploaded_files)
    st.markdown(
        f'<p style="color:#b0b8cc;font-size:0.8rem;margin-bottom:0.6rem;'
        f'font-family:\'IBM Plex Mono\',monospace;">'
        f'{n} file{"s" if n > 1 else ""} ready · select model and language in the sidebar</p>',
        unsafe_allow_html=True,
    )
    run_btn = st.button("Transcribe", use_container_width=True)

    if run_btn:
        with st.spinner(f'Loading model "{model_size}"…'):
            model, device = load_model(model_size)
        st.success(f"Model **{model_size}** ready on {device.upper()}")

        for uploaded_file in uploaded_files:
            st.markdown("---")
            st.markdown(
                f'<div class="file-header">/ <span>{uploaded_file.name}</span></div>',
                unsafe_allow_html=True,
            )

            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                options = {}
                if language:
                    options["language"] = language
                if task:
                    options["task"] = task

                with st.spinner(f"Transcribing {uploaded_file.name}…"):
                    result = model.transcribe(tmp_path, **options)

                detected_lang = result.get("language", "unknown")
                text = result["text"].strip()
                segments = [
                    {
                        "id"   : seg["id"],
                        "start": round(seg["start"], 2),
                        "end"  : round(seg["end"], 2),
                        "text" : seg["text"].strip(),
                    }
                    for seg in result.get("segments", [])
                ]

                word_count = len(text.split())
                char_count = len(text)
                duration   = segments[-1]["end"] if segments else 0

                st.markdown(
                    f'<span class="info-pill">detected: <span>{detected_lang.upper()}</span></span>'
                    f'<span class="info-pill">words: <span>{word_count:,}</span></span>'
                    f'<span class="info-pill">chars: <span>{char_count:,}</span></span>'
                    f'<span class="info-pill">segments: <span>{len(segments)}</span></span>'
                    f'<span class="info-pill">duration: <span>{format_time(duration)}</span></span>',
                    unsafe_allow_html=True,
                )

                tab1, tab2, tab3 = st.tabs(["Transcript", "Segments", "Export"])

                with tab1:
                    st.markdown(
                        f'<div class="transcript-box">{text}</div>',
                        unsafe_allow_html=True,
                    )

                with tab2:
                    if segments:
                        rows_html = "".join(
                            f'<div class="segment-row">'
                            f'<span class="seg-time">[{format_time(seg["start"])} → {format_time(seg["end"])}]</span>'
                            f'<span>{seg["text"]}</span>'
                            f'</div>'
                            for seg in segments
                        )
                        st.markdown(
                            f'<div class="segment-table">{rows_html}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.info("No segment data available.")

                with tab3:
                    base = Path(uploaded_file.name).stem
                    st.markdown('<div class="label" style="margin-top:0.8rem;">Download</div>', unsafe_allow_html=True)

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.download_button(
                            "TXT",
                            data=text.encode("utf-8"),
                            file_name=f"{base}_transcript.txt",
                            mime="text/plain",
                            use_container_width=True,
                        )
                    with c2:
                        json_data = json.dumps(
                            {
                                "file": uploaded_file.name,
                                "language": detected_lang,
                                "text": text,
                                "segments": segments,
                            },
                            ensure_ascii=False,
                            indent=2,
                        )
                        st.download_button(
                            "JSON",
                            data=json_data.encode("utf-8"),
                            file_name=f"{base}_transcript.json",
                            mime="application/json",
                            use_container_width=True,
                        )
                    with c3:
                        st.download_button(
                            "SRT",
                            data=build_srt(segments).encode("utf-8"),
                            file_name=f"{base}_transcript.srt",
                            mime="text/plain",
                            use_container_width=True,
                        )

            except Exception as e:
                st.error(f"Failed to transcribe **{uploaded_file.name}**: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

else:
    st.markdown(
        '<div class="empty-state">'
        "<p>No files selected</p>"
        "<small>MP3 · WAV · M4A · FLAC · OGG · AAC · WMA · MP4 · WEBM</small>"
        "</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align:center;padding:0.4rem 0 0.8rem;">'
    '<p style="color:#1a1d27;font-size:0.82rem;font-family:IBM Plex Mono,monospace;font-weight:500;margin-bottom:0.15rem;">Ian</p>'
    '<p style="color:#b0b8cc;font-size:0.75rem;font-family:IBM Plex Sans,monospace;margin-bottom:0.6rem;">'
    "Magister Ilmu Komputer &nbsp;·&nbsp; Universitas Gadjah Mada"
    "</p>"
    '<p style="color:#d0d4e0;font-size:0.7rem;font-family:IBM Plex Mono,monospace;">'
    "OpenAI Whisper &nbsp;·&nbsp; Streamlit"
    "</p>"
    "</div>",
    unsafe_allow_html=True,
)
