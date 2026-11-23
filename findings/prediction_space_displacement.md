# Prediction Space Displacement: Local Detours vs. Trajectory Forks

**Date:** 2026-11-23  
**Experiment:** `experiments/prediction_space_displacement.py`  
**Results:** `results/prediction_space_displacement.json`  
**Corpus:** 436 poems, 11,784 high-S₂ events (S₂ ≥ 2.0, artifact-free)

---

## Research Question

When a poet surprises the reader with a high-S₂ token, does that surprise *redirect* the poem's informational trajectory — or is it merely a local detour that leaves the subsequent path intact?

We define **Prediction Space Displacement (PSD)** around a surprise at position *i* as the Jaccard similarity between the sets of GPT-2's top-10 predicted alternatives at:
- position *i−1* (just before the surprise)
- position *i+1* (just after the surprise)

> **PSD = Jaccard({alts[i−1]}, {alts[i+1]})**

- **Low PSD** = the prediction space changed dramatically around the surprise → "trajectory fork"
- **High PSD** = the prediction space was largely unchanged → "local detour"

This is a new dimension of the Straussian gap. Where S₂ measures *how* surprising a token is, PSD measures *whether the surprise changes what comes next*.

---

## Finding 1: The Aggregate Null — Surprise Size Does Not Predict Trajectory Change

| S₂ Bin | n | Mean PSD |
|--------|---|----------|
| 2–3 bits | 2,818 | **0.0918** |
| 3–5 bits | 3,972 | **0.1003** |
| 5–8 bits | 3,181 | **0.0981** |
| 8–12 bits | 1,398 | **0.0966** |
| 12+ bits | 415 | **0.0834** |

The global mean PSD across all 11,784 events is **0.0966** — meaning that after a poetic surprise, the two neighboring prediction spaces share only ~10% of their alternatives (by Jaccard). This confirms that **poetic surprises are informationally disruptive** in general: the prediction landscape before and after a surprise moment barely overlaps.

However: **the magnitude of the surprise (S₂) is essentially uncorrelated with PSD (Pearson r = −0.0029)**. Whether the surprise is 2 bits or 20 bits above entropy makes almost no difference to how much the prediction space shifts.

This extends the null finding of `findings/prediction_diversity_s2.md` to the *aftermath* of surprise: not only does the structure of the pre-surprise prediction space fail to predict S₂, but S₂ itself fails to predict post-surprise prediction-space displacement.

---

## Finding 2: Era-Level Variation — Form Determines Whether Surprises Redirect

Despite the aggregate null, **eras vary substantially in their mean PSD**:

### Lowest PSD eras (surprises most redirect the trajectory)

| Era | n | Mean PSD |
|-----|---|----------|
| triolet | 17 | **0.010** |
| japanese_classical | 14 | **0.048** |
| nursery_rhyme | 39 | **0.055** |
| deep_image | 18 | **0.058** |
| song_lyrics | 77 | **0.065** |
| found_poetry | 179 | **0.068** |
| spoken_word | 53 | **0.072** |
| prose_poetry | 271 | **0.075** |
| procedural | 138 | **0.076** |
| limerick | 69 | **0.076** |

### Highest PSD eras (surprises are local detours)

| Era | n | Mean PSD |
|-----|---|----------|
| latin_american | 104 | **0.113** |
| war_poetry | 142 | **0.122** |
| protest_political | 48 | **0.122** |
| concrete | 52 | **0.124** |
| rondeau | 24 | **0.130** |
| metaphysical | 184 | **0.134** |
| old_english | 141 | **0.149** |

**Old English poetry has the highest mean PSD (0.149)**: surprises in Beowulf and the elegies are local deviations that do not redirect the kenning-based formulaic trajectory. **Metaphysical poetry (0.134)** follows: once a Donne conceit is established, surprise within the conceit does not change the poem's predictive arc.

**Triolets (0.010) and Japanese classical poetry (0.048)** are most trajectory-disruptive — a surprising word in a 7-line, refrain-locked form sends the prediction space into entirely uncharted territory, since the tight constraint makes every surprise a genuine "fork."

---

## Finding 3: The Direction of S₂–PSD Correlation Splits by Form Type

A within-era Pearson analysis reveals a systematic split:

