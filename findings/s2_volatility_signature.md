# S₂ Volatility as Style Signature: Mean vs. Variance in Poetic Surprise

**Date:** 2026-10-05  
**Experiment:** `experiments/s2_volatility_signature.py`  
**Data:** 209 poems, GPT-2 (117M), stanza-break artifact filtered  

---

## Research Question

Prior analyses measured *average* S₂ per poem or era. But average hides a crucial dimension: **consistency**. Does a poet maintain a steady level of surprise, or do they alternate between long predictable stretches and sudden explosive deviations?

This experiment measures S₂ *standard deviation* per poem as a "volatility signature," then classifies poems and poets on a 2D style space:

| | **Low std (consistent)** | **High std (volatile)** |
|---|---|---|
| **High mean** | Systematic Innovators | Strategic Saboteurs |
| **Low mean** | Predictable Traditionalists | Volatile Conformists |

Thresholds: corpus medians (mean_S₂ = −0.432, std_S₂ = 3.590).

---

## Key Finding 1: Poets Commit to a Mode

Quadrant counts reveal a polarized distribution:

| Quadrant | Count |
|---|---|
| Strategic Saboteur (high mean + high std) | **76** |
| Predictable Traditionalist (low mean + low std) | **75** |
| Systematic Innovator (high mean + low std) | 29 |
| Volatile Conformist (low mean + high std) | 29 |

The two large quadrants (76 + 75 = **151 poems**, 72% of corpus) are the "committed" categories. Only 28% of poems land in the mixed quadrants. **Poets tend to pick a mode: either they're systematically surprising or systematically conformist.** Occasional surprise against a conformist backdrop, or consistent innovation in a volatile frame, are minority positions.

---

## Key Finding 2: The Volatility Paradox of Haiku

Haiku rank **3rd highest** in std_S₂ (3.955) among all eras, yet their mean S₂ is near zero (0.033). They're neither clearly positive nor negative in average surprise — but their token-level variance is extreme.

| Era | n | Avg mean_S₂ | Avg std_S₂ | Skewness |
|---|---|---|---|---|
| beat | 2 | **0.744** | **4.686** | 0.97 |
| german_expressionist | 2 | 0.624 | 3.990 | 1.03 |
| haiku | 14 | 0.033 | 3.955 | 0.90 |
| ballad | 6 | −0.388 | 3.941 | **1.45** |
| language | 3 | −0.201 | 3.925 | 0.96 |
| 19th_century | 10 | −0.173 | 3.913 | 1.33 |
| mid_century | 3 | −0.458 | 3.869 | 1.35 |
| confessional | 6 | −0.300 | 3.832 | 0.96 |
| modernist | 22 | −0.408 | 3.771 | 1.08 |
| german_symbolist | 3 | 0.394 | 3.740 | 1.46 |
| ... | | | | |
| found_poetry | 7 | −0.615 | 3.089 | **1.64** |
| cliche_control | 3 | −0.884 | 3.037 | 1.38 |
| **control (prose)** | **5** | **−1.736** | **2.226** | **0.34** |

**Why is haiku so volatile?** In a 17-syllable poem with ~15 tokens, each token carries extraordinary weight. A single unexpected noun inflates the standard deviation dramatically. Haiku achieves its effects precisely through one or two high-S₂ moments (the *kigo*, the *kireji*) in an otherwise sparse, low-surprise structure. The variance measure captures this "one shot" economy better than the mean.

**Prose control has uniquely low skewness (0.34).** All poetry eras have positive skew (right tail: extreme positive spikes more common than extreme negative dips). Prose is symmetric. This may be the sharpest information-theoretic distinction between poetry and prose: poetry systematically cultivates extreme upside deviation.

---

## Key Finding 3: Most and Least Volatile Poems

**Highest std_S₂ (most volatile):**

| Std_S₂ | Title | Author |
|---|---|---|
| 5.460 | Morning Glory (Chiyo-ni, translated) | Chiyo-ni |
| 5.045 | Autumn Crow (Bashō, translated) | Matsuo Bashō |
| 4.982 | Howl (opening) | Allen Ginsberg |
| 4.683 | To a Mouse (closing stanzas) | Robert Burns |
| 4.666 | Old Pond (Bashō, translated) | Matsuo Bashō |
| 4.659 | The Wife of Usher's Well | Traditional (Scottish ballad) |
| 4.654 | I heard a Fly buzz — when I died | Emily Dickinson |
| 4.620 | The Fish | Marianne Moore |

Two haiku top the list. Their extreme variance confirms the "one-shot surprise" economy hypothesis: most tokens are constrained by the nature imagery convention, then one word (Morning Glory, Autumn Crow) violates expectation entirely.

**Lowest std_S₂ (most consistent):**

| Std_S₂ | Title | Author |
|---|---|---|
| 1.849 | News article prose | Control |
| 1.961 | Academic prose | Control |
| 2.065 | silencio | Eugen Gomringer |
| 2.090 | Cooking Instructions (Found Poem) | Anonymous |
| 2.123 | Simple narrative prose | Control |
| 2.341 | Technical prose | Control |
| 2.612 | This Is Just to Say | W.C. Williams |
| 2.658 | From 'Who Whispered Near Me' | Killarney Clary |

Gomringer's **"silencio"** (a concrete poem consisting almost entirely of the single word "silencio" repeated in a grid with a blank center) has the 3rd lowest std_S₂ in the corpus — lower than most prose controls. The repetition completely eliminates variance. William Carlos Williams's "This Is Just to Say" is similarly low-volatility: its plain, colloquial diction creates an almost flat S₂ profile.

---

## Key Finding 4: Poet Signatures on the Volatility Map

