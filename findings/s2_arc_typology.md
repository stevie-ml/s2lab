# S₂ Arc Typology: Classifying Poems by Their Information Curve Shape

**Date:** 2026-11-11  
**Experiment:** `experiments/s2_arc_typology.py` → `results/s2_arc_typology.json`  
**Corpus:** 362 poems filtered to ≥40 artifact-free tokens (from 411 total)  
**Builds on:** `findings/quarter_arc_mid_dip.md`, `findings/within_poem_type_arc.md`

---

## Research Question

The quarter-arc experiment established the dominant pattern: poems front-load their
surprise (Q1 highest S₂ → Q4 lowest). But 52.2% show a mid-poem trough and 21.3% have
Q1 as minimum. This experiment formalizes these observations into a **typology of S₂ arc
shapes** and asks:

1. What fraction of poems follow each arc type?
2. Do different literary traditions favor different arc shapes?
3. Can arc type serve as an author signature?
4. Which poems are the most extreme exemplars of each type?

---

## Method

For each poem with ≥40 artifact-free tokens (p_newline < 0.9), compute mean S₂ per
quarter (Q1–Q4). Classify into arc types:

| Type | Definition |
|------|-----------|
| **DECLINE** | Highest in Q1, lowest in Q3 or Q4 (front-loaded surprise) |
| **ASCENT** | Lowest in Q1, highest in Q4 (builds to climax) |
| **U_SHAPE** | Q2 or Q3 is minimum, Q1 and Q4 both higher (mid-poem trough) |
| **ARCH** | Q2 or Q3 is maximum, Q1 and Q4 both lower (mid-poem peak) |
| **FLAT** | All quarters within ~1.0 bit of each other (consistent density) |
| **ERRATIC** | No classifiable pattern |

---

## Corpus-Level Distribution

| Arc Type | Count | % |
|----------|-------|---|
| **FLAT** | 114 | **31.5%** |
| **U_SHAPE** | 84 | **23.2%** |
| **DECLINE** | 80 | **22.1%** |
| **ARCH** | 50 | **13.8%** |
| **ASCENT** | 34 | **9.4%** |
| ERRATIC | 0 | 0% |

**Most striking finding**: FLAT is the plurality at 31.5% — meaning the most common
information curve in poetry is not a dramatic arc but a steady baseline of consistent
(if negative) surprise. Poetry maintains a stable relationship to language's expectations
more often than it creates dramatic information landscapes.

The classic "front-loaded" DECLINE arc is only 22.1% of the corpus — common, but not
dominant. More poems show U_SHAPE (23.2%) than pure DECLINE, suggesting the mid-poem
trough (deviate → settle → partial recovery) is a canonical structural pattern.

---

## Era Breakdown: Which Traditions Favor Which Arc?

| Era | n | DEC% | ASC% | U% | ARCH% | FLAT% |
|-----|---|------|------|----|-------|-------|
| **german_expressionist** | 6 | **67%** | 0% | 33% | 0% | 0% |
| **harlem_renaissance** | 7 | **57%** | 0% | 0% | 14% | 29% |
| **limerick** | 5 | **60%** | 0% | 20% | 20% | 0% |
| **new_york_school** | 26 | **42%** | 0% | 31% | 19% | 8% |
| contemporary | 19 | 26% | **37%** | 11% | 16% | 11% |
| double_dactyl | 5 | 0% | **40%** | 0% | **40%** | 20% |
| confessional | 6 | 17% | **33%** | 17% | **33%** | 0% |
| **surrealist** | 8 | 25% | 0% | **50%** | 0% | 25% |
| **fixed_form** | 8 | 12% | 0% | **50%** | 25% | 12% |
| **19th_century** | 18 | 22% | 0% | **39%** | 6% | 33% |
| **18th_century** | 8 | 0% | 0% | 12% | 0% | **88%** |
| **dramatic_monologue** | 7 | 14% | 0% | 14% | 0% | **71%** |
| **biblical** | 8 | 12% | 0% | 12% | 12% | **62%** |
| **early_modern** | 10 | 10% | 0% | 20% | 10% | **60%** |
| **found_poetry** | 9 | 11% | 0% | 11% | 22% | **56%** |
| old_english | 5 | 0% | 0% | **40%** | 20% | **40%** |
| **victorian** | 30 | 20% | 10% | 7% | **23%** | **40%** |
| beat | 8 | 0% | 12% | **38%** | 12% | **38%** |

