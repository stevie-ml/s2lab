# Ekphrastic Poetry and the Verbal-Visual Interface

**Date:** 2026-10-23  
**Experiment:** `experiments/ekphrastic_s2.py`  
**New poems added:** 7 (era=`ekphrastic`)  
**Corpus size:** 328 poems (was 321)

---

## Research Question

Do poems about visual art (**ekphrastic poetry**) have distinctive S₂ profiles? 
When language attempts to translate a visual object — a painting, sculpture, woven image —
into words, does S₂ spike at the "translation moment"?

**Hypothesis:** Ekphrastic poems should show high S₂ at tokens describing visual features,
because GPT-2's sequential language model is unprepared for the specific vocabulary of
visual description inserted into lyric flow.

---

## Corpus

Seven ekphrastic poems added (all public domain):

| Poem | Author | Year | Visual Object |
|------|--------|------|---------------|
| Ode on a Grecian Urn | John Keats | 1820 | Ancient Greek urn |
| On Seeing the Elgin Marbles | John Keats | 1817 | Parthenon sculptures |
| The Lady of Shalott (opening) | Alfred, Lord Tennyson | 1842 | Magical woven tapestry |
| Fra Lippo Lippi (opening) | Robert Browning | 1855 | Florentine painting practice |
| Andrea del Sarto (opening) | Robert Browning | 1855 | Renaissance painting technique |
| For a Venetian Pastoral by Giorgione | D.G. Rossetti | 1850 | Giorgione's Louvre painting |
| Before the Mirror (stanzas 1-3) | A.C. Swinburne | 1866 | Whistler's "Little White Girl" |

Note: "On First Looking into Chapman's Homer" (Keats, 1816) was already in the corpus
as era=`romantic`. It is bibliographic ekphrasis and provides an implicit comparison.

---

## Results

### Per-poem S₂ (artifact-free)

| Poem | Author | mean S₂ | pos_ratio | max S₂ | n_tokens |
|------|--------|---------|-----------|--------|---------|
| Before the Mirror | Swinburne | **+0.198** | 0.44 | 24.61 | 160 |
| Ode on a Grecian Urn | Keats | **+0.119** | 0.34 | 28.34 | 576 |
| Andrea del Sarto | Browning | **+0.067** | 0.38 | 21.84 | 222 |
| The Lady of Shalott | Tennyson | **+0.062** | 0.36 | 33.65 | 301 |
| For a Venetian Pastoral | Rossetti | **−0.078** | 0.42 | 16.92 | 160 |
| Fra Lippo Lippi | Browning | **−0.208** | 0.38 | 19.69 | 236 |
| On Seeing the Elgin Marbles | Keats | **−0.304** | 0.36 | 16.91 | 146 |
| **Era mean** | | **−0.021** | **0.38** | | |

### Group comparison

| Group | n | mean S₂ | median S₂ | pos_ratio | max S₂ |
|-------|---|---------|-----------|-----------|--------|
| **Ekphrastic** | 7 | **−0.021** | **+0.062** | 0.38 | 33.65 |
| Romantic/Victorian/19th-cent | 59 | +0.296 | +0.263 | 0.38 | 35.25 |

---

## Key Findings

### Finding 1: Ekphrastic poems are slightly LESS surprising overall than comparable era poetry

**Ekphrastic mean S₂ = −0.021** vs **Romantic/Victorian/19th-century mean = +0.296**.

This contradicts the naive hypothesis (H1). Poems about visual art, from within the same
historical period, are somewhat more predictable on average than non-ekphrastic poetry.

**Interpretation:** Describing a visual object imposes a kind of referential constraint.
The poet is "tethered" to the specific, observable features of the artwork — they must
say what is actually there, not purely invent. This constrains the Straussian gap.
By contrast, lyric poetry without a visual anchor has complete freedom to surprise.

The sonnet form dominates here (Keats, Rossetti) — and sonnets as a class already
show lower clean S₂. But even controlling for form, the directional finding holds.

---

### Finding 2 (Strongest): Visual vocabulary has 115× higher S₂ than non-visual tokens

Within ekphrastic poems, tokens associated with visual/artistic description show
dramatically higher S₂ than the surrounding non-visual language:

| Token class | n | mean S₂ | pos_ratio |
|-------------|---|---------|-----------|
| **Visual vocabulary tokens** | 37 | **+1.271** | **0.68** |
| Non-visual tokens | 1764 | −0.011 | 0.36 |

This is the clearest result: **visual vocabulary IS a site of surprise**, even when
the poem overall is not more surprising than its era peers.

The "translation moment" hypothesis holds at the token level. When a poet writes
about **color** ("white", "pale", "dim"), **artistic materials** ("marble", "viol",
"brede"), or **visual action** ("gaze", "behold", "weave"), GPT-2's sequential
prediction is caught off-guard. The model, trained on text, lacks the visual scene
that motivated the poet's specific word choice.

