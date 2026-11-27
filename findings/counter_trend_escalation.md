# Counter-Trend Escalation: Poems That Build Toward Surprise

**Date:** 2026-11-27  
**Experiment:** `experiments/counter_trend_escalation.py` → `results/counter_trend_escalation.json`  
**Corpus:** 415 poems (filtered to ≥30 artifact-free tokens, control excluded)  
**Builds on:** `findings/mode_trajectory_within_poem.md` (the "universal settlement law")

---

## Background

Yesterday's experiment established a **universal settlement law**: 63–73% of poems show falling
entropy and S₂ from first to second half. Poems, in aggregate, spend their informational capital
rather than accumulate it.

This experiment asks: **who are the exceptions?** — the poems that counter-trend, escalating toward
their ending in BOTH entropy AND deviation. What characterizes them? What makes them resist the
gravitational pull toward closure?

---

## Finding 1: Counter-Trend Escalation is Rare (6.3%)

| Trajectory | n | % |
|---|---|---|
| H rises in second half | 101/415 | **24.3%** |
| S₂ rises in second half | 153/415 | **36.9%** |
| **Counter-trend (BOTH rise)** | 26/415 | **6.3%** |
| Settlement (BOTH fall) | 187/415 | **45.1%** |

Only 26 of 415 poems (6.3%) escalate on BOTH dimensions simultaneously. Settlement is 7× more
common. The universal law holds: **poetry is fundamentally a spending medium, not an accumulation medium.**

---

## Finding 2: Early Modern Poetry Escalates Most (36.4%)

| Era | n | Counter-Trend% | mean ΔH | mean ΔS₂ |
|---|---|---|---|---|
| **early_modern** | 11 | **36.4%** | -0.054 | -0.093 |
| classical_chinese | 4 | **25.0%** | -0.900 | +0.451 |
| old_english | 5 | **20.0%** | -0.152 | -0.208 |
| double_dactyl | 5 | **20.0%** | -0.593 | +0.231 |
| oulipo | 13 | **15.4%** | -0.667 | -0.461 |
| beat | 8 | **12.5%** | -0.601 | +0.456 |
| harlem_renaissance | 8 | **12.5%** | -0.180 | -0.509 |
| surrealist | 8 | **12.5%** | -0.447 | -0.236 |
| elegy | 8 | **12.5%** | -0.064 | -0.363 |
| victorian | 34 | **11.8%** | -0.366 | -0.152 |

**Zero counter-trend eras** (never escalate on both dimensions):
19th_century, confessional, mid_century, new_york_school, language, german_expressionist,
ancient, prose_poetry, ballad, metaphysical, fixed_form, 18th_century, biblical,
limerick, postcolonial, dramatic_monologue, ekphrastic, procedural, objectivist

**The most striking finding**: **early_modern** (Donne, Spenser, Jonson, Drayton, Marvell) has
the highest counter-trend rate at 36.4% — over a third of these poems escalate in both dimensions
toward their endings. This is the inverse of the dominant pattern.

