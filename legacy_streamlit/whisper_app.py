# -*- coding: utf-8 -*-
"""
Whisper Transcription App - Streamlit Version

Run with:
    streamlit run whisper_app.py
"""

from pathlib import Path

import streamlit as st

from transcribrrrr.config import (
    CLEANUP_MODES,
    CLOUD_SAFE_MODELS,
    LANGUAGE_OPTIONS,
    LARGE_MODELS,
    MODEL_OPTIONS,
    MODEL_SPECS,
    PRESETS,
    SUPPORTED_AUDIO_TYPES,
    TASK_OPTIONS,
)
from transcribrrrr.diarization import explain_unavailable, is_available
from transcribrrrr.exporters import build_json, build_srt, build_zip
from transcribrrrr.formatting import bars, format_time, safe_html
from transcribrrrr.styles import CSS
from transcribrrrr.system_checks import has_ffmpeg
from transcribrrrr.text_cleanup import clean_transcript
from transcribrrrr.transcription import (
    get_device,
    load_whisper_model,
    transcribe_upload,
)

st.set_page_config(
    page_title="Whisper Transcriber",
    page_icon="🎙️",
    layout="wide",
)
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_model(model_size: str):
    return load_whisper_model(model_size)


def model_index(model_name: str) -> int:
    return MODEL_OPTIONS.index(model_name) if model_name in MODEL_OPTIONS else 0


def option_index(options, value) -> int:
    return options.index(value) if value in options else 0


def render_model_table(model_size: str) -> None:
    rows = ""
    for name, (speed, accuracy) in MODEL_SPECS.items():
        active = ' class="active"' if name == model_size else ""
        marker = "→ " if name == model_size else "&nbsp;&nbsp; "
        cloud_tag = (
            ' <span style="color:#009e82;font-size:0.65rem;">cloud</span>'
            if name in CLOUD_SAFE_MODELS
            else ""
        )
        rows += (
            f"<tr{active}>"
            f"<td>{marker}{name}{cloud_tag}</td>"
            f"<td>{bars(speed)}</td>"
            f"<td>{bars(accuracy)}</td>"
            f"</tr>"
        )

    st.markdown(
        f"""<table class="model-table">
            <thead><tr><th>Model</th><th>Speed</th><th>Accuracy</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""",
        unsafe_allow_html=True,
    )


def render_badges(
    model_size: str, lang_label: str, task: str, cleanup_mode: str
) -> None:
    is_gpu = get_device() == "cuda"
    badge_class = "badge-gpu" if is_gpu else "badge-cpu"
    device_label = "GPU" if is_gpu else "CPU"

    st.markdown(
        f'<span class="info-pill">model: <span>{safe_html(model_size)}</span></span>'
        f'<span class="info-pill">lang: <span>{safe_html(lang_label.lower())}</span></span>'
        f'<span class="info-pill">task: <span>{safe_html(task)}</span></span>'
        f'<span class="info-pill">cleanup: <span>{safe_html(cleanup_mode)}</span></span>'
        f'<span class="{badge_class}">{device_label}</span>',
        unsafe_allow_html=True,
    )


def render_file_header(file_name: str) -> None:
    st.markdown(
        f'<div class="file-header">/ <span>{safe_html(file_name)}</span></div>',
        unsafe_allow_html=True,
    )


def render_stats(result) -> None:
    text = result.get("cleaned_text") or result["text"]
    segments = result["segments"]
    duration = segments[-1]["end"] if segments else 0

    st.markdown(
        f'<span class="info-pill">detected: <span>{safe_html(result["language"]).upper()}</span></span>'
        f'<span class="info-pill">words: <span>{len(text.split()):,}</span></span>'
        f'<span class="info-pill">chars: <span>{len(text):,}</span></span>'
        f'<span class="info-pill">segments: <span>{len(segments)}</span></span>'
        f'<span class="info-pill">duration: <span>{format_time(duration)}</span></span>',
        unsafe_allow_html=True,
    )


