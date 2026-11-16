# The Entrainment Effect: GPT-2 'Learns' Poem Style, But Poets Don't Always Follow

**Date:** 2026-11-16  
**Experiment:** `experiments/entrainment_arc_typology.py`  
**Corpus:** 422 texts (408 analyzed, requiring ≥20 artifact-free tokens)  
**Research question:** As a poem progresses from start to finish, does GPT-2's prediction field narrow — and when it does, does the poet also become more conformist?

---

## Motivation

GPT-2 reads a poem token by token with an expanding context window. As the poem accumulates, the model gains more information about the poet's vocabulary, style, and subject matter. Does this contextual learning make GPT-2 "entrain" to the poem's style — narrowing its prediction field (entropy drops) and becoming increasingly confident? And if so, does the poet track that narrowing by also conforming more, or do they exploit the model's confidence to maintain or increase their deviance?

---

## Finding 1: GPT-2 Systematically Entrains to Poem Style

Analyzing all tokens in quartile bins (Q1=first 25%, Q4=last 25%):

| Quartile | Mean Entropy | Mean S₂ | Mean Top-1 Prob | % Positive S₂ |
|---|---|---|---|---|
| Q1 (0–25%)   | **6.663** | **−0.218** | 0.2595 | **37.4%** |
| Q2 (25–50%)  | 6.158 | −0.427 | 0.3007 | 33.5% |
| Q3 (50–75%)  | 6.037 | −0.525 | 0.3108 | 32.1% |
| Q4 (75–100%) | 5.990 | −0.494 | **0.3155** | 32.0% |

**Key results:**
- Entropy drops 0.673 bits from Q1 to Q4 — GPT-2 becomes more confident as it reads
- Top-1 probability rises from 0.26 to 0.32 — the model's leading prediction strengthens
- % of positive-S₂ tokens drops from 37.4% to 32.0% — the first quartile is informationally richest
- Mean S₂ also drops, from −0.218 to −0.494 — but the decline flattens after Q2

**Across poems:** 78.2% of poems (n=408) show entropy drops from Q1 to Q4 (mean: 0.852 bits), confirming the entrainment effect is consistent, not a corpus-level artifact.

---

## Finding 2: Two Main Arc Patterns — Convergence vs. Defiant Crystallization

Classifying each poem by whether entropy and S₂ rise or drop from Q1 to Q4:

| Arc Type | H_drop | S2_drop | Label | % of corpus |
|---|---|---|---|---|
| **Type A** | >0.3 | >0.3 | *Entrainment Convergence* — model and poet both settle | **30.6%** |
| **Type B** | >0.3 | <−0.1 | *Defiant Crystallization* — model entrains, poet keeps defying | **27.2%** |
| **Type D** | <−0.3 | >0.3 | *Settling into Chaos* — context unpredictable, poet follows | 10.5% |
| **Type C** | <−0.3 | <−0.3 | *Escalating Tension* — both H and S₂ rise | 1.2% |
| Other | — | — | Mixed / borderline | 30.5% |

**Type B (Defiant Crystallization)** is the most striking: these poems *teach* GPT-2 their style (entropy narrows significantly) while the poet simultaneously *increases* their deviation. The model becomes confident — and the poet exploits that confidence to deliver greater surprises.

### Best examples of Type B (Defiant Crystallization):

| Poem | Era | H drop | S₂ gain (Q1→Q4) |
|---|---|---|---|
| Edward Lear: "There Was an Old Person of Ware" | limerick | 1.34 | +3.43 |
| Carolyn Forché: "The Colonel" | prose_poetry | 1.04 | +3.06 |
| Lawrence Ferlinghetti: "In Goya's greatest scenes" | beat | 2.01 | +2.38 |
| Synthetic: Protocol III (procedural test case) | procedural | 3.20 | +2.18 |
| Anne Sexton: "The Truth the Dead Know" | confessional | 1.54 | +2.13 |
| Issa: "Three Haiku" | haiku | 1.87 | +2.02 |
| Wang Wei: "Deer Park" (literal trans.) | classical_chinese | 2.52 | +1.96 |

