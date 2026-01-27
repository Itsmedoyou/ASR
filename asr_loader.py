import os
import json

def extract_transcript(asr, data):
    """
    ASR-aware transcript extraction.
    Returns a canonical representation.
    """

    text = ""

    if asr == "whisper":
        text = (
            data.get("raw_transcript")
            or data.get("normalized_transcript")
            or ""
        )

    elif asr == "deepgram":
        text = (
            data.get("raw_transcript")
            or data.get("transcript")
            or ""
        )

    elif asr == "assembly":
        text = (
            data.get("text")
            or data.get("raw_transcript")
            or ""
        )

    text = text.strip() if isinstance(text, str) else ""

    return {
        "text": text,
        "is_empty": len(text) == 0,
        "is_failure": data.get("error") is not None
    }


def load_asr_folder(folder_path, asr_name):
    """
    Load all ASR JSON files from a folder and return
    a canonical mapping:

    audio_file -> {
        audio_file,
        asr,
        text,
        is_empty,
        is_failure
    }
    """

    records = {}

    if not os.path.exists(folder_path):
        return records

    for fname in os.listdir(folder_path):
        if not fname.endswith(".json"):
            continue

        file_path = os.path.join(folder_path, fname)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        audio = data.get("audio_file")
        if not audio:
            continue

        extracted = extract_transcript(asr_name, data)

        records[audio] = {
            "audio_file": audio,
            "asr": asr_name,
            "text": extracted["text"],
            "is_empty": extracted["is_empty"],
            "is_failure": extracted["is_failure"]
        }

    return records