def render_segments(segments) -> None:
    if not segments:
        st.info("No segment data available.")
        return

    rows = []
    for segment in segments:
        speaker = f'{safe_html(segment["speaker"])}: ' if segment.get("speaker") else ""
        rows.append(
            f'<div class="segment-row">'
            f'<span class="seg-time">[{format_time(segment["start"])} → {format_time(segment["end"])}]</span>'
            f"<span>{speaker}{safe_html(segment['text'])}</span>"
            f"</div>"
        )

    rows_html = "".join(rows)
    st.markdown(f'<div class="segment-table">{rows_html}</div>', unsafe_allow_html=True)


def render_downloads(result) -> None:
    base = Path(result["file"]).stem
    transcript = result.get("cleaned_text") or result["text"]

    st.markdown(
        '<div class="label" style="margin-top:0.8rem;">Download</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "TXT",
            data=transcript.encode("utf-8"),
            file_name=f"{base}_transcript.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "JSON",
            data=build_json(result).encode("utf-8"),
            file_name=f"{base}_transcript.json",
            mime="application/json",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "SRT",
            data=build_srt(result["segments"]).encode("utf-8"),
            file_name=f"{base}_transcript.srt",
            mime="text/plain",
            use_container_width=True,
        )


def render_result(result) -> None:
    render_file_header(result["file"])
    render_stats(result)

    transcript = result.get("cleaned_text") or result["text"]
    tab1, tab2, tab3 = st.tabs(["Transcript", "Segments", "Export"])

    with tab1:
        st.markdown(
            f'<div class="transcript-box">{safe_html(transcript)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="label" style="margin-top:1rem;">Copy-friendly</div>',
            unsafe_allow_html=True,
        )
        st.text_area(
            label="copy",
            value=transcript,
            height=180,
            label_visibility="collapsed",
            key=f"copy_{result['file']}",
        )

    with tab2:
        render_segments(result["segments"])

    with tab3:
        render_downloads(result)


with st.sidebar:
    st.markdown("## Configuration")

    preset_name = st.selectbox("Preset", list(PRESETS.keys()), index=1)
    preset = PRESETS[preset_name]

    model_size = st.selectbox(
        "Model",
        MODEL_OPTIONS,
        index=model_index(preset["model"]),
        help="tiny/base untuk cloud. Gunakan medium/turbo/large saat resource lokal memadai.",
    )

    if model_size in LARGE_MODELS:
        st.warning(
            f"Model **{model_size}** membutuhkan RAM besar. Streamlit Cloud free tier biasanya cocok untuk **tiny** atau **base**.",
            icon="⚠️",
        )

    lang_labels = list(LANGUAGE_OPTIONS.keys())
    lang_label = st.selectbox(
        "Language",
        lang_labels,
        index=option_index(lang_labels, preset["language"]),
    )
    language = LANGUAGE_OPTIONS[lang_label]

    task = st.radio(
        "Task",
        TASK_OPTIONS,
        index=option_index(TASK_OPTIONS, preset["task"]),
        help="translate: output in English regardless of source language",
    )

    cleanup_mode = st.selectbox(
        "Transcript cleanup",
        CLEANUP_MODES,
        index=option_index(CLEANUP_MODES, preset["cleanup"]),
    )

    enable_diarization = st.checkbox(
        "Speaker diarization",
        help="Opsional. Butuh pyannote.audio dan Hugging Face token saat berjalan lokal.",
    )
    hf_token = ""
    if enable_diarization:
        hf_token = st.text_input(
            "Hugging Face token",
            type="password",
            help="Token dipakai langsung saat runtime dan tidak disimpan.",
        )
        if not is_available():
            st.info(explain_unavailable())
        elif not hf_token:
            st.info("Masukkan Hugging Face token untuk menjalankan diarization.")

    st.markdown("---")
    st.markdown('<div class="label">Model Comparison</div>', unsafe_allow_html=True)
    render_model_table(model_size)

    st.markdown("---")
    st.markdown('<div class="label">Output Formats</div>', unsafe_allow_html=True)
    st.markdown(
        """<div style="font-family:'IBM Plex Mono',monospace;font-size:0.78rem;color:#555;line-height:2.2;">
        TXT &nbsp;&nbsp;&nbsp; Plain text<br>
        JSON &nbsp;&nbsp; With timestamps<br>
        SRT &nbsp;&nbsp;&nbsp; Subtitle file<br>
        ZIP &nbsp;&nbsp;&nbsp; Batch export
        </div>""",
        unsafe_allow_html=True,
    )


