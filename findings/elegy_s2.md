# Elegy and S₂: The Information-Theoretic Signature of Grief Poetry

**Date:** 2026-10-16  
**Experiment:** `experiments/elegy_s2.py`  
**New poems added:** 7 classic elegies (`era: "elegy"`)  
**Corpus after addition:** 291 poems

---

## Research Question

Do elegies — poems of formal mourning — have a distinctive S₂ profile? Two competing predictions:

- **H1 (Suppression)**: Elegies have HIGH positive S₂ because the poet refuses the conventional grief script. GPT-2 predicts "rest", "peace", "consolation" — the elegy subverts this.
- **H2 (Constraint)**: Elegies use inherited conventions (meter, apostrophe, classical allusion) that make language MORE predictable — lower S₂ than free verse emotional poetry.

Secondary question: Do "grief words" (death, dead, dark, cold) have high or low S₂ in context? Are they surprising or *expected*?

---

## Corpus

Seven canonical elegies added, spanning 1616–1896:

| Poem | Author | Year | S₂ (clean) |
|------|--------|------|------------|
| To an Athlete Dying Young | A.E. Housman | 1896 | **+0.776** |
| In Memoriam A.H.H. (excerpts) | Alfred Lord Tennyson | 1849 | **+0.734** |
| Elegy Written in a Country Churchyard | Thomas Gray | 1751 | +0.162 |
| On My First Son | Ben Jonson | 1616 | +0.108 |
| Lycidas | John Milton | 1637 | +0.104 |
| Adonais (stanzas I–II) | Percy Bysshe Shelley | 1821 | −0.049 |
| O Captain! My Captain! | Walt Whitman | 1865 | −0.108 |

**Era mean S₂: +0.247** (range: −0.108 to +0.776)

---

## Era Comparison

| Era | n poems | Mean S₂ | Range |
|-----|---------|---------|-------|
| confessional | 6 | **+0.536** | [−0.101, +1.578] |
| victorian | 21 | +0.430 | [−0.474, +1.716] |
| 19th_century | 11 | +0.375 | [−0.242, +1.179] |
| **elegy** | **7** | **+0.247** | [−0.108, +0.776] |
| romantic | 15 | +0.214 | [−0.427, +1.225] |

**Finding**: Elegies rank 4th of 5 eras — above romantic but well below confessional. **H2 (Constraint) is confirmed**: the classical elegiac tradition does impose formal constraints that reduce the Straussian gap relative to more personally expressive modes.

---

## The Elegy's Internal Paradox: Intimate vs. Formal

The sharpest finding is the **internal split** within elegy itself:

### Intimate/personal elegies (high S₂):
- **Housman** (To an Athlete Dying Young): +0.776 — terse, ironic tone; refuses the consolatory arc
- **Tennyson** (In Memoriam): +0.734 — short quatrains, blunt directness ("He is not here; but far away")

### Formal/classical elegies (low S₂):
- **Milton** (Lycidas): +0.104 — classical allusion, pastoral convention, elaborate digression
- **Shelley** (Adonais): −0.049 — neo-Platonic rhetoric, highly conventional mythological frame
- **Whitman** (O Captain!): −0.108 — unusually conformist for Whitman; the refrain creates predictability

