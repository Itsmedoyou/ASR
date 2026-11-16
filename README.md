# ASR Evaluation Project

**Evaluating ASR Systems Without Ground Truth Using Agreement & Reliability**

---

## 🎯 Goal

Design and implement a **robust evaluation framework** to compare multiple Automatic Speech Recognition (ASR) systems on **real-world voice data** where **ground truth is largely unavailable**.

Instead of claiming absolute accuracy, this project estimates **relative correctness, reliability, and production safety** using agreement-based proxy metrics.

---

## 🔊 ASR Systems Evaluated

We evaluate **three architecturally independent ASR systems**:

1. **Whisper**
   - Local, open-source, multilingual
   - Recall-first, rollback-style decoding
   - Rarely silent, but may hallucinate

2. **Deepgram**
   - Cloud-based ASR
   - Precision-first decoding
   - Explicit silent failures when uncertain

3. **AssemblyAI**
   - Cloud-based, LM-heavy decoding
   - Semantic plausibility and fluency oriented
   - Tends to paraphrase rather than transcribe verbatim

Architectural independence ensures that **agreement between systems is meaningful**.

---

## 📁 Project Structure

```
ASR/
├── data/                    # Not included: private call audio
│   ├── raw_audio/           # Original audio files
│   └── sampled_audio/       # ~267 files used for evaluation
├── results/
│   ├── whisper/
│   ├── deepgram/
│   ├── assembly/
│   └── *_hindi/             # Language-specified variants
├── analysis/                # Re-runnable evaluation scripts
├── reports/                 # JSON outputs of all metrics
├── manual_label/            # Small human-labeled subset (~25)
├── asr_loader.py            # Unified ASR JSON parser
└── README.md
```

All evaluation scripts read from `results/` and write to `reports/`, ensuring reproducibility.

---

## 📊 Methodology Overview (The Flow)

This project follows a **layered evaluation pipeline**, where each step answers a different question.

### Step 1: Add a Third ASR (AssemblyAI)

Initially, only two ASRs were evaluated.
A third ASR was added to enable **triangulation**, which is essential when no system can be treated as ground truth.

AssemblyAI introduces a **semantic-plausibility bias**, making it useful for detecting paraphrasing and outlier behavior.

---

### Step 2: Pairwise Edit Distance & Pairwise WER (Similarity)

We first measure **how similar ASR outputs are**.

#### Edit Distance

Minimum number of:

- insertions
- deletions
- substitutions
  required to transform one transcript into another.

#### Word Error Rate (WER)

```
WER = (Substitutions + Insertions + Deletions) / Number of words in reference
```

In this project:

- **WER is symmetric**
- Computed as:
  `WER(ASR_A → ASR_B)`
- No ASR is treated as ground truth

**What this tells us:**
Which ASRs produce _similar text_.

**What it does NOT tell us:**
Which ASR is _correct_.

---

### Step 3: Why Pairwise WER Is Not Enough

Two ASRs can:

- strongly agree
- and still be wrong in the same way

Therefore, similarity alone cannot establish correctness.

This leads to **triangulation**.

---

### Step 4: Triangulation (Reliability)

Triangulation answers a stronger question:

> Which ASR behaves most reliably when multiple independent systems are compared?

#### How triangulation works (per audio file):

1. Compute all pairwise WERs:

   ```
   WER(W, D), WER(W, A), WER(D, A)
   ```

2. Identify the **minimum WER pair** → _consensus pair_

3. The remaining ASR → _outlier_

4. Define confidence:

   ```
   confidence = 1 − min_pairwise_WER
   ```

#### What triangulation gives us:

- Relative reliability (not absolute accuracy)
- Systematic outlier detection
- Per-file behavior, not just averages

**Key idea:**

- Pairwise WER = distance
- Triangulation = reliability

---

### Step 5: Consensus Transcript (Stable Signal Extraction)

Using triangulation, we extract **what multiple ASRs agree on**.

For each file:

- Take the two ASRs with lowest WER
- Extract overlapping tokens
- Form a **consensus transcript**

This transcript:

- Is **not ground truth**
- Represents **high-confidence content**
- Shows what is stable across systems

---

### Step 6: Keyword / Entity Stability (Meaning Preservation)

WER measures **surface disagreement**, not meaning.

To evaluate semantic robustness:

```
keyword_stability = |common_keywords| / |all_keywords|
```

Keywords include:

- numbers
- entities
- intent-bearing words

**Why this matters:**

- Fluent paraphrases may score poorly
- But stable keywords indicate preserved intent

This explains why AssemblyAI often sounds good but diverges lexically.

---

### Step 7: Empty / Failed Transcription Rate (Usability)

We explicitly measure:

```
empty_rate = failed_files / total_files
```

This captures **hard failures**:

- empty output
- unusable transcript

**Production insight:**

- Silent failure is worse than noisy failure
- No transcript cannot be recovered downstream

---

### Step 8: Latency (Deployability)

Latency is observed comparatively:

- Whisper → slower but predictable
- Deepgram → fastest
- AssemblyAI → variable

Latency is a **secondary constraint** after reliability.

---

## 🧪 Language-Specified Experiment (Controlled)

A small subset was transcribed with **explicit language hints**.

Purpose:

- Controlled intervention
- Isolate effect of language priors

Findings:

- Deepgram improves significantly
- Whisper changes little
- AssemblyAI remains semantically oriented

These results **explain behavior**, not override main conclusions.

---

## 🧠 Manual Ground Truth (Validation Only)

~25 samples were manually labeled to:

- sanity-check triangulation
- confirm correlation between agreement and correctness

Manual labels were **not** used to rank ASRs directly.

---

## 📌 Key Findings

| Aspect                | Whisper   | Deepgram | AssemblyAI   |
| --------------------- | --------- | -------- | ------------ |
| Output availability   | Very high | Low      | Medium       |
| Agreement with others | High      | High     | Low          |
| Keyword stability     | Medium    | High     | Low          |
| Failure mode          | Noisy     | Silent   | Inconsistent |
| Latency               | Slower    | Fast     | Variable     |

---

## ✅ Final Recommendation

### Production Architecture

- **Primary ASR:** Whisper
  - Guarantees coverage
  - No silent failures
  - Errors are visible and recoverable

- **Secondary / Validator:** Deepgram
  - High precision when confident
  - Fast
  - Explicit failure signaling

- **Not recommended as primary:** AssemblyAI
  - Fluent but lexically unstable
  - Frequent triangulation outlier
  - Better suited for summarization, not correctness

### One-line Verdict

> **Whisper is the safest primary ASR under uncertainty, with Deepgram as a precision-oriented secondary system for validation and recovery.**

---

## 🔁 Reproducibility

All metrics can be regenerated by running:

```bash
python -m analysis.analyze_behavior
python -m analysis.cross_asr_similarity
python -m analysis.pairwise_wer
python -m analysis.triangulated_confidence
python -m analysis.consensus_transcript
python -m analysis.keyword_stability
```

## 🧠 Final Mental Model

- **Pairwise WER** → similarity
- **Triangulation** → reliability
- **Consensus transcript** → stable signal
- **Keyword stability** → meaning preservation
- **Empty rate** → production safety
- **Latency** → deployability
