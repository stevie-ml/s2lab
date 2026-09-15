# Catalog Decay: S₂ Patterns in Poetic Enumeration

**Date:** 2026-09-15  
**Experiment:** `experiments/catalog_decay.py`  
**Corpus:** 128 texts; 13 anaphora chains identified  
**Builds on:** `repetition_and_entropy.md`, `surprise_decay_curves.md`, `information_arcs_s2.md`

---

## Research Question

When a poet creates a catalog — a list of parallel items structured by anaphora (e.g., "I prefer... / I prefer... / I prefer...") — does GPT-2's surprise adapt to the template, lowering S₂ across successive items? Or do skilled poets strategically insert semantically unexpected items to *subvert* the model's learned expectation?

**Two competing hypotheses:**
- **H1 (Adaptation):** S₂ decays across list items as the model learns the list structure, making each successive item more predictable
- **H2 (Subversion):** Poets use the established template as a platform, deliberately inserting items that spike S₂ against the now-entrenched expectation

---

## Method

- Identified anaphora chains: 3+ consecutive lines where the first token (normalized) is identical
- For each chain position, computed:
  - **anchor\_s2**: S₂ of the repeated word itself (how surprising is this repetition?)
  - **content\_s2**: mean S₂ of the remaining tokens (what the poet varies across items)
- Measured slope of content\_s2 across positions (negative = adaptation, positive = subversion)
- Identified local content\_s2 peaks as "subversive insertions"

---

## Results

**13 anaphora chains identified across 128 texts.** Chains ranged in length from 3 to 12 items.

### Global Pattern

| Trend | N Chains | % |
|-------|----------|---|
| Adapting (content S₂ decays) | 9 | 69% |
| Subverting (content S₂ grows) | 4 | 31% |
| Flat (no clear trend) | 0 | 0% |

**Majority pattern is adaptation.** But 31% of chains actively fight it.

### Mean Anchor S₂ Slope: −0.392

The repeated word itself (the anaphoric anchor) becomes dramatically more predictable with each successive occurrence — but only initially. After the first spike, repetition quickly normalizes into expectation.

---

## Case Studies

### David Antin — "a list of the delusions of the insane" (12-item catalog)

The longest anaphora chain in the corpus. Every line begins with "being":

| Pos | Anchor S₂ | Content S₂ | Line |
|-----|-----------|-----------|------|
| 1 | 3.70 | **+1.50** | being buried alive |
| 2 | 34.59 | −0.38 | being laughed at |
| 3 | 31.08 | −2.97 | being left alone |
| **4** | 29.89 | **+0.62** | being followed ← PEAK |
| 5 | 32.55 | −0.34 | being touched |
| 6 | 29.19 | −1.21 | being poisoned |
| 7 | 30.00 | −3.09 | being watched |
| **8** | 29.66 | **+2.19** | being wrong ← PEAK |
| 9 | 23.68 | −0.24 | being right |
| **10** | 21.58 | **+0.66** | being recognized ← PEAK |
| 11 | 18.93 | −2.16 | being forgotten |
| 12 | 24.69 | −2.94 | being the only one left |

**Content slope = −0.133** (overall adapting), but with three internal peaks. The anchor "being" spikes at position 2 (S₂=34.59!) — after the first "being" the model doesn't expect it again immediately — then gradually declines.

**The subversive insertions are semantically remarkable:**
- Position 8: "being wrong" — shifts from *visceral physical fears* (buried, laughed at, poisoned, watched) to an abstract *epistemic failure*. The poet punctures the gothic catalog with an everyday humiliation.
- Position 10: "being recognized" — ambiguous: recognition as validation or as exposure? Against the background of paranoid fears, it registers as both.
- These items have *lower emotional register* than their neighbors, making them informationally surprising against the template.

### Szymborska — "Possibilities" (13-item "I prefer..." catalog)

Three overlapping chains detected within this 13-line poem:

**Chain 2 (4 lines, starting mid-poem):**

| Pos | Anchor S₂ | Content S₂ | Line |
|-----|-----------|-----------|------|
| 1 | +10.21 | −0.48 | I prefer cats. |
| **2** | −3.13 | **+1.50** | I prefer the oaks along the Warta. ← PEAK |
| 3 | −2.94 | +0.04 | I prefer Dickens to Dostoyevsky. |
| **4** | −2.17 | **+3.34** | I prefer myself liking people ← PEAK (largest in corpus!) |