### Key Era Insights

**German Expressionism (67% DECLINE)**: The era most committed to front-loaded surprise.
Expressionist poems explode with unexpected imagery early, then settle. The "assault" is
structural, not just lexical.

**New York School (42% DECLINE)**: Also front-loaded — casual opening lines that
immediately establish idiosyncratic vocabulary create Q1 peaks.

**18th Century (88% FLAT)**: The most remarkable finding. 7 of 8 18th-century poems
(Pope, Dryden, Swift, etc.) have flat information curves — Augustan verse maintains a
steady, controlled S₂ baseline. No dramatic arcs, no surprise eruptions. The neoclassical
ideal of decorum extends to information dynamics.

**Dramatic Monologue (71% FLAT)**: Browning, Tennyson, and others in this form maintain
consistent surprise density — the persona speaks in a steady register without peaks or
troughs.

**Contemporary (37% ASCENT)**: The era most likely to build to a climax. Contemporary
poetry — perhaps influenced by prose poetry and narrative structures — most commonly
escalates toward a final surprising moment.

**Surrealist (50% U_SHAPE)**: Half of surrealist poems show the mid-poem valley pattern.
They open with surprise, become more predictable as surrealist imagery accumulates and
the model "adjusts," then recover toward the end.

**Fixed Form (50% U_SHAPE)**: Sonnets and villanelles tend toward mid-poem troughs —
the volta or refrain structure creates natural dips and recoveries.

---

## Extreme Exemplars

### Top ASCENT Poems (Anti-Culmination, Q4 >> Q1)

| Author | Title | Q1 | Q4 | Δ |
|--------|-------|----|----|---|
| Carolyn Forché | The Colonel (excerpt) | −1.44 | +1.62 | **+3.06** |
| Lawrence Ferlinghetti | In Goya's greatest scenes | −1.39 | +0.99 | +2.38 |
| Anne Sexton | The Truth the Dead Know | −0.53 | +1.59 | +2.13 |
| Marianne Moore | Poetry (opening) | −1.73 | +0.22 | +1.95 |
| Sylvia Plath | Daddy (opening) | −1.44 | +0.49 | +1.93 |
| Matthew Arnold | Dover Beach (closing stanzas) | −1.26 | +0.49 | +1.75 |
| W.B. Yeats | Sailing to Byzantium (stanza 1) | −1.23 | +0.36 | +1.59 |

**Forché leads the ASCENT** by a wide margin. "The Colonel" begins with extremely flat
reportage and builds to its horrifying final image (the severed ears). The poem's
information arc perfectly mirrors its rhetorical strategy: lull, then shock.

**Ferlinghetti's "In Goya's"** builds through catalog to its final political declaration.
**Plath's "Daddy"** (opening section) starts conventionally before its famous disruptions.

### Top DECLINE Poems (Front-Loaded, Q1 >> Q4)

| Author | Title | Q1 | Q4 | Δ |
|--------|-------|----|----|---|
| Layli Long Soldier | Whereas (excerpt) | +2.53 | −2.29 | **+4.83** |
| Wallace Stevens | The Emperor of Ice-Cream | +1.38 | −2.00 | +3.38 |
| Anne Carson | The Glass Essay (opening) | +1.95 | −1.10 | +3.05 |
| Bruce Andrews | Islets/Irritations (excerpt) | +1.70 | −1.08 | +2.78 |
| John Ashbery | Wet Casements | +2.57 | −0.14 | +2.71 |
| Frank O'Hara | The Day Lady Died | +1.36 | −1.21 | +2.57 |
| E.E. Cummings | anyone lived in a pretty how town | +1.51 | −0.98 | +2.50 |

