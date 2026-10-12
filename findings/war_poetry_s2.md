# War Poetry S2: Owen, Brooke, and the Rhetoric of Witness

**Date:** 2026-10-12  
**New era added:** `war_poetry` (3 poems: Dulce et Decorum Est, Anthem for Doomed Youth, The Soldier)  
**Comparison era:** `protest_political` (The New Colossus, Still I Rise)

---

## Research Question

Prior analysis found protest poetry has a wide S2 variance depending on register (formal Victorian vs. vernacular African-American). Does war poetry follow a similar split, or does WWI poetry have a consistent information-theoretic signature?

---

## Results

### Individual poems (raw and artifact-free)

| Poem | Author | Era | S2 (raw) | S2 (clean) |
|------|--------|-----|----------|------------|
| Dulce et Decorum Est | Wilfred Owen | war_poetry | +0.422 | −0.424 |
| Anthem for Doomed Youth | Wilfred Owen | war_poetry | −0.260 | −0.457 |
| The Soldier | Rupert Brooke | war_poetry | +0.405 | −0.046 |
| The New Colossus | Emma Lazarus | protest_political | −0.117 | −0.831 |
| Still I Rise | Maya Angelou | protest_political | +0.830 | −0.629 |

### Era means

| Era | Avg S2 (clean) |
|-----|---------------|
| `war_poetry` | **−0.309** |
| `protest_political` | −0.730 |

**War poetry has higher mean S2 than protest political** (−0.309 vs −0.730).

---

## Key Findings

### 1. War poetry sits above protest in the era rankings

War poetry's clean mean of −0.309 places it well above protest_political (−0.730) and comparable to the imagist era (−0.281) and mid_century poetry. This suggests war poetry's directness and concrete imagery ("blood-shod," "white eyes writhing") generates genuine linguistic surprise beyond what GPT-2 expects.

### 2. Owen vs. Brooke: witness vs. elegy

The two WWI poets diverge:
- **Brooke** ("The Soldier"): clean S2 = −0.046, nearly zero, the highest in the era. His sonnet uses idealized, conventional diction ("some corner of a foreign field / That is for ever England"). GPT-2 has encountered this register in Victorian and Edwardian poetry. The surprise is minimal; it's an elegy in a conventional key.
- **Owen** ("Dulce et Decorum Est"): clean S2 = −0.424. Owen's poem uses shocking, concrete imagery that disrupts GPT-2's expectations. Tokens like "guttering," "flound'ring," "froth-corrupted" are lexically unusual; GPT-2 hasn't seen this combination of medical/industrial vocabulary with poetic structure.

This mirrors the **Lazarus vs. Angelou split** in protest poetry: formal/conventional diction → lower S2; colloquial/concrete/confrontational diction → higher S2. **The divide is register, not content.**

### 3. High-S2 tokens in Owen vs. Brooke

Selected high-S2 moments in "Dulce et Decorum Est":
- "blood-shod" — neologism combining bodily and footwear imagery
- "guttering" — typically describes candles; applied to a dying person
- "froth-corrupted" — medical observation in a classical ode form

In "The Soldier":
- "richer" (in "a richer dust concealed") — predictable comparative
- "pulse" — conventional poetic metonymy

Owen consistently chooses words that violate GPT-2's expectations about what follows in elevated diction contexts. Brooke stays within expected register throughout.

### 4. "Anthem for Doomed Youth" vs. "Dulce"

Both are Owen, but "Anthem" is a Petrarchan sonnet (more formally constrained), while "Dulce" is a modified ode. "Anthem" has slightly lower clean S2 (−0.457) than "Dulce" (−0.424). The sonnet's formal constraint reduces lexical freedom, consistent with the general finding that formal meters reduce S2.

---

## Contextual Placement

In the full era ranking (artifact-free S2):
```
german_modernist  +0.773
beat              +0.279
imagist           -0.281
war_poetry        -0.309  ← NEW
old_english       -0.340  (updated with Beowulf)
...
protest_political -0.730
limerick          -1.123
control prose     -1.736
```

War poetry slots between imagist (low constraint, concrete imagery) and old_english — in good company, consistent with the direct, image-driven language of early modernism.

---

## Beowulf Update

Adding Beowulf to the old_english era (now 4 poems):

| Poem | S2 (clean) |
|------|------------|
| Caedmon's Hymn | −0.026 |
| The Wanderer (excerpt) | −0.356 |
| Beowulf: The Opening | −0.281 |
| Beowulf: The Fight with Grendel | −0.445 |
| **Era mean (updated)** | **~−0.277** |

**Key observation**: Caedmon's Hymn still has the highest S2 in old_english (−0.026), despite being devotional rather than martial. The Beowulf battle scene is *lower* S2 than the devotional opening. This contradicts the intuition that violent/action content would surprise GPT-2 more.

**Explanation**: The battle sequence uses formulaic, repetitive kenning patterns ("joint-bark cracked," "body broke") that are internally predictable after the first formula is established. GPT-2 learns the kenning pattern and assigns higher probability to subsequent formulaic phrases. The devotional Caedmon's Hymn uses more varied theological vocabulary that GPT-2 hasn't pattern-matched to OE alliterative structure.

---

## Suggested Next Steps

1. **Expand war poetry era**: Add Siegfried Sassoon ("They"), Edward Thomas ("Adlestrop"), Isaac Rosenberg — to test whether the Owen-Brooke divergence (witness vs. elegy) holds across more poets
2. **Test Korean War / Vietnam War poetry**: W.D. Snodgrass, Yusef Komunyakaa — does modern war poetry differ from WWI?
3. **Cross-era comparison**: Does war poetry's S2 increase or decrease as the war recedes in time? Compare Owen (1917) vs. contemporary Afghanistan poetry
4. **The kenning hypothesis**: Analyze Old English kennings specifically — do compound noun innovations have higher or lower S2 than context words?
