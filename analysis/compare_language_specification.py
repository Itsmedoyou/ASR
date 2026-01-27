import os
import json

def rate(x, total):
    return round(x / total, 3) if total else 0

def compare(u, s):
    return {
        "total_files": {
            "unspecified": u["total"],
            "specified": s["total"]
        },
        "empty_rate": {
            "unspecified": rate(u["empty"], u["total"]),
            "specified": rate(s["empty"], s["total"]),
            "delta": rate(u["empty"], u["total"]) - rate(s["empty"], s["total"])
        },
        "short_output_rate": {
            "unspecified": rate(u["short_outputs"], u["total"]),
            "specified": rate(s["short_outputs"], s["total"]),
            "delta": rate(u["short_outputs"], u["total"]) - rate(s["short_outputs"], s["total"])
        }
    }


def main():
    with open("reports/behavior_summary.json", "r", encoding="utf-8") as f:
        behavior = json.load(f)

    comparison = {
        "whisper": compare(
            behavior["whisper_unspecified"],
            behavior["whisper_hindi"]
        ),
        "deepgram": compare(
            behavior["deepgram_unspecified"],
            behavior["deepgram_hindi"]
        ),
        "assembly": compare(
            behavior["assembly_unspecified"],
            behavior["assembly_hindi"]
        )
    }

    os.makedirs("reports", exist_ok=True)
    with open("reports/language_specification_comparison.json", "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2)

    print("✅ Language specification comparison updated for 3 ASRs")


if __name__ == "__main__":
    main()