**Long Soldier's "Whereas"** has the most extreme DECLINE (+4.83 bit drop Q1→Q4). The
poem opens with legal appropriations of the word "whereas" at high S₂, then settles.

**Stevens' "Emperor"** opens with its famous challenging phrase and quiets. **O'Hara's
"Lady Died"** delivers its high-S₂ opening (the "lunch poems" style) before the final
flat elegy.

### Most Extreme U_SHAPE (Mid-Poem Valley)

The deepest valleys belong to Wordsworth's "I Wandered Lonely as a Cloud" (valley = −2.84,
ends = +0.30) — the poem opens and closes with surprising imagery but becomes highly
predictable in its middle daffodil stanzas. This matches close reading: the poem's
middle stanzas are its most conventional.

### Most Extreme ARCH (Mid-Poem Peak)

Claudia Rankine's "Citizen" excerpt peaks strongly in mid-poem (peak = +1.91) with
unusually low endpoints. Ashbery's "The Painter" shows a similar structure (peak = +1.55).

---

## Author Signatures

| Author | n | Dominant Arc | % |
|--------|---|-------------|---|
| **John Ashbery** | 17 | DECLINE | 53% |
| **Emily Dickinson** | 7 | DECLINE | 43% |
| **Gerard Manley Hopkins** | 6 | DECLINE | 50% |
| Traditional (Scottish ballad) | 5 | DECLINE | 40% |
| **Walt Whitman** | 9 | U_SHAPE | 56% |
| **Percy Shelley** | 4 | U_SHAPE | 75% |
| **T.S. Eliot** | 5 | U_SHAPE | 40% |
| **Alexander Pope** | 4 | U_SHAPE | 50% |
| **Gertrude Stein** | 4 | ARCH | 50% |
| Tennyson | 5 | ARCH | 40% |
| **William Blake** | 7 | ASCENT | 29% |
| **Lewis Carroll** | 5 | ASCENT | 40% |
| **John Keats** | 9 | FLAT | 44% |
| **Robert Browning** | 7 | FLAT | 57% |
| **Thomas Hardy** | 6 | FLAT | 50% |

**Ashbery, Dickinson, Hopkins**: DECLINE poets — front-load their surprise, settle.
**Whitman, Shelley, Eliot**: U_SHAPE poets — dip in the middle (catalog/meditation = low S₂
middle), bracket by surprise.  
**Stein, Tennyson**: ARCH poets — build to mid-poem climax then resolve.
**Keats, Browning, Hardy**: FLAT poets — steady information landscapes, characteristic
of Romantic lyric ode, dramatic monologue, and Victorian novel-poem.

---

## Theoretical Significance

The arc typology reveals that the information dynamics of a poem are not random but
**form a coherent rhetorical structure**. The connection between arc type and literary
tradition suggests that:

1. **Information arc is a formal choice** — as deliberate as meter or stanza structure.
2. **The 18th century invented flat information poetry** — Augustan verse achieves its
   "correctness" through statistical as well as syntactic regularity.
3. **The contemporary ascent** corresponds to the influence of prose narrative on poetry
   — building toward the resonant final image mirrors the short story's arc.
4. **Surrealism and free verse gravitate toward U_SHAPE** — the model's initial surprise
   yields to pattern-recognition as surrealist conventions become "readable."

---

## Suggested Next Steps

1. **Multi-modal arc analysis**: Correlate arc type with actual turn counts (line breaks),
   looking for poems where the information dip/peak aligns with formal structural moments.
2. **Arc type × semantic fields**: Does the ARCH arc's mid-poem peak correspond to the
   arrival of a central metaphor? Does the U_SHAPE valley correspond to pure description?
3. **Longitudinal author arcs**: Does an author's dominant arc type shift across their
   career? Ashbery's early DECLINE vs. late FLAT?
4. **The "perfect arc"**: Which poems have the most dramatic arc shape (highest range
   between Q1 and Q4 minimum)? Build a canonical anthology.
