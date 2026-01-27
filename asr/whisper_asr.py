import os
import json
import whisper
from scripts.normalized_tf_text import normalize_text

# ---------------- CONFIG ----------------
AUDIO_DIR = "data/sampled_audio"
OUTPUT_DIR = "results/whisper"
MODEL_SIZE = "small"
# ----------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading Whisper model:", MODEL_SIZE)
model = whisper.load_model(MODEL_SIZE)

audio_files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith(".wav")]
if not audio_files:
    raise RuntimeError("No .wav files found in data/representative")

print("Found representative files:", audio_files)

for audio_file in audio_files:
    audio_path = os.path.abspath(os.path.join(AUDIO_DIR, audio_file))

    output = {
        "audio_file": audio_file,
        "asr": "whisper",
        "status": "failed",
        "raw_transcript": "",
        "normalized_transcript": "",
        "error": None
    }

    try:
        result = model.transcribe(
            audio_path,
            fp16=False
        )

        raw_text = result.get("text", "").strip()
        normalized_text = normalize_text(raw_text)

        output["status"] = "success"
        output["raw_transcript"] = raw_text
        output["normalized_transcript"] = normalized_text

    except Exception as e:
        output["error"] = str(e)

    output_path = os.path.join(OUTPUT_DIR, f"{audio_file}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    if output["status"] == "success":
        print(f"✅ Whisper ASR SUCCESS: {audio_file} | chars={len(output['raw_transcript'])}")
    else:
        print(f"❌ Whisper ASR FAILED: {audio_file} | {output['error']}")
