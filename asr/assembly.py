# asr/assembly.py
import sys
import os
import json
import assemblyai as aai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.normalized_tf_text import normalize_text


AUDIO_DIR = "data/sampled_audio"
OUTPUT_DIR = "results/assembly"

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
os.makedirs(OUTPUT_DIR, exist_ok=True)

transcriber = aai.Transcriber()

for file in os.listdir(AUDIO_DIR):
    if not file.endswith(".wav"):
        continue

    audio_path = os.path.join(AUDIO_DIR, file)

    result = {
        "audio_file": file,
        "asr": "assembly",
        "language": "unspecified",
        "status": "failed",
        "raw_transcript": "",
        "normalized_transcript": "",
        "error": None
    }

    try:
        transcript = transcriber.transcribe(audio_path)
        text = transcript.text or ""

        result["status"] = "success"
        result["raw_transcript"] = text
        result["normalized_transcript"] = normalize_text(text)

    except Exception as e:
        result["error"] = str(e)

    with open(os.path.join(OUTPUT_DIR, f"{file}.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"AssemblyAI done: {file}")