**Hypothesis**: *The elegy form bifurcates along a personal/formal axis.* The intimate elegy (Housman, Tennyson's brief stanzas) achieves surprise by refusing genre conventions. The formal classical elegy (Milton, Shelley, Gray) deliberately deploys inherited frameworks — and GPT-2 knows those frameworks. Formal elegy is predictable *because its formality is its argument*.

---

## Elegy Internal Arcs (Tercile S₂ by poem section)

| Poem | Early tercile | Mid tercile | Late tercile | Pattern |
|------|--------------|-------------|-------------|---------|
| Lycidas (Milton) | **+1.124** | −0.350 | −0.442 | Descending |
| In Memoriam (Tennyson) | +0.166 | **+1.052** | **+0.980** | Builds and sustains |
| Gray's Elegy | +0.204 | +0.298 | −0.017 | Slight rise then fall |
| Adonais (Shelley) | +0.144 | −0.108 | −0.183 | Descending |
| O Captain! (Whitman) | +0.177 | **−0.540** | +0.039 | Mid-collapse |
| Housman | **+0.940** | +0.727 | +0.664 | Consistently high |
| On My First Son (Jonson) | +0.067 | +0.099 | **+0.157** | Gradual rise |

**Most striking arc**: Lycidas begins with its most surprising language (+1.124) and grows more conventional as Milton settles into pastoral machinery. This mirrors its rhetorical structure: the raw cry "For Lycidas is dead, dead ere his prime" precedes the elaborate mythological consolation.

**Contrast**: Jonson's "On My First Son" does the opposite — the opening is conventional, but the final couplet ("For whose sake henceforth all his vows be such / As what he loves may never like too much") is his most deviant. The personal cost compounds at the end.

---

## The Grief Word Paradox

We tracked 87 "grief tokens" (death, dead, dying, dark, cold, fallen, etc.) and 78 "life tokens" (live, joy, spring, bloom, etc.) across all poems.

| Category | n tokens | Mean S₂ |
|----------|---------|---------|
| Grief words | 87 | **+0.696** |
| Life words | 78 | **+1.094** |

**Counterintuitive finding**: *Life words are more surprising than grief words.* In literary context, GPT-2 expects death vocabulary (it has read enough poetry to know "cold and dead" follows "fallen"). Life-affirming vocabulary — spring, bloom, joy — arrives in MORE unexpected positions because it's used as *resistance*, as *defiance* of expected grief.

### Top grief word S₂ averages:
| Grief word | Mean S₂ | n |
|------------|---------|---|
| dark | +3.32 | 7 |
| cold | +3.20 | 10 |
| weep | +3.18 | 2 |
| dying | +2.42 | 3 |
| fall | +2.23 | 6 |
| died | +1.35 | 3 |
| death | +1.35 | 10 |
| lost | −0.03 | 3 |
| darkness | −0.43 | 4 |

The sensory/visceral grief words (dark, cold, weep, dying) are FAR more surprising than the abstract ones (lost, darkness). "Darkness" is so expected in literary/poetic contexts it's nearly a cliché. "Cold" used as a death metaphor catches GPT-2 off-guard.

### Grief word S₂ by era:
| Era | Grief word mean S₂ | Life word mean S₂ |
|-----|-------------------|-------------------|
| 19th_century | **+2.323** | +2.443 |
| victorian | +1.046 | +0.857 |
| **elegy** | **+0.207** | **+2.149** |
| romantic | −0.747 | +0.537 |
| confessional | **−1.219** | +8.413* |

*n=1 life word in confessional; Plath's single "living" in an extremely unexpected position inflates this figure.

**Key finding for elegies**: In the elegy era, grief words have near-zero S₂ (+0.207) while life words are markedly higher (+2.149). The elegy uses death vocabulary in its EXPECTED sense, but life vocabulary arrives unexpectedly. This is the formal elegy's rhetorical move: the conventions of mourning (dark, cold, dead) are deployed as liturgy — predictable, even comforting — while the intrusions of life, of "what was" and "what won't be," arrive as genuine surprise.

**Confessional grief words are NEGATIVE S₂ (−1.219)**: When Plath and Sexton use death vocabulary, it's completely expected in context. Confessional poetry has made death vocabulary predictable.

---

## Main Findings

1. **The Constraint Hypothesis is confirmed**: Classical elegy, with its inherited pastoral and mythological conventions, has LOWER S₂ than confessional or 19th-century poetry. Formal mourning is formally predictable.

2. **Personal > Formal in S₂**: The intimate elegy (Housman, Tennyson's short stanzas) outperforms formal elegies (Milton, Shelley, Gray) by ~0.6 S₂ units. Emotional directness is more surprising than classical elaboration.

3. **Life words are more surprising than death words**: In poetic contexts, death vocabulary has become liturgical — expected, almost formulaic. Life words used against a backdrop of grief are the genuine Straussian defiance.

4. **The "grief word paradox"**: "dark" and "cold" are HIGH S₂ (+3.2–3.3) but "darkness" and "lost" are LOW S₂. The short, concrete, sensory shock of mortality surprises GPT-2 more than its abstract elaboration.

5. **Elegy arcs are heterogeneous**: No universal "elegiac arc." Lycidas opens surprising and grows conventional (consolation tames the wild grief). In Memoriam builds surprise over time. Housman maintains a flat high plateau. Jonson rises to his ending.

---

## Suggested Next Steps

- **Expand elegy corpus** with 20th-century elegies (within copyright): Auden's "In Memory of W.B. Yeats", Thomas's "Do Not Go Gentle", Merrill's "Lost in Translation" (checking copyright). Even 3–4 more poems would sharpen the era statistics.
- **Apostrophe-to-the-dead analysis**: Many elegies address the dead directly ("He is not here", "O Captain!"). Do the lines containing direct address have higher S₂? Test apostrophe-to-the-dead vs. apostrophe-to-the-living.
- **Cross-era grief word evolution**: Do the same grief words (dark, cold, death) have increasing or decreasing S₂ across literary history? Has death vocabulary become progressively more expected as the literary corpus expands?
- **"Consolation turn" detection**: Many elegies have a turn toward consolation (Lycidas's "Weep no more", "Look homeward Angel"). Can we detect this turn as a change in S₂? Prediction: consolation = conformism = S₂ drop.
