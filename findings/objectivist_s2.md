# Objectivist Poetry and S₂: Precision vs. Compression

**Date:** 2026-11-24  
**New poems added:** 6 (Oppen ×2, Niedecker ×2, Reznikoff ×1, Zukofsky ×1)  
**Hypothesis:** Does objectivist precision correlate with lower or higher S₂ than imagism?

---

## Background

The Objectivist movement (1930s–1960s) emphasized three principles:
1. **Sincerity**: accurate perception of the thing as it actually is
2. **Objectification**: the poem itself as a constructed object (not mere expression)
3. **Precision**: choosing the exact word over the approximate word

This creates a tension: *precision* might mean choosing **expected** words (the word that
most precisely names the thing = the most conventionally used word). But *exact naming*
might require choosing **unexpected** words (the precise technical term, the unusual
sense of a common word).

The Imagists (a predecessor movement) similarly prized the concrete image; Objectivism
adds philosophical rigor and formal self-awareness. This experiment asks whether this
distinction is detectable in S₂.

---

## Results: Objectivist Poet Profiles

| Poet | Poems | Avg S₂ (clean) | Pos S₂% | n tokens | Style |
|------|-------|---------------|---------|---------|-------|
| **Lorine Niedecker** | 2 | **+0.769** | **43.9%** | 187 | High deviation |
| Charles Reznikoff | 1 | −0.458 | 33.0% | 173 | Mid-range |
| Louis Zukofsky | 1 | −0.544 | 25.6% | 242 | Low deviation |
| George Oppen | 2 | **−0.648** | **23.4%** | 334 | Low deviation |

**The movement is internally split**: Niedecker's S₂ (+0.769) is 1.4 bits higher than
Oppen's (−0.648). Within a single movement claiming shared aesthetic principles, the
information-theoretic signature varies by **1.4 bits** — wider than the gap between many
distinct literary eras.

---

## Per-Poem Results

| Poem | Author | Avg S₂ (raw) | Avg S₂ (clean) | Pos S₂% | Max S₂ |
|------|--------|-------------|----------------|---------|--------|
| Paean to Place (excerpt) | Niedecker | 3.44 | **+0.877** | 53.4% | 36.73 |
| My Life by Water | Niedecker | 2.64 | **+0.672** | 35.4% | 33.61 |
| Psalm (Oppen) | Oppen | 0.69 | −0.622 | 24.1% | 28.14 |
| "A"-1 (opening) | Zukofsky | 0.79 | −0.544 | 25.6% | **44.36** |
| Testimony: Railroad | Reznikoff | 0.46 | −0.458 | 33.0% | 29.02 |
| Of Being Numerous (opening) | Oppen | 0.02 | **−0.666** | 22.8% | 26.78 |

---

## Comparison: Objectivist vs. Imagist

| Era | Avg S₂ (clean) | Pos S₂% |
|-----|---------------|---------|
| **imagist** (all 5) | −0.020 | 42.0% |
| **imagist** (excl. Niedecker) | −0.455 | 38.1% |
| **objectivist** (all 6) | −0.197 | 30.6% |
| **objectivist** (excl. Niedecker) | −0.550 | 27.3% |

Excluding Niedecker (who appears in both traditions):
- Imagism: avg −0.455, pos 38.1%
- Objectivism: avg −0.550, pos 27.3%

**Objectivism, stripped of Niedecker, is LOWER S₂ than imagism** — consistent with the
hypothesis that philosophical precision leads to statistically expected word choice.
But the effect is small (−0.095 difference) and based on few poems.

---

## The Niedecker Anomaly

Lorine Niedecker straddles both movements but is anomalously HIGH S₂ in both:
- Imagist label: "Lorine's Work" → clean S₂ = +1.724 (highest imagist poem)
- Objectivist label: two poems → clean S₂ = +0.672 and +0.877

**Why is Niedecker high S₂?**  
Niedecker's style is extreme *compression* — she removes articles, connectives, and
particles to leave only essential nouns and verbs. This compression creates high S₂
not through metaphor or unusual diction, but through **syntactic omission**: the model
expects connective tissue that Niedecker deletes. Where GPT-2 is confident a conjunction
or article will follow, she provides a bare noun. This is a compression-driven Straussian
gap, not a metaphor-driven one.

