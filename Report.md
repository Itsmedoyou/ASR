- Analysis & Recommendation
  Relative Accuracy / Consistency
  Because no large-scale ground truth is available, accuracy is evaluated indirectly through consistency. We measure how often an ASR agrees with other independent ASRs using pairwise WER, triangulated confidence, and consensus formation.
  Across the unspecified-language dataset, Whisper and Deepgram form the most frequent consensus pair, appearing together in the lowest-WER pair for a majority of samples. This indicates that these two systems are often decoding the same underlying speech signal, even when their surface forms differ slightly. AssemblyAI, in contrast, appears more frequently as the triangulation outlier, meaning its transcripts diverge from the other two more often.
  Pairwise WER averaged over the dataset is high (>1 in many cases), which is expected in noisy, conversational, multilingual speech. Importantly, relative comparisons still hold: Deepgram shows lower disagreement with Whisper than AssemblyAI does, and triangulated confidence scores are consistently higher when Deepgram is part of the consensus pair. This suggests that Deepgram is more consistent with the majority signal, while AssemblyAI is less stable.
  Thus, in terms of relative accuracy under uncertainty, Whisper and Deepgram outperform AssemblyAI, with Deepgram showing stronger agreement when it produces output.

Error Patterns (Numbers, Names, Code-Switching)
Each ASR exhibits a distinct and repeatable error profile.
Whisper demonstrates a recall-first behavior. It frequently produces transcripts even under poor audio conditions, but this leads to noisy errors: extra filler words, incorrect substitutions, and occasional hallucinations. These errors increase WER but remain visible and analyzable.
Deepgram follows a precision-first strategy. It is more conservative, often producing shorter outputs or no output at all when confidence is low. When it does transcribe, its errors tend to be localized (e.g., missing entities or partial phrases) rather than expansive hallucinations. This results in stronger agreement with Whisper in consensus cases, especially for transactional phrases, numbers, and structured utterances.
AssemblyAI shows a tendency toward semantic smoothing. Its transcripts are often fluent but diverge lexically from other ASRs, especially in cases involving numbers, proper nouns, or code-switching. This explains why AssemblyAI frequently becomes the triangulation outlier: it captures intent but not exact wording.
Keyword and entity stability analysis supports this observation. Stable keywords (e.g., “account”, “bank”, “amount”, “login”) are preserved more consistently between Whisper and Deepgram than with AssemblyAI, particularly in the unspecified-language setting.

Latency
Latency observations reveal another important trade-off.
Whisper, being a local ASR, incurs higher per-utterance latency and is constrained by local compute resources. However, its latency is predictable and does not depend on network conditions.
Deepgram exhibits the lowest transcription latency among the evaluated systems when operating under normal network conditions. This makes it attractive for real-time or near–real-time applications, provided silent failures are handled.
AssemblyAI falls between the two, with acceptable latency but no clear advantage over Deepgram in speed or over Whisper in robustness.
Latency alone does not determine ASR quality, but it influences architectural decisions. In this context, Deepgram’s speed strengthens its role as a secondary or validating ASR, rather than a sole primary system.

Final Recommendation
Based on relative consistency, observable error behavior, and operational reliability, Whisper is recommended as the primary ASR for a production voice system, with Deepgram used as a secondary validation or fallback ASR.
Whisper’s key advantage is that it almost always produces output. Its failures are noisy but visible, making them debuggable and correctable. In production systems, this property is critical: a wrong transcript can be flagged, retried, or reviewed, whereas a silent failure cannot.
Deepgram complements Whisper by providing higher precision and strong agreement when it does transcribe. Although its silent failures make it unsuitable as a standalone primary ASR, its low latency and consistency with Whisper make it ideal for confidence scoring, triangulation, or selective override.
AssemblyAI, while useful for fluent, human-readable transcripts, shows lower consistency with the other ASRs and is therefore not recommended for correctness-critical production workflows.
Language-Specified Evaluation (Controlled Experiment)
To better understand the behavior of each ASR under reduced uncertainty, we conducted a controlled experiment where the language was explicitly specified for a subset of Hindi-dominant audio samples. This experiment was not intended to represent the primary production setting, but rather to isolate the impact of language priors on ASR behavior.
By holding the audio constant and modifying only the language input parameter, we evaluated how each ASR responds when the language detection problem is removed. This allowed us to analyze changes in transcription stability, failure rates, and cross-ASR agreement under controlled conditions.

Key Observations
When the language was explicitly specified, Deepgram showed a significant reduction in empty or failed transcriptions, along with improved agreement with other ASRs. This indicates that Deepgram benefits strongly from language priors and is more sensitive to uncertainty in language detection.
Whisper, in contrast, showed less dramatic change between the specified and unspecified settings. Its failure mode remained noisy rather than silent, suggesting that Whisper already embeds strong multilingual robustness and relies less on external language hints.
AssemblyAI showed moderate improvement in fluency but continued to diverge lexically from other ASRs, reinforcing its tendency toward semantic smoothing rather than strict transcription fidelity.
