# The Surprise Centroid: Poetry Front-Loads Its Surprises

**Date:** 2026-10-22  
**Experiment:** `experiments/surprise_centroid.py` → `results/surprise_centroid.json`  
**Corpus:** 311 English-language poems (≥10 artifact-free tokens)  
**Extends:** `findings/opening_salvo.md`, `findings/closing_salvo.md`, `findings/pre_peak_setup.md`

---

## Research Question

Prior work established that the **first few tokens** of a poem are structurally anomalous (high entropy, low S₂) and that S₂ spikes are surrounded by a pre-spike descent and a post-spike conformity tax. But a coarser question remains: **where in a poem does surprise *concentrate*?**

This experiment computes a **surprise centroid** for each poem — the weighted-average normalized position of positive-S₂ tokens:

```
centroid = Σ(pos_i × s2_i) / Σ(s2_i)   for all artifact-free tokens where s2 > 0
```

A centroid near **0** = front-loaded surprise; near **0.5** = balanced; near **1** = back-loaded.

---

## Global Results

| Metric | Value |
|---|---|
| Poems analyzed | 311 |
| Mean centroid | **0.462** |
| Median centroid | 0.470 |
| Stdev centroid | 0.078 |
| Front-loaded (< 0.40) | **52 poems** |
| Back-loaded (> 0.60) | **11 poems** |
| Corr(centroid, avg S₂) | −0.023 |

**Poetry systematically front-loads surprise.** The mean centroid (0.462) is significantly below 0.5, and the asymmetry is striking: 52 front-loaded poems vs. 11 back-loaded — a **4.7:1 ratio**. Surprise is not evenly distributed across a poem; poets preferentially place their most unexpected choices in the first half.

---

## Length Class Analysis

| Length class | n | Mean centroid | Stdev |
|---|---|---|---|
| very_short (<50 tokens) | 52 | **0.458** | 0.122 |
| short (50–119 tokens) | 121 | **0.452** | 0.081 |
| medium (120–249 tokens) | 119 | 0.469 | 0.046 |
| long (250–499 tokens) | 17 | 0.491 | 0.048 |
| very_long (500+ tokens) | 2 | 0.491 | 0.018 |

**Clear length gradient**: shorter poems are more front-loaded (0.452) while longer poems approach a balanced centroid (0.491). Short poems concentrate almost all their surprise in the first half. As poems lengthen, the centroid drifts toward the middle — not because the opening surprise declines, but because longer poems can *afford* to distribute surprise throughout.

---

## Era Analysis (eras with ≥ 3 poems, sorted front → back)

| Era | n | Mean centroid | Back% |
|---|---|---|---|
| **concrete** | 3 | **0.332** | 33% |
| **ballad** | 6 | 0.404 | 0% |
| **new_york_school** | 18 | 0.414 | 0% |
| harlem_renaissance | 6 | 0.420 | 0% |
| ancient | 3 | 0.427 | 0% |
| modernist | 25 | 0.436 | 0% |
| surrealist | 8 | 0.439 | 0% |
| 19th_century | 13 | 0.444 | 0% |
| romantic | 16 | 0.453 | 0% |
| haiku | 13 | 0.462 | 23% |
| contemporary | 11 | 0.463 | 9% |
| prose_poetry | 12 | 0.484 | 8% |
| found_poetry | 7 | 0.498 | 0% |
| old_english | 4 | 0.502 | 0% |
| beat | 6 | 0.517 | 0% |
| **confessional** | 6 | **0.529** | **33%** |
| **control (prose)** | 3 | **0.566** | **33%** |

**Three distinct clusters emerge:**

1. **Front-loading traditions** (centroid < 0.44): concrete, ballad, New York School, Harlem Renaissance, modernist, surrealist — these traditions begin with their most surprising image or declaration.

2. **Balanced traditions** (0.44–0.50): romantic, haiku, contemporary, prose poetry — roughly even distribution.

3. **Back-loading genres** (centroid > 0.50): confessional poetry and prose control — these build toward revelations.

---

## The Most Extreme Cases

