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

OUTPUT_PATH = "reports/pairwise_wer.json"


def compare_pair(a_data, b_data):
    wers = []

    for audio in a_data:
        if audio not in b_data:
            continue

        a = a_data[audio]
        b = b_data[audio]

        if a["is_empty"] or b["is_empty"]:
            continue

        try:
            w = wer(a["text"], b["text"])
            wers.append(w)
        except Exception:
            continue

    return {
        "total_compared": len(wers),
        "avg_wer": round(sum(wers) / len(wers), 3) if wers else None
    }


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

    print("✅ Pairwise WER saved to reports/pairwise_wer.json")


if __name__ == "__main__":
    main()
