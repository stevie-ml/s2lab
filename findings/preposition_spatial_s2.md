# The Spatial Precision Premium: Preposition Choice and S₂

**Date:** 2026-11-24  
**Experiment:** `experiments/preposition_spatial_s2.py` → `results/preposition_spatial_s2.json`  
**Corpus:** 445 texts, 4,330 artifact-free preposition tokens (p_newline < 0.9)

---

## Research Question

Prepositions are the most transparent function words in the language — they establish relationships between nouns and their contexts in space, time, and logic. English has two tiers:

- **Common prepositions** (*of, to, in, for, with, on, at, by, from*): high-frequency connectors, often nearly grammatical in function (the "of" in "a cup of tea" is nearly empty of spatial meaning)
- **Spatial/directional prepositions** (*through, under, among, beside, beyond, beneath, across, above, below, etc.*): low-frequency, with strong positional semantics

**Research question**: Is there a systematic S₂ difference between these tiers? Do poets use spatial prepositions in contexts where GPT-2 expects a generic connector — particularly "of"?

---

## Finding 1: The 3.17-Bit Spatial Precision Gap

| Preposition class | n | Avg S₂ | Pos S₂% |
|---|---|---|---|
| **Common** (of/to/in/for/with/on/at/by/from) | 3,717 | **−1.280** | 15.4% |
| **Spatial** (through/under/among/beside/etc.) | 613 | **+1.890** | 56.0% |
| **Gap** | — | **+3.171 bits** | — |

The gap between common and spatial prepositions (3.17 bits) is one of the largest systematic differences measured in this corpus. More than half (56%) of spatial preposition tokens have positive S₂ — the poet's spatial choice was more surprising than context warranted.

**"of" is the most expected preposition** (avg S₂ = −2.130), reflecting its near-grammatical status as a universal connector. When a poet writes "of," they are almost always doing what language expects.

---

## Finding 2: The Of-Override Effect

**30 documented cases** where GPT-2's top prediction was "of" and the poet wrote a specific spatial preposition instead. These represent the clearest form of *spatial precision override* — the poet imposed a specific positional relationship where conventional language would have been content with vague connection.

**Of-override by spatial preposition:**

| Spatial prep used | n | Avg S₂ |
|---|---|---|
| through | 4 | +2.90 |
| into | 3 | +1.48 |
| around | 2 | +7.12 |
| beneath | 2 | +7.14 |
| below | 2 | +6.09 |
| without | 2 | +2.20 |
| above | 2 | +2.36 |
| upon | 2 | +2.07 |
| behind, among, since, until, beside, before, under, toward, near, over, between | 1 each | varies |

**All directions of spatial override represented**: downward (beneath/below/under), backward (behind), surrounding (around/among/between), separating (without/before/since/until), penetrating (through/into/across), elevating (above/upon/over).

**Top examples:**

1. `...The throb[behind]` — GPT-2 expected "of" for a possessive; poet imposed a backward spatial grammar (S₂=13.42, Whitman/concrete)
2. `...[around]` — Dickinson substitutes encircling for connection (S₂=9.94)
3. `...This arm[beneath]` — Whitman "beneath" where "of" would have served (S₂=8.52)
4. `...the lily[among]` — Song of Solomon uses collective distribution "among" for "of" (S₂=7.88)
5. `...In Flanders Fields[below]` — McCrae makes the grave literally downward (S₂=7.45)

---

## Finding 3: Prep-to-Prep Swaps — Where Precision Matters Most

Beyond "of-overrides," there are **172 cases** where the actual preposition and GPT-2's top prediction were both prepositions. The most common swap reveals a spatial *specificity hierarchy*:

| Expected | Actual | n | Avg S₂ | Interpretation |
|---|---|---|---|---|
| of | around/beneath/behind/etc. | 30 | +4.5 | Spatial precision overrides possession |
| in | among | 9 | +7.9 | Collective distribution over containment |
| in | beneath | 5 | +3.7 | Vertical downward over mere location |
| with | among | 4 | +7.9 | Distribution among a group over companionship |
| the | among | 4 | +7.9 | Spatial collective overrides definiteness |

