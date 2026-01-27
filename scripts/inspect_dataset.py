import os
from collections import defaultdict
import wave

DATA_DIR = "data/raw_audio"

groups = defaultdict(list)
durations = []

for fname in os.listdir(DATA_DIR):
    if not fname.endswith(".wav"):
        continue

    base_id = fname.split("__")[0]
    path = os.path.join(DATA_DIR, fname)

    try:
        with wave.open(path, "rb") as w:
            frames = w.getnframes()
            rate = w.getframerate()
            duration = frames / float(rate)
            durations.append(duration)
            groups[base_id].append(duration)
    except Exception as e:
        print(f"Failed to read {fname}: {e}")

print(f"Total audio files: {sum(len(v) for v in groups.values())}")
print(f"Unique recordings (UUIDs): {len(groups)}")

chunk_counts = sorted(
    ((k, len(v)) for k, v in groups.items()),
    key=lambda x: x[1],
    reverse=True
)

print("\nTop 10 recordings by chunk count:")
for k, c in chunk_counts[:10]:
    print(k, c)

print("\nDuration stats (seconds):")
print(f"Min: {min(durations):.2f}")
print(f"Max: {max(durations):.2f}")
print(f"Avg: {sum(durations)/len(durations):.2f}")
