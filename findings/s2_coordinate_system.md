# The S₂ Coordinate System: Mapping Surprisal-Entropy Space

**Date:** 2026-10-07
**Experiment:** `experiments/s2_coordinate_system.py`
**Corpus:** 225 texts (11 new poems added this run)
**New poems:** Gregory Corso ×2, Lawrence Ferlinghetti ×2, Gottfried Benn ×2, Georg Heym ×2, Louise Glück (prose), Russell Edson (prose), Carolyn Forché (prose)

---

## Motivation

Every token in the corpus lives at a point in 2D (surprisal, entropy) space. S₂ = surprisal − entropy captures the diagonal, but the two dimensions carry different meanings:

- **Surprisal** = how wrong GPT-2 was (how low was the actual token's probability)
- **Entropy** = how certain GPT-2 was before writing anything

These two dimensions together define four distinct *surprise regimes*:

| Quadrant | Surprisal | Entropy | Meaning |
|---|---|---|---|
| **Q1** | High | High | *Ambiguous surprise* — model was uncertain AND still wrong |
| **Q2** | High | Low | *Confident mismatch* — model was sure; poet defied it |
| **Q3** | Low | Low | *Confident match* — model was sure; poet agreed |
| **Q4** | Low | High | *Lucky guess* — model was uncertain; prediction happened right |

**Q2 is the purest Straussian moment** — the poet departed from a *confident* consensus, not just an uncertain one. Q1 surprises happen when language was already in flux; Q2 surprises are true anti-consensus moves.

Thresholds set at corpus medians (surprisal median = 4.77 bits; entropy median = 6.34 bits) on artifact-filtered tokens (p_newline < 0.9).

---

## Results

### Corpus-Level Quadrant Distribution (artifact-free)

| Quadrant | Count | % | Avg S₂ |
|---|---|---|---|
| Q1: High surp + High ent (ambiguous surprise) | 9,130 | **36.8%** | +0.926 |
| Q2: High surp + Low ent  (confident mismatch) | 3,286 | **13.2%** | +4.123 |
| Q3: Low surp  + Low ent  (confident match) | 9,131 | **36.8%** | −1.891 |
| Q4: Low surp  + High ent (lucky guess) | 3,287 | **13.2%** | −4.382 |

By construction, Q1≈Q3 and Q2≈Q4 in token count (quadrant size depends on median splits). The striking result is in the **S₂ averages**:
- Q2 tokens average **+4.12 bits** — far higher than Q1's +0.93
- Q4 tokens average **−4.38 bits** — far lower than Q3's −1.89
- The 13.2% of tokens in Q2 account for *most* of the positive S₂ signal in the corpus

**Finding:** Confident mismatches (Q2) are rare but informationally dominant — they drive the poetry-vs-prose gap more than ambiguous surprises do.

---

### Two Strategies for Poetic Surprise: Q2/Q1 Ratio

Poets cluster into two camps:

**Confident-mismatch strategists** (Q2 > Q1, Q2/Q1 > 1.0): They disproportionately choose surprising tokens at moments when the model was MOST CERTAIN. Their defiance is precise.

| Poet | Q2% | Q1% | Q2/Q1 | n |
|---|---|---|---|---|
| Thomas Jefferson (found text) | 10.8% | 5.4% | **2.00** | 148 |
| Emmett Williams | 20.0% | 10.9% | **1.83** | 55 |
| **W.S. Merwin** | 23.3% | 13.3% | **1.75** | 60 |
| Russell Edson | 22.0% | 16.2% | **1.36** | 241 |
| Charles Baudelaire | 21.2% | 17.8% | **1.19** | 146 |
| Frank O'Hara | 25.9% | 22.8% | **1.14** | 162 |

**Ambiguous-surprise strategists** (Q1 >> Q2): They produce surprises mainly in high-entropy contexts — where language was already in flux. Their deviations are less targeted.

| Poet | Q1% | Q2% | Q1/Q2 | n |
|---|---|---|---|---|
| Ernest Dowson | 44.4% | 2.5% | **18.0** | 81 |
| Ron Silliman | 56.0% | 4.0% | **14.0** | 50 |
| Gertrude Stein | 42.9% | 3.6% | **12.0** | 84 |
| Vachel Lindsay | 39.6% | 3.3% | **12.0** | 91 |
| John Donne | 49.4% | 7.6% | **6.5** | 172 |
| William Blake | 45.5% | 8.5% | **5.4** | 567 |

---

### Eras Ranked by Confident-Mismatch Rate

| Era | poems | Q2% | Q1% | Note |
|---|---|---|---|---|
| prose_poetry | 9 | **18.8%** | 24.0% | Artifact-free! High Q2 rate |
| biblical | 7 | 18.0% | 20.5% | |
| german_modernist | 2 | 17.5% | 44.4% | High Q1 also |
| spoken_word | 2 | 17.1% | 32.1% | |
| latin_american | 3 | 15.9% | 26.4% | |
| beat | 2 | 14.9% | 39.2% | Raw S₂ high; Q2 moderate |
| german_expressionist | 4* | 13.4% | 49.8% | Very high Q1 |
| control (prose) | 5 | 8.6% | 21.5% | Lowest Q2 |

*German expressionist now expanded with Benn and Heym poems.

**Key observation:** German expressionist has very high Q1 (49.8%) but low Q2 (13.4%) — the Q1/Q2 ratio of ~3.7 means their surprises happen predominantly in *uncertain* contexts. Their high raw S₂ comes from volume of ambiguous surprises, not precise confident mismatches.

Beat's raw S₂ is high but Q2 rate is moderate (14.9%) — suggesting beat's high surprisal comes partly from entropy rather than targeted anti-consensus moves.

**Prose poetry leads in Q2% (18.8%)** with no stanza-break artifact. The prose poem tradition (Glück, Forché, Edson) generates genuine confident mismatches at a higher rate than any poetic era.

---

### Top Confident-Mismatch Tokens (Purest Anti-Consensus Moves, artifact-free)

| Token | S₂ | Surp | Ent | Model expected | Source |
|---|---|---|---|---|---|
| "climbs" | +28.25 | 28.54 | 0.29 | `,`, `\n` | Ferlinghetti, "Constantly Risking Absurdity" |
| "glass" | +25.63 | 25.73 | 0.09 | `,` | Marianne Moore, "The Fish" |
| "whenever" | +25.60 | 25.89 | 0.29 | `,`, `\n` | Ferlinghetti, "Constantly Risking Absurdity" |
| "shook" | +22.04 | 25.64 | 3.60 | `the`, `a` | Gerard Manley Hopkins, "God's Grandeur" |
| "prank" | +22.02 | 24.74 | 2.72 | `the`, `his` | Christopher Smart, "For I Will Consider My Cat Jeoffry" |
| "suffering" | +20.68 | 22.48 | 1.80 | `,`, `\n` | Ferlinghetti, "In Goya's greatest scenes" |
| "badly" | +20.59 | 22.23 | 1.64 | `glass`, `of` | Elizabeth Bishop, "One Art" |
| "list" | +19.48 | 20.65 | 1.18 | `ever`, `is` | Thomas Wyatt, "Whoso List to Hunt" |
| "Jesus" | +19.03 | 22.23 | 3.20 | `,`, `stall` | E.E. Cummings, "Buffalo Bill's" |
| "stacked" | +18.16 | 22.97 | 4.81 | `time`, `tense` | Claudia Rankine, "Citizen" |

**Note on Ferlinghetti:** His visual-layout poems ("Constantly Risking Absurdity," "In Goya's greatest scenes") use extreme indentation — these create a **spatial-layout artifact** analogous to the stanza-break artifact, where the model expects continuation punctuation after a run of spaces. Tokens like `gro`, `p`, `in`, `to` are fragment-tokens of content words that appear after unusual whitespace. These should be filtered or flagged in future work as "spatial-layout positions."

---

## Discussion: The W.S. Merwin Finding

**W.S. Merwin has the highest Q2/Q1 ratio (1.75) among poets with substantial sample sizes and Q2 rates.** Merwin famously removed all punctuation from his poetry — no commas, no periods. This seemingly simple act has a profound effect on the model's confidence dynamics:

Without punctuation, the model must predict word boundaries and clause endings without the usual syntactic signposts. This means:
1. The model often reaches high confidence for certain completions at clause boundaries (predicting common collocations like `the` + noun, or `and` + verb)
2. Merwin's unpunctuated line-turns then deliver something completely different — a new clause beginning unexpectedly

The result: Merwin's surprises happen disproportionately when the model was most certain. He doesn't just add chaos; he targets the model's moments of certainty.

---

## New Poem Findings

| New Poem | Era | Avg S₂ | Q2/Q1 | Note |
|---|---|---|---|---|
| "Marriage" (Corso) | beat | +0.960 | ? | Highest avg S₂ of new additions |
| "Umbra Vitae" (Heym) | german_expressionist | +0.599 | ? | High Q1 pattern |
| "The Wild Iris" (Glück) | prose_poetry | +0.397 | ? | Prose, no artifact |
| "The Colonel" (Forché) | prose_poetry | −0.301 | ? | Documentary prose, lower S₂ |
| "Pillow" (Edson) | prose_poetry | −0.854 | ? | Fabulist prose, most predictable |
| "Constantly Risking…" (Ferlinghetti) | beat | −0.077 | ? | Spatial-layout artifact contaminates |

Corso's "Marriage" (avg S₂ = +0.960) is the highest-S₂ beat poem in the corpus, beating Ginsberg's "Howl" opening. This may reflect Corso's more varied syntactic structure versus Ginsberg's long catalog lines.

---

## Suggested Next Steps

1. **Filter spatial-layout artifact**: Ferlinghetti and other visual poets have whitespace-created token positions analogous to the stanza-break artifact. Develop a "space-run" filter (tokens following >2 consecutive space tokens) to complement the existing newline filter.

2. **Q2 deep-dive for Merwin**: Get the full Merwin corpus (not just fragments) and test whether the Q2/Q1 ratio holds at scale — this would be a strong finding for a paper on punctuation-removal as anti-consensus strategy.

3. **Prose poetry Q2 profile**: With 12 prose poems now in the corpus, test whether prose poetry's high Q2 rate holds with expanded sample (add Simic, Ponge in translation, Russell Edson full poems).

4. **Two-strategy taxonomy**: Formalize the Q2 vs Q1 strategist distinction. Q2 poets (O'Hara, Merwin, Edson, Baudelaire) vs. Q1 poets (Stein, Donne, Blake, Milton) — does this map onto the colloquial/formal distinction? Q2 = colloquial syntax with surprising lexis; Q1 = archaic/unusual syntax where even function words become uncertain?