st.markdown("# Whisper Transcriber")
st.markdown(
    '<p style="color:#9ca3b8;margin-top:-0.8rem;margin-bottom:1.4rem;font-size:0.88rem;">'
    "Upload audio &nbsp;·&nbsp; Track progress &nbsp;·&nbsp; Clean transcript &nbsp;·&nbsp; Export TXT / JSON / SRT / ZIP"
    "</p>",
    unsafe_allow_html=True,
)

render_badges(model_size, lang_label, task, cleanup_mode)

if not has_ffmpeg():
    st.error(
        "ffmpeg belum tersedia di sistem. Install ffmpeg dulu agar Whisper bisa membaca audio/video."
    )

st.markdown("<br>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload audio files",
    type=SUPPORTED_AUDIO_TYPES,
    accept_multiple_files=True,
)

if "results" not in st.session_state:
    st.session_state.results = []

if uploaded_files:
    st.markdown("<br>", unsafe_allow_html=True)

    for uploaded_file in uploaded_files:
        render_file_header(uploaded_file.name)
        st.audio(uploaded_file)

    st.markdown("<br>", unsafe_allow_html=True)
    file_count = len(uploaded_files)
    st.markdown(
        f'<p style="color:#b0b8cc;font-size:0.8rem;margin-bottom:0.6rem;'
        "font-family:'IBM Plex Mono',monospace;\">"
        f'{file_count} file{"s" if file_count > 1 else ""} ready · preset: {safe_html(preset_name)}</p>',
        unsafe_allow_html=True,
    )

    run_btn = st.button(
        "Transcribe", use_container_width=True, disabled=not has_ffmpeg()
    )

    if run_btn:
        st.session_state.results = []
        status = st.empty()
        progress = st.progress(0)

        status.info(f'Loading model "{model_size}"...')
        model, device = load_model(model_size)
        status.success(f"Model {model_size} ready on {device.upper()}")

        diarization_token = (
            hf_token if enable_diarization and is_available() and hf_token else None
        )

        for index, uploaded_file in enumerate(uploaded_files, 1):
            status.info(f"Transcribing {index}/{file_count}: {uploaded_file.name}")
            try:
                result = transcribe_upload(
                    uploaded_file=uploaded_file,
                    model=model,
                    language=language,
                    task=task,
                    diarization_token=diarization_token,
                )
                result["cleanup_mode"] = cleanup_mode
                result["cleaned_text"] = clean_transcript(result["text"], cleanup_mode)
                st.session_state.results.append(result)
                status.success(f"Done {index}/{file_count}: {uploaded_file.name}")
            except Exception as exc:
                st.error(f"Failed to transcribe **{uploaded_file.name}**: {exc}")
            finally:
                progress.progress(index / file_count)

        status.success(
            f"Finished {len(st.session_state.results)}/{file_count} file(s)."
        )

if st.session_state.results:
    st.markdown("---")
    st.markdown("## Results")

    if len(st.session_state.results) > 1:
        st.download_button(
            "Download ZIP",
            data=build_zip(st.session_state.results),
            file_name="transcripts.zip",
            mime="application/zip",
            use_container_width=True,
        )

    for result in st.session_state.results:
        st.markdown("---")
        render_result(result)
else:
    st.markdown(
        '<div class="empty-state">'
        "<p>No transcript yet</p>"
        "<small>MP3 · WAV · M4A · FLAC · OGG · AAC · WMA · MP4 · WEBM</small>"
        "</div>",
        unsafe_allow_html=True,
    )

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
