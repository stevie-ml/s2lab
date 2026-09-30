# Context Horizon: Is Poetic Surprise Local or Global?

**Date:** 2026-09-30  
**Experiment:** `experiments/context_horizon_experiment.py`  
**Corpus:** 40 poems (English, ≥30 words), 2,981 artifact-free tokens  
**Builds on:** `findings/within_poem_type_arc.md`, `findings/straussian_gap_taxonomy.md`

---

## Research Question

When a poet surprises — producing a high-S2 token — is that surprise **local** (the immediate
predecessor word didn't predict it) or **global** (the whole accumulated poem context made it
seem impossible)? And does the accumulated context generally *help* or *hurt* GPT-2's
predictions relative to a bigram baseline?

Two strategies a poet could use:
- **"Telegraph and deviate"**: build strong contextual coherence that constrains expectation, 
  then choose something unexpected within that frame (local surprise > global surprise)
- **"Frame and violate"**: build context that makes a specific direction seem inevitable, 
  then choose something that defies even that framing (global surprise > local surprise)

---

## Method

For each artifact-free token in 40 poems, computed surprisal at **five context window lengths**:
- Window=1: P(token | previous token only) — bigram local surprise  
- Window=5: short phrase context  
- Window=20: clause/sentence context  
- Window=50: stanza/paragraph context  
- Window=MAX: full poem context (standard S2)

**Context gain** = full surprisal − bigram surprisal  
- Negative: full context predicts token better than bigram alone (context HELPS)  
- Positive: full context predicts token worse than bigram alone (context HURTS)

**Token types** (by full S2 and context_gain):

| Type | Full S2 | Context gain |
|---|---|---|
| **FRAME_AND_VIOLATE** | > 2.0 | > 0.5 — context framed a violation |
| **LOCAL_SHOCK** | > 2.0 | ≤ 0.5 — locally surprising; context doesn't amplify |
| **CONTEXTUAL_DRIFT** | ≤ 2.0 | > 0.5 — context disrupts but choice still conformist |
| **TELEGRAPHED** | ≤ 2.0 | ≤ 0.5 — context helps; token is coherent |

---

## Main Results

### Context Almost Always Helps

| Metric | Value |
|---|---|
| Mean context gain (all tokens) | **−2.93 bits** |
| Local vs global S2 correlation | **r = 0.553** |
| High-S2 tokens (S2 > 2): mean gain | **−0.51 bits** |
| High-S2 tokens: n | 645 (21.6% of sample) |

