import os
import json
from difflib import SequenceMatcher
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

OUTPUT_PATH = "reports/cross_asr_similarity.json"

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def compare_pair(a_data, b_data):
    stats = {
        "total_common": 0,
        "both_empty": 0,
        "a_only": 0,
        "b_only": 0,
        "both_present": 0,
        "avg_similarity": 0.0
    }

    sims = []

    for audio in a_data:
        if audio not in b_data:
            continue

        stats["total_common"] += 1
        a = a_data[audio]
        b = b_data[audio]

        if a["is_empty"] and b["is_empty"]:
            stats["both_empty"] += 1
            continue
        if not a["is_empty"] and b["is_empty"]:
            stats["a_only"] += 1
            continue
        if a["is_empty"] and not b["is_empty"]:
            stats["b_only"] += 1
            continue

        stats["both_present"] += 1
        sims.append(similarity(a["text"], b["text"]))

    if sims:
        stats["avg_similarity"] = round(sum(sims) / len(sims), 3)

    return stats


def main():
    report = {}

    for mode, paths in CONFIGS.items():
        loaded = {
            asr: load_asr_folder(path, asr)
            for asr, path in paths.items()
            if os.path.exists(path)
        }

        mode_report = {}
        keys = list(loaded.keys())

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]
                mode_report[f"{a}_vs_{b}"] = compare_pair(
                    loaded[a], loaded[b]
                )

        report[mode] = mode_report

    os.makedirs("reports", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("✅ Cross-ASR similarity updated for 3 ASRs")


if __name__ == "__main__":
    main()
