# Punctuation as an Information-Theoretic Device

**Date:** 2026-09-04  
**Experiment:** `experiments/punctuation_s2.py`  
**Corpus:** 89 poems, English and German (GPT-2)

---

## Research Question

Do punctuation marks affect the S₂ profiles of poems? Specifically:
1. What are the S₂ values of punctuation tokens themselves?
2. Do tokens *after* punctuation have higher or lower S₂ (fresher context = more freedom, or tighter constraint)?
3. Is Dickinson's em-dash informationally distinctive?
4. Does punctuation density correlate with overall poem S₂?

---

## Key Findings

### 1. Punctuation tokens are the most predictable thing in a poem

| Token class | Avg S₂ |
|---|---|
| **All tokens** | +0.183 |
| Non-punctuation | **+0.435** |
| Punctuation | **−1.538** |
| Post-punctuation | **−0.864** |

Punctuation marks have an average S₂ of −1.54 — by far the most negative in the corpus. GPT-2 is extremely confident about where periods, commas, and semicolons should appear, and when a poet places one, it almost always confirms the model's prediction. This makes sense: punctuation placement is one of the most rule-governed aspects of English. A poem that regularly places dashes and periods is not surprising GPT-2 at the token level — the *syntax* is doing what the model expects.

### 2. Post-punctuation tokens are MORE predictable, not less

**Counter-intuitive finding:** tokens immediately following punctuation have avg S₂ = −0.86, substantially more negative than the corpus mean (+0.18). One might expect that punctuation "resets" the context, giving poets more freedom to be surprising. The opposite is true.

**Why?** Punctuation *constrains* the next token through distribution shift. After a period, GPT-2 concentrates probability mass on "The", "A", "I", "He" — a narrow set of likely sentence starters. After a comma, it expects conjunctions and articles. The "fresh start" is paradoxically the most constrained position.

This is a general pattern, with one important exception.

### 3. The em-dash creates more openness than other punctuation

| Post-punct type | Avg post-token S₂ |
|---|---|
| **All punctuation** | −0.864 |
| **Dashes only (–, —)** | **−0.273** |

Post-dash tokens are substantially less negative than post-punctuation in general. The em-dash does not narrow predictions the way a period does. A dash can follow any grammatical position, interrupt any phrase, and launch what follows in a more open-ended direction. GPT-2 does not know what comes after a dash nearly as well as it knows what comes after a period.

This is informationally consistent with how poets use the dash: as a mid-thought pivot, not a boundary. The dash sustains ambiguity; the period forecloses it.

**Dickinson's dash density vs. other poets:**

| Poet | Dash density | Avg S₂ | Post-punct S₂ |
|---|---|---|---|
| Emily Dickinson | **0.098** | 0.540 | −1.075 |
| Walt Whitman | 0.000 | 0.760 | −1.498 |
| Gerard Manley Hopkins | 0.021 | 0.338 | −0.037 |

Dickinson has the highest dash density in the corpus (9.8% of tokens are dashes). Her post-punctuation tokens have higher S₂ than Whitman's, consistent with the dash being more informationally open than periods/commas. However, the overall post-punct S₂ is still negative for all three — the "fresh context" effect dominates even for Dickinson.

### 4. Punctuation density does not predict overall S₂

**Pearson r (punct_density vs. avg_s2) = −0.004** — essentially zero correlation.

Whether a poem is densely punctuated or nearly punctuation-free, it has no systematic S₂ advantage. The poems at the top and bottom of the punctuation-density ranking show highly variable S₂:

**Most punctuated poems (top 3):**
- Baudelaire "The Stranger" (0.257 density): avg S₂ = −0.34
- Marianne Moore "Poetry" (0.200): avg S₂ = −0.22
- Frank O'Hara "Why I Am Not a Painter" (0.186): avg S₂ = +0.80

**Least punctuated poems (bottom 3):**
- E.E. Cummings "Buffalo Bill's" (0.011): avg S₂ = −0.31
- André Breton "Free Union" (0.000): avg S₂ = −0.33
- WCW "The Red Wheelbarrow" (0.032): avg S₂ = +3.59

The Red Wheelbarrow achieves the corpus's 2nd-highest S₂ with almost no punctuation. Baudelaire's prose poem is low-S₂ despite heavy punctuation. The mechanism: punctuation density affects the punctuation tokens (which are predictable), but the dominant S₂ signal comes from the non-punctuation tokens, which poetry shapes through word choice, meter, and diction — not punctuation alone.

**However:** when we split by median punctuation density, high-punctuation poems average S₂ = +0.28 vs. low-punctuation S₂ = +0.09. This weak trend (not a correlation) may reflect that stylized poets (Dickinson, Brooks, Long Soldier) who use deliberate punctuation also tend to use surprising diction.

### 5. Notable outlier: Layli Long Soldier

Long Soldier "Whereas" (excerpt) has high punctuation density (0.155) AND very high post-punctuation S₂ (+2.13) — the only highly-punctuated poem where post-punct tokens are strongly positive-S₂. Her experimental form uses punctuation structurally (the legal "whereas" clause format) to set up genuinely unexpected continuations. The punctuation marks a frame, but what fills the frame is maximally surprising.

### 6. Gwendolyn Brooks "We Real Cool"

Brooks has high punctuation density (0.178) and very high avg S₂ (+2.18) — the highest of all densely-punctuated poems. But post-punct S₂ is strongly negative (−3.16). The "We" that follows each line break (punctuation boundary) is perfectly predicted — after the full stop of each short line, "We" is GPT-2's top guess, and that's what Brooks delivers. But the REST of each line is maximally surprising ("lurk late", "sing sin", "Jazz June"). The poem operates by making the anchor word predictable and the predicate unpredictable: a high-contrast information structure.

---

## Summary Table: S₂ by Token Class

| Class | Avg S₂ | Description |
|---|---|---|
| Non-punct tokens | +0.435 | Main carrier of poetic surprise |
| All tokens | +0.183 | Corpus mean |
| Post-dash tokens | −0.273 | Informationally open but still constrained |
| Post-punct tokens | −0.864 | Tight distributional constraint after boundary |
| Punctuation tokens | −1.538 | Most predictable class in poetry |

---

## Theoretical Implication: The Double Role of Punctuation

Punctuation operates as an information *frame* rather than an information *source*. Punctuation tokens are themselves predictable (poets don't surprise us with commas) and post-punctuation tokens are also more predictable than the poem average. But punctuation *structures* the S₂ landscape by dividing the poem into zones:

- **The mid-line interior** is where S₂ peaks — this is where the poet has maximum freedom.
- **Post-punctuation positions** are where the poet is most constrained — the reader's predictions narrow after a stop.
- **The em-dash** is an intermediate case: it creates a boundary without fully resetting expectations, leaving more room for surprise than a period.

This may explain why poets like Dickinson, who use heavy punctuation mid-line rather than at line-ends, preserve more information-theoretic freedom than poets who follow standard sentence grammar: the dash creates a pause without imposing a fresh-start constraint.

---

## Next Steps

1. **Mid-line vs. end-of-line punctuation**: Separate the analysis by *where* punctuation occurs (mid-line vs. line-final). Does mid-line punctuation constrain differently from end-line?
2. **Punctuation and S₂ peaks**: Are the highest-S₂ tokens clustered in mid-line positions (avoiding punctuation zones)?
3. **Dickinson close reading**: Analyze all 4 Dickinson poems token by token to map exactly where the dashes sit relative to S₂ peaks.
4. **The "frame" hypothesis**: Test whether long-soldier-style structural punctuation systematically produces higher post-punct S₂ than conventional punctuation.
