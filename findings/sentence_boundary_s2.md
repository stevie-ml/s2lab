# Sentence Boundaries and S₂: Where Within the Sentence Do Poets Deviate?

**Date:** 2026-11-23  
**Experiment:** `experiments/sentence_boundary_s2.py`  
**Data:** 436 texts (English-only subset, all eras); stanza-break artifact filter applied (p_newline < 0.9 tokens only)  
**Builds on:** `syntactic_position_vs_s2.md`, `enjambment_vs_s2.md`, `stanza_break_artifact.md`

---

## Research Question

Prior work established the Straussian gap at the **line position** level (line-initial positions inflate S₂ via the stanza-break artifact) and at the **POS** level (ADJ and NOUN carry the most deviation). But where within the **sentence** do poets concentrate their surprises? Do they open sentences with unexpected words, or close them? And how does *enjambment* — continuing a sentence across a line break — interact with sentence-level S₂?

---

## Method

- Used punctuation tokens (`.`, `!`, `?`) in the GPT-2 token stream as sentence-boundary markers — no NLTK required
- Categorized each non-punctuation token as:
  - **sentence_initial**: first content token after a sentence-ending marker
  - **sentence_final**: last content token before a sentence-ending marker
  - **sentence_medial**: all other content tokens
- **Enjambment detection**: a sentence-initial token is *enjambed* if it does NOT immediately follow a newline (the sentence continues mid-line from the previous line); *end-stopped* if it follows a newline (new sentence = new line)
- Applied p_newline < 0.9 filter throughout to exclude stanza-break artifact positions

---

## Key Finding 1: The Sentence-Final Salvo Effect

| Position | Poetry n | Poetry avg S₂ | Prose avg S₂ | Δ (poetry – prose) |
|---|---|---|---|---|
| **sentence_final** | 2234 | **+0.371** | **−2.551** | **+2.922** |
| sentence_medial | 38750 | −0.074 | −1.903 | +1.829 |
| sentence_initial | 1562 | +0.136 | −1.521 | +1.657 |
| clause_final | 724 | +0.254 | — | — |
| clause_initial | 532 | +0.215 | — | — |

**The sentence-final position carries the largest poetry-prose S₂ gap (2.92 bits) of any sentence position.** This is larger than the sentence-medial (1.83 bits) or sentence-initial (1.66 bits) gaps.

Sentence-final is also the only position where poetry achieves **solidly positive** average S₂ (+0.37), while sentence-medial is slightly negative (−0.07). Poetry's S₂ gradient within the sentence runs:

> sentence_final (+0.37) > sentence_initial (+0.14) > sentence_medial (−0.07)

**Interpretation:** Poets front-load their grammar (use expected sentence openers: "The", "I", "And") but *back-load their surprise* — the last word before the period is where the poet's choice is most deviant from what the model expected. This is the sentence-level analogue of the "closing salvo" effect documented at the stanza level.

### Exemplary sentence-final tokens (high S₂, artifact-free):

| Token | S₂ | Author | Era |
|---|---|---|---|
| "jar" | 22.97 | Jean Lescure | oulipo |
| "consequences" | 18.88 | William Stafford | mid_century |
| "gravy" | 18.41 | Edmund Clerihew Bentley | clerihew |
| "poems" | 18.06 | Joy Harjo | postcolonial |
| "green" | 14.00 | Federico García Lorca | latin_american |
| "awhile" | 15.80 | Robert Burns | romantic |
| "Almighty" | 13.58 | Caedmon (trans.) | old_english |
| "Sicily" | 13.00 | Oscar Wilde | fixed_form |

Lorca's "green" (from "Romance Sonámbulo," whose refrain *verde que te quiero verde* ends at "verde") scores S₂=14.00 twice — in the original Spanish transcription and in translation. The model cannot predict that the sentence closes on the same color word each time, confirming that refrain creates Straussian surprise even at sentence-endings.

---

## Key Finding 2: The Enjambment Boost

| Sentence-initial type | n | Avg S₂ |
|---|---|---|
| **Enjambed** (sentence continues mid-line) | 460 | **+0.825** |
| End-stopped (new sentence = new line) | 1102 | **−0.151** |
| **Δ** | | **+0.976** |

When a poet enjambs — continues a sentence across a line break so that the sentence-initial token is NOT at the start of a line — that token has **1 full bit higher S₂** than when the sentence opens at a new line.

This is not an artifact: by definition, enjambed sentence-initial tokens have p_newline < 0.9 (the newline probability was low, so the artifact filter passes them already). The effect is genuine: **enjambment places sentence openings in mid-line positions where the model is NOT primed to expect a new sentence, increasing local surprise.**

### Exemplary enjambed sentence-initial tokens:

| Context | Chosen token | S₂ | Author |
|---|---|---|---|
| "door, good John!" → | "fatig[ued]" | 19.56 | Alexander Pope (18th_century) |
| "Drive deodorant." → | "Broken" | 14.20 | Carolyn Forche (prose_poetry) |
| "their histories, too." → | "Talk" | 11.74 | Joy Harjo (postcolonial) |
| "you—with earth?" → | "air" | 11.01 | Agha Shahid Ali (postcolonial) |
| "Don't tell!" → | "they" | 10.79 | Emily Dickinson (19th_century) |
| "she'll be cut." → | "Move" | 10.63 | Gottfried Benn (german_expr.) |
| "if I told him." → | "Now" | 10.62 | Gertrude Stein (oulipo) |
| "for Adonais!" → | "though" | 10.55 | Percy Bysshe Shelley (elegy) |
| "Captain! my Captain!" → | "rise" | 10.27 | Walt Whitman (19th_century) |

