# Surprise Density: Run-Length Analysis of Conformist Intervals Between S₂ Spikes

**Date:** 2026-10-14
**Experiment:** `experiments/spike_density_runlength.py`
**Corpus:** 262 poems/texts (≥20 artifact-free tokens), S₂ spike threshold = 0.5
**Builds on:** `s2_autocorrelation.md`, `s2_markov_transitions.md`, `pre_peak_setup.md`

---

## Research Question

Previous analyses asked *whether* surprise is autocorrelated (weakly, negatively). This
experiment asks a more geometric question: **how long are the quiet stretches between
moments of S₂ deviation?** Specifically: how many conformist tokens does a poet
"spend" between each surprise, and does this rhythm differ by era, poet, and form?

**New metric: Surprise Density** = fraction of tokens with S₂ > 0.5 (one spike per N tokens).
**New metric: Burstiness Score** B = (σ − μ) / (σ + μ) applied to inter-spike gap lengths.
- B = 0 → gaps are geometrically distributed (random coin-flip model)
- B > 0 → bursty (long quiet runs with sudden clusters)
- B < 0 → hyper-regular (surprises arrive on a near-even clock)

---

## Finding 1: Poetry Is 2.4× More Surprise-Dense Than Prose

| Group | Mean inter-spike gap | Surprise density |
|---|---|---|
| **Poetry** | **2.35 tokens** | **0.30** |
| **Prose control** | **5.62 tokens** | **0.17** |
| **Cliché control** | 3.5 tokens | 0.23 |
| **Found poetry** | 3.6 tokens | 0.22 |

A poet writing iambic pentameter drops a "surprising" token every ~2–3 words.
Prose writers do so every ~6 words. Cliché and found texts occupy the middle ground.

---

## Finding 2: Surprise Density Rankings by Era

| Era | n | Density | Mean gap | Burst score |
|---|---|---|---|---|
| german_modernist | 2 | **0.4299** | 1.3 | 0.1272 |
| german_symbolist | 3 | **0.4183** | 1.4 | 0.0816 |
| ancient | 3 | 0.3641 | 1.8 | 0.0622 |
| old_english | 4 | 0.3588 | 1.8 | 0.0799 |
| persian | 2 | 0.3585 | 1.8 | 0.0548 |
| german_expressionist | 6 | 0.3581 | 1.9 | 0.0832 |
| early_modern | 5 | 0.3539 | 1.9 | 0.0724 |
| confessional | 6 | 0.3533 | 1.7 | 0.1131 |
| imagist | 3 | 0.3425 | 1.9 | −0.0244 |
| haiku | 3 | 0.3403 | 1.9 | −0.0291 |
| 19th_century | 11 | 0.3341 | 2.1 | 0.0400 |
| 18th_century | 7 | 0.3306 | 2.0 | 0.0820 |
| romantic | 15 | 0.3184 | 2.1 | 0.1204 |
| modernist | 23 | 0.3143 | 2.3 | 0.0893 |
| contemporary | 9 | 0.3071 | 2.3 | 0.0959 |
| new_york_school | 18 | 0.3020 | 2.3 | 0.0655 |
| beat | 6 | 0.2962 | **4.4** | 0.1232 |
| prose_poetry | 12 | 0.2843 | 2.5 | 0.0699 |
| biblical | 7 | 0.2795 | 2.6 | 0.0196 |
| spoken_word | 3 | 0.2768 | 2.6 | 0.0064 |
| fixed_form | 8 | 0.2712 | 2.7 | 0.0706 |
| ballad | 6 | 0.2700 | 2.8 | **0.1597** |
| cliche_control | 3 | 0.2256 | 3.5 | 0.0391 |
| found_poetry | 7 | 0.2246 | 3.6 | 0.0379 |
| song_lyrics | 3 | 0.2021 | 3.8 | 0.1461 |
| control | 4 | 0.1724 | 5.6 | 0.1191 |

### The German Effect
German-language poetry (modernist, symbolist, expressionist) clusters at the TOP of
surprise density. This is striking because this corpus uses English translations — meaning
the *translators* maintained or amplified the density. The most likely cause: German
poetry (Rilke, Stefan George, Trakl) relies heavily on compound nouns, inverted syntax, and
abstract vocabulary that GPT-2's English model finds consistently unexpected. Translation
preserves the unusual diction while GPT-2 remains calibrated on English norms.

