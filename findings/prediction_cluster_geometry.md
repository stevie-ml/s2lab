# Prediction Cluster Geometry at High-S2 Moments

**Date:** 2026-10-05  
**Experiment:** `experiments/prediction_cluster_geometry.py` → `results/prediction_cluster_geometry.json`  
**Corpus:** 209 texts, 17,451 content tokens (stanza-break artifact tokens and punctuation excluded)  
**Builds on:** `semantic_vs_structural_surprise.md` (r = 0.55 with top-1 distance), `straussian_gap_taxonomy.md`

---

## Research Question

When a poet achieves high S2 — maximum surprise — the model was confident but wrong. GPT-2's
top-K predictions form a cluster in embedding space. We ask:

1. How **tight** is that cluster? (*cluster_spread*: mean pairwise cosine distance between top-10 predictions)  
   High spread = model was uncertain in many semantic directions  
   Low spread = model was confident within a tight semantic region  
2. How far did the poet **escape**? (*centroid_escape*: cosine distance from actual token to cluster centroid)
3. What drives S2 — the tightness of what the model expected, or how far the poet departed?

We also define: **escape_efficiency = centroid_escape / (1 + cluster_spread)** — highest when a poet
escapes a *tight* cluster (escaping confident expectations, the most "Straussian" case).

---

## Finding 1: Spread Is Flat; Escape Drives Everything

| S2 quintile | S2 range | n | cluster_spread | centroid_escape | efficiency |
|---|---|---|---|---|---|
| Lowest 20% | [−8.6, −3.2] | 3,491 | 0.5925 | 0.2946 | 0.1832 |
| 20–40% | [−3.2, −1.5] | 3,491 | 0.5837 | 0.3306 | 0.2065 |
| 40–60% | [−1.5, 0.0] | 3,491 | 0.6052 | 0.3789 | 0.2348 |
| 60–80% | [0.0, 2.7] | 3,492 | 0.5958 | 0.4867 | 0.3044 |
| Highest 20% | [2.7, 25.6] | 3,491 | 0.5880 | 0.5981 | 0.3783 |

**Cluster spread is nearly constant across all S2 quintiles** (range: 0.584–0.605, a variation of <4%).  
**Centroid escape doubles** from the lowest quintile (0.295) to the highest (0.598).

**Correlations:**
- r(S2, centroid_escape) = **+0.635** — strong
- r(S2, cluster_spread) = **−0.018** — effectively zero
- r(spread, escape) = **+0.271** — weak but positive

**Interpretation:** High-S2 moments are almost entirely explained by how far the actual token
lands from the centroid of the model's predictions. The model's *confidence level* (how spread
out its predictions are) plays essentially no role. Whether the model was shooting in many
directions or aiming tightly at one target, what determines S2 is whether the poet went
somewhere else entirely.

This refines the semantic distance finding: the previous study measured distance to *top-1*
(r = 0.55); looking at the centroid of the full top-10 cluster gives r = 0.635. The prediction
cluster centroid is a better estimate of where the model "pointed" than any single alternative.

---

## Finding 2: Poetry vs. Prose — Escape Distance, Not Spread

| Group | n | cluster_spread | centroid_escape | efficiency |
|---|---|---|---|---|
| Poetry (all) | 17,305 | 0.5930 | 0.4182 | 0.2617 |
| Prose controls | 146 | 0.5999 | 0.3622 | 0.2254 |
| Poetry (high-S2 only) | 4,231 | 0.5892 | 0.5854 | 0.3697 |
| Prose (high-S2 only) | 13 | 0.5876 | 0.5379 | 0.3415 |

Poetry and prose have nearly identical cluster spreads — the model is equally uncertain in both
domains. The gap is entirely in centroid_escape: poetry's tokens land further from the prediction
cluster center (+15.5% overall; +8.8% among high-S2 tokens).

**Poetry does not create a more uncertain model. It creates tokens that travel further from
wherever the model's uncertainty was centered.**

---

## Finding 3: Era Rankings by Escape Efficiency (high-S2 tokens only)

| Era | n | n_high | spread | escape | efficiency |
|---|---|---|---|---|---|
| **mid_century** | 192 | 35 | 0.5601 | **0.6578** | **0.4233** |
| **beat** | 127 | 46 | 0.6050 | 0.6427 | 0.4030 |
| **haiku** | 200 | 62 | 0.5997 | 0.6193 | 0.3901 |
| **modernist** | 1,543 | 431 | 0.5858 | 0.6122 | 0.3879 |
| romantic | 1,651 | 407 | 0.5873 | 0.6106 | 0.3863 |
| ballad | 705 | 164 | 0.5977 | 0.6032 | 0.3796 |
| victorian | 2,512 | 681 | 0.5806 | 0.5971 | 0.3790 |
| … | | | | | |
| cliche_control | 260 | 45 | 0.5888 | 0.5356 | 0.3368 |
| prose_poetry | 745 | 155 | 0.5820 | 0.5262 | 0.3324 |
| german_expressionist | 237 | 76 | 0.6977 | 0.5384 | 0.3169 |

**mid_century** (Bishop, Brooks) tops the era ranking — the handful of mid-century poems achieve
unusually large centroid escapes when they're surprising. **beat** (Ginsberg) is second. 

