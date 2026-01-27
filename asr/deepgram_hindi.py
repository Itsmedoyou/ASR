import os
import json
import requests

from asr.hindi_file_list import HINDI_AUDIO_FILES

# ---------------- CONFIG ----------------
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
AUDIO_DIR = "data/sampled_audio"
OUTPUT_DIR = "results/deepgram_hindi"
# ----------------------------------------

if not DEEPGRAM_API_KEY:
    raise RuntimeError("DEEPGRAM_API_KEY not set")

os.makedirs(OUTPUT_DIR, exist_ok=True)

url = (
    "https://api.deepgram.com/v1/listen"
    "?model=nova-2"
    "&language=hi"
    "&smart_format=true"
)

headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "audio/wav"
}

for audio_file in HINDI_AUDIO_FILES:
    audio_path = os.path.join(AUDIO_DIR, audio_file)

    if not os.path.exists(audio_path):
        print(f"⚠️ Missing file: {audio_file}")
        continue

    output = {
        "audio_file": audio_file,
        "asr": "deepgram",
        "language": "hi",
        "raw_transcript": "",
        "error": None
    }

    try:
        with open(audio_path, "rb") as audio:
            response = requests.post(url, headers=headers, data=audio)

        if response.status_code != 200:
            raise RuntimeError(response.text)

        result = response.json()

        output["raw_transcript"] = (
            result.get("results", {})
            .get("channels", [{}])[0]
            .get("alternatives", [{}])[0]
            .get("transcript", "")
        )

    except Exception as e:
        output["error"] = str(e)

    out_path = os.path.join(OUTPUT_DIR, f"{audio_file}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Deepgram Hindi done: {audio_file}")
