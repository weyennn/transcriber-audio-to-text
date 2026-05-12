CSS = """
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

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e8eaf2;
    }

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

    .label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        color: #b0b8cc;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin-bottom: 0.7rem;
    }

    .file-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.9rem;
        color: #b0b8cc;
        padding: 0.8rem 0 0.6rem;
        border-bottom: 1px solid #e4e7f0;
        margin-bottom: 1rem;
    }
    .file-header span { color: #1a1d27; }

    .empty-state {
        text-align: center;
        padding: 5rem 2rem;
    }
    .empty-state p { font-size: 0.85rem; color: #b0b8cc; margin: 0; }
    .empty-state small { font-size: 0.75rem; color: #cdd0dc; }

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

    .next-step {
        background: #f0fdf8;
        border: 1px solid #009e8230;
        border-left: 3px solid #009e82;
        border-radius: 6px;
        padding: 0.9rem 1.2rem;
        margin-top: 1.2rem;
        font-size: 0.84rem;
        color: #2d3148;
        line-height: 1.7;
    }
    .next-step .next-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #009e82;
        margin-bottom: 0.35rem;
    }
    .next-step code {
        background: #d6f5ee;
        border-radius: 3px;
        padding: 0.1rem 0.4rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: #007a65;
    }

    .stTextArea textarea {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.88rem;
        line-height: 1.75;
        background: #ffffff;
        border: 1px solid #e4e7f0;
        border-radius: 8px;
        color: #2d3148;
        resize: vertical;
    }
    .stTextArea textarea:focus {
        border-color: #009e8260;
        box-shadow: 0 0 0 2px #009e8215;
    }
</style>
"""
