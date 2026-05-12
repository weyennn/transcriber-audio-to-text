import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import torch
import whisper

from .diarization import diarize_audio, label_segments_with_speakers


def get_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def load_whisper_model(model_size: str) -> Tuple[Any, str]:
    device = get_device()
    return whisper.load_model(model_size, device=device), device


def transcribe_upload(
    uploaded_file: Any,
    model: Any,
    language: Optional[str],
    task: str,
    diarization_token: Optional[str] = None,
) -> Dict[str, Any]:
    suffix = Path(uploaded_file.name).suffix
    tmp_path = None

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        options = {"task": task}
        if language:
            options["language"] = language

        result = model.transcribe(tmp_path, **options)
        text = result["text"].strip()
        segments = [
            {
                "id": segment["id"],
                "start": round(segment["start"], 2),
                "end": round(segment["end"], 2),
                "text": segment["text"].strip(),
            }
            for segment in result.get("segments", [])
        ]

        if diarization_token:
            speaker_turns = diarize_audio(tmp_path, diarization_token)
            segments = label_segments_with_speakers(segments, speaker_turns)

        return {
            "file": uploaded_file.name,
            "language": result.get("language", "unknown"),
            "text": text,
            "segments": segments,
        }
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
