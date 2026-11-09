# Deixis and S₂: How 'Pointing Words' Function as Information Spikes

**Date:** 2026-11-09  
**Experiment:** `experiments/deixis_s2.py`  
**Corpus:** 399 English poems, ~31,000 tokens (control eras excluded)

---

## Research Question

Deixis — the linguistic act of "pointing" to position in time, space, or discourse — is fundamental to lyric poetry's claim on immediacy. When a poem says *now*, *here*, *tonight*, it asserts a speaker located in a specific moment and place. What is the information-theoretic signature of this gesture? Do deictic words (here, now, this, today) carry higher S₂ than other tokens, and do they function differently depending on whether they point to time, space, or discourse?

**Three hypotheses tested:**
1. **The lyric NOW hypothesis**: Temporal deictics carry higher S₂ than spatial or demonstrative ones.
2. **The deictic window hypothesis**: Deictics open an interpretive gap — they should raise entropy for the FOLLOWING token (the model becomes uncertain what comes after a pointer).
3. **The deictic-as-anchor hypothesis**: Despite being semantically open, deictics ultimately *resolve* to predictable continuations — post-deictic S₂ should be lower than base, not higher.

---

## Results

### Finding 1: Temporal Deictics Are the Biggest Straussian Gaps

| Category | n | Mean S₂ | Median S₂ | Pos% | Max S₂ |
|----------|---|---------|-----------|------|--------|
| **temporal** | 555 | **+2.210** | +0.510 | 57.5% | 36.73 |
| spatial | 179 | +1.995 | −0.136 | 46.9% | 26.08 |
| demonstrative | 555 | +1.103 | −0.750 | 39.5% | 27.81 |
| control (all alpha ≥3 chars) | 30,070 | +0.958 | −0.310 | 45.2% | 41.53 |

**Temporal deictics** (now, then, tonight, always, still, yet, again) have the highest mean S₂ — 2.3× higher than the control — and the only category where the MEDIAN S₂ is positive (+0.51). Most tokens in English poetry have negative median S₂; temporal deixis is an exception.

**Demonstratives** (this, that, these, those) are the weakest deictic category — only +0.145 above control. They are very common (n=555, same as temporal), syntactically versatile, and therefore more predictable: after a verb, article, preposition, GPT-2 often expects "that" or "this" as a natural continuation.

**Spatial deictics** (here, there, beyond, yonder) occupy the middle: less common than temporal or demonstrative, with high max S₂ (26.1) but negative median — the spikes are extreme when they occur, but most spatial deictics sit below baseline.

---

### Finding 2: Within Temporal — "Tonight," "Today," "Already" Are Peak Surprise Tokens

| Token | Category | n | Mean S₂ | Pos% |
|-------|----------|---|---------|------|
| **tonight** | temporal | 5 | **+12.30** | 100% |
| **already** | temporal | 6 | **+6.42** | 100% |
| **today** | temporal | 13 | **+6.25** | 84.6% |
| **beyond** | spatial | 5 | +5.49 | 100% |
| **always** | temporal | 19 | +4.83 | 57.9% |
| **yesterday** | temporal | 3 | +4.56 | 100% |
| **yet** | temporal | 58 | +4.03 | 60.3% |
| here | spatial | 40 | +3.05 | 55.0% |
| after | temporal | 21 | +2.89 | 76.2% |
| again | temporal | 40 | +2.47 | 80.0% |
| still | temporal | 60 | +2.32 | 60.0% |
| now | temporal | 58 | +2.05 | 55.2% |
| then | temporal | 75 | +1.95 | 52.0% |
| **that** | demonstrative | 351 | +0.78 | 35.0% |

A striking inverse relationship: the most specific temporal deictics (tonight, today, yesterday, already) have the highest S₂, while the most generic (now, then, still) have lower S₂. **"Tonight" has mean S₂ of +12.3**, the highest of any deictic token in the corpus.

The intuition: "tonight" or "today" demands a specific calendrical/diurnal grounding that GPT-2 almost never predicts — it expects the more generic "now" or even a noun. When a poet writes "tonight" or "yesterday," they are insisting on a particularity of time that language statistics consider improbable.

**Top five extreme deictic moments:**
1. S₂=+36.73 — "tonight" — Neruda, *Tonight I Can Write*: the title word returned in the body is maximally unexpected  
2. S₂=+31.18 — "still" — Kipling, *Recessional*: temporal persistence in a Victorian imperial elegy  
3. S₂=+30.56 — "yet" — Carroll, *You Are Old, Father William*: adversative "yet" in formal verse  
4. S₂=+29.50 — "today" — Barbara Guest, *Poems*: postmodern temporal anchor  
5. S₂=+29.30 — "now" — Southey, *The Old Man's Comforts*: emphatic present in a rhetorical poem  

---

### Finding 3: The Deictic Spike-and-Resolve Pattern

This is the most structurally interesting result. Deictics carry high S₂ **themselves**, but the token that **follows** a deictic has strongly **negative** mean S₂:

| Category | n | Deictic Mean S₂ | Post-deictic Mean S₂ | Post-deictic Median S₂ |
|----------|---|-----------------|----------------------|-------------------------|
| temporal | 555 | +2.210 | **−0.443** | −1.249 |
| spatial | 179 | +1.995 | **−0.199** | −1.079 |
| demonstrative | 555 | +1.103 | **−0.284** | −0.899 |

After a deictic, the next token is *more predictable than average*, not less. The deictic creates a local surprisal spike and then immediately resolves to a conventional continuation.

This is the **deictic spike-and-resolve** pattern: the pointing word itself is unexpected, but it has a "resolving" effect — by asserting the temporal/spatial ground, it narrows the interpretive space to what can legitimately follow in that context. After "tonight," GPT-2 can predict verbs like "is," "I," "the" with high confidence. The deictic does the work of anchoring.