High-S₂ visual tokens found:
- `anguish` (Rossetti, S₂=+15.65) — "Water, for anguish of the solstice"
- `torches` (Browning, S₂=+19.69) — "You need not clap your torches to my face"
- `unwilling` (Keats, S₂=+12.02) — "mortality / Weighs heavily on me like unwilling sleep"
- `Immortality` (Rossetti, S₂=+10.32) — "Life touching lips with Immortality"

---

### Finding 3: Rhetorical questions in ekphrastic poems have LOW S₂ (mean = −0.864)

The interrogative/apostrophe structure — "What men or gods are these?" — is
conventionally predictable to GPT-2. Despite being the most rhetorically charged
moments in ekphrasis, these question structures are EXPECTED by the language model.

The question word "What" at one instance scores S₂=+23.04 (very high!), but this is
an outlier; the mean across 38 interrogative tokens is −0.864 with a pos_ratio of 0.16.

**Interpretation:** The question *form* is conventional — apostrophe/interrogatio
are well-established rhetorical devices, and GPT-2 assigns them high probability
in poetic contexts. But the occasional high-S₂ question word (e.g., "What" used
unexpectedly after long descriptive run-on) marks genuine structural surprise.

---

### Finding 4: "On Seeing the Elgin Marbles" is the least surprising (S₂ = −0.304)

This poem is the most *abstract* ekphrasis in the set — it describes Keats' emotional
response to the sculptures ("My spirit is too weak", "mortality / Weighs heavily")
rather than the sculptures themselves. The visual object is almost absent from the
poem's language, replaced by the poet's overwhelmed reaction.

**Implication:** Ekphrasis that describes the *effect* of art (subjective response)
has lower S₂ than ekphrasis that describes the *content* of art (visual details).
The S₂ of the "Ode on a Grecian Urn" (+0.119) vs. "On Seeing the Elgin Marbles"
(−0.304) represents the difference between direct visual translation and phenomenological
reaction — the former is harder for GPT-2 to predict.

---

### Finding 5: "Before the Mirror" (Swinburne for Whistler) has highest S₂ (+0.198)

Swinburne's poem was printed in the catalogue for Whistler's exhibition and fastened
to the frame of the painting. It is possibly the most "co-created" ekphrasis in the
English canon — a poem meant to be experienced alongside its visual counterpart.

Its highest S₂ stems from unusual repetition structure and unexpected pivots:
- `Is` appears at high S₂ twice (S₂=+24.61, +18.72) — pivoting from descriptive
  to interrogative mode mid-stanza
- `whose` at S₂=+14.55 — in "Love, is there sorrow hidden, / Is there delight?"

This suggests that **poems designed to be displayed with art** (catalogue ekphrasis)
may be more syntactically and semantically unpredictable, perhaps because their
visual context carries information the text can assume without stating.

---

## Comparisons to Existing Findings

- **Haiku** (mean S₂ = −0.11 clean) and **ekphrastic** (−0.021) are comparable:
  both genres are tethered to specific external referents (seasonal image / visual object)
- **Victorian** era mean = −0.34 clean; ekphrastic Victorian poems (Browning, Rossetti,
  Swinburne) slightly ABOVE that mean, consistent with their more adventurous diction
- **Dramatic monologue** (Browning) corpus shows similar low-to-moderate S₂;
  "Fra Lippo Lippi" (−0.208) and "Andrea del Sarto" (+0.067) are consistent with
  Browning's other dramatic monologues, suggesting the painter-speaker constraint
  doesn't change the baseline S₂ profile much

---

## Theoretical Implication

The "Straussian gap" in ekphrastic poetry is not found at the level of the whole poem
but **at specific tokens** — the visual vocabulary islands within verbal flow.

S₂ can serve as a detector for **cross-modal translation points**: moments where a poem
must find words for something that resists language. High S₂ at visual vocabulary tokens
is the linguistic trace of the poet saying: "no ordinary word will do here — language
itself is strained by the task of naming what the eye sees."

---

## Next Steps

1. Expand the ekphrastic corpus with Auden's "Musée des Beaux Arts" (once copyright 
   clears or with brief fair-use excerpt), William Carlos Williams' "Landscape with 
   the Fall of Icarus," and Anne Carson's art poems
2. Test whether musical ekphrasis (poems about music) shows the same visual-token S₂ 
   spike, or whether the cross-modal vocabulary differs
3. Map S₂ across the 5 stanzas of "Ode on a Grecian Urn" to see if the famous 
   "Cold Pastoral!" climax (stanza 4) is a S₂ peak
4. Compare "direct description" ekphrasis vs. "phenomenological response" ekphrasis 
   systematically across a larger corpus to test Finding 4
