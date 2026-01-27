import os
import random
import shutil
import wave
from collections import defaultdict

RAW_DIR = "data/raw_audio"
SAMPLED_DIR = "data/sampled_audio"

TARGET_MIN = 240
TARGET_MAX = 260
MAX_PER_UUID = 3

random.seed(42)

def get_duration(path):
    with wave.open(path, "rb") as wf:
        return wf.getnframes() / wf.getframerate()

def get_uuid(filename):
    return filename.split("_")[0]

def duration_bucket(seconds):
    if seconds < 3:
        return "short"
    elif seconds <= 7:
        return "medium"
    else:
        return "long"

# Load files
files = []
for f in os.listdir(RAW_DIR):
    if f.endswith(".wav"):
        path = os.path.join(RAW_DIR, f)
        duration = get_duration(path)
        files.append({
            "file": f,
            "path": path,
            "uuid": get_uuid(f),
            "duration": duration,
            "bucket": duration_bucket(duration)
        })

# Group by UUID
by_uuid = defaultdict(list)
for f in files:
    by_uuid[f["uuid"]].append(f)

uuids = list(by_uuid.keys())
random.shuffle(uuids)

selected = []
used_per_uuid = defaultdict(int)

# -------- PASS 1: Coverage --------
for uuid in uuids:
    if len(selected) >= int(TARGET_MIN * 0.7):
        break
    clip = random.choice(by_uuid[uuid])
    selected.append(clip)
    used_per_uuid[uuid] += 1

# -------- PASS 2: Fill & Balance --------
remaining = [f for f in files if f not in selected]
random.shuffle(remaining)

for clip in remaining:
    if len(selected) >= TARGET_MAX:
        break
    uuid = clip["uuid"]
    if used_per_uuid[uuid] >= MAX_PER_UUID:
        continue
    selected.append(clip)
    used_per_uuid[uuid] += 1

# Copy files
os.makedirs(SAMPLED_DIR, exist_ok=True)
for clip in selected:
    shutil.copy(clip["path"], os.path.join(SAMPLED_DIR, clip["file"]))

# Report stats
bucket_counts = defaultdict(int)
for clip in selected:
    bucket_counts[clip["bucket"]] += 1

print(f"Final sample size: {len(selected)}")
print("Duration distribution:")
for k in ["short", "medium", "long"]:
    print(f"  {k}: {bucket_counts[k]}")