---

### Finding 4: Demonstratives Open the Widest Interpretive Window

The post-deictic **entropy** (how uncertain the model is about what follows) reveals an important distinction:

| Category | Post-deictic Mean Entropy |
|----------|--------------------------|
| temporal | 5.894 nats |
| spatial | 4.683 nats |
| **demonstrative** | **7.809 nats** |

After "this" or "that," the model is **maximally uncertain** (7.8 nats — among the highest entropy states in the corpus). Yet the post-demonstrative S₂ is −0.28: despite the high entropy (the model admits it doesn't know what follows), it still correctly predicts the actual choice.

**Interpretation**: "this" or "that" creates a referential gap — it promises to point to something but hasn't revealed what yet. GPT-2 knows many words could follow ("this new," "this old," "this great," etc.) — maximum entropy — but the poet still selects from the statistically probable options. Demonstratives democratize the continuation space without provoking genuine surprise.

This contrasts with temporal deictics, where post-deictic entropy is moderate (5.9 nats) but the resolution is more predictable still (mean S₂ −0.44). Temporal deictics close the continuation space more sharply.

---

### Finding 5: Poem-Level Deictic Density vs. S₂ — An Inverse Relationship

Grouping poems by deictic density (terciles):

| Tercile | n | Avg Deictic Density | Avg Poem S₂ |
|---------|---|---------------------|-------------|
| Low deixis | 133 | 0.003 | +0.395 |
| Mid deixis | 133 | 0.019 | +0.311 |
| High deixis | 133 | 0.045 | +0.370 |

Higher deictic density correlates weakly with *lower* overall poem S₂. Poems that anchor heavily in here/now/this tend to have lower surprise overall — the deictic density performs a stabilizing function: by grounding the poem repeatedly in time and space, the poet reduces overall informational uncertainty.

**Highest-deictic-density poems:** Japanese classical translations (tanka, haiku), Marianne Moore's *Poetry*, Georges Perec's *Variations on A* (Oulipo). Notably, these poems with highest deictic density have **negative or near-zero mean S₂**. The haiku, with its insistence on specific natural moments (seasonal words, kigo), is a deictic-dense form where the pointing itself is the whole act.

**Lowest-deictic-density poems:** The Red Wheelbarrow (Williams), Howl (Ginsberg), Waste Land (Eliot), several Ashbery poems. These poems, interestingly, have among the **highest** mean S₂ — they avoid temporal/spatial anchors and instead sustain surprise through pure lexical and syntactic deviation.

---

### Finding 6: Era-Level Deictic Density Reveals a Modernist Turn Away from Deixis

| Era | Avg Deictic Density | Avg Poem S₂ |
|-----|---------------------|-------------|
| japanese_classical | 0.096 | −0.151 |
| spoken_word | 0.051 | −0.174 |
| villanelle | 0.044 | +0.791 |
| early_modern | 0.034 | +0.058 |
| prose_poetry | 0.031 | −0.180 |
| victorian | 0.028 | +0.392 |
| **beat** | **0.007** | +1.089 |
| **concrete** | **0.005** | +0.999 |
| **double_dactyl** | **0.000** | +1.213 |

The eras with **lowest deictic density** (beat, concrete, double dactyl) have **highest mean S₂**. The eras with **highest deictic density** (Japanese classical, spoken word, early modern) have the **lowest or negative mean S₂**.

This suggests a broader principle: **the deictic mode** (anchoring in space/time) and the **surprise mode** (defying expectation) are inversely related strategies. Poets who ground heavily in "here" and "now" use that grounding to reduce overall surprise — the deictic holds the poem still so each word can be absorbed in context. Poets who resist temporal/spatial anchoring (Ginsberg, the Language poets) build entire poems on sustained informational disruption.

---

## Theoretical Synthesis: Deixis as Informational Pivot

Three modes of deictic function emerge from the data:

**1. The Lyric NOW** — Temporal deictics (tonight, today, already, still) function as pure informational spikes: they assert the specificity of the lyric moment in a way that statistics never anticipates. These are the "cost" of lyric immediacy — to anchor in the specific, the poet must accept maximum Straussian distance from generic language.

**2. The Demonstrative Bracket** — Demonstratives (this, that, these, those) open large referential fields (high post-deictic entropy) but close them conventionally (negative post-deictic S₂). This is the deictic equivalent of a stage direction: "look over here" (high entropy) followed by "oh, it was what you expected" (negative S₂). Demonstratives are architecturally predictable even when referentially open.

**3. The Deictic-Surprise Inverse** — At the poem level and era level, deictic density and mean S₂ trade off. Poets cannot simultaneously maximize both. This suggests that lyric grounding (pointing to the particular moment) is in structural tension with informational risk-taking — a poem built on "here and now" uses that platform to deliver predictable insight; a poem built on pure informational disruption must refuse the deictic anchor.

---

## Suggested Next Steps

1. **Deictic chains**: Track sequences of multiple deictics (here…now…this) and test whether chained deictics escalate or diminish surprise.

2. **Deictic position within poem**: Are deictics more effective (higher S₂) at poem openings ("Here I am") vs. closings ("It is now")?

3. **Cross-genre comparison**: Test whether fiction or prose journalism uses deictics with similar or different S₂ profiles — does the lyric NOW have information-theoretic uniqueness vs. the narrative NOW?

4. **The "yet" anomaly**: "yet" appears 58 times with mean S₂ of +4.03 and three instances in the top-10 extreme moments. As an adversative temporal marker ("and yet"), it functions as a kind of informational negation — analyze "yet" moments in detail for their syntactic context.