### Negative r eras (larger surprises redirect LESS)

| Era | Pearson r | Interpretation |
|-----|-----------|----------------|
| villanelle | −0.160 | Refrain returns trajectory after any surprise |
| haiku | −0.177 | Compression means surprise is immediately absorbed |
| found_poetry | −0.119 | External source text constrains re-entry |
| beat | −0.110 | Improvisational energy absorbed by the oral flow |
| language | −0.083 | Syntactic disruption is itself the expected move |

### Positive r eras (larger surprises DO redirect more)

| Era | Pearson r | Interpretation |
|-----|-----------|----------------|
| metaphysical | +0.101 | Bigger conceit leaps change the metaphorical domain |
| concrete | +0.308 | Spatial/visual disruption has cumulative effect |
| spoken_word | +0.349 | Performed surprise (emphasis) genuinely redirects |
| prose_poetry | +0.196 | No formal constraint to absorb the surprise |

**The split is interpretable**: in forms with strong structural constraints (villanelle, haiku, beat oral tradition), even large surprises are "absorbed" and do not change the subsequent prediction space — the form enforces a return to the expected path. In freer or more visually-structured forms (concrete poetry, spoken word, prose poetry), larger surprises genuinely redirect the poem's trajectory.

This suggests that **poetic form is not just an aesthetic constraint but an informational constraint**: it determines whether surprise has cumulative (trajectory-changing) or local (ornamental) effects.

---

## Finding 4: Exemplary Trajectory Forks and Local Detours

### Local Detours (high PSD — the trajectory absorbs the surprise)

| Poet | Token | S₂ | PSD | Note |
|------|-------|-----|-----|------|
| Pablo Neruda | " stones" | 11.98 | 0.818 | Surrealist noun in mid-poem; path unchanged |
| George Herbert | " free" | 4.30 | 0.818 | Conceit absorbs the adjective |
| Emmett Williams (concrete) | "for" | 11.13 | 0.818 | Visual constraint overrides semantic surprise |

The most striking: **Neruda's " stones" with S₂ = 11.98** (extremely high) but PSD = 0.82. The model is enormously surprised by this word, but the prediction space before and after is nearly identical. The surrealist image intrudes and leaves without redirecting the poem's trajectory.

### Trajectory Forks (low PSD — the surprise changes what comes next)

The lowest-PSD events tend to cluster around proper nouns ("cloud," "val-" subwords from "valleys") and strongly content-shifted moments where the prediction space completely reorients. After a proper noun in an unexpected position, the entire semantic horizon of the poem changes: who and what the poem is "about" shifts.

---

## Theoretical Interpretation

We can now distinguish two fundamentally different functions of poetic surprise:

1. **Ornamental surprise** (high PSD): a local deviation that creates reader surprise without redirecting the informational trajectory. The poem "knows where it's going" — the high-S₂ token is a detour, not a turn. Common in: formal verse, extended conceits, kenning-based Old English.

2. **Directional surprise** (low PSD): a fork in the informational path. After this token, GPT-2's prediction space fundamentally shifts. The poem's subsequent language is constrained differently. Common in: free verse spoken word, concrete poetry, prose poetry, some triolet.

The aggregate null result (r ≈ 0 between S₂ and PSD) confirms that these two types of surprise are **orthogonal dimensions**: a surprise can be large but ornamental, or small but trajectory-changing. Neither S₂ alone nor the prediction diversity (from prior work) distinguishes them.

**PSD is a new independent axis of the Straussian gap**: not how surprising, but how consequential.

---

## Suggested Next Steps

1. **Measure PSD at structurally significant positions** (volta, turn, envoi) vs. non-structural positions within the same poems to test if PSD is higher at "pivots."
2. **Within-poem PSD trajectory**: does PSD increase as a poem approaches its close? Do poems end on trajectory forks or local detours?
3. **PSD vs. reader re-reading rates**: if ornamental surprise (high PSD) characterizes poems where "the trajectory stays intact," those poems might be MORE predictable on second reading. Directional-surprise poems (low PSD) might feel different on second reading.
4. **Control the subword artifact**: some lowest-PSD events involve subword tokens (partial-word GPT-2 BPE splits) where the prediction space shifts for mechanical reasons. A stricter filter to whole-word tokens would clean this.
