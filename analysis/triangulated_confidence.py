import os
import json
from jiwer import wer
from asr_loader import load_asr_folder

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

OUTPUT_PATH = "reports/triangulated_confidence.json"


def triangulate(records):
    results = []

    asrs = list(records.keys())
    common_audio = set.intersection(
        *[set(r.keys()) for r in records.values()]
    )

    for audio in common_audio:
        texts = {a: records[a][audio] for a in asrs}

        # skip if any ASR is empty
        if any(t["is_empty"] for t in texts.values()):
            continue

        try:
            wd = wer(texts["whisper"]["text"], texts["deepgram"]["text"])
            wa = wer(texts["whisper"]["text"], texts["assembly"]["text"])
            da = wer(texts["deepgram"]["text"], texts["assembly"]["text"])
        except Exception:
            continue

        pairs = {
            ("whisper", "deepgram"): wd,
            ("whisper", "assembly"): wa,
            ("deepgram", "assembly"): da
        }

        consensus_pair = min(pairs, key=pairs.get)
        min_wer = pairs[consensus_pair]
        outlier = list(set(asrs) - set(consensus_pair))[0]

        results.append({
            "audio_file": audio,
            "consensus_pair": list(consensus_pair),
            "outlier": outlier,
            "min_wer": round(min_wer, 3),
            "confidence": round(1 - min_wer, 3)
        })

    return results


def main():
    report = {}

    for mode, paths in CONFIGS.items():
        loaded = {
            asr: load_asr_folder(path, asr)
            for asr, path in paths.items()
            if os.path.exists(path)
        }

        if len(loaded) < 3:
            report[mode] = {"error": "missing ASR data"}
            continue

        report[mode] = triangulate(loaded)

    os.makedirs("reports", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("✅ Triangulated confidence saved to reports/triangulated_confidence.json")


if __name__ == "__main__":
    main()
