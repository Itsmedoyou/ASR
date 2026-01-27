import os
import random
import shutil
import wave

# -------- CONFIG --------
RAW_AUDIO_DIR = "data/raw_audio"
OUTPUT_DIR = "data/sampled_audio/representative"

MIN_DURATION_SEC = 2.0     # ignore very short / silent files
MAX_DURATION_SEC = 20.0    # ignore very long outliers
NUM_SAMPLES = 8            # pick between 5–10
# ------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_wav_duration(filepath):
    try:
        with wave.open(filepath, "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)
    except Exception:
        return 0.0

# Step 1: scan and filter files
valid_files = []

for filename in os.listdir(RAW_AUDIO_DIR):
    if not filename.lower().endswith(".wav"):
        continue

    filepath = os.path.join(RAW_AUDIO_DIR, filename)
    duration = get_wav_duration(filepath)

    if MIN_DURATION_SEC <= duration <= MAX_DURATION_SEC:
        valid_files.append((filename, duration))

# Safety check
if len(valid_files) < NUM_SAMPLES:
    raise ValueError("Not enough valid audio files found. Adjust duration limits.")

# Step 2: randomly sample representative files
selected_files = random.sample(valid_files, NUM_SAMPLES)

# Step 3: copy to new folder
for filename, duration in selected_files:
    src = os.path.join(RAW_AUDIO_DIR, filename)
    dst = os.path.join(OUTPUT_DIR, filename)
    shutil.copy2(src, dst)
    print(f"Copied: {filename} ({duration:.2f}s)")

print("\nRepresentative audio sample set created successfully.")
