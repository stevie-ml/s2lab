# Does Structural Repetition Have a Frequency? A Spectral Null Result

**Date:** 2026-09-21
**Experiment:** `experiments/spectral_refrain.py`
**Corpus:** 168 texts (155 with ≥40 tokens); 8 fixed-form refrain poems added this run
**Companion finding:** `stanza_break_artifact.md` — this experiment is how that confound was discovered

---

## Question

Prior work measured the S₂ series in the time domain only:

| Experiment | Measures |
|---|---|
| `s2_spikiness.py` | variance — how big are the swings |
| `s2_momentum.py` | autocorrelation at lags 1, 2, 5 — local alternation |
| `surprise_decay.py` | what happens 1–10 tokens after a spike |

All three are blind to **long-period** structure. Lag-1 autocorrelation cannot detect that a poem returns to the same state every 40 tokens. The natural tool is the frequency domain.

Fixed forms provide an ideal test case, because they impose a refrain at a *known, mandatory interval*:

| Form | Structural period |
|---|---|
| villanelle | A₁ returns at lines 6, 12, 18; A₂ at 9, 15, 19 |
| ballade | refrain closes every stanza (8 lines) |
| rondeau | rentrement returns as a short tag |
| sestina | six end-words rotate on a 6-line period |

**H1:** fixed-form poems have lower spectral flatness than free verse (repetition → concentrated spectral power).
**H2:** a poem's dominant period aligns with its observed refrain interval.

Eight public-domain refrain poems were added to test this: Wilde *Theocritus* (villanelle), Robinson *The House on the Hill*, Dowson *Villanelle of the Poet's Road*, Henley *Villanelle*, Rossetti *The Ballad of Dead Ladies*, Dobson *In After Days* (rondeau), Poe *Annabel Lee*, Kipling *Sestina of the Tramp-Royal*.

---

## Method

For each poem, the mean-removed S₂ series is transformed by direct DFT. Reported per poem:

| Metric | Definition |
|---|---|
| **spectral flatness** | geometric mean / arithmetic mean of the power spectrum. 1.0 = white noise; →0 = one dominant periodicity |
| **dominant period** | period (in tokens) of the highest-power frequency bin |
| **peak prominence** | max bin power / median bin power |
| **refrain period** | mean token-distance between verbatim line repeats, measured from the data rather than assumed from the form label |

Because the stanza-break artifact injects layout impulses that whiten any spectrum, everything is computed twice: raw, and with artifact positions (p(newline) ≥ 0.9) replaced by the poem's clean median. Replacement rather than deletion keeps the series evenly sampled, which the DFT requires.

---

## Result 1: H1 rejected — repetition does not concentrate spectral power

| Group | n | flatness raw | flatness artifact-free |
|---|---|---|---|
| poems with repeated lines (≥2 returns) | 11 | 0.5667 | 0.5422 |
| poems with no repeated lines | 141 | 0.5674 | 0.5685 |

A difference of 0.026 after cleaning, on n=11. Fixed-form poems specifically sit at **0.5716 artifact-free — flatter than the corpus mean**, i.e. marginally *more* noise-like than free verse, the opposite of the hypothesis.

The whole corpus occupies a narrow band (0.487–0.669 raw). No era separates meaningfully.

## Result 2: H2 rejected — the dominant period never matches the refrain

| Poem | len | dominant period | refrain period | ratio |
|---|---|---|---|---|
| Wilde, *Theocritus* | 102 | 2.3 | 55.5 | **0.04** |
| Dowson, *Villanelle of the Poet's Road* | 94 | 7.8 | 48.5 | **0.16** |
| Rossetti, *The Ballad of Dead Ladies* | 170 | 4.0 | 91.0 | **0.04** |
| Robinson, *The House on the Hill* | 114 | 2.2 | 46.5 | **0.05** |
| Henley, *Villanelle* | 125 | 3.0 | 64.0 | **0.05** |

Dominant periods cluster at **2–4 tokens** in every case — the fast alternation already documented in `s2_momentum_prose_poetry.md` as negative lag-1 autocorrelation (surprise → release → surprise). That short-range oscillation dominates the spectrum completely. The poem's formal architecture, operating at 45–90 tokens, contributes no detectable power.

---

## Interpretation: repetition produces impulses, not oscillations

A refrain does not make S₂ rise and fall smoothly on a 50-token cycle. What it produces is a **single sharp event** at the moment of return, followed by immediate collapse — the returning line is, after all, the most predictable text in the poem once the model has seen it.

An impulse is spectrally **flat**: a delta function has power at all frequencies equally. So a form built entirely on periodic repetition produces a *white* spectrum, which is exactly what was measured. The null result is not an absence of structure; it is the signature of impulse-like structure.

This is why the two hypotheses failed together. They both assumed repetition would behave like a wave. It behaves like a drumbeat.

---

## Caveat that became the main finding

The first version of this experiment reported that fixed-form refrain heads gain **+15.7 bits of S₂** on their second occurrence, with entropy falling to 0.009 bits. That looked like a spectacular result about poetic form.

It was an artifact. The spikes landed on ordinary non-refrain lines too, and were caused by GPT-2 predicting a stanza break. See **`findings/stanza_break_artifact.md`** — the confound inflates line-head S₂ by 102% of its reported value and scrambles every era and poem ranking in this lab.

The spectral null above survives cleaning. The mechanism claim did not.

---

## Next steps

- **Test the impulse account directly.** Compute each poem's S₂ kurtosis and crest factor. If repetition produces impulses, refrain poems should have high kurtosis with flat spectra — a specific, falsifiable joint signature.
- **Look below the noise floor.** A matched-filter or Lomb–Scargle periodogram tuned to each poem's *known* refrain interval is far more sensitive than picking the global max bin, and could detect refrain power that the dominant-period statistic misses.
- **Detrend the fast oscillation.** The 2–4 token alternation swamps everything. High-pass removal, or spectral analysis of a line-level rather than token-level S₂ series (one value per line, n≈20 per poem), would put formal periods in range.
- **n=11 repeaters is thin.** Verbatim line matching also missed *Annabel Lee*, the rondeau and the sestina, whose repeats vary slightly ("In a kingdom by the sea" / "In this kingdom by the sea"). Fuzzy line matching would roughly double the sample.
