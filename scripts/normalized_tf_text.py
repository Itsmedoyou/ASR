import re

def normalize_text(text: str) -> str:
    """
    Normalize ASR transcript for fair cross-ASR comparison.

    Rules:
    1. Lowercase
    2. Remove punctuation
    3. Normalize whitespace
    4. Preserve numbers
    5. Preserve Hinglish / mixed-language words as-is

    No translation, no language detection.
    """

    if not text or not isinstance(text, str):
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove punctuation (keep letters, numbers, spaces)
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # 3. Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


# -----------------------
# Simple local test
# -----------------------
if __name__ == "__main__":
    samples = [
        "Okay madam, console option dabaoon?",
        "Payment ho gaya hai!",
        "It's good if it's for 3 months, it won't be for 1 month.",
        "Other other other recent mobile number"
    ]

    for s in samples:
        print("RAW :", s)
        print("NORM:", normalize_text(s))
        print("-" * 40)
