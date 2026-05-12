SUPPORTED_AUDIO_TYPES = [
    "mp3",
    "wav",
    "m4a",
    "flac",
    "ogg",
    "aac",
    "wma",
    "mp4",
    "webm",
]

MODEL_OPTIONS = ["tiny", "base", "small", "medium", "turbo", "large"]
LARGE_MODELS = {"small", "medium", "turbo", "large"}
CLOUD_SAFE_MODELS = {"tiny", "base"}

LANGUAGE_OPTIONS = {
    "Auto-detect": None,
    "Indonesia": "id",
    "English": "en",
    "Jawa": "jw",
    "Sunda": "su",
    "Melayu": "ms",
}

TASK_OPTIONS = ["transcribe", "translate"]

MODEL_SPECS = {
    "tiny": (4, 1),
    "base": (3, 2),
    "small": (3, 3),
    "medium": (2, 4),
    "turbo": (4, 4),
    "large": (1, 5),
}

PRESETS = {
    "Podcast": {
        "model": "base",
        "language": "Auto-detect",
        "task": "transcribe",
        "cleanup": "Paragraphs",
    },
    "Rapat": {
        "model": "base",
        "language": "Indonesia",
        "task": "transcribe",
        "cleanup": "Minutes",
    },
    "Kuliah": {
        "model": "small",
        "language": "Indonesia",
        "task": "transcribe",
        "cleanup": "Paragraphs",
    },
    "Interview": {
        "model": "base",
        "language": "Auto-detect",
        "task": "transcribe",
        "cleanup": "Paragraphs",
    },
    "Subtitle Video": {
        "model": "base",
        "language": "Auto-detect",
        "task": "transcribe",
        "cleanup": "Clean only",
    },
}

CLEANUP_MODES = ["Original", "Clean only", "Paragraphs", "Minutes"]