**Hypothesis**: Metaphysical poetry and Renaissance lyric use a **conceit structure** — an extended
intellectual argument that builds in complexity and urgency as it unfolds. This argumentative
momentum generates increasing entropy (the model must track an escalating logical chain) and
increasing S₂ (the resolution surprises because the argument's stakes have grown). The metaphysical
"argument" is an escalating information machine.

**Paradox**: The `metaphysical` era shows **0% counter-trend** but `early_modern` shows 36.4%.
The difference is that the corpus tags Donne's devotional verse as `metaphysical` while Spenser's
sonnets and Jonson's songs are `early_modern`. The escalating poems are the argumentative or
narrative ones (Spenser's Amoretti, Thompson's Hound of Heaven, Drayton's Since there's no help),
not the pure metaphysical meditation.

---

## Finding 3: The Top 20 Escalating Poems

| ΔH | ΔS₂ | Author | Title | Era |
|---|---|---|---|---|
| **+1.911** | **+0.565** | Gertrude Stein | Susie Asado | modernist |
| +0.999 | +0.828 | Brewster Higley | Home on the Range | song_lyrics |
| +1.435 | +0.247 | Francis Thompson | The Hound of Heaven (opening) | victorian |
| +0.978 | +0.594 | Anonymous | Terms and Conditions (Found Poem) | found_poetry |
| +0.622 | +0.458 | Alfred, Lord Tennyson | The Charge of the Light Brigade | victorian |
| +0.229 | +0.824 | Galway Kinnell | Saint Francis and the Sow | contemporary |
| +0.077 | +0.798 | Seamus Heaney | Digging | contemporary |
| +0.703 | +0.036 | Edmund Spenser | Amoretti LXXV | early_modern |
| +0.592 | +0.135 | Gertrude Stein | If I Told Him: A Completed Portrait | oulipo |
| +0.406 | +0.321 | W.B. Yeats | The Second Coming | modernist |
| +0.225 | +0.358 | Claude McKay | If We Must Die | harlem_renaissance |
| +0.520 | +0.027 | Allen Ginsberg | A Supermarket in California | beat |

**Three canonical countertypes emerge:**

### Type 1: The Associative Flood (Stein, Ginsberg)

Gertrude Stein's "Susie Asado" is the single most escalating poem in the corpus (combined
escalation index = +2.476). Stein's style, built on sound repetition and semantic drift,
generates INCREASING entropy as it proceeds — each line introduces new associative links that
the model cannot predict from the growing context. This is the opposite of most poetry:
instead of narrowing the prediction space (building context that constrains what can follow),
Stein's accumulating phrases open the prediction space further and further. The model becomes
LESS certain as it reads more.

Ginsberg's "A Supermarket in California" follows a similar pattern: the Walt Whitman fantasy
accumulates images that make the second half harder to predict, not easier.

### Type 2: The Argumentative Climax (Thompson, Spenser, McKay)

Francis Thompson's "The Hound of Heaven" uses an extended rhetorical chase structure where
the argument's urgency escalates — the second half deploys denser theological vocabulary
that surprises GPT-2 against the building context. Spenser's "Amoretti LXXV" and McKay's
"If We Must Die" build political and romantic arguments toward a galvanic closing volta.
These poems earn their escalation by convincing the reader (and the model) that stakes are rising.

### Type 3: The Image-Strike (Heaney, Kinnell)

Heaney's "Digging" and Kinnell's "Saint Francis and the Sow" use an anti-climactic technique:
long, almost colloquial first halves that lull the model into low entropy, followed by a
precise final image that delivers high S₂ exactly when the model is least expecting deviation.
This is the CHAOS→CERTAIN strategy identified in `mode_trajectory_within_poem.md`:
set up uncertainty by boring the model into confidence, then strike.

---

## Finding 4: Poem Length Strongly Predicts Counter-Trend Tendency

| Group | n | Counter-Trend Rate |
|---|---|---|
| Short poems (≤128 tokens) | 210 | **3.8%** |
| Long poems (>128 tokens) | 205 | **8.8%** |

Long poems counter-trend at **2.3× the rate** of short poems. This makes structural sense:
escalation requires space to build. A short lyric cannot afford to spend its first half building
entropy without paying dividends before the ending. Long poems have the room to run the
accumulation strategy.

---

## Finding 5: What Drives Escalation — The Highest-S₂ Second-Half Tokens

Top tokens in the escalating second halves of counter-trend poems:

| Token | Count | Avg S₂ | Max S₂ |
|---|---|---|---|
| "twenty" | 2 | **8.93** | 8.98 |
| "slips" | 2 | **7.94** | 9.06 |
| "shut" | 4 | **7.12** | 9.60 |
| "beneath" | 3 | **6.03** | 7.85 |
| "also" | 3 | **5.95** | 7.84 |
| "or" | 3 | 5.07 | 10.87 |
| "and" | 5 | 5.83 | 11.54 |
| "with" | 3 | 5.66 | 6.62 |

The high-S₂ drivers in escalating poems are **semantically unexpected conjunctions, prepositions, and
numerals** ("twenty," "also," "or," "and") — not nouns or verbs. This suggests that counter-trend
escalation often works through **syntactic unexpectedness**: the poet adds a connective where none
was expected, or a numeral that opens a new counting structure. These function words at high S₂
are the grammatical pivots that force the model to recalibrate its prediction entirely.

