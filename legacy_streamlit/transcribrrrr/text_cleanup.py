import re
from typing import Iterable

FILLER_WORDS = {
    "anu",
    "eee",
    "eh",
    "em",
    "hmm",
    "kayak",
    "mmm",
    "uh",
    "umm",
}


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def remove_filler_words(text: str, fillers: Iterable[str] = FILLER_WORDS) -> str:
    pattern = r"\b(" + "|".join(re.escape(word) for word in fillers) + r")\b"
    text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+([,.!?])", r"\1", text)
    return normalize_whitespace(text)


def sentence_case(text: str) -> str:
    parts = re.split(r"([.!?]\s+)", text)
    output = []

    for part in parts:
        if not part or re.match(r"[.!?]\s+", part):
            output.append(part)
            continue
        output.append(part[:1].upper() + part[1:])

    result = "".join(output)
    return result[:1].upper() + result[1:] if result else result


def ensure_sentence_end(text: str) -> str:
    if text and text[-1] not in ".!?":
        return f"{text}."
    return text


def to_paragraphs(text: str, sentences_per_paragraph: int = 3) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs = [
        " ".join(sentences[index : index + sentences_per_paragraph]).strip()
        for index in range(0, len(sentences), sentences_per_paragraph)
    ]
    return "\n\n".join(paragraph for paragraph in paragraphs if paragraph)


def minutes_format(text: str) -> str:
    paragraphs = to_paragraphs(text, sentences_per_paragraph=2).split("\n\n")
    bullets = "\n".join(f"- {paragraph}" for paragraph in paragraphs if paragraph)
    return f"Catatan:\n{bullets}" if bullets else text


def clean_transcript(text: str, mode: str) -> str:
    if mode == "Original":
        return text

    cleaned = ensure_sentence_end(sentence_case(remove_filler_words(text)))

    if mode == "Paragraphs":
        return to_paragraphs(cleaned)
    if mode == "Minutes":
        return minutes_format(cleaned)
    return cleaned
