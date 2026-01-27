import json
import os
from asr_loader import load_asr_folder

TRIANGULATION_PATH = "reports/triangulated_confidence.json"
OUTPUT_PATH = "reports/consensus_transcripts.json"

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


def choose_consensus_text(a, b):
    """
    Choose the more conservative transcript between two.
    Currently: shorter length heuristic.
    """
    if len(a) <= len(b):
        return a
    return b


def main():
    with open(TRIANGULATION_PATH, "r", encoding="utf-8") as f:
        triangulated = json.load(f)

    final_output = {}

    for mode, entries in triangulated.items():
        loaded = {
            asr: load_asr_folder(path, asr)
            for asr, path in CONFIGS[mode].items()
        }

        mode_results = []

        for item in entries:
            audio = item["audio_file"]
            a1, a2 = item["consensus_pair"]

            if audio not in loaded[a1] or audio not in loaded[a2]:
                continue

            t1 = loaded[a1][audio]["text"]
            t2 = loaded[a2][audio]["text"]

            consensus_text = choose_consensus_text(t1, t2)

            mode_results.append({
                "audio_file": audio,
                "consensus_asrs": [a1, a2],
                "confidence": item["confidence"],
                "consensus_transcript": consensus_text
            })

        final_output[mode] = mode_results

    os.makedirs("reports", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print("✅ Consensus transcripts saved to reports/consensus_transcripts.json")


if __name__ == "__main__":
    main()