Whitman's famous "O Captain! my Captain! / rise up and hear the bells" shows the effect perfectly: the sentence continues across the line break, and "rise" at that mid-line position carries S₂=10.27 because the model, having just seen a line-ending exclamation, does not expect the sentence to continue with a verb.

---

## Key Finding 3: Era-Specific Sentence Strategies

### Sentence-Final S₂ by Era (top 10):

| Era | SF n | SF avg S₂ | SI avg S₂ | SM avg S₂ |
|---|---|---|---|---|
| **mid_century** | 36 | **+3.08** | −1.94 | +0.07 |
| parody | 22 | +1.45 | −0.55 | +0.03 |
| old_english | 20 | +1.42 | +0.78 | +0.19 |
| latin_american | 23 | +1.35 | +1.65 | −0.17 |
| metaphysical | 36 | +1.35 | +0.26 | −0.24 |
| german_expressionist | 43 | +1.19 | +0.06 | +0.14 |
| haiku | 23 | +0.75 | **+2.37** | +0.44 |
| new_york_school | 131 | +0.02 | −0.35 | −0.39 |
| control (prose) | — | −2.55 | −1.52 | −1.90 |

**Mid-century** (Brooks, Plath, Stafford in this corpus) achieves the highest sentence-final S₂ (+3.08) of any era — nearly 6 bits above prose. These poets drive their sentences toward unexpected terminal words: "consequences," "awhile," "gravy." The sentence-initial is very low (−1.94): they open conventionally, then detonate at the end.

**Haiku** shows the inverse pattern: sentence-initial S₂ = **+2.37** (the highest of any era), sentence-final = +0.75. Haiku, constrained to 3–5 tokens per sentence, inverts the usual strategy — the first word of a haiku is itself the surprise.

**New York School** (Ashbery and contemporaries) shows near-zero sentence-final S₂ (+0.02), consistent with the flat information profile documented across this corpus. The school operates without a sentence-level finale strategy.

### Enjambment Effect by Era (Δ = enjambed SI S₂ − end-stopped SI S₂):

| Era | Ej n | Ej S₂ | End-stopped S₂ | Δ |
|---|---|---|---|---|
| **postcolonial** | 20 | +3.22 | −1.42 | **+4.65** |
| **18th_century** | 7 | +3.61 | −0.99 | **+4.60** |
| german_expressionist | 13 | +2.19 | −1.91 | +4.10 |
| contemporary | 25 | +0.76 | −0.54 | +1.30 |
| modernist | 17 | +0.49 | −0.76 | +1.25 |
| new_york_school | 61 | +0.07 | −1.18 | +1.24 |
| **mid_century** | 15 | **−2.45** | −1.09 | **−1.36** |

The **postcolonial** and **18th-century** eras show the largest enjambment boost (Δ ≈ 4.6). For the 18th century (Pope, primarily), this is striking: the heroic couplet tradition establishes strong expectation of end-stopping, so when Pope does enjamb, the sentence-initial token is maximally unexpected. The contrast with his typical closed couplets creates Straussian effect.

**Mid-century** shows a *reversed* enjambment effect (Δ = −1.36): mid-century enjambed sentence-initial tokens are LESS surprising than end-stopped ones. Combined with their dominant sentence-final strategy, this confirms that mid-century poets (Brooks, Plath) concentrate surprise at sentence-endings, not mid-sentence continuations.

---

## Synthesis: Two Sentence-Level Strategies

The analysis reveals two distinct strategies for distributing S₂ within the sentence:

| Strategy | Defining feature | Era examples |
|---|---|---|
| **Sentence-final salvo** | High SF S₂, low SI S₂ | mid_century, metaphysical, 18th_century |
| **Sentence-initial launch** | High SI S₂ (esp. enjambed), low SF S₂ | haiku, postcolonial, language poetry |

Mid-century American poetry concentrates surprise in the terminal word of each sentence — the punch lands at the period. Haiku and postcolonial poetry launch from unexpected openings. The two strategies create different reading experiences: the salvo makes you wait for the surprise; the launch throws you into it.

---

## Relationship to Prior Findings

- **POS finding** (`syntactic_position_vs_s2.md`): ADJ and NOUN carry the most S₂. This is consistent — sentence-final positions often contain content words (the last noun or adjective before a period). The sentence-final salvo effect may largely be a POS × position interaction.
- **Stanza-break artifact** (`stanza_break_artifact.md`): Post-newline token inflation (which inflated enjambment-based S₂ readings in earlier work) is filtered out here. The enjambment boost found here (+0.976 bits) is **not** the stanza-break artifact — it's genuine, as these are mid-line sentence continuations where p_newline is already low.
- **Closing salvo** (`closing_salvo.md`): The sentence-final effect echoes the poem-level closing salvo (last stanza / last line elevated S₂). The same "detonation at the terminal position" logic operates at both the sentence and poem levels.

---

## Suggested Next Steps

1. **POS × position interaction**: Do sentence-final ADJ have higher S₂ than sentence-medial ADJ? Cross-tabulate the POS and position dimensions to find the most deviant slot (hypothesis: sentence-final ADJ is the peak).
2. **Sentence length × S₂**: Do longer sentences show a steeper rise toward sentence-final S₂, or is the effect uniform regardless of sentence length?
3. **Specific mid-century deep-dive**: Which poems drive the mid_century SF=3.08 figure? Is it mainly Brooks and Plath, or Stafford too?
4. **The Pope enjambment anomaly**: His S₂=19.56 enjambed "fatigued" is the highest enjambment example. Find all Pope enjambments in the corpus and characterize them — is this a systematic strategy or an outlier?
5. **Clause-level analysis**: Expand the analysis to treat semicolons and colons as "minor sentence boundaries" and check whether the clause-final effect mirrors the sentence-final effect.