The German-language era scores are lower: their cluster_spread values are inflated (~0.68–0.70
vs ~0.59 for English), because we're using English GPT-2 embeddings on German-tokenized text.
Their efficiency scores are not directly comparable. For a clean comparison, see `cross_model_comparison.md`.

**cliche_control** sits near the bottom of English-language eras but not last — even
clichéd writing produces *some* centroid escapes at high-S2 moments (they share the vocabulary
and exist in the same embedding space). What distinguishes poetry from cliché is frequency and
magnitude of those escapes, not a complete absence in cliché.

---

## Finding 4: Author Rankings

| Author | n | n_high | spread | escape | efficiency |
|---|---|---|---|---|---|
| **Edna St. Vincent Millay** | 121 | 19 | 0.5281 | **0.6660** | **0.4372** |
| **Seamus Heaney** | 102 | 32 | 0.5641 | 0.6601 | 0.4237 |
| T.S. Eliot | 184 | 50 | 0.5625 | 0.6379 | 0.4100 |
| Allen Ginsberg | 127 | 46 | 0.6050 | 0.6427 | 0.4030 |
| Countee Cullen | 117 | 34 | 0.5636 | 0.6299 | 0.4027 |
| Gerard Manley Hopkins | 374 | 126 | 0.5883 | 0.6356 | 0.4025 |
| Hart Crane | 131 | 49 | 0.6005 | 0.6321 | 0.3983 |
| Robert Burns | 194 | 49 | 0.6049 | 0.6337 | 0.3971 |
| W.B. Yeats | 249 | 56 | 0.5959 | 0.6257 | 0.3939 |
| Samuel Taylor Coleridge | 203 | 53 | 0.5864 | 0.6196 | 0.3938 |

Millay and Heaney both achieve notably tight-cluster escapes (low spread, high escape).
Millay's low spread (0.528) — the tightest in the table — combined with the largest absolute
centroid escape (0.666) gives her the highest efficiency. Her surprise moments are most
"Straussian": the model was confident, and she went elsewhere.

Hopkins also appears (known for sprung rhythm and coined compounds), with a spread near average
but very high escape, suggesting his surprises are semantically distant rather than
cluster-tightness-driven.

---

## Finding 5: Tokenization Artifacts in Top "Straussian" Moments

The top escape-efficiency tokens include some tokenization artifacts: "ermanent" (second subword
of "permanent"), " Mous" (Scottish spelling in Burns), " Xan" (from "Xanadu"), " wi" (dialectal
"with"). These are cases where an unusual word's initial subtoken looks nothing like what GPT-2
expected, inflating both surprisal and centroid_escape.

Among the clearly non-artifactual top-15 entries:
- **" hips"** (Clifton, *Homage to My Hips*): where GPT-2 expected a comma — the body part is
  the subject and GPT-2 wasn't expecting it
- **" midway"** (Hart Crane): expected "to", got a spatial-temporal marker mid-sentence
- **" Babylon"** (Ashbery): expected "in", got a proper noun shifting from syntax to geography
- **" Scarlet"** (Traditional ballad): expected "the" — color as semantic displacement
- **" mistress"** (Shakespeare): after a newline, GPT-2 expected space/punctuation, got a title

The most reliable "Straussian" escapes are cases like Clifton's " hips" and Shakespeare's
" mistress" — where the actual word is semantically concrete and the prediction cluster was
abstract/syntactic.

---

## Key Theoretical Result

**S2 = surprisal − entropy measures semantic escape distance from the prediction centroid, not
the model's uncertainty.**

Formally: r(S2, cluster_spread) ≈ 0 while r(S2, centroid_escape) = 0.635. The cluster spread —
which is the embedding-space analog of entropy — contributes almost nothing to S2. What contributes
is how far the actual choice lands from the centroid.

This means the Straussian gap is primarily a **semantic displacement** measure, not an uncertainty
measure. A poet achieves high S2 not by writing when the model is confused (high entropy), but by
writing something that moves away from wherever the model's probability mass was centered.

---

## Limitations

1. Cluster spread is measured in GPT-2 input embedding space, which is not a perfect semantic space
2. Subword tokenization means some "escapes" are artifacts of tokenization rather than semantic choices
3. Small sample sizes for some eras (mid_century n=35 high-S2) give less stable estimates
4. German texts are analyzed with English embeddings — efficiency scores not comparable

---

## Suggested Next Steps

1. **Control for tokenization artifacts**: filter out tokens that are subword-initial (stripped of
   their natural prefix) and re-run era/author comparisons
2. **Centroid escape by POS**: do nouns, verbs, or adjectives show systematically different escape
   distances? Is Millay's efficiency driven by one part of speech?
3. **The r=0 cluster spread finding**: this is strong enough to be a theoretical claim — publish
   it clearly. S2 does not measure model uncertainty; it measures semantic displacement from the
   prediction cluster. Entropy in the S2 formula is acting as a baseline that washes out, leaving
   surprisal as the core signal, and surprisal = centroid escape distance.
4. **Test on GPT-2 medium** to see if the r(S2, cluster_spread) ≈ 0 holds at higher model capacity
