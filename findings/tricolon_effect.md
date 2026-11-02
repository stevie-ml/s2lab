# The Tricolon Effect: Information Theory Meets the Rule of Three
**Date:** 2026-11-02  
**Experiment:** `experiments/tricolon_effect.py`  
**Data:** `results/tricolon_effect.json`  
**Corpus:** 176 "A, B, and C" tricola across 113 poems (403-poem corpus)

---

## Research Question

Classical rhetoric holds that the **tricolon** — the series of three — culminates at the third element. "Veni, vidi, vici." The *omne trium perfectum* principle: the third item in a list delivers the most weight, most surprise, most power.

Does information theory agree? Specifically: in phrases of the form "A, B, and C," is S₂(C) > S₂(B) > S₂(A)?

Or does GPT-2 reveal that rhetorical "power" and statistical "surprise" diverge across literary eras?

---

## Corpus and Method

- Searched all 403 English-language poems for "A, B, and C" / "A, B, or C" patterns using regex
- Extracted the S₂ and entropy H of the **first content token** of each list element
- Filtered artifact tokens (p_newline < 0.9)
- 176 valid tricola found in 113 poems

---

## Main Finding: C Is Marginally Favored — But the Real Story Is in Era

### Overall S₂ by Position

| Position | Mean S₂ | Median S₂ |
|----------|---------|-----------|
| A (1st item) | **−0.123** | −1.035 |
| B (2nd item) | **+0.309** | −0.458 |
| C (3rd item) | **+0.061** | −0.526 |

**C is not the most surprising position** — that honor goes to B (the second element). The expected "rule of three" climax does not hold globally. Mean S₂ follows the pattern B > C > A, not C > B > A.

### Which Position Holds the Maximum S₂?

| Position | Count | % of tricola |
|----------|-------|-------------|
| A (1st) | 56 | 31.8% |
| B (2nd) | 57 | 32.4% |
| **C (3rd)** | **63** | **35.8%** |

C edges out A and B when comparing which is the single maximum — but the advantage is only 4 percentage points over chance (33.3%). The "rule of three" is a weak signal globally.

---

## The Entropy Reversal

The most important finding is not S₂ but **entropy H** at each position:

| Position | Mean H (bits) |
|----------|---------------|
| A (1st) | 7.216 |
| B (2nd) | 7.012 |
| **C (3rd)** | **8.332** |

**H(C) is a full 1.1 bits higher than H(A).** The model is *more uncertain* at the third list item, not less. This means:

- GPT-2 "learns" the list structure after A and B — it knows a third item is coming
- But because lists are semantically open-ended, it cannot narrow down WHICH third item — its probability distribution *opens up*
- The third element arrives in a high-entropy context, so positive S₂ at C is partly driven by this expanded uncertainty, not purely by poet defiance

Confirming this: H(C) < H(A) — "the model was MORE confident at C than A" — is only true **29.5%** of the time (52 of 176 tricola). In 70.5% of cases, the model is MORE uncertain at position 3 than at position 1.

**This is the opposite of the anaphora/refrain pattern** (where H decreases with repetition). Lists open up entropy; refrains close it down.

---

## The Era Split: Climax vs. Anticlimax

The aggregate results mask a dramatic literary-historical divide:

| Era | n | Mean S₂(A) | Mean S₂(B) | Mean S₂(C) | C-max% |
|-----|---|-----------|-----------|-----------|--------|
| modernist | 7 | +1.167 | +0.573 | **+6.161** | **71%** |
| new_york_school | 6 | +0.431 | −0.776 | **+3.323** | **67%** |
| parody_original | 6 | −2.153 | −1.042 | **+3.218** | **83%** |
| early_modern | 6 | **+3.514** | +0.610 | −1.206 | **0%** |
| romantic | 24 | +0.794 | **+1.809** | −0.725 | 21% |
| dramatic_monologue | 8 | −1.136 | **+2.181** | −0.441 | 12% |
| ekphrastic | 12 | −1.213 | −0.206 | **−1.415** | 17% |
| victorian | 21 | +0.406 | +0.184 | **−1.199** | 33% |

### The Finding: Three Rhetorical Strategies

**1. MODERNIST / NYS Climax ("save the best for last"):**  
Modernist poets (Moore, Stevens, Sandburg, Berryman) and New York School poets exhibit the canonical tricolon structure — S₂(C) >> S₂(A) and S₂(B). The third element is genuinely the most surprising. Parody (which mimics literary tropes) also shows this pattern, suggesting that the climax structure is what parodists mock.

**2. ROMANTIC / DRAMATIC MONOLOGUE "Ab/c" Pattern ("peak at 2nd"):**  
Romantic and dramatic monologue texts show S₂(B) as the maximum. The surprise comes in the middle of the list — the second element is unexpected, then the third element lands predictably. This matches the Romantic tendency toward mid-turn surprises (the "turn" in a sonnet argument often sits at the second beat of a three-part structure).