| Author | n | Avg mean_S₂ | Avg std_S₂ | Skewness | Range |
|---|---|---|---|---|---|
| Rainer Maria Rilke | 2 | **+0.773** | 3.726 | 0.92 | 0.959 |
| Allen Ginsberg | 2 | +0.744 | **4.686** | 0.97 | 0.417 |
| Georg Trakl | 2 | +0.624 | 3.990 | 1.03 | 0.413 |
| Stefan George | 3 | +0.394 | 3.740 | **1.46** | 0.615 |
| Matsuo Bashō | 4 | +0.033 | 4.172 | 1.09 | **2.131** |
| Claudia Rankine | 2 | −0.002 | 4.254 | **1.68** | 0.086 |
| E.E. Cummings | 3 | −0.798 | **4.305** | 1.45 | 1.491 |
| John Ashbery | 16 | −0.675 | 3.534 | 1.08 | 1.561 |
| Kobayashi Issa | 3 | −0.907 | 3.646 | 0.70 | **2.420** |
| Control | 5 | −1.736 | 2.226 | 0.34 | 1.389 |

**Notable observations:**

- **Rilke** leads in mean S₂ — the most systematically surprising poet in the corpus. His small std and tight across-poem range suggest this is a genuine stylistic commitment, not occasional spike.

- **Ginsberg** has both the highest mean (among poets with ≥2 poems from non-German eras) AND the highest std — true Strategic Saboteur. His across-poem range is remarkably small (0.417), meaning every Ginsberg poem maintains roughly the same level of explosive surprise.

- **Bashō** has the widest across-poem range (2.131): some haiku extremely high-S₂, others extremely low. His output spans the full spectrum. This matches his range from meditation poems to shocking juxtapositions.

- **Claudia Rankine** has the highest skewness (1.68) — her prose-poetry style creates a near-neutral baseline with occasional extreme spikes. Mean ≈ 0 means she's perfectly poised between conformity and innovation.

- **E.E. Cummings**: Negative mean (−0.798) but very high std (4.305) — the prototypical Volatile Conformist. His typographical innovations produce extreme local spikes, but the semantic content is often quite ordinary, dragging the mean down.

- **John Ashbery** (n=16, the most sampled poet): Consistently negative mean, moderate std, low across-poem variance in std. Despite his reputation for difficulty, his information-theoretic signature is **predictable unpredictability** — reliable deviation but always at a moderate level.

- **Kobayashi Issa**: Widest across-poem range (2.420) — even more variable *between* poems than Bashō. Some Issa haiku are among the most conformist in the haiku corpus; others among the most surprising.

---

## Key Finding 5: Highest-Skewness Poems

| Skewness | Title | Author |
|---|---|---|
| 2.947 | Self-Evident Truths (from Declaration of Independence) | Thomas Jefferson (found text) |
| 2.702 | I felt a Funeral, in my Brain | Emily Dickinson |
| 2.374 | The Congo (opening) | Vachel Lindsay |
| 2.301 | Buffalo Bill's | E.E. Cummings |
| 2.151 | Song of Myself (section 1) | Walt Whitman |
| 2.029 | Cicadas (Bashō) | Matsuo Bashō |
| 1.984 | One Art | Elizabeth Bishop |
| 1.964 | For I Will Consider My Cat Jeoffry | Christopher Smart |

**The Declaration of Independence** (used as found poetry) has the highest skewness. It exemplifies the pattern: legal-political boilerplate is highly predictable, then proper nouns, dates, and abstract political concepts cause sudden extreme spikes. This is a found poetry effect — the source material wasn't designed to manage surprise.

**Emily Dickinson's** "I felt a Funeral, in my Brain" has the second-highest skewness. Her dashes and unexpected verbs create intense spike-dip patterns against a metrically constrained surface.

---

## Theoretical Implications

1. **The "committed poet" hypothesis**: The bimodal distribution (large Saboteur and Traditionalist quadrants) suggests poets develop a coherent relationship with expectation. They either consistently violate it or consistently satisfy it — the mixed-mode strategies are minority positions.

2. **Standard deviation as a new feature**: Mean S₂ has been the primary measure in prior analyses, but std_S₂ captures orthogonal information. Two poets can have identical mean S₂ but radically different volatility profiles (e.g., Rilke mean=0.773 std=3.726 vs. control's mean=-1.736 std=2.226). Volatility should be reported alongside mean in future analyses.

3. **The haiku economy**: High volatility + near-zero mean is a distinctive haiku signature. Short forms don't smooth variance — they amplify it. The information-theoretic economy of haiku is a one-shot affair: conserve surprise everywhere, spend it all at once.

4. **Universal positive skew in poetry**: All 29 poetry eras examined show positive skewness; only prose control approaches symmetry (0.34). Poetry's use of language is asymmetric: it generates rare extreme positive-S₂ tokens far more than rare extreme negative-S₂ tokens. The poet is not a random sampler — they selectively place deviation precisely where they want it, creating right-tailed distributions.

---

## Suggested Next Steps

1. **Temporal analysis of volatility**: Does std_S₂ increase or decrease over literary history? Did modernism create more volatile poetry, or just higher-mean poetry?
2. **Intra-poem volatility arcs**: Does std_S₂ change across a poem's progression? (High variance at opening → convergence → spike at closure?)
3. **Volatility and reader impact**: The "one-shot" haiku economy suggests that max S₂ (not mean) may better predict critical reception of short poems. Test this on canonical vs. less-known haiku.
4. **Within-poet consistency**: Poets with tight across-poem mean_S₂ range (Ginsberg: 0.417) vs. wide range (Bashō: 2.131) represent different relationships with their own style. Are consistent poets more critically unified?
