import os
import json
import re
from asr_loader import load_asr_folder

CONSENSUS_PATH = "reports/consensus_transcripts.json"
OUTPUT_PATH = "reports/keyword_stability.json"

CONFIGS = {
    "unspecified": {
        "whisper": "results/whisper",
        "deepgram": "results/deepgram",
        "assembly": "results/assembly"
    },
    "hindi": {
        "whisper": "results/whisper_hindi",
        "deepgram": "results/deepgram_hindi",
        "assembly": "results/assembly_hindi"
    }
}

NUMBER_RE = re.compile(r"\b\d+\b")
CAPITAL_RE = re.compile(r"\b[A-Z][a-zA-Z]+\b")
WORD_RE = re.compile(r"\b[a-zA-Z]{4,}\b")


def extract_keywords(text):
    keywords = set()

    keywords.update(NUMBER_RE.findall(text))
    keywords.update(CAPITAL_RE.findall(text))

    for w in WORD_RE.findall(text.lower()):
        keywords.add(w)

    return keywords


def main():
    with open(CONSENSUS_PATH, "r", encoding="utf-8") as f:
        consensus_data = json.load(f)

    report = {}

    for mode, items in consensus_data.items():
        loaded = {
            asr: load_asr_folder(path, asr)
            for asr, path in CONFIGS[mode].items()
        }

        results = []

        for item in items:
            audio = item["audio_file"]

            sets = []
            for asr in loaded:
                if audio in loaded[asr]:
                    text = loaded[asr][audio]["text"]
                    if text:
                        sets.append(extract_keywords(text))

            if len(sets) < 2:
                continue

            intersection = set.intersection(*sets)
            union = set.union(*sets)

            stability = len(intersection) / len(union) if union else 0

            results.append({
                "audio_file": audio,
                "keyword_stability": round(stability, 3),
                "common_keywords": list(intersection)
            })

        report[mode] = results

    os.makedirs("reports", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("✅ Keyword stability saved to reports/keyword_stability.json")


if __name__ == "__main__":
    main()