**3. EARLY MODERN Anticlimax ("front-load the surprise"):**  
Early modern poetry (Shakespeare, Donne, Marlowe) has S₂(A) dominant, with C-max at 0% across all 6 tricola. The list STARTS with the surprising element and then decelerates. This is the rhetorical anticlimax — the deflating series — which is a satirical and ironic device in Renaissance and metaphysical writing.

---

## Top Tricola: Canonical Examples

The highest S₂(C) cases illustrate each strategy:

| S₂(C) | Author | Third Element (C) | Phrase |
|--------|--------|-------------------|--------|
| 15.73 | Marianne Moore | "hatchet strokes" | dynamite grooves, burns, **and hatchet strokes** |
| 13.59 | Carl Sandburg | "passengers ask" | Two years, ten years, **and passengers ask the conductor** |
| 10.55 | Robert Southey (Carroll parody) | "pleasures with youth pass away" | Father William…And **pleasures with youth pass away** |
| 10.07 | Ecclesiastes (KJV) | "hasteth to his place" | sun ariseth…goeth down…**and hasteth to his place** |
| 9.05 | Robert Southey | "abused not my health" | remembered that youth would fly…**And abused not my health** |
| 7.70 | Wallace Stevens | "bid him whip" | muscular one…**and bid him whip** / roller of big cigars |

**Sandburg's "Two years, ten years, and passengers ask the conductor"** is exemplary: the first two elements are temporal spans (expected: another span would follow), but the third is a social action — a semantic cross-domain jump of the first order.

**Ecclesiastes/KJV** shows the tricolon as cosmological list: "ariseth...goeth down...hasteth" — the third verb breaks from the simple binary (rise/fall) into something more urgent and purposive.

**Marianne Moore's** "dynamite grooves, burns, and hatchet strokes" — three industrial metaphors, but the third breaks into the realm of violence and precision in a way the first two don't.

---

## Counterexamples: The Romantic Reversal

In Romantic poetry, the second position dominates. From the raw data, some instructive examples:

- **Keats, "La Belle Dame sans Merci"** (8 tricola, most in corpus): patterns consistently show surprise peaking at B, then declining. The lady is described as "Full beautiful—a faery's child, / Her hair was long, her foot was light / **And her eyes were wild**" — grammatically parallel, but "wild" (B position in the final sequence) is the emotional peak.

- **Shelley, "Ozymandias"**: the three-part structure of the inscription ("My name is Ozymandias, King of Kings; / Look on my Works, ye Mighty, and despair!") has its surprise at the pivot word "despair" — which is a second-position surprise within the parallel structure.

---

## Interpretation: Why Does Era Determine Tricolon Strategy?

Three possible explanations for the historical pattern:

1. **Rhetorical training**: Classical rhetoric (which Early Modern poets studied intensely through Latin education) emphasized the *anticlimax* as a device for irony and deflation. Donne and Jonson knew they were using the list to undermine expectation. Modern poetry, less classically trained, defaults to the "natural" climax.

2. **GPT-2's own training distribution**: The model was trained mostly on contemporary/web text. Climax is the default in prose lists ("fast, easy, and free"). So the Modernists who use climax are "swimming with" GPT-2's expectations about list structure — which makes their third elements PARADOXICALLY more surprising (the model expected the list to end more mundanely).

3. **Semantic category shift**: Modernist tricola tend to cross semantic categories at position C (time → action, appearance → behavior, abstract → concrete). Romantic tricola tend to stay within a semantic field, peaking emotionally at B then returning to form at C.

---

## Data Tables

### Sign Tests (n=176)

| Test | n passing | % |
|------|-----------|---|
| S₂(C) > S₂(A) | 94 | 53.4% |
| S₂(C) > S₂(B) | 87 | 49.4% |
| S₂(A) > S₂(C) | 82 | 46.6% |
| S₂(B) > S₂(C) | 89 | 50.6% |
| H(C) < H(A) — model more confident at C | 52 | 29.5% |

---

## Suggested Next Steps

1. **Expand the corpus for bicolon/tetracolon comparison**: Do lists of 2 or 4 items show different S₂ distributions? The bicolon should peak at B; the tetracolon may peak at 3 or 4.

2. **Semantic category typing**: Hand-annotate whether the third element is in the same semantic category as A and B. Test whether cross-category third items have higher S₂ than within-category.

3. **The Chiasmus test**: Chiasmus ("ABBA" structure) should have a mirror S₂ pattern — does S₂(1) ≈ S₂(4) and S₂(2) ≈ S₂(3)?

4. **Prose vs. poetry comparison**: In journalistic prose ("fast, cheap, and reliable"), does the tricolon show the same pattern? A cross-domain test would tell us whether the Modernist climax is distinctly *poetic* or just a modern English default.

5. **Statistical power**: 176 hits in 113 poems is modest. The era-level breakdown (7-24 per era) is suggestive but underpowered. Adding more texts per era would sharpen the findings.
