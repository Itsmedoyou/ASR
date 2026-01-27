import os
import json
import whisper

from asr.hindi_file_list import HINDI_AUDIO_FILES

# ---------------- CONFIG ----------------
AUDIO_DIR = "data/sampled_audio"
OUTPUT_DIR = "results/whisper_hindi"
MODEL_SIZE = "small"
LANGUAGE = "hi"   # <-- IMPORTANT: force Hindi
# ----------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading Whisper model:", MODEL_SIZE)
model = whisper.load_model(MODEL_SIZE)

for audio_file in HINDI_AUDIO_FILES:
    audio_path = os.path.join(AUDIO_DIR, audio_file)

    if not os.path.exists(audio_path):
        print(f"⚠️ Missing file: {audio_file}")
        continue

    output = {
        "audio_file": audio_file,
        "asr": "whisper",
        "language": "hi",
        "raw_transcript": "",
        "error": None
    }

    try:
        result = model.transcribe(
            audio_path,
            language=LANGUAGE,
            fp16=False
        )

        output["raw_transcript"] = result.get("text", "").strip()

    except Exception as e:
        output["error"] = str(e)

    out_path = os.path.join(OUTPUT_DIR, f"{audio_file}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Whisper Hindi done: {audio_file}")