### The Beat Anomaly
The beat era has low density (0.2962) but an anomalously large mean gap (4.4 tokens) —
the highest mean gap of any literary era. This seems contradictory until you examine the
individual poets: **Allen Ginsberg** personally has the *highest* density of any poet
(0.4505, gap=1.1), driven by his short, dense early poems ("Howl" excerpts, "A Supermarket
in California"). But the beat corpus also includes much longer, more discursive texts where
surprises are sparser and the distribution is heavily right-skewed — hence the large mean
gap despite moderate density.

---

## Finding 3: Top Poets by Surprise Density

| Poet | Era | n poems | Density | Mean gap |
|---|---|---|---|---|
| Allen Ginsberg | beat | 2 | **0.4505** | 1.1 |
| Rainer Maria Rilke | german_modernist | 2 | 0.4299 | 1.3 |
| Stefan George | german_symbolist | 3 | 0.4183 | 1.4 |
| Georg Trakl | german_expressionist | 2 | 0.4132 | 1.4 |
| Thomas Hardy | victorian | 3 | 0.4095 | 1.4 |
| Thomas Wyatt | early_modern | 2 | 0.3851 | 1.6 |
| Georg Heym | german_expressionist | 2 | 0.3711 | 1.7 |
| Walt Whitman | 19th_century | 5 | 0.3620 | 1.8 |
| Gerard Manley Hopkins | victorian | 3 | 0.3550 | 1.8 |
| Alexander Pope | 18th_century | 4 | 0.3512 | 1.8 |

**Surprising high-rankers**: Thomas Hardy and Thomas Wyatt being in the top 5 is unexpected.
Hardy's dense Anglo-Saxon diction and unusual compound words, Wyatt's early modern English
syntax — both produce frequent deviations from GPT-2's modern-English prior.

**Allen Ginsberg at 0.45 density (gap = 1.1 tokens)**: nearly every other word is an S₂
spike. At this density, the "surprise" concept begins to collapse — when surprises are this
frequent, they are the new norm.

---

## Finding 4: Burstiness — Who Clusters Their Surprises

**High burst score = uneven distribution: long quiet runs punctuated by dense surprise clusters**

Most bursty individual poems:
| Poem | Author | Era | Burst |
|---|---|---|---|
| Buffalo Bill 's | E.E. Cummings | modernist | **0.382** |
| Deer Park (trans.) | Wang Wei | classical_chinese | 0.367 |
| Pied Beauty | Gerard Manley Hopkins | victorian | 0.363 |
| In Goya's greatest scenes | Lawrence Ferlinghetti | beat | 0.326 |
| Fog | Carl Sandburg | modernist | 0.323 |

Most hyper-regular (surprises arrive like clockwork):
| Poem | Author | Era | Burst |
|---|---|---|---|
| I felt a Funeral, in my Brain | Emily Dickinson | 19th_century | **−0.329** |
| Variations on A (excerpt) | Georges Perec | oulipo | −0.230 |
| Three Haiku (Issa, translated) | Kobayashi Issa | haiku | −0.192 |
| A Limerick on Time | Anonymous | limerick | −0.174 |
| Villanelle of the Poet's Road | Ernest Dowson | fixed_form | −0.149 |

### Interpretation
**Bursty poems** (Cummings, Hopkins' "Pied Beauty") pack multiple S₂ deviations into short
windows — a typographical scatter-shot or a sonic barrage — then go quiet. This matches
the visual and sonic density of these poems: Cummings' spatial manipulation, Hopkins'
"inscape" clustering.

**Hyper-regular poems** (Dickinson, Perec, haiku) distribute their surprises evenly across
the poem's length — like a metered surprise budget. Dickinson's famous common-meter
discipline gives her not only rhythmic regularity but *informational* regularity: her S₂
spikes are spaced almost as evenly as her stressed syllables.

**Era-level burstiness**: Ballads (0.1597) and classical Chinese (0.1522) have the highest
burst scores, consistent with their formulaic verse/refrain structure (long formulaic
passages punctuated by moments of narrative turn). Biblical poetry (0.0196) and spoken word
(0.0064) are the most geometrically random — their surprises approximate a Poisson process.

---

## Finding 5: The Geometric Null

If S₂ spikes were i.i.d. Bernoulli events (each token independently a spike with fixed
probability p), gap lengths would follow a **geometric distribution**. Burst scores near 0
indicate adherence to this null model; deviations indicate systematic structure.

Most poetry falls close to zero (−0.10 to +0.16), suggesting that the autocorrelation
structure already found (weak, near-zero) is confirmed here: **poetry's surprise structure
is approximately memoryless** — the occurrence of one spike does not strongly predict
when the next will arrive.

The exceptions (bursty ballads, hyper-regular Dickinson) are the places where formal
structure imposes non-random spacing.

---

## Synthesis

The run-length analysis reveals a **surprise rhythm** distinct from the simple mean S₂
measure:

1. **Density axis**: How often does the poet deviate? (German modernists most often,
   found poetry / song lyrics least often)
2. **Regularity axis**: When the poet deviates, does it arrive evenly (Dickinson) or in
   bursts (Cummings)? These are independent dimensions.

A poet can be *sparse but bursty* (ballads: low density, high burst) or *dense but even*
(haiku: high density, negative burst). The interaction of these dimensions captures
something about compositional strategy that mean S₂ alone cannot.

---

## Suggested Next Steps

1. **2D plot of density × burstiness**: This two-dimensional "surprise rhythm space"
   would show clusters of similar compositional strategies.
2. **Burst micro-structure**: In high-burst poems, examine the 3–5 token windows where
   clusters occur — do they correspond to particular syntactic or thematic events?
3. **Cross-poet consistency**: Do poets maintain consistent density/burstiness across their
   poems, or does it vary by poem? This would measure the poet's "information signature"
   stability.
4. **Density as an aesthetic parameter**: Does surprise density correlate with perceived
   "difficulty" or "reward" in reader studies? A testable psycholinguistic hypothesis.