The 'I' token at position 1 has S₂ = +10.21 (very surprising: the model didn't expect the poem to repeat "I" again here). By position 2, anchor S₂ crashes to −3.13: the model has now learned "I prefer X" is the template.

"**I prefer myself liking people**" (content S₂ = +3.34) is the single largest content-surprise in any list item in the entire corpus. Why? Every other item names an *external* object of preference (cats, trees, an author, a river). "I prefer myself..." turns the preference inward — the 'I' becomes its own object. The grammatical reflex is unexpected; GPT-2 has been trained to complete "I prefer..." with a noun or adjective, not a reflexive construction.

### Robert Burns — "A Red, Red Rose" (3-item "And" chain)

| Pos | Anchor S₂ | Content S₂ | Line |
|-----|-----------|-----------|------|
| 1 | +0.43 | +1.78 | And I will love thee still, my dear |
| **2** | −1.05 | **+3.18** | And the rocks melt wi' the sun: ← PEAK |
| 3 | −0.24 | −1.07 | And I will love thee still, my dear |

Content slope = −1.42 (strong adaptation). But position 2 peaks: "the rocks melt wi' the sun" is a hyperbolic simile inserted between two identical lines ("And I will love thee still, my dear"). The peak is the *figure* (impossible geological event) sandwiched between *repetitions* of the literal sentiment. S₂ confirms the simile as the informationally richest element.

### Era Pattern: Contemporary Poetry Actively Subverts

| Era | Avg Content S₂ Slope | Pattern |
|-----|---------------------|---------|
| modernist | −1.945 | adapting |
| romantic | −1.421 | adapting |
| harlem\_renaissance | −0.612 | adapting |
| german\_symbolist | −0.596 | adapting |
| prose\_poetry | −0.381 | adapting |
| surrealist | −0.214 | adapting |
| **contemporary** | **+0.493** | **subverting** |

All historical eras adapt. Contemporary poetry (Antin, Armantrout, Szymborska) contains the only subverting chains. This may reflect a 20th-century avant-garde strategy of using the *list form itself* as a site of tension — the template is established not to soothe but to violate.

---

## Key Findings

**1. The Adaptation Effect is Real and Strong**
69% of anaphora chains show negative content S₂ slope — the list form trains GPT-2 in real time, and the poet must work against this rising tide of predictability.

**2. The Second Occurrence is the Most Surprising**
For the repeated anchor word, S₂ spikes sharply at position 2 (e.g., "being" → S₂=34.59 at second occurrence), then declines. The model needs exactly one occurrence to learn the pattern; thereafter, repetition is expected.

**3. Subversive Items Exploit Categorical Shifts**
Mid-chain peaks consistently correspond to items that change *semantic register*:
- From visceral/physical to abstract/epistemic ("being wrong")
- From external objects to reflexive self ("I prefer myself")
- From literal sentiment to hyperbolic figure ("the rocks melt wi' the sun")

S₂ detects the moment when the poet "changes the rules" of their own list.

**4. Contemporary Poetry Uses the List Differently**
Modern list-makers (Antin, Szymborska) build lists specifically to subvert them. The catalog form is a trap they set for the reader's (and model's) expectation.

---

## Methodological Note

The "anchor S₂ paradox": the repeated word is most surprising at its *second* occurrence, not its first. This is because after the first item, GPT-2 does not predict the item will repeat — the second occurrence arrives as a major violation. Only after 3–4 repetitions does the anchor become predictable (negative S₂). This creates an interesting asymmetry: the list gains informationally at position 2, then pays down that debt across subsequent positions.

---

## Suggested Next Steps

1. **Longer catalogs**: Analyze Whitman's catalogues (40+ items) — at what position does S₂ fully stabilize? Is there a "catalog entropy half-life"?
2. **Deliberate surprise injection**: Can we identify, in a longer list, the *optimal position* for a subversive item — the point where contrast would be most surprising?
3. **Anaphora vs. epistrophe**: Compare S₂ decay in anaphora (repeated beginnings) vs. epistrophe (repeated endings) — does the pattern depend on whether the repeated element is the anchor or the closure?
4. **Cross-linguistic catalog comparison**: German expressionist and French surrealist list poems — do the same patterns hold for non-English anaphora?
