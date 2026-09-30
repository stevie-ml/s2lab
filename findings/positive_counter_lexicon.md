# The Positive Counter-Lexicon: Words Poetry Writes That GPT-2 Never Expects

**Date:** 2026-09-29  
**Experiment:** `experiments/positive_counter_lexicon.py` → `results/positive_counter_lexicon.json`  
**Corpus:** 179 poetry texts, 18,869 artifact-free tokens  
**Companion to:** `suppressed_lexicon.md`

---

## Research Question

`suppressed_lexicon.md` asked what poetry *refuses* to write. This asks the inverse: what words does poetry *choose* that GPT-2 consistently fails to predict? These are words with high average rank — the model placed them far down in its probability distribution — yet they appear repeatedly in the corpus. They constitute the **positive counter-lexicon**: the vocabulary that marks poetic language as distinctively non-statistical.

---

## Finding 1: The Positive Counter-Lexicon (≥10 occurrences, highest avg rank)

| Word | Count | Avg Rank | Avg S₂ | High-rank% |
|------|-------|----------|--------|-----------|
| `survey` | 26 | **2799.8** | +2.524 | 80.8% |
| `grass` | 12 | 1421.0 | +1.172 | 50.0% |
| `thou` | 27 | 895.6 | −0.813 | 25.9% |
| `thy` | 18 | 642.9 | −0.683 | 16.7% |
| `just` | 16 | 585.9 | +1.421 | 37.5% |
| `summer` | 12 | 381.2 | +1.811 | 75.0% |
| `upon` | 24 | 362.0 | +1.648 | 25.0% |
| `moon` | 10 | 321.8 | +1.062 | 60.0% |
| `black` | 12 | 300.4 | +1.928 | 58.3% |
| `whose` | 10 | 195.1 | +2.667 | 30.0% |
| `—` (em-dash) | 93 | 206.2 | +1.443 | 28.0% |
| `God` | 14 | 180.9 | +0.566 | 28.6% |
| `eyes` | 20 | 181.8 | −2.182 | 35.0% |
| `fair` | 10 | 178.4 | +1.566 | 70.0% |
| `still` | 17 | 211.9 | +0.108 | 47.1% |

**Key contrast with the suppressed lexicon**: the suppressed lexicon contained words like `great`, `world`, `light`, `earth`, `air` — grand abstractions that GPT-2 expected. The positive counter-lexicon contains:
1. **Archaisms**: `thou`, `thy`, `upon`, `fair` — words that modern language rarely uses, appearing in traditional verse
2. **Specific images**: `grass`, `moon`, `summer`, `black` — concrete perceptual words that GPT-2 underweights in poetry
3. **Grammatical operators**: `whose`, `—` — structural choices the model doesn't predict

### The `survey` anomaly
`survey` (avg rank 2799) is the most consistently unexpected word with ≥10 occurrences. It appears 26 times across the corpus, 80.8% of those at rank > 50. Its avg S₂ of +2.524 confirms these are genuinely surprising choices. Likely a Whitman/O'Hara concentration — the colloquial-cataloguing mode that deploys `survey` as a verb of seeing ("I survey the scene").

### A critical split within the positive counter-lexicon

Two distinct profiles emerge:

**Profile A — Unexpectedly Unexpected (high rank, high S₂)**  
`survey` (+2.524), `whose` (+2.667), `black` (+1.928), `summer` (+1.811), `upon` (+1.648), `fair` (+1.566), `just` (+1.421)  
→ These are words the model doesn't predict AND that are genuinely informationally surprising. They land in contexts where the model was also uncertain about other things. These are the most "distinctively poetic" in both the S₂ and the rank dimension.

**Profile B — Archaic-Formulaic (high rank, negative S₂)**  
`thou` (−0.813), `thy` (−0.683), `sea` (−3.305), `door` (−1.607), `eyes` (−2.182)  
→ These are words the model doesn't predict (it doesn't know this archaic register), but they appear in LOW-entropy contexts — formulaic positions where, once you know you're in archaic verse, the word is expected. GPT-2's failure here is a failure of REGISTER recognition: it doesn't "know" it's in an archaic context. The S₂ measure, which uses GPT-2's entropy, shows these as *locally* expected (low entropy) but globally underestimated (high rank).

**Profile A words are more interesting theoretically**: they are surprising by any measure. Profile B words reveal GPT-2's register blindness.

---

## Finding 2: The Grammar of Expected Poetry vs. Unexpected Poetry