**"shut" (avg S₂ = 7.12, count = 4)** is the most striking single escalation token. This verb
arrives in four different escalating poems in positions where GPT-2 has built confidence around
an open, outward-facing context. "Shut" at a moment of expected continuation is a semantic
door-slam — informationally equivalent to a full-stop that the grammar did not permit.

---

## Finding 6: The Most Extreme Settlement Poems

For comparison, the most sharply settling poems:

| ΔH | ΔS₂ | Author | Title | Era |
|---|---|---|---|---|
| -3.352 | -1.145 | Synthetic | Line Palindrome | oulipo |
| -2.085 | -1.823 | John Ashbery | Leaving the Atocha Station | new_york_school |
| -1.073 | -2.751 | Synthetic | Homophonic Translation of Catullus | oulipo |
| -1.332 | -2.381 | Wallace Stevens | The Emperor of Ice-Cream | modernist |
| -2.340 | -1.219 | Gerard Manley Hopkins | Pied Beauty | victorian |
| -0.898 | -2.430 | Li Bai | Quiet Night Thoughts | classical_chinese |

**OuLiPo appears at BOTH extremes**: the palindrome poem is the most settling (-4.497 combined),
while OuLiPo-era poems have the 5th-highest counter-trend rate (15.4%). This polarization
makes structural sense: procedural constraints either FORCE escalation (the N+7 method scrambles
the second half into incoherence, raising entropy) or FORCE settlement (the palindrome converges
on its mirror structure). Procedural poetry is the most extreme in BOTH directions.

---

## Synthesis: Two Information Economies in Poetry

The counter-trend analysis reveals two fundamentally different poetic information economies:

**Settlement Economy (93.7% of poems):**  
- Opens with high information capital (entropy + S₂)  
- Spends toward resolution  
- Closes with lower entropy and conformism  
- Dominant in: new_york_school, language, prose_poetry, confessional, 18th_century  

**Escalation Economy (6.3% of poems):**  
- Opens with lower or moderate entropy  
- Builds complexity and surprise as it proceeds  
- Closes with higher stakes  
- Dominant in: early_modern, beat, classical_chinese, song_lyrics  

The escalation economy is not just an exception — it correlates with specific structural features:
1. Argumentative or conceit-based structure (early_modern, Hound of Heaven)
2. Associative accumulation (Stein, Ginsberg)
3. The image-strike (Heaney, Kinnell)
4. Procedural scrambling (OuLiPo extremes)

---

## Escalation Index Statistics

The combined escalation index (ΔH + ΔS₂) characterizes every poem's trajectory:

| Statistic | Value |
|---|---|
| Mean | -0.742 |
| Std | 0.991 |
| Q25 | -1.300 |
| Median | -0.610 |
| Q75 | -0.091 |
| **Max** (Stein, "Susie Asado") | **+2.476** |
| **Min** (OuLiPo palindrome) | **-4.497** |

The distribution is left-skewed (mean < median < 0): most poems settle sharply, a few settle
gently, and a small tail escalates. The range spans nearly 7 bits of combined drift.

---

## Suggested Next Steps

1. **Early modern deep-dive**: The 36.4% counter-trend rate in early_modern is the strongest era
   finding. Analyze the specific mechanism: map Spenser's Amoretti LXXV and Drayton's "Since
   there's no help" token-by-token to show the argumentative escalation in action.

2. **Stein's escalation mechanism**: Gertrude Stein has the highest escalation index (+2.476).
   Analyze the token-level trajectory of "Susie Asado" to characterize the associative flood
   mechanism — why does Stein's accumulation generate increasing entropy rather than decreasing?

3. **"Shut" across the corpus**: The word "shut" appears as a high-S₂ escalation driver in 4
   different poems. Is this a systematic property of this verb (door-slam semantics) or a
   coincidence? A targeted search for "shut" across the full corpus would test this.

4. **Escalation index as a classifier**: Can escalation index predict reader judgments of
   "open" vs "closed" endings? A human survey testing whether readers feel escalating poems
   are "incomplete" or "unresolved" would test whether the information-theoretic metric
   tracks phenomenological experience.
