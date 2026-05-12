from typing import Any, Dict, List, Tuple


def is_available() -> bool:
    try:
        import pyannote.audio  # noqa: F401
    except ImportError:
        return False
    return True


def explain_unavailable() -> str:
    return (
        "Speaker diarization butuh dependency opsional `pyannote.audio` dan "
        "Hugging Face token. Install dependency tersebut saat menjalankan lokal "
        "jika ingin memisahkan pembicara."
    )


def diarize_audio(audio_path: str, hf_token: str) -> List[Tuple[float, float, str]]:
    from pyannote.audio import Pipeline

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=hf_token,
    )
    diarization = pipeline(audio_path)

    return [
        (turn.start, turn.end, speaker)
        for turn, _, speaker in diarization.itertracks(yield_label=True)
    ]


def label_segments_with_speakers(
    segments: List[Dict[str, Any]], speaker_turns: List[Tuple[float, float, str]]
) -> List[Dict[str, Any]]:
    labeled_segments = []

    for segment in segments:
        midpoint = (segment["start"] + segment["end"]) / 2
        speaker = "Speaker ?"

        for start, end, label in speaker_turns:
            if start <= midpoint <= end:
                speaker = label
                break

        labeled_segment = dict(segment)
        labeled_segment["speaker"] = speaker
        labeled_segments.append(labeled_segment)

    return labeled_segments