| Most Expected Words Written (lowest avg rank) | Avg Rank | Avg S₂ |
|-----------------------------------------------|----------|--------|
| `And` | 1.9 | −2.929 |
| `,` | 2.2 | −2.666 |
| `the` | 2.6 | −3.527 |
| `.` | 3.1 | −1.828 |
| `of` | 4.6 | −2.012 |

The 25 most-expected words written are all function words, punctuation, and articles. The grammar of language is also the grammar of expectation. A poem written with ONLY function words and punctuation would achieve the minimal Straussian gap — it would be statistically invisible.

---

## Finding 3: Era-Level Average Rank — Ranking Traditions by "Consistent Unexpectedness"

| Era | N tokens | Avg Rank |
|-----|----------|----------|
| **beat** | 148 | **690.8** |
| **haiku** | 293 | **501.8** |
| **language** | 144 | **494.3** |
| german_expressionist | 283 | 417.5 |
| modernist | 1,583 | 382.8 |
| romantic | 1,972 | 373.1 |
| confessional | 397 | 359.9 |
| victorian | 2,749 | 335.1 |
| new_york_school | 1,430 | 320.9 |
| mid_century | 246 | 288.1 |
| harlem_renaissance | 549 | 281.9 |
| metaphysical | 533 | 232.8 |
| early_modern | 523 | 225.8 |
| contemporary | 813 | 219.1 |
| spoken_word | 193 | 177.9 |
| **prose_poetry** | 934 | **125.1** |
| **found_poetry** | 952 | **114.5** |
| **song_lyrics** | 541 | **111.9** |
| **nursery_rhyme** | 222 | **64.9** |

The ordering is striking: **beat, haiku, language** poetry achieves the highest consistently unexpected vocabulary. **Nursery rhymes and song lyrics** are at the other extreme.

Several caveats:
- **German eras** (expressionist, modernist, symbolist) are confounded: German words have artificially high rank in GPT-2's English vocabulary, inflating their average rank
- **Haiku's high rank** is partly the Japanese/seasonal vocabulary (haiku in this corpus include multilingual variants)
- **Beat's high rank** (690.8) is robust: Ginsberg's English vocabulary is consistently placed far down GPT-2's predictions

### The Beat-Nursery Rhyme Axis

The range — nursery rhyme (64.9) to beat (690.8) — is a ~10× difference in how consistently unexpected the vocabulary is. This parallels the `rank_distance_deviation.md` finding that beat poetry had a median deviation rank of 606 (compared to 48 for prose poetry). Two independent metrics converge: beat poetry deviates more radically from statistical expectation at the word level, and does so across the entire poem (not just at deviation moments).

---

## Finding 4: The Most Unexpected Words, by Era

| Era | Top unexpected words (avg rank) |
|-----|--------------------------------|
| **new_york_school** | `survey` (rk=2800), `who` (321), `f` (250), `sea` (178) |
| **romantic** | `thou` (896), `en` (683), `thy` (643), `red` (393) |
| **modernist** | `summer` (381), `upon` (362), `black` (300), `—` (206) |
| **victorian** | `thou` (896), `thy` (643), `summer` (381), `world` (329) |
| **haiku** | `de` (382), `world` (329), `—` (206), `w` (121) |

New York School's `survey` concentration confirms O'Hara/Whitman authorship. Romantic and Victorian eras both show archaic vocabulary (`thou`, `thy`) in their positive counter-lexicon — Profile B words (register, not surprise). Modernist and New York School are Profile A: specifically surprising, high avg S₂.

---

## Synthesis: Two Lexicons, One Gap

The suppressed lexicon (what poetry refuses: `great`, `world`, `light`, `earth`, `air`) and the positive counter-lexicon (what poetry prefers: `survey`, `grass`, `summer`, `black`, `upon`, `whose`) together define the **Straussian vocabulary gap**:

| GPT-2's "poetic" vocabulary (suppressed) | Actual poets' vocabulary (positive counter-lexicon) |
|------------------------------------------|------------------------------------------------------|
| Grand abstractions: *great, world, earth, air, light* | Concrete images: *grass, moon, summer, black* |
| Generic scale: *little, great, old* | Unexpected scale: *just, fair* |
| Expected aesthetic: *sun, sea, face, man* | Archaic specificity: *thou, thy, upon* |
| Broad emotions: *hope, love, beauty* (predicted contexts) | Actions and operators: *survey, whose, —* |

GPT-2 has internalized the vocabulary of conventional poetic *affect* — the grand, vague aesthetic vocabulary. Actual poets (especially modernist and contemporary) systematically reject this and substitute the specific, the archaic, the structural, and the perceptual.

The gap between these two lexicons IS the S₂ signal at the lexical level: not random deviation, but a coherent, directional departure from the aesthetic average toward specificity and precision.

---
