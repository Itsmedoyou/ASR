import os
import json
import requests
from scripts.normalized_tf_text import normalize_text

# ---------------- CONFIG ----------------
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
AUDIO_DIR = "data/sampled_audio"
OUTPUT_DIR = "results/deepgram"
# ----------------------------------------

if not DEEPGRAM_API_KEY:
    raise RuntimeError("DEEPGRAM_API_KEY not set")

os.makedirs(OUTPUT_DIR, exist_ok=True)

url = "https://api.deepgram.com/v1/listen?model=nova-2&smart_format=true"

headers = {
    "Authorization": f"Token {DEEPGRAM_API_KEY}",
    "Content-Type": "audio/wav"
}

audio_files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith(".wav")]
if not audio_files:
    raise RuntimeError("No .wav files found in data/representative")

print("Found representative files:", audio_files)

for audio_file in audio_files:
    audio_path = os.path.join(AUDIO_DIR, audio_file)

    output = {
        "audio_file": audio_file,
        "asr": "deepgram",
        "status": "failed",
        "raw_transcript": "",
        "normalized_transcript": "",
        "error": None
    }

    try:
        with open(audio_path, "rb") as audio:
            response = requests.post(url, headers=headers, data=audio)

        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {response.text}")

        result = response.json()

        raw_text = (
            result
            .get("results", {})
            .get("channels", [{}])[0]
            .get("alternatives", [{}])[0]
            .get("transcript", "")
        )

        normalized_text = normalize_text(raw_text)

        output["status"] = "success"
        output["raw_transcript"] = raw_text
        output["normalized_transcript"] = normalized_text

    except Exception as e:
        output["error"] = str(e)

    output_path = os.path.join(OUTPUT_DIR, f"{audio_file}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    if output["status"] == "success":
        print(f"✅ Deepgram ASR SUCCESS: {audio_file} | chars={len(output['raw_transcript'])}")
    else:
        print(f"❌ Deepgram ASR FAILED: {audio_file} | {output['error']}")
