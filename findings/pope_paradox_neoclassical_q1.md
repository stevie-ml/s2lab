# The Pope Paradox Resolved: Neoclassical Lexical Density and Q1 Dominance

**Date:** 2026-10-13  
**Experiment:** `experiments/pope_paradox.py` → `results/pope_paradox.json`  
**Corpus:** 271 texts; focal poets = 15; focal eras = 8  
**New poems added (5):** Pope × 3 (An Essay on Criticism, Epistle to Dr. Arbuthnot, Essay on Man),
  Dryden × 1 (MacFlecknoe), Johnson × 1 (The Vanity of Human Wishes)  
**Builds on:** `q2_q1_strategy_taxonomy.md` (2026-10-11) — flagged Pope as a paradox

---

## Background: The Paradox

The Q2/Q1 taxonomy found Alexander Pope to be the **most extreme Q1 strategist** in the corpus
(Q2/Q1 ratio = 0.13 in the prior study, 0.18 in this extended study with 4 Pope poems total).

**Q1 moments** = high surprisal + high entropy: the model's prediction field was diffuse;
the poet chose something unexpected from a wide-open space.  
**Q2 moments** = high surprisal + low entropy: the model was confident; the poet defied it ("syntax traps").

The paradox: **heroic couplets should produce Q2 moments.** The closed couplet's
strict meter and rhyme should create high-confidence model predictions about line endings
and clause boundaries — and then Pope's deviations should be Q2 "syntax traps." Instead,
Pope is the most Q1-dominant formal poet in the corpus.

---

## Results: Poet-Level Q2/Q1 Ratios and Prediction Field Structure

| Poet | Q2/Q1 Ratio | Q1 H_top10 | Q2 H_top10 | H_top10 Gap | Q1 content% | Model predicts fn@Q1% |
|------|-------------|-----------|-----------|------------|------------|----------------------|
| **Alexander Pope** | **0.18** | 2.813 | 2.088 | 0.725 | **91.5%** | **59.6%** |
| John Dryden | 0.27 | 2.685 | 1.821 | 0.864 | **96.2%** | **69.2%** |
| John Milton | 0.29 | 2.900 | 2.106 | 0.795 | 91.8% | 55.2% |
| W.B. Yeats | 0.32 | 2.859 | 1.938 | 0.921 | 90.3% | 52.1% |
| John Donne | 0.33 | 2.832 | 1.985 | 0.847 | 88.2% | 50.9% |
| John Keats | 0.35 | 2.870 | 2.215 | 0.655 | 90.0% | 47.8% |
| George Herbert | 0.35 | 2.809 | 1.996 | 0.813 | 87.2% | 52.3% |
| Samuel Johnson | 0.44 | 2.808 | 1.644 | 1.165 | **96.0%** | **48.0%** |
| Gerard Manley Hopkins | 0.44 | 2.820 | 1.909 | 0.911 | 88.9% | 51.1% |
| William Carlos Williams | 0.50 | 3.063 | 1.721 | 1.342 | 90.5% | 43.2% |
| Carolyn Forché | 1.80 | 2.958 | 2.427 | 0.530 | 83.1% | 42.0% |
| Russell Edson | 2.20 | 2.763 | 2.204 | 0.559 | 82.4% | 41.5% |
| Frank O'Hara | 1.53 | 2.631 | 2.099 | 0.532 | 81.7% | 39.2% |
| **W.S. Merwin** | **8.00** | 3.119 | 2.430 | 0.689 | 78.1% | 35.4% |

---

## The Resolution: Neoclassical Lexical Density

### What Happens at Pope's Q1 Moments

At Pope's 141 Q1 surprise moments:
- **91.5% are content words** (nouns, verbs, adjectives): "Muse," "Goddess," "alike," "mislead," "err"
- **59.6% of the time, GPT-2 predicted a function word**: "the," "and," "of," "to," "in"
- Mean top-1 prediction probability: **0.126** (low certainty — multiple function words are equally plausible)
- Mean H_top10 = **2.813** (very diffuse prediction field)

**The pattern:** GPT-2 arrives at a syntactic position and expects one of several function-word connectors.
Pope writes a content word instead. The prediction field is diffuse not because GPT-2 is confused about
grammar, but because multiple grammatically valid function words are all plausible — and then Pope
bypasses all of them.

### The Heroic Couplet as Compression Engine

In a Pope couplet like:

> *'Tis with our judgments as our watches, none*  
> *Go just alike, yet each believes his own.*

After "our watches," GPT-2 expects a connective (", which", "that", "and") — a function word
bridging the comparison. Pope writes "none" — a content word that immediately begins the second
clause rather than explicitly connecting the first. The couplet COMPRESSES the connective tissue
out; Pope's surprise is not "defiance of confident prediction" (Q2) but "elimination of the
expected connectors" (Q1 with function→content substitution).

