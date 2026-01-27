# asr/assembly_hindi.py
import sys
import os
import json
import assemblyai as aai

# Ensure project root is on PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.normalized_tf_text import normalize_text
from asr.hindi_file_list import HINDI_AUDIO_FILES

# ---------------- CONFIG ----------------
AUDIO_DIR = "data/sampled_audio"          # ✅ same as Deepgram
OUTPUT_DIR = "results/assembly_hindi"
# ---------------------------------------

# API key (fail fast)
api_key = os.getenv("ASSEMBLYAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "ASSEMBLYAI_API_KEY not set. "
        "Run: setx ASSEMBLYAI_API_KEY \"your_key_here\""
    )

aai.settings.api_key = api_key

os.makedirs(OUTPUT_DIR, exist_ok=True)

# AssemblyAI config
config = aai.TranscriptionConfig(language_code="hi")
transcriber = aai.Transcriber(config=config)

# ---------------- RUN ----------------
for audio_file in HINDI_AUDIO_FILES:
    audio_path = os.path.join(AUDIO_DIR, audio_file)

    if not os.path.exists(audio_path):
        print(f"⚠️ Missing file: {audio_file}")
        continue

    result = {
        "audio_file": audio_file,
        "asr": "assembly",
        "language": "hi",
        "status": "failed",
        "raw_transcript": "",
        "normalized_transcript": "",
        "error": None
    }

    try:
        transcript = transcriber.transcribe(audio_path)

        if transcript.status == "error":
            raise RuntimeError(transcript.error)

        text = transcript.text or ""

        result["status"] = "success"
        result["raw_transcript"] = text
        result["normalized_transcript"] = normalize_text(text)

    except Exception as e:
        result["error"] = str(e)

    out_path = os.path.join(OUTPUT_DIR, f"{audio_file}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ AssemblyAI Hindi done: {audio_file}")
