import os
import json
import re
from asr_loader import load_asr_folder

DEVANAGARI_RE = re.compile(r'[\u0900-\u097F]')
LATIN_RE = re.compile(r'[A-Za-z]')

CONFIGS = {
    "whisper_unspecified": ("results/whisper", "whisper"),
    "whisper_hindi": ("results/whisper_hindi", "whisper"),
    "deepgram_unspecified": ("results/deepgram", "deepgram"),
    "deepgram_hindi": ("results/deepgram_hindi", "deepgram"),
    "assembly_unspecified": ("results/assembly", "assembly"),
    "assembly_hindi": ("results/assembly_hindi", "assembly"),
}

def analyze_records(records):
    stats = {
        "total": 0,
        "empty": 0,
        "short_outputs": 0,
        "devanagari": 0,
        "latin": 0,
        "mixed": 0
    }

    for r in records.values():
        stats["total"] += 1

        text = r["text"]
        if r["is_empty"]:
            stats["empty"] += 1
            continue

        if len(text.split()) <= 2:
            stats["short_outputs"] += 1

        has_dev = bool(DEVANAGARI_RE.search(text))
        has_lat = bool(LATIN_RE.search(text))

        if has_dev and has_lat:
            stats["mixed"] += 1
        elif has_dev:
            stats["devanagari"] += 1
        elif has_lat:
            stats["latin"] += 1

    return stats


def main():
    summary = {}

    for name, (path, asr) in CONFIGS.items():
        if not os.path.exists(path):
            summary[name] = {"error": "folder not found"}
            continue

        records = load_asr_folder(path, asr)
        summary[name] = analyze_records(records)

    os.makedirs("reports", exist_ok=True)
    with open("reports/behavior_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("✅ Behavior analysis updated for all 3 ASRs")


if __name__ == "__main__":
    main()