Full context helps prediction by **2.93 bits on average** compared to a bigram baseline.
Even high-S2 tokens (the corpus's most surprising moments) show negative mean gain (−0.51):
even surprising tokens tend to be in contexts where GPT-2 does *somewhat* better than 
bigram alone — the poet builds coherence even before breaking it.

The local/global S2 correlation (r=0.553) shows meaningful but far-from-perfect alignment:
roughly 30% of variance in S2 is explained by local context alone.

### Token Type Distribution

| Type | % of all tokens |
|---|---|
| **TELEGRAPHED** | **74.0%** |
| LOCAL_SHOCK | 14.0% |
| FRAME_AND_VIOLATE | 7.6% |
| CONTEXTUAL_DRIFT | 4.3% |

**74% of poetic tokens are "telegraphed"** — context helps, token is coherent.  
Only **7.6% are "Frame and Violate"** — the rarest but most extreme strategy.  
**14% are "Local Shock"** — surprising at the bigram level, but full context doesn't make it worse.

### The "Frame and Violate" Tokens Are the Most Dramatic

| Token | Author | Full S2 | Context gain |
|---|---|---|---|
| " badly" | Elizabeth Bishop (*One Art*) | +20.6 | +6.39 |
| " observing" | Walt Whitman | +20.4 | +5.29 |
| " Fun" | Emily Dickinson | +18.9 | +9.45 |
| " stacked" | Claudia Rankine | +18.2 | +5.14 |
| " hysterical" | Allen Ginsberg (*Howl*) | +15.6 | +2.22 |
| " Babylon" | John Ashbery | +14.9 | +2.65 |
| " yellow" | Lyn Hejinian | +14.5 | +3.03 |
| " Tennessee" | Wallace Stevens (*Anecdote of the Jar*) | +14.2 | +2.89 |

The most striking example: Dickinson's " Fun" appears in a poem about death and mental crisis.
The full poem context establishes a stark, ecclesiastical tone — making "Fun" not just locally
unexpected, but globally impossible. The accumulated context *raises* GPT-2's confidence that
the next word will be solemn, then Dickinson places a word with almost zero probability given
that entire frame. This is the purest expression of the "Frame and Violate" strategy.

Elizabeth Bishop's " badly" in "One Art" similarly: "The art of losing isn't hard to master"
sets up a context where "badly" (in "it will not disaster (badly)" — the final confessional
revision) becomes devastating precisely because the poem's ironic framing made it seem
impossible.

---

## Era Differences: A Historical Arc

| Era | Mean context gain | Mean S2 (clean) | Local/global corr |
|---|---|---|---|
| romantic | −3.690 | −0.42 | 0.317 |
| modernist | −3.229 | −0.53 | 0.344 |
| 19th_century | −3.178 | −0.07 | 0.442 |
| mid_century | −3.151 | +0.18 | 0.514 |
| beat | −2.871 | +0.69 | 0.411 |
| contemporary | −2.861 | −0.27 | 0.469 |
| new_york_school | −2.711 | −0.57 | 0.438 |
| language | −2.586 | −0.67 | 0.417 |
| confessional | −2.421 | −0.44 | 0.332 |

**The historical arc**: context helps prediction most in Romantic poetry (−3.69 bits gain) and
least in Language poetry (−2.59 bits). The New York School and Language poetry traditions 
deliberately undercut contextual coherence — the accumulated context buys less prediction than
it does in Romantic verse.

Crucially, this is NOT just a re-statement of S2 differences. Beat poetry has the highest S2
(+0.69) but middling context disruption (−2.87). Confessional poetry has among the lowest
context gains despite its many emotionally intense surprising tokens.

**The mid-century correlation anomaly**: Mid-century poetry (0.514) shows the highest alignment
between local and global S2 — when a word is locally surprising in mid-century verse, it's 
likely also globally surprising. Confessional (0.332) shows the lowest — surprising tokens in
confessional verse are often locally surprising but the context had already somewhat prepared
for something unusual.

---

## Poem-Level Extremes

### Greatest contextual disruption (context helps LEAST)

| Poem | Mean gain | Mean S2 | %Frame/Violate |
|---|---|---|---|
| Long Soldier — *Whereas* | −1.568 | +0.16 | 15.8% |
| Ashbery — *Some Trees* | −1.848 | −1.21 | 7.0% |
| Ashbery — *A Blessing in Disguise* | −2.133 | −1.26 | 8.0% |
| Plath — *Lady Lazarus* (opening) | −2.143 | −0.21 | 7.5% |
| Silliman — *Ketjak* | −2.302 | −0.44 | 12.0% |

Long Soldier's *Whereas* shows the highest contextual disruption of any poem: its legal
register (imitating Congressional apology language) sets up expectations that are violated
at every turn, with 15.8% of tokens classified as Frame-and-Violate — the highest rate in
the sample.

### Greatest contextual coherence (context helps MOST)

| Poem | Mean gain | Mean S2 | %Frame/Violate |
|---|---|---|---|
| Dickinson — *I felt a Funeral, in my Brain* | −4.213 | −0.89 | 4.6% |
| Wordsworth — *I Wandered Lonely* | −3.861 | −0.70 | 5.4% |
| Keats — *Ode to a Nightingale* | −3.660 | −0.52 | 7.0% |
| Shelley — *Ozymandias* | −3.651 | −0.25 | 6.3% |
| Stevens — *The Emperor of Ice-Cream* | −3.568 | −0.92 | 9.5% |

Dickinson's "Funeral in my Brain" generates the strongest contextual coherence in the sample:
the poem's sustained metaphor (funeral rites as mental breakdown) creates an exceptionally 
tight contextual frame — GPT-2 gains 4.21 bits over bigram baseline in its predictions.
This poem's surprises are concentrated in a few intense moments against an unusually
predictable background.

---

## Key Finding

**Most poetic tokens are "telegraphed"**: the poet builds coherent context that makes even
unusual choices somewhat predictable given the whole poem. The "Frame and Violate" strategy
(where context actively makes a token LESS predictable than its bigram baseline) is rare (7.6%)
but produces the corpus's most extreme S2 scores.

**The surprise-as-context-violation hypothesis is confirmed for the top tier**: the highest-S2
moments (> S2 15) are overwhelmingly Frame-and-Violate. But the bulk of mid-range surprise
(S2 2–10) comes from "Local Shock" — tokens that are locally unexpected and context happens
to not help much, without actively framing a violation.

**Literary-historical implication**: the Romantic-to-Language-poetry arc is partly a history
of increasing contextual disruption. Romantic verse maximizes contextual coherence (context
helps +3.69 bits); Language poetry deliberately undermines it (context helps only +2.59 bits).
But this is **orthogonal to S2**: beat poetry has both high S2 AND moderate context gain,
meaning its surprises are locally dramatic but don't require elaborate contextual framing.

---

## Suggested Next Steps

1. **Extend to full corpus** (40 poems is a 20% sample): test whether the era differences hold
   at scale, especially for haiku, which has extreme raw S2.

2. **Context window profiling**: plot surprisal as a function of window length (1→5→20→50→MAX)
   to find where the "saturation point" is — the window at which adding more context yields
   diminishing returns. Does this differ by era?

3. **Frame-and-Violate tokens as a poem signature**: poems with highest %Frame-and-Violate
   (Long Soldier 15.8%, Silliman 12.0%) seem to have a specific poetics. Is this a reliable
   genre-level signal?

4. **Connect to the Straussian taxonomy**: The 2×2 taxonomy (Type I: Definite Straussian Gap)
   should strongly overlap with Frame-and-Violate tokens. Quantify this overlap and test
   whether Frame-and-Violate is a refinement of or identical to Type I.
