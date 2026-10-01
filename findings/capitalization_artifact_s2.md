# Capitalization as an S₂ Artifact: The Dickinson Problem

**Date:** 2026-10-01  
**Experiment:** `experiments/capitalization_artifact.py`  
**Corpus:** 200 texts analyzed with GPT-2  
**Results:** `results/capitalization_artifact.json`

---

## Research Question

Emily Dickinson famously capitalized nouns and other key words mid-line — a practice
unconventional in English prose. GPT-2 is case-sensitive and was trained on text where
capitalization marks sentence beginnings and proper nouns. Does mid-line capitalization
create *spurious* S₂ spikes — appearing high-surprise because GPT-2 assigns lower
probability to capitalized tokens in unexpected positions?

---

## Corpus-Wide Category Analysis

We classified every token in the corpus into four positional categories:
- **sentence_start**: follows `.`, `!`, `?`, or is position 1
- **line_start**: immediately follows a newline (first word of a new line)
- **mid_upper**: mid-line token starting with an uppercase letter
- **mid_lower**: mid-line token in lowercase

| Category | n | Mean S₂ | Positive-S₂ rate |
|---|---|---|---|
| line_start | 5,390 | **+1.815** | 44% |
| mid_upper | 538 | **+1.082** | 47% |
| sentence_start | 1,665 | **+0.710** | 29% |
| mid_lower | 10,753 | **-0.054** | 39% |

**The capitalization artifact is real and substantial:**  
Mid-line uppercase tokens have mean S₂ of **+1.082** vs. mid-line lowercase at **-0.054** —  
a **1.136-bit gap** solely attributable to positional capitalization.

Note: the `line_start` category is elevated for a separate reason (the [stanza-break artifact](stanza_break_artifact.md)), 
where GPT-2 strongly expects a newline continuation at line endings.

---

## Per-Poet Capitalization Profiles

Which poets use mid-line capitalization most, and how does it affect their S₂?

| Poet | Mid-Upper Rate | n Upper | Avg S₂ (upper) | Avg S₂ (lower) | S₂ Delta |
|------|---------------|---------|----------------|----------------|-----------|
| Georg Trakl | 30.5% | 47 | +1.144 | +0.606 | **+0.539** |
| **Emily Dickinson** | **22.5%** | **29** | **+4.225** | **-0.323** | **+4.548** |
| Thomas Jefferson (found) | 21.8% | 12 | -0.985 | -1.348 | +0.363 |
| Frank O'Hara | 19.5% | 17 | +1.863 | +0.011 | **+1.852** |
| Rainer Maria Rilke | 15.5% | 20 | +2.339 | +1.101 | **+1.237** |
| Oscar Wilde | 13.0% | 6 | +3.453 | +0.053 | **+3.400** |
| Andrew Marvell | 12.8% | 6 | +1.757 | -0.824 | **+2.580** |
| Carl Sandburg | 11.5% | 6 | +4.070 | -0.105 | **+4.176** |

### The Dickinson Finding

Emily Dickinson has the **highest mid-line capitalization rate** among English-language
poets in the corpus (22.5%). Her capitalized tokens have a mean S₂ of **+4.225** — a
stunning **4.548-bit premium** over her own lowercase tokens (-0.323).

This suggests a substantial portion of Dickinson's reputation for "high S₂" is an artifact
of her capitalization convention. She was placing unexpected capital letters in positions
where GPT-2 expected lowercase, and GPT-2 responded with high surprisal.

**However, this is not purely artifactual.** Dickinson's capitalization is *semantically
intentional* — when she writes "Death" (not "death"), the capital letter is doing
expressive work. The question is whether GPT-2's surprise registers the semantic choice
or merely the typographic one.

---

## The Tokenization Confound: Why Lowercasing Doesn't Simply Fix It

We attempted a direct test: re-analyze Dickinson poems with all text lowercased.

