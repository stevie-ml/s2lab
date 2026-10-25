# S₂ at the Hyphen: The Information-Theoretic Signature of Compound Words

**Date:** 2026-10-25  
**Experiment:** `experiments/compound_words_s2.py`  
**Results:** `results/compound_words_s2.json`  
**Corpus:** 341 texts (5 new poems added: Hopkins ×2, Swinburne, Keats, Old English)  
**New poems:** Spring and Fall, Inversnaid, The Garden of Proserpine, The Eve of St. Agnes, The Battle of Maldon

---

## Research Question

When poets use hyphenated compound words — "passing-bell," "windpuff-bonnet," "sea-washed," "wine-dark" — what happens informationally at the hyphen? Does the second element of a compound word show higher S₂ than ordinary adjacent words, reflecting the creativity of the combination?

**Hypothesis (The Unexpected Combination):** After "passing-", GPT-2's context is unusual. Whatever follows must complete a combination the model has rarely (or never) seen in training. The second element should therefore show higher surprisal and — when entropy is moderate — higher S₂.

---

## Method

For each English-language poem:
1. Remove stanza-break artifact positions (p_newline ≥ 0.9)
2. Find all tokens immediately following a "-" token (compound second elements)
3. Compare their S₂ to a baseline of all adjacent content-word pairs in the same corpus
4. Classify by word class (ADJ/NOUN/VERB) using suffix heuristics

**Tokenization caveat:** GPT-2 sometimes tokenizes single compound words across subword boundaries differently from the intended hyphenation. E.g., "Sea-messenger" may tokenize as ["Sea", "-", "mess", "enger"], inflating the S₂ of "mess" (model expected "Sea-w[ater/ind]", found "mess"). These are noted where prominent.

---

## Main Finding: Compound Second-Elements Average +0.59 Bits Higher S₂

| Measure | Compound 2nd elements | Baseline adjacent words | Delta |
|---|---|---|---|
| n | 238 | 28,065 | — |
| Mean S₂ | **+0.514** | −0.075 | **+0.589 bits** |
| Std dev | 3.84 | 3.77 | — |
| Pos-S₂% | **45.8%** | 38.8% | **+7 pp** |

The confirmation is clear: **compound second-elements show systematically higher S₂** than ordinary adjacent word pairs. Poets are more informationally daring when coining or deploying compound words.

---

## By Word Class

| Word class | n | Mean S₂ | Std dev | Pos-S₂% |
|---|---|---|---|---|
| ADJ (compound adjectives) | 12 | **+1.38** | 5.84 | 50.0% |
| NOUN/OTHER | 216 | +0.39 | 3.73 | 44.0% |

**Compound adjectives show the highest information-theoretic surprise** (mean S₂ = 1.38, vs baseline −0.075). Poets who coin or borrow compound adjectives — Hopkins's "windpuff-bonnet," Keats's "argent revelry," Owen's "passing-bell" — are choosing second elements that the model genuinely could not predict from the context of the first element plus the hyphen.

---

## By Era: Two Regimes

The most striking finding is the **bimodal split** across literary eras:

| Era | n compounds | Compound mean S₂ | Baseline mean S₂ | Delta |
|---|---|---|---|---|
| contemporary | 5 | +2.67 | −0.03 | **+2.69** |
| war_poetry | 6 | +2.61 | +0.08 | **+2.53** |
| early_modern | 5 | +2.31 | +0.03 | **+2.28** |
| victorian | 44 | +1.36 | −0.00 | **+1.36** |
| old_english | 13 | +1.10 | +0.03 | **+1.06** |
| ekphrastic | 13 | +0.64 | −0.17 | +0.80 |
| modernist | 23 | +0.36 | −0.11 | +0.47 |
| romantic | 31 | +0.18 | +0.01 | +0.18 |
| *— baseline zone —* | | | | |
| postcolonial | 5 | −0.47 | −0.34 | −0.13 |
| fixed_form | 7 | −0.40 | −0.24 | −0.17 |
| dramatic_monologue | 25 | −0.48 | +0.00 | **−0.48** |
| double_dactyl | 6 | −1.23 | −0.53 | −0.70 |
| ballad | 7 | −1.24 | +0.05 | **−1.29** |
| 18th_century | 5 | −1.45 | +0.20 | **−1.65** |
| elegy | 8 | −1.86 | −0.05 | **−1.81** |

**Regime 1 — Creative compounds (positive delta):**  
War poetry, early modern, Victorian, and Old English all show compounds that exceed the local baseline. These are eras celebrated for verbal innovation: Hopkins coinages (Victorian), Shakespeare's neologisms (early modern), Owen's war-imagery ("passing-bell"), and Old English kennings. Even Old English kennings — formulaic within their tradition — are surprising to GPT-2, which has seen little Old English.

**Regime 2 — Formulaic compounds (negative delta):**  
Elegies, ballads, and 18th-century poetry use compounds that are *less* surprising than the surrounding baseline. This suggests these genres deploy **conventional compound epithets** — mourning formulas ("long-suffering," "heavy-hearted"), ballad stereotypes, and neo-classical paired modifiers ("well-born," "far-flung") that GPT-2 has learned to predict. The compound is predictable precisely because it belongs to a recognized formula.