The pattern is consistent: poets prefer **more specific, more directional, more spatially charged** prepositions over what conventional grammar supplies. "Among" and "beneath" are the greatest overachievers — they carry the most semantic freight at the positions where GPT-2 predicted something weaker.

---

## Finding 4: Era Differences — Beat and Objectivist as Spatial Precision Maximalists

| Era | n_common | avg_common S₂ | n_spatial | avg_spatial S₂ | Gap |
|---|---|---|---|---|---|
| **beat** | 59 | −0.280 | 10 | **+5.698** | **+5.978** |
| **objectivist** | 49 | −1.183 | 14 | **+4.755** | **+5.938** |
| latin_american | 29 | −0.761 | 7 | +4.263 | +5.024 |
| metaphysical | 43 | −0.843 | 7 | +3.575 | +4.418 |
| early_modern | 123 | −1.153 | 13 | +3.257 | +4.410 |
| ekphrastic | 117 | −1.645 | 20 | +2.450 | +4.095 |
| dramatic_monologue | 292 | −1.498 | 40 | +2.596 | +4.094 |
| romantic | 234 | −1.258 | 31 | +2.805 | +4.063 |
| new_york_school | 196 | −1.016 | 23 | +2.009 | +3.025 |
| oulipo | 34 | −0.952 | 8 | +1.395 | +2.347 |

**Beat and Objectivist poets show the largest gap (+5.98 and +5.94 bits)** — meaning their spatial prepositions are almost 6 bits more surprising than their common prepositions. This aligns with the aesthetic programs of both movements: Ferlinghetti and Ginsberg's street-level spatial consciousness, and George Oppen's interest in precise spatial ontology ("among" rather than "in" is the difference between distributed presence and contained location).

The smallest gaps appear in **OuLiPo** (+2.35) and **New York School** (+3.03) — poets who value wit, surface, and casual address over precise spatial grammar.

---

## Finding 5: Directional Asymmetry

A key structural fact: **there are zero cases where GPT-2's top prediction was a spatial preposition and the poet wrote "of" instead.** The of-override operates in one direction only: toward specificity, never away from it.

Poets *upgrade* their spatial grammar; they never *downgrade* from precise positioning to generic connection. This confirms that the spatial precision premium is a genuine poetic choice, not a statistical artifact — poets consistently make the more specific spatial choice when language allows the vague one.

---

## Interpretation: The Spatial Precision Doctrine

The combined evidence suggests a **spatial precision doctrine** in poetry:

1. **Generic "of" is the default** — conventional language connects things with "of" because almost any relationship can be vaguely characterized as possession or parthood
2. **Poets override with precision** — when they write "beneath" or "among" or "through," they force the reader to perceive a specific directional/positional/distributive relationship
3. **Different traditions practice this differently** — Beat and Objectivist poets maximize this practice; OuLiPo poets minimize it in favor of other forms of constraint
4. **This is unidirectional** — the upgrade from vague to precise is a one-way street

This connects to William Carlos Williams' "No ideas but in things" (Objectivist) and Ferlinghetti's street-level spatial consciousness (Beat): both aesthetic programs emphasize precise spatial grammar over abstract connection. The S₂ data confirms that this precision is *genuinely unexpected* — not just stylistic flourish but a systematic deviation from what the language machine anticipates.

---

## Suggested Next Steps

1. **Classify the spatial overrides by dimension** — which axes do poets favor? Vertical (above/below/beneath/over/under), penetrating (through/into/across), peripheral (beside/beyond/near), temporal (since/until/before/after)?
2. **Test: does spatial preposition S₂ correlate with imagist/concrete score?** The imagist program should produce more spatial precision
3. **The 'of' economy** — examine poems where "of" is entirely avoided. Does a low "of"-rate poem have higher spatial S₂?
4. **GPT-2 small vs. medium** — do more powerful models show smaller spatial preposition S₂ (better at predicting spatial precision)?