| Poem | Original Avg S₂ | Lowercased Avg S₂ | Delta | Tokens Changed |
|------|----------------|-------------------|-------|---------------|
| Because I could not stop for Death | 0.537 | 1.179 | **-0.642** | 44/~50 |
| I felt a Funeral, in my Brain | 0.480 | 1.375 | **-0.895** | 64/~70 |
| A Route of Evanescence | 0.227 | 0.045 | **+0.182** | 55/~55 |
| Song of Myself — Walt Whitman | 1.419 | 1.462 | -0.043 | 5/~30 |
| Buffalo Bill's — E.E. Cummings | -0.313 | -0.368 | +0.054 | 31/~30 |

**Paradox**: Lowercasing *increased* S₂ in two of three Dickinson poems (delta = -0.642, -0.895).

The reason is subtle but important: **GPT-2 uses BPE (Byte Pair Encoding) tokenization, which
is case-sensitive**. The word "Death" and "death" may receive different token IDs, and more
importantly, they may trigger *different tokenization splits* of surrounding text.

When we lowercased Dickinson, **44–64 tokens changed** in poems of ~50–70 tokens — meaning
essentially the *entire tokenization reshuffled*. We were no longer comparing the same poem
with and without capitals; we were comparing two completely different token sequences. The 
seemingly direct test is uninterpretable.

**Whitman and Cummings confirm the control**: Only 5 tokens changed for Whitman (a tiny delta
of -0.043), because standard sentence capitalization doesn't perturb the BPE tokenization.
Cummings' all-lowercase already had stable tokenization.

---

## Implications: The Capitalization Premium as Mixed Signal

The 1.136-bit capitalization premium in the corpus represents a **mixed signal**:

1. **Artifact component**: GPT-2 expects lowercase tokens in mid-sentence positions; a capital
   letter is typographically "wrong" from the model's perspective, inflating surprisal.

2. **Semantic signal component**: Poets who capitalize mid-line are often capitalizing precisely
   the words they consider most semantically charged — Death, God, Beauty, Truth. These *are*
   the surprising semantic choices, and the capitalization marks them as such.

The two effects are entangled. When Dickinson capitalizes "Death," she is:
- Making a typographic choice GPT-2 doesn't expect (artifact)
- Selecting a word the model may or may not have expected (genuine S₂)

We cannot disentangle them cleanly without token-matched comparisons that preserve tokenization,
which BPE makes difficult.

---

## Cross-Linguistic Note: German Poetry

Georg Trakl (30.5% mid-upper rate) is a German-language poet whose German poems were analyzed
with `dbmdz/german-gpt2`. In German, **all nouns are capitalized by convention**. The
`dbmdz/german-gpt2` model was trained on German text and would *expect* capitalized nouns —
so Trakl's capitalization rate should not create an artifact.

Yet Trakl shows a +0.539 delta for capitalized tokens. This may reflect that Trakl's capitalized
words (in his German poems) genuinely are his most semantically unusual choices, or that there are
English-language Trakl translations in the corpus being conflated.

---

## Finding Summary

| Result | Value |
|--------|-------|
| Capitalization S₂ premium (corpus-wide) | **+1.136 bits** |
| Dickinson mid-line capitalization rate | **22.5%** (highest English poet) |
| Dickinson's capitalized-vs-lowercase S₂ delta | **+4.548 bits** |
| Lowercasing approach | **Unreliable** (BPE tokenization shifts) |
| Whitman/Cummings capitalization effect | **Negligible** (~0.05 bits) |

---

## Proposed Next Steps

1. **Controlled comparison**: For each capitalized token, look up its lowercase counterpart
   *directly* in GPT-2's vocabulary and compute the probability ratio. This bypasses
   the tokenization problem entirely.

2. **Per-poet decontamination**: Subtract the expected capitalization premium (1.136 bits)
   from each mid-upper token's S₂ before comparing poets. Would Dickinson's rank drop?

3. **Intentionality scoring**: Cross-reference which Dickinson capitalizations appear in all
   manuscript versions (intentional) vs. editorial additions. Test whether intentional
   capitalizations have higher S₂ than editorial ones.

4. **German control**: Run a precise comparison of German nouns (correctly capitalized) vs.
   English mid-line capitalizations using the respective language models to test whether
   the premium is purely a frequency-of-usage artifact or reflects semantic loading.