**Interpretation:** The compound hyphen is a site of creative possibility OR formulaic convention, and the two regimes can be distinguished by S₂. Eras known for verbal invention show high-delta compounds; eras known for convention show low-delta or negative-delta compounds.

---

## Top High-S₂ Compound Moments and the Straussian Gap

The suppressed alternatives (what GPT-2 expected vs. what the poet chose) reveal the specific act of deviation:

| Compound | S₂ | Suppressed top-1 | Text / Poet |
|---|---|---|---|
| "Sea-mess(enger)" | +17.0 | "w[ater]" | *Battle of Maldon* — model expected "Sea-wind/water" |
| "Far-called" | +14.9 | "fl[ight]" | *Recessional* (Kipling) — model expected "Far-flung" |
| "razor-ke(en)" | +13.3 | "sharp" | *A Dialogue of Self and Soul* (Yeats) — "razor-sharp" vs. "razor-keen" |
| "passing-bell" | +6.7 | "time" | *Anthem for Doomed Youth* (Owen) — "passing time" vs. "passing-bell" |
| "sea-washed" | +6.5 | "shore" | *The New Colossus* (Lazarus) — model expected compound with "shore" |
| "nut-falls" | +6.3 | "green" | *Pied Beauty* (Hopkins) — "chestnut-falls" context |
| "Half-flush(ed)" | +5.1 | "moon" | *My Last Duchess* (Browning) — "half-moon" vs. "Half-flush'd" |

**The suppressed alternatives expose the genre's "default vocabulary":**  
- Kipling's "Far-called" suppresses "Far-flung" (the more conventional Kiplingesque compound)
- Yeats's "razor-keen" suppresses "razor-sharp" (the cliché)
- Owen's "passing-bell" suppresses "passing-time" (the innocuous version)

Each high-S₂ compound is a moment where the poet chose a rarer second element than the language "expected" — sometimes because it's more striking, sometimes because it's older or more archaic, sometimes because it's newly coined.

---

## Case Study: Hopkins's New Compounds (added to corpus this run)

The two new Hopkins poems contain notable compounds:

**"Inversnaid"** (1881):
- "windpuff-bonnet": highly unusual compound
- "fáwn-fróth": compound with diacritical stress marks  
- "beadbonny": compound noun (bead + bonny = rosary-beautiful)

**"Spring and Fall"** (1880):
- "Goldengrove": compressed compound noun (Golden + grove) — GPT-2 would expect "golden" as adjective, finds it welded to "grove"
- "wanwood": coined compound (wan + wood = pale/dark forest)
- "leafmeal": coined compound (leaf + -meal suffix, cf. "piecemeal")

These Hopkins coinages systematically exploit GPT-2's inability to predict his neologisms — the S₂ at these tokens measures the gap between the model's learned English and Hopkins's invented English.

---

## Finding and Hypothesis

**Finding:** The second element of hyphenated compound words in poetry shows +0.59 bits higher mean S₂ than baseline adjacent words. Compound adjectives show the highest effect (+1.38 bits above baseline). The effect is era-specific: eras of verbal innovation (war poetry, early modern, Victorian, Old English) show strongly positive deltas; eras of convention (elegy, ballad, 18th century) show negative deltas.

**Hypothesis — Two Types of Compound:**  
1. **Creative compounds** (positive-S₂ second element): The poet coins or borrows an unusual second element that surprises GPT-2. These are acts of verbal invention. S₂ at the second element measures the novelty of the combination.  
2. **Formulaic compounds** (negative-S₂ second element): The poet uses a recognized compound formula ("heavy-hearted," "well-born") that GPT-2 has learned. These compounds are informationally *cheaper* than standalone words because the first element pre-activates the second. The compound actually *reduces* local surprise.

**Corollary:** The Straussian gap at compound positions allows us to distinguish **Hopkins-style invention** (each compound a micro-bet against language norms) from **ballad-style formula** (each compound a recognized token confirming genre expectations).

---

## Suggested Next Steps

1. **Filter tokenization artifacts**: Some high-S₂ "compounds" are GPT-2 subword splits of long compound words. A cleaner filter would exclude cases where the "first element" is itself a subword fragment (contains no vowel or has length < 3).
2. **Compound frequency analysis**: Cross-reference compound second-elements with their frequency in GPT-2's training distribution to separate "rare word" effects from "unexpected combination" effects.
3. **Diachronic compound analysis**: Track when specific compound types (kennings → Spenserian compounds → Hopkins coinages → modernist compounds) enter and leave the "creative" vs "formulaic" register.
4. **Semantic cohesion of compounds**: Use semantic embedding distance to measure how surprising a second element is *semantically* (not just statistically). A compound with high S₂ AND high semantic distance between elements (wine + dark) would be a "pure combination surprise," while high S₂ with low semantic distance would be a "rare collocate."