**Interpretation:** Defiant Crystallization is especially prominent in:
- **Extreme short forms** (haiku, limerick) — the form builds tight expectations within the first line, then the ending detonates them
- **Prose poetry** (Forché, Sexton) — the prose register initially lowers GPT-2's uncertainty, making the eventual surprise more forceful
- **High-entrainment forms** (procedural, ballad) — the model learns the template quickly, amplifying the effect of departures

---

## Finding 3: Maximum S₂ Spike Is Front-Loaded, Not Climactic

The position of each poem's single maximum S₂ token:

| Quartile | % of poems with max spike there |
|---|---|
| Q1 (first 25%) | **37.3%** |
| Q2 (25–50%) | 25.2% |
| Q3 (50–75%) | 17.2% |
| Q4 (last 25%) | 20.3% |

Mean position of max spike: **0.424** (early second quartile); median: **0.382**.

**The max S₂ spike most often occurs in the first third of a poem** — not at the end. This directly contradicts a "climax" model of poetic surprise. Poems don't build to their most surprising moment; they tend to establish their most extreme deviance early, then sustain or modulate it.

This may reflect a "threshold" model: the first occurrence of an entirely unexpected word or phrase is maximally surprising; subsequent deviations, however large, are anticipated by the reader (and GPT-2) as part of the established voice.

---

## Finding 4: Formal/Repetitive Forms Entrain Most Strongly

Forms with highest mean entropy drop (Q1→Q4):

| Form | Mean H drop | n |
|---|---|---|
| villanelle | **3.974** | 3 |
| haiku | **2.882** | 3 |
| song_lyrics | 2.517 | 3 |
| control (prose) | 2.504 | 5 |
| concrete poetry | 2.246 | 3 |
| classical Chinese | 1.826 | 4 |
| fixed_form (sonnet etc.) | 1.819 | 8 |
| limerick | 1.657 | 10 |
| ballad | 1.612 | 6 |

The villanelle's refrains and repetitions teach GPT-2 precisely what to expect — the most extreme entrainment of any form. Interestingly, **control prose also shows strong entrainment** (2.504), suggesting that formal repetition and prose-register coherence both narrow the prediction field, while free verse and modernist poetry (lower in the ranking) resist it.

---

## Synthesis: The Information Dynamics of Poem Reading

Three models of how poems manage surprise over time:

1. **Convergence** (Type A, 30.6%): Both model and poet "settle in" — the poem establishes a register and both GPT-2 and the poet increasingly conform to it. Classic narrative and confessional verse.

2. **Defiant Crystallization** (Type B, 27.2%): The model "learns" the style, while the poet uses that narrowed expectation to amplify their deviance. The surprise grows *because* the context is better understood. Characteristic of limericks, prose poetry, haiku, and confessional poetry at its best.

3. **Front-loaded Spike** (independent of arc type): Regardless of overall arc, the single most extreme surprise moment typically occurs in the first third of a poem — the "first contact" effect.

The **Defiant Crystallization** pattern is theoretically important: it shows that high S₂ late in a poem is not random noise but a *consequence* of entrainment. When the model has learned to expect a voice, any departure from that voice is more informationally significant than departures from cold context.

---

## Suggested Next Steps

1. **Per-poet arc classification**: Which poets consistently use Defiant Crystallization as their strategy? Do they correlate with perceived "difficulty" or critical recognition?
2. **Arc type × reader response**: Do Type B poems receive different critical attention? Correlate arc type with canonical status.
3. **Finer-grained entrainment window**: Track per-token entropy across the poem (not just Q1/Q4) to identify the exact point of entrainment and whether it's gradual or step-like.
4. **Interaction with form**: Within limericks and villanelles, do the high-entrainment tokens correspond to specific formal positions (refrain lines, rhyme slots)?
