import io
import json
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .formatting import srt_time


def build_srt(segments: List[Dict[str, Any]]) -> str:
    lines = []
    for index, segment in enumerate(segments, 1):
        lines.append(str(index))
        lines.append(f"{srt_time(segment['start'])} --> {srt_time(segment['end'])}")
        lines.append(segment["text"])
        lines.append("")
    return "\n".join(lines)


def build_json(result: Dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=False, indent=2)


def build_zip(results: Iterable[Dict[str, Any]]) -> bytes:
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for result in results:
            base = Path(result["file"]).stem
            transcript = result.get("cleaned_text") or result["text"]

            archive.writestr(f"{base}/{base}_transcript.txt", transcript)
            archive.writestr(f"{base}/{base}_transcript.json", build_json(result))
            archive.writestr(
                f"{base}/{base}_transcript.srt", build_srt(result["segments"])
            )

    return buffer.getvalue()