### Three Types of Neoclassical Q1 Dominance

The data reveals three distinct mechanisms, all producing Q1 dominance:

| Poet | Mechanism | Signature |
|------|-----------|-----------|
| **Pope, Dryden** | **Lexical density** | Model predicts fn words (59–69%), gets content words; low top-1 prob (0.13–0.15) |
| **Milton, Donne, Herbert** | **Syntactic inversion** | Archaic word orders create genuine grammatical uncertainty; H_top10 high at ALL moments |
| **Hopkins, Yeats** | **Compound/archaic lexis** | Unusual compounds and archaisms make even content-word predictions diffuse |

Pope is distinct even within this Q1-dominant cluster: his mechanism is the most **syntactically shallow**
and the most **lexically dense**. He doesn't invert clauses (Milton) or forge compounds (Hopkins) — he
simply omits the connective tissue that contemporary English relies on.

---

## Era-Level Confirmation

| Era | Q2/Q1 | Q1 content% | Model predicts fn@Q1% |
|-----|-------|------------|----------------------|
| metaphysical | 0.31 | 87.5% | 52.5% |
| **18th_century** | **0.35** | **94.0%** | **59.8%** |
| beat | 0.52 | 93.5% | 35.9% |
| victorian | 0.52 | 89.2% | 49.2% |
| romantic | 0.53 | 90.5% | 50.2% |
| early_modern | 0.57 | 86.4% | 59.3% |
| modernist | 0.60 | 90.5% | 46.6% |
| new_york_school | 0.71 | 89.8% | 52.4% |

**18th-century verse has the highest content-word rate at Q1 moments (94.0%) and the highest
function-word prediction rate (59.8%)** — confirming that the neoclassical era, not just Pope, 
exploits lexical density as its primary surprise mechanism.

Note the **Beat paradox** (ratio 0.52, content 93.5%, fn predicted 35.9%):
Beat poetry is also Q1-dominant with high content-word density, BUT the model isn't predicting
function words at those moments — it's predicting other content words. Beat's Q1 surprise is
genuine lexical unpredictability (unusual choices within an open content-word field),
not neoclassical density compression.

---

## The Johnson Contrast: A More "Ambush-Ready" Neoclassical Style

Samuel Johnson, also neoclassical (Q2/Q1 = 0.44), shows a different profile:
- **Q2 mean S2 = 7.95** vs Pope's 6.31 — Johnson's syntax traps are more powerful when they fire
- **Q2 H_top10 = 1.644** vs Pope's 2.088 — Johnson creates tighter, more confident prediction fields for Q2 moments
- Johnson's "The Vanity of Human Wishes" uses inverted Latin syntax more aggressively than Pope's essays,
  creating genuine Q2 "ambushes" at syntactic pivots

Johnson is thus a **transitional figure** between Pope's pure density strategy and
the archaic-syntax Q1 dominance of Milton/Donne.

---

## Summary Finding

**The Pope Paradox is resolved by the distinction between two mechanisms of Q1 dominance:**

1. **Syntactic inversion** (Milton, Donne): archaic word-orders create diffuse prediction fields
   throughout the clause, including at function-word positions.

2. **Lexical density** (Pope, Dryden): grammatically conventional syntax but content words substituted
   for expected function-word connectors. The couplet's compression engine strips out "the," "and,"
   "of" and replaces them with nouns, verbs, and adjectives.

The heroic couplet does NOT produce Q2 moments because its constraint operates at the *phonological*
level (rhyme, meter) rather than the *syntactic* level (clause boundaries, punctuation). GPT-2's
prediction engine operates on tokens in sequence and does not "know" it's inside a couplet. The
model can only form confident predictions from syntactic context — and Pope's couplets have
low-confidence syntax despite high formal constraint.

In information-theoretic terms, Pope's practice is a **density tax**: he charges the reader more
surprisal-per-connective than contemporary English would, by making every connector do double
work as a content word. The Straussian gap is not what he suppressed (the model's function words)
but the connective tissue the model would have written instead of his nouns.

---

## Suggested Next Steps

1. **Token-level Pope analysis**: Map specific positions in a Pope couplet where function→content
   substitution occurs. Does it cluster at syntactic pivots (after comma, after "as," "than")?

2. **Dryden vs. Pope within neoclassical**: Dryden's fn-prediction rate (69.2%) exceeds Pope's (59.6%).
   Is Dryden's heroic couplet DENSER than Pope's? Count average content-to-function-word ratio.

3. **The "density" measure**: Create a poem-level statistic: proportion of syntactic positions
   where a content word appears instead of the model's top-1 function-word prediction. This would
   quantify "neoclassical compression" as a single number.

4. **Add more 18th-century texts**: Gray's "Elegy," Cowper's "The Task," Goldsmith's "The Deserted
   Village" would deepen the era analysis. Do all 18th-century forms show this pattern, or only
   heroic-couplet verse?
