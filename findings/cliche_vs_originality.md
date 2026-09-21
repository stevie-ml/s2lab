# The Cliché Test: Does S2 Track Poetic Originality?

**Date:** 2026-09-21  
**Experiment:** `experiments/cliche_test.py`  
**New poems added:** 6 (3 synthetic clichés, 1 Christopher Smart, 2 canonical Romantics)

---

## Research Question

If S2 measures the "gap between expectation and choice," then formulaic,
clichéd poetry should produce low S2 — GPT-2 has been trained on those stock
phrases and should predict them confidently. Conversely, wildly original poetry
should produce high S2.

**Predicted ordering**: cliché < prose < generic poetry < ecstatic verse

We tested this by adding three synthetic, deliberately formulaic poems
(greeting-card style, labeled `cliche_control`) and three canonical originals
not previously in the corpus: Christopher Smart's "For I Will Consider My Cat
Jeoffry" (1763), Coleridge's "Kubla Khan" (1816), and Blake's "Proverbs of
Hell" from *The Marriage of Heaven and Hell* (1793).

---

## Key Results

### Group S2 Averages (selected eras)

| Group | n | Avg S2 | ±σ | %+S2 |
|---|---|---|---|---|
| **Prose Control** | 5 | **-1.663** | 0.674 | 20% |
| **Synthetic Cliché** | 3 | **-0.034** | 0.295 | 28% |
| Found Poetry | 7 | -0.317 | 0.388 | 28% |
| New York School | 18 | -0.179 | 0.623 | 36% |
| Contemporary | 9 | 0.070 | 0.739 | 36% |
| Romantic | 14 | 0.050 | 0.636 | 36% |
| Victorian | 14 | 0.370 | 0.772 | 39% |
| Modernist | 18 | 0.370 | 1.160 | 38% |
| Confessional | 6 | 0.503 | 0.621 | 41% |
| **Beat** | 2 | **1.031** | 0.541 | 47% |
| **Haiku** | 8 | **1.429** | 0.770 | 43% |

### Individual New Poems

| Title | Era | Avg S2 | %+S2 | Max S2 |
|---|---|---|---|---|
| Autumn Comes (cliché) | cliche_control | -0.328 | 30% | 21.2 |
| Life Is a Journey (cliché) | cliche_control | -0.038 | 30% | 24.1 |
| My Heart Burns for You (cliché) | cliche_control | +0.263 | 25% | 28.8 |
| Proverbs of Hell (Blake) | romantic | **-0.678** | 29% | 22.7 |
| For I Will Consider My Cat Jeoffry (Smart) | 18th_century | **-0.377** | 29% | 22.0 |
| Kubla Khan (Coleridge) | romantic | +0.220 | 38% | 15.4 |

---

## Findings

### Finding 1: Cliché sits between prose and poetry — S2 is a partial quality signal

The prediction was partially confirmed:

- **Prose** avg S2: **−1.663**  
- **Synthetic Cliché** avg S2: **−0.034**  
- **All Poetry** avg S2: **+0.227**

Clichéd poems occupy the gap between prose and poetry, closer to the poetry
range but meaningfully below the poetic average. None of the three cliché
poems fell below the prose-control average. This confirms that S2 is sensitive
to the poetry/prose distinction even in formulaic verse.

**Why do clichéd poems have any positive S2 at all?** The highest-S2 tokens
in the cliché poems are almost entirely line-initial words ("For", "Together",
"We", "Your", "The") — not content words. The line-break artifact documented
in prior experiments lifts the apparent S2 even for formulaic text.

### Finding 2: The Ecstatic Reversal — anaphora lowers S2 more than clichés

The most striking result: **Christopher Smart's "For I Will Consider My Cat
Jeoffry"** and **Blake's "Proverbs of Hell"** — two of the most
semantically inventive poems in English — both score *lower* S2 than the
clichéd greeting-card poems.

- Smart (Jubilate Agno): avg S2 = **−0.377** (below two of three clichés)
- Blake (Proverbs of Hell): avg S2 = **−0.678** (below all clichés and near
  found/spoken word)

**Why?** Both poems use rigid anaphoric structures:

- Smart: every line begins "For he..." / "For I will..." / "For..."
- Blake: every proverb is a standalone declarative sentence of similar length

After the first few lines, GPT-2 "learns" the pattern within its context
window and confidently predicts "For" at each line start. The repetitive
structure makes line-initial tokens statistically expected — canceling the
line-break artifact that otherwise lifts S2. The semantic wildness of the
content (a cat's ten daily duties, aphoristic reversals of moral convention)
is invisible to GPT-2's statistical expectations because the *form* has
become predictable.

### Finding 3: S2 measures structural, not semantic, originality

This experiment reveals a fundamental asymmetry in what S2 captures:

| Dimension | Affects S2? | Evidence |
|---|---|---|
| Clichéd content with irregular line breaks | Yes (+) | Cliché avg −0.034 > prose −1.663 |
| Original content with rigid anaphoric form | No (−) | Smart −0.377 despite wild content |
| Original content with irregular form | Yes (+) | Kubla Khan +0.220 |
| Clichéd content with no line breaks | No | Prose controls consistently negative |

S2 tracks **structural unpredictability** (the form of how lines break, how
sentences are arranged) more reliably than it tracks **semantic originality**
(whether the content is inventive or stock). A greeting-card rhyme with
irregular stanza breaks can outpace an ecstatically original anaphoric poem.

### Finding 4: Kubla Khan confirms the standard model

Coleridge's "Kubla Khan" behaves as expected for canonical Romantic poetry:
avg S2 = +0.220, pos_s2_ratio = 38%. Its complex syntax, unusual vocabulary
("Xanadu", "Alph", "cedarn", "momently"), and absence of repetitive structure
produce a moderate-high S2 consistent with other Romantic poems.

---

## Implications for the S2 Framework

1. **S2 is not a quality metric per se.** It measures deviations from
   GPT-2's statistical model of language. Originality that operates within
   a predictable formal structure (anaphora, aphorism) will register as
   low S2 even if the content is semantically radical.

2. **The "formal constraint paradox"**: OuLiPo and other constraint-based
   poetry (already observed to have negative S2 in prior experiments)
   is part of a broader pattern: *repetitive or formulaic structure
   suppresses S2 regardless of semantic content.*

3. **A refined originality measure** might require separating:
   - S2_structural (from line breaks, syntactic position)
   - S2_content (residual after controlling for position)
   The position-corrected signal might better track semantic originality.

4. **The line-break artifact is a dominant signal.** In poetry, a large
   fraction of high-S2 tokens are line-initial. This is not "cheating" —
   poets do make unexpected choices at line beginnings — but it means poems
   with more line breaks (shorter lines) will tend to have higher apparent S2.

---

## Next Steps

- Compute S2 with line-break tokens excluded ("content S2 only") and
  re-rank poems — does the quality ordering change?
- Add more anaphoric poems (Walt Whitman's catalog sections, Allen Ginsberg's
  extended anaphoras) to test whether anaphora consistently suppresses S2
  even in Beat poetry (currently the highest-S2 era at 1.031)
- Add more cliché text: self-help prose, motivational speeches. Do they
  score higher than prose control but lower than poetry (like the cliché poems)?
- Test the "position-corrected S2" hypothesis: compute avg S2 only for
  non-line-initial tokens and see if ranking changes
