# Whisper Turbo Transcriber - Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/weyennn/transcriber-audio-to-text/blob/main/colab_run.ipynb)

Notebook transkripsi audio/video berbasis [OpenAI Whisper](https://github.com/openai/whisper), dibuat untuk jalan gratis di Google Colab dengan GPU. Default model memakai `turbo`, lalu hasil bisa didownload sebagai TXT, JSON, SRT, dan ZIP.

---

## Fitur

- Jalan langsung di Google Colab, tanpa deploy server
- Default model `turbo` untuk Colab GPU
- Upload banyak file sekaligus
- Pilihan model: `tiny`, `base`, `small`, `medium`, `turbo`, `large`
- Auto-detect bahasa atau pilih Indonesia, English, Jawa, Sunda, Melayu
- Mode `transcribe` atau `translate`
- Cleanup transkrip: original, clean only, paragraphs, minutes
- Export per file:
  - TXT untuk teks bersih
  - JSON untuk data lengkap + timestamp
  - SRT untuk subtitle
- Prompt siap pakai untuk menyempurnakan hasil di ChatGPT, Claude, Gemini, Copilot, atau AI lain
- Batch download dalam `transcripts.zip`

---

## Tutorial Penggunaan

### 1. Buka Notebook

Klik badge **Open in Colab** di atas.

Atau buka manual:

```text
colab_run.ipynb
```

### 2. Aktifkan GPU

Di Google Colab:

```text
Runtime -> Change runtime type -> T4 GPU -> Save
```

Setelah itu jalankan cell dari atas ke bawah.

### 3. Jalankan Setup

Cell setup akan menginstall:

- `ffmpeg`
- `openai-whisper`
- `torch`
- `tqdm`

Setup perlu dijalankan lagi setiap kali sesi Colab baru.

### 4. Pilih Pengaturan

Di cell **Pengaturan Transkripsi**, ubah opsi berikut:

```python
MODEL_SIZE = 'turbo'
LANGUAGE_LABEL = 'Indonesia'
TASK = 'transcribe'
CLEANUP_MODE = 'Paragraphs'
```

Rekomendasi:

| Kebutuhan | Setting |
|---|---|
| Transkrip Indonesia biasa | `LANGUAGE_LABEL = 'Indonesia'`, `TASK = 'transcribe'` |
| Bahasa campuran / tidak yakin | `LANGUAGE_LABEL = 'Auto-detect'` |
| Output English | `TASK = 'translate'` |
| Hasil paling mentah | `CLEANUP_MODE = 'Original'` |
| Transkrip siap baca | `CLEANUP_MODE = 'Paragraphs'` |
| Catatan rapat sederhana | `CLEANUP_MODE = 'Minutes'` |

### 5. Upload File

Jalankan cell **Upload File**, lalu pilih file audio/video dari laptop.

Format umum yang bisa dipakai:

```text
mp3, wav, m4a, flac, ogg, aac, wma, mp4, webm
```

### 6. Jalankan Transkripsi

Jalankan cell **Jalankan Transkripsi**.

Notebook akan:

1. Load model Whisper
2. Proses semua file
3. Simpan output ke folder `outputs/`
4. Membuat file `transcripts.zip`

### 7. Preview dan Download

Cell **Preview Hasil** menampilkan ringkasan hasil.

Cell **Lanjut Rapikan dengan AI** menampilkan prompt yang bisa langsung dicopy ke:

- ChatGPT
- Claude
- Gemini
- Copilot
- AI assistant lain

Notebook juga otomatis menyimpan prompt lengkap ke ZIP sebagai file:

```text
nama-file_ai_prompt.md
```

Kalau upload banyak file, setiap folder hasil punya prompt masing-masing. Cell notebook hanya menampilkan preview prompt file pertama supaya output Colab tidak terlalu panjang.

Cell **Download ZIP** akan mendownload:

```text
transcripts.zip
```

Isi ZIP:

```text
nama-file/
  nama-file_transcript.txt
  nama-file_transcript.json
  nama-file_transcript.srt
  nama-file_ai_prompt.md
```

---

## Menyempurnakan Transkrip dengan AI

Setelah ZIP selesai, buka file `.txt` atau `_ai_prompt.md`.

Cara paling simpel:

1. Buka ChatGPT, Claude, Gemini, atau Copilot
2. Copy isi file `_ai_prompt.md`
3. Paste ke AI
4. Kirim

Catatan privasi: jangan kirim transkrip berisi data sensitif, rahasia kerja, data pasien, atau informasi pribadi ke AI eksternal kalau belum yakin dengan kebijakan privasi layanan tersebut.

Prompt default meminta AI untuk:

- memperbaiki tanda baca dan kapitalisasi
- merapikan paragraf
- menjaga makna asli
- tidak menambah informasi baru
- menandai bagian yang kurang jelas
- membuat ringkasan dan poin penting

Untuk transkrip rapat, gunakan `CLEANUP_MODE = 'Minutes'`. Prompt otomatis berubah menjadi format catatan rapat:

- ringkasan
- poin pembahasan
- keputusan
- action items
- pertanyaan / bagian kurang jelas

Contoh prompt manual:

```text
Tolong rapikan transkrip berikut tanpa mengubah makna.

Instruksi:
- Perbaiki tanda baca, kapitalisasi, dan typo ringan.
- Buat paragraf yang rapi dan mudah dibaca.
- Jangan menambah informasi baru di luar transkrip.
- Jika ada bagian yang tidak jelas, tandai dengan [kurang jelas].
- Setelah transkrip rapi, buat ringkasan singkat dan daftar poin penting.

Transkrip:
[paste transkrip di sini]
```

---

## Model Guide

| Model | Kecepatan | Akurasi | Cocok Untuk |
|---|---:|---:|---|
| `tiny` | Sangat cepat | Rendah | Tes cepat |
| `base` | Cepat | Cukup | Audio pendek / resource rendah |
| `small` | Sedang | Bagus | Balance ringan |
| `medium` | Lambat | Bagus | Akurasi lebih tinggi |
| `turbo` | Cepat | Sangat bagus | Rekomendasi Colab GPU |
| `large` | Lambat | Sangat bagus | Akurasi tinggi, resource besar |

Kalau memakai Colab Free, mulai dari `turbo`. Jika crash atau GPU tidak tersedia, turunkan ke `small`, `base`, atau `tiny`.

---

## Troubleshooting

### GPU tidak aktif

Jika muncul:

```text
PERINGATAN: GPU tidak aktif
```

Aktifkan:

```text
Runtime -> Change runtime type -> T4 GPU
```

Lalu jalankan ulang dari cell setup.

### Runtime disconnect

Colab Free bisa disconnect otomatis. Kalau terjadi:

1. Reconnect runtime
2. Jalankan ulang setup
3. Upload ulang file
4. Jalankan transkripsi lagi

### File terlalu panjang

Untuk audio/video panjang, lebih stabil kalau dipotong menjadi beberapa bagian. Misalnya per 30-60 menit.

### `turbo` crash

Solusi:

1. Pastikan GPU aktif
2. Ganti `MODEL_SIZE` ke `small` atau `base`
3. Upload file lebih pendek

---

## Untuk Developer

Struktur repo:

```text
README.md
colab_run.ipynb
requirements.txt
legacy_streamlit/
  whisper_app.py
  transcribrrrr/
  requirements.txt
  packages.txt
```

Workflow utama yang direkomendasikan untuk penggunaan gratis dengan model `turbo` adalah `colab_run.ipynb`.

Folder `legacy_streamlit/` menyimpan versi app Streamlit lama jika nanti ingin dijalankan lokal atau dikembangkan lagi.

Validasi notebook:

```bash
jq empty colab_run.ipynb
```

Validasi kode Streamlit/helper:

```bash
python -m py_compile legacy_streamlit/whisper_app.py legacy_streamlit/transcribrrrr/*.py
```

---

## Credits

**Ian**  
Magister Ilmu Komputer, Universitas Gadjah Mada