**The "write" spike** (S₂ = 23.69, "My Life by Water"):
- Context: empty/whitespace → poet wrote "write"
- GPT-2 expected: punctuation or new word after whitespace
- Niedecker's minimalism: the word arrives in white space without syntactic preparation

---

## Most Striking Objectivist Moments

| S₂ | Token | Poet | Context | Interpretation |
|----|-------|------|---------|---------------|
| 23.69 | "write" | Niedecker | whitespace | Compression — verb arrives in void |
| 20.09 | "optics" | Oppen | "is to say" | Philosophical exactness — "optics" after "is to say" is maximally precise, maximally unexpected |
| 18.19 | "accustomed" | Zukofsky | (space) | Unusual adjective in unusual position |
| 17.66 | "Their" | Oppen | whitespace | Line-initial, stanza-break adjacent |
| 17.37 | "park" | Oppen | whitespace | Proper noun fragment (from "In the park") |

**Oppen's "optics"** (S₂ = 20.09) is the most theoretically interesting:
> *"Which is to say **optics**:"*

The word "optics" arriving after "is to say" is a perfect example of Oppen's philosophical
precision. GPT-2 expects a common abstract noun (truth, vision, something, the fact). Oppen
chooses "optics" — a technical word that names a philosophical position (things can only be
known through their observable effects). The model's uncertainty is high, but Oppen's choice
is exact. This is objectivism's S₂ signature: **precision that surprises**.

---

## Zukofsky's Structural Spikes

The "A"-1 excerpt shows highest max S₂ in the objectivist set (44.36 for "rises"), but
this is the stanza-break artifact — the word "rises" follows a line ending with a comma,
where GPT-2 expected a newline token. The clean max is therefore "accustomed" (18.19).

What's notable about Zukofsky's poem is its **refrain structure** ("Round of fiddles
playing Bach" appears twice). Refrains should produce LOW S₂ at repetition (GPT-2 has
"seen" the phrase), but Zukofsky interleaves the refrain with new material, so the
second occurrence still achieves S₂ = 28.21 for "Round" — the model still expects a
newline at that position.

---

## Reznikoff: Documentary Poetry at the Prose Boundary

Reznikoff's "Testimony" (clean S₂ = −0.458) is the most prose-like objectivist poem
tested, confirming its method: transcribed court records restructured as verse. The
lineation imposes visual/rhythmic structure, but the language remains prose-adjacent.

Comparison:
- Reznikoff clean S₂: −0.458
- Control prose avg S₂: −1.721
- Poetry avg S₂ (clean): −0.414
- Reznikoff: exactly at the poetry average

Reznikoff's "found text" approach creates poetry at the informational boundary — it
reads to GPT-2 as indistinguishable from average poetry despite being (by genre origin)
prose. The lineation alone is sufficient to shift the S₂ from prose to poetry range.

---

## Conclusions

1. **Objectivism is internally split**: Niedecker's compression (+0.769) vs. Oppen's
   precision (−0.648) differ by 1.4 bits — a larger gap than between many different eras.

2. **The two faces of objectivist surprise**:
   - **Compression-based** (Niedecker): syntactic omission creates high S₂ by removing
     the words GPT-2 expects
   - **Precision-based** (Oppen, Zukofsky): choosing the exact word, which is unexpected
     because precision requires rare vocabulary ("optics," "accustomed")

3. **Reznikoff's documentary poetry** is at the prose-poetry S₂ boundary — exactly at
   the corpus average for poetry, confirming that lineation alone can shift a text from
   prose to poetry range.

4. **Objectivism vs. Imagism**: After removing Niedecker's outlier, objectivism is
   slightly lower S₂ than imagism (−0.550 vs −0.455). The philosophical precision of
   objectivism leads, on average, to more expected word choices than the image-focused
   intensity of imagism.

---

## Suggested Next Steps

1. **Add more Niedecker**: Her compression-based S₂ is the clearest single-poet finding.
   Testing all her short lyrics would establish whether this is consistent.

2. **Oppen's "Of Being Numerous" full text**: The excerpt shows monotone low S₂; the
   full poem (40 sections) might reveal whether his S₂ varies across its arc.

3. **Compression as independent variable**: Measure Niedecker's type-token ratio vs S₂.
   Does more compression always correlate with higher S₂, or only in her specific style?

4. **Second-generation objectivists** (Robert Duncan, Larry Eigner): Does the influence
   carry the compression-or-precision split forward?
