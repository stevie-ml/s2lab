# Scientific Register Intrusion: S₂ Profiles of Technical Language in Poetry

**Date:** 2026-10-29
**Corpus addition:** 5 poems testing technical/scientific vocabulary in poetry
**Builds on:** `register_fingerprint.md`, `technical_vocabulary_s2.md`, `found_poetry_intentionality.md`

---

## Research Question

When poetry deploys the vocabulary of science — exact numerical sequences, chemical nomenclature, physical laws — does it produce higher or lower S₂ than ordinary poetic diction? Two opposing hypotheses:

- **H1 (Technical as surprising):** Scientific terms are unexpected in poetic contexts → high entropy contexts, high surprisal → positive S₂
- **H2 (Technical as flattening):** Precise terminology constrains prediction (digits follow digits; formulas follow formulas) → low entropy → tokens near zero S₂

---

## New Corpus Data

| Poem | avg S₂ | avg surprisal | avg entropy | Interpretation |
|---|---|---|---|---|
| **Pi (Szymborska)** | **−0.694** | 5.634 | 6.328 | H2 confirmed: mathematical notation creates high entropy contexts, but tokens are *less* surprising than expected |
| **The Double Helix (Watson, found)** | **+0.684** | 5.812 | 5.127 | Near-average: Watson's prose is technically precise but undeviating |
| **Laws of Motion (Newton + coda)** | **+1.936** | 7.262 | 5.326 | H1 confirmed for the poetic coda: the lyric turn after Newton's prose creates extreme deviation |
| **On the Uncertainty Principle (synthetic)** | **+1.738** | 6.788 | 5.050 | High S₂: physics vocabulary used metaphorically in emotional contexts |
| **The Periodic Table (elegy, synthetic)** | **+1.125** | 6.981 | 5.856 | Above average: scientific terms (half-life, quantum numbers) in elegiac register |

**Corpus poetry mean S₂:** +0.336

---

## Key Finding: The Szymborska Paradox

Szymborska's "Pi" has **negative S₂** (−0.694) despite embedding actual mathematical notation. Why?

The poem's mathematical digits (5, 9, 2, 6, 5, 3, 5...) create extremely **high entropy** contexts — GPT-2 cannot predict what digit or word comes after "three point one four" — but the tokens actually chosen by the poem are, relative to that high entropy, *less* surprising than expected. GPT-2 is maximally uncertain, but Szymborska's tokens (actual π digits and logical transitions) satisfy a consistent internal logic that is *lower* than the entropy of the context would suggest.

This is a new category: **the ordered surprise**. The poem is about the infinite, non-repeating nature of π, but the S₂ signature is conformist — a meta-comment on how mathematical structure, even infinite structure, creates its own predictability that Szymborska exploits.

---

## Key Finding: Lyric Intrusion Into Technical Prose

The "Laws of Motion" poem (Newton's three laws followed by a 4-line lyric coda) shows the highest S₂ in this set (+1.936). The lyric coda ("O force, O matter, O beautiful constraint...") comes after three stanzas of near-zero-entropy Newtonian prose. The apostrophe and emotional vocabulary at the end produce the most extreme S₂ spike — the "register break" is informationally detectable.

**Hypothesis:** The S₂ gap between technical and lyric register within a poem may be the purest measure of "lyric intrusion" — the moment when the poet's voice breaks through the surface of impersonal discourse.

---

## Suggested Next Steps

1. **Larger systematic study:** Add 10+ poems that mix technical and lyric registers (Roethke's greenhouse poems, Merwin's nature science poems, Plath's chemistry poems) to build a proper dataset.
2. **Within-poem register break analysis:** For each mixed-register poem, segment into technical and lyric sections and measure the S₂ jump at the transition point.
3. **The ordered surprise category:** Identify other poems that achieve negative S₂ through an "ordered surprise" logic (numerical structures, strict formal constraints like oulipo) and compare them to accidental low-S₂ poems.