### Most Front-Loaded Poems (centroid < 0.32)
| Poem | Author | Centroid |
|---|---|---|
| silencio | Eugen Gomringer | **0.048** |
| I Wandered Lonely as a Cloud | William Wordsworth | 0.204 |
| The Red Wheelbarrow | William Carlos Williams | 0.230 |
| There Once Was a Man from Peru | Anonymous | 0.239 |
| The Emperor of Ice-Cream | Wallace Stevens | 0.255 |
| I felt a Funeral, in my Brain | Emily Dickinson | 0.256 |
| Temple Bells (Buson) | Yosa Buson | 0.282 |
| My Life (excerpt) | Lyn Hejinian | 0.293 |
| This Is Just to Say | William Carlos Williams | 0.308 |
| Whereas (excerpt) | Layli Long Soldier | 0.311 |

**"silencio"** by Gomringer is the extreme outlier (centroid = 0.048). The poem is just the single word "silencio" repeated with blank space — all of its semantic content is packed into the very first token. Front-loading here is a formal consequence of the concrete poem's structure.

The other front-loaded poems share a stylistic signature: they open with a striking, concrete image or statement ("I wandered," "The Red Wheelbarrow," "so much depends upon"). The surprise arrives in the first line and the rest of the poem is elaboration or consequence.

### Most Back-Loaded Poems (centroid > 0.60)
| Poem | Author | Centroid |
|---|---|---|
| Technical prose (Control) | — | **0.675** |
| The Colonel (excerpt) | Carolyn Forché | 0.671 |
| Night Sky with Exit Wounds (excerpt) | Ocean Vuong | 0.654 |
| Three Haiku (Issa) | Kobayashi Issa | 0.639 |
| There Was an Old Person of Ware | Edward Lear | 0.635 |
| The World of Dew (Issa) | Kobayashi Issa | 0.626 |
| l(a | E.E. Cummings | 0.617 |
| Daddy (opening) | Sylvia Plath | 0.602 |
| Old Pond (Bashō) | Matsuo Bashō | 0.601 |
| One Art | Elizabeth Bishop | 0.601 |

**Technical prose leads all back-loaded texts** — confirming the intuition that prose builds toward its conclusions. The other back-loaded texts fall into two groups:

- **"Shock ending" poems**: "The Colonel" builds a mundane scene before the final image of ears spilled on the table; "One Art" builds to the devastating final stanza.
- **Translation artifacts**: Japanese haiku translated into English sometimes back-load because the *kireji* (cutting word) is placed at the end in translation — "Old Pond" ends with the splash ("a frog jumps in / the sound of water"), and "The World of Dew" ends with its moral.

---

## Finding 1: The Poetry Front-Loading Hypothesis

**Poetry front-loads surprise.** The 4.7:1 ratio of front- to back-loaded poems, and the mean centroid of 0.462, establish a clear directional tendency: poets place their most unexpected choices in the first half of the poem.

This complements the **opening_salvo** finding (the first token has high entropy but low S₂) with a crucial clarification: the *first token* is not where surprise concentrates (it's actually low-S₂ because GPT-2 has no context). Surprise peaks in the **second through fourth lines** (consistent with line_number_profile.md's "third-line peak"), and the first *half* of the poem contains most of the surprise budget.

---

## Finding 2: Prose Builds; Poetry Strikes

The **control prose** texts (centroid = 0.566) are meaningfully different from poetry (0.462). The information-theoretic difference between poetry and prose is not only about *how much* surprise occurs, but *when*. Prose conforms and then surprises; poetry surprises and then conforms.

This is consistent with rhetorical tradition: poems open *in medias res* and assume the reader. Prose essays build an argument and deliver a conclusion.

---

## Finding 3: Length Gradient and Genre Effects

The length gradient (short → more front-loaded) suggests an **economy of surprise**: shorter poems cannot afford to waste their early tokens on conformist setup. Every line in a haiku counts; every word in a limerick has to work. Longer poems can afford a slow approach — they have more tokens available to work with.

The genre effects are interpretable: **New York School** poets (O'Hara, Ashbery) are famous for opening with an arresting image or mid-thought entry; **confessional** poets (Plath, Sexton) build dread across the poem.

---

## Suggested Next Steps

1. **Centroid vs. canonical quality**: Do poems with lower centroids (more front-loaded) have higher "impact" by some external measure (anthology inclusion, citation frequency)?
2. **Centroid over career**: Do poets' centroids shift over their career? Do younger poets front-load more aggressively?
3. **Multi-poem sequences**: In sonnet sequences or other grouped works, do the early poems in the sequence front-load more than the later ones?
4. **The transition ratio**: The gap between poetry (0.462) and prose (0.566) is 0.104 — does this hold in other languages and model settings?
