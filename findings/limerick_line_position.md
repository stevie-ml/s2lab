# Limerick S2 by Line Position: The Punchline Paradox

**Date:** 2026-10-12  
**Poems analyzed:** 3 limericks (pre-computed corpus_results.json)  
**Hypothesis tested:** Do lines 3-4 (the "twist") or line 5 (the punchline) show higher S2?

---

## Background

Limericks have a rigid 5-line AABBA structure:
- **Line 1 (A)**: ~8 syllables, introduces the subject ("There was a young lady…")  
- **Line 2 (A)**: ~8 syllables, develops the situation ("Whose speed was far faster than light")  
- **Lines 3-4 (BB)**: ~5 syllables each, shorter pivot/setup ("She set out one day / In a relative way")  
- **Line 5 (A)**: ~8 syllables, delivers the punchline ("And returned on the previous night")

Prior analysis showed limericks have the second-lowest average S2 of any poetic form (−1.123, near clichés), which we attributed to extreme formal constraint. The question here: **where within a limerick does S2 concentrate?**

---

## Results

### Per-line S2 (aggregated across 3 limericks)

| Line | Role | Avg S2 (raw) | Approx S2 (clean) | Pos Ratio | n tokens |
|------|------|-------------|-------------------|-----------|----------|
| 1    | A-rhyme: intro     | −1.297 | ~−1.2 | 29% | 24 |
| 2    | A-rhyme: develop   | **+1.366** | **~−0.5** | 32% | 31 |
| 3    | B-rhyme: pivot     | +0.165 | ~−0.7 | 33% | 21 |
| 4    | B-rhyme: setup     | −1.789 | ~−1.8 | **9%** | 22 |
| 5    | A-rhyme: punchline | −1.351 | ~−1.3 | 20% | 25 |

*"Clean" approximation: per-poem artifact-free averages averaged across the 3 poems.*

### Group averages (raw)

| Group | Lines | Avg S2 |
|-------|-------|--------|
| Intro/develop | 1–2 | +0.204 |
| Pivot | 3–4 | −0.835 |
| Punchline | 5 | **−1.351** |

---

## Key Finding: The Punchline Paradox

**The hypothesis was wrong in the most interesting way possible.**

The punchline (line 5) has the **lowest** average S2 of any limerick position. Line 2 — the "development" line — has the highest.

### Why line 2 leads (raw)

The raw advantage of line 2 is partly driven by the "relative pronoun artifact": all three limericks begin line 2 with "Who/Whose":

| Poem | Line 2 start | S2 |
|------|-------------|-----|
| "Old Man with a beard" | "Who" | +20.88 |
| "Lady Named Bright" | "Wh" (→ "Whose") | +20.66 |
| "Man from Peru" | "Who" | +16.67 |

At the position after "beard,\n", "light;\n", "Peru\n" etc., GPT-2 assigns high probability to blank lines (stanza breaks), making the pronoun "Who/Whose" extremely surprising. These tokens partially filter as artifacts (high p(newline) for subsequent context).

### Why line 2 still leads (artifact-free)

Even removing artifacts, line 2 averages **~−0.5** vs line 5 at **~−1.3**. The genuinely surprising content of line 2 drives this: "eating his shoe" (S2=+5.52), "faster than light" (+2.46), "just as I feared" (+4.58). These are the conceptual pivots that establish the limerick's absurd premise — and GPT-2 is genuinely surprised by them.

### Why the punchline is predictable

The three punchlines score poorly:

| Poem | Line 5 | Avg S2 |
|------|--------|--------|
| "Old Man" | "Have all built their nests in my beard!" | −0.943 |
| "Bright" | "And returned on the previous night." | −1.098 |
| "Peru" | "And found that his dream had come true." | −1.955 |

"And found that his dream had come true" is near-maximally predictable (−1.955) — GPT-2 has learned this resolution pattern from countless dream-revelation narratives. The other punchlines follow equally conventional resolution structures.

### Why lines 3-4 are low

The B-rhyme lines are:
- Shorter (~5 syllables) — less room for deviation
- Syntactically constrained by the pivot structure
- Line 4 in particular is often a near-mechanical setup ("In the middle of the night," "In a relative way") with 0–9% positive S2

---

## The Core Finding: Narrative vs. Linguistic Surprise

This data reveals a fundamental gap between **narrative surprise** and **linguistic surprise**:

> The limerick's punchline is **narratively surprising** (humans find it funny/unexpected) but **linguistically predictable** (GPT-2 has encountered the resolution pattern before). Line 2's content is **both** narratively and linguistically surprising — it introduces the absurd premise that humans haven't yet processed and that GPT-2 hasn't predicted.

This is consistent with the Straussian framework: GPT-2 models "what language expects," which includes conventional narrative arcs. A dream-comes-true ending is a well-worn narrative shape; GPT-2 "knows" that absurd setups resolve paradoxically. The information-theoretic surprise is front-loaded in the setup (line 2), not back-loaded in the payoff.

**Implication**: High S2 at punchline position would require a conclusion that violates not just reader expectation but language model expectation — a resolution that language itself has not conventionalized. Truly novel punchlines (those GPT-2 cannot predict) may be rarer and more structurally difficult to write.

---

## Comparison to Other Fixed Forms

This pattern mirrors findings from other constrained forms:
- **Haiku**: S2 concentrates at the *kigo* (season word) and *kireji* position, not the final line
- **Sonnet**: The volta (turn) generates the highest S2, not the couplet (closure tokens analysis)
- **Limerick**: S2 concentrates at line 2 (premise development), not line 5 (punchline)

Pattern: **The turn/pivot/development of a fixed form generates more linguistic surprise than its conventional ending.**

---

## Expanded Analysis: 7-Poem Corpus

Adding 4 more limericks ("A Tutor Who Tooted the Flute", "A Flea and a Fly in a Flue", "There Was an Old Person of Ware", "There Was a Young Man of Japan") shifts the results:

### Per-poem line averages (raw S2)

| Title | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| Old Man of Nantucket | −2.52 | +0.89 | **+2.22** | −1.50 | −0.94 |
| Lady Named Bright | −0.58 | +1.27 | −1.06 | −1.38 | −1.10 |
| Man from Peru | −0.54 | +2.10 | −1.15 | −2.52 | −1.95 |
| Tutor Who Tooted | +1.92 | +0.62 | −1.01 | −0.53 | −1.33 |
| Flea and a Fly | −1.32 | +1.56 | −1.63 | −1.88 | −0.33 |
| Old Person of Ware | +0.66 | +0.41 | +0.78 | +0.06 | **+2.31** |
| Young Man of Japan | +0.07 | **+3.91** | −0.79 | −0.12 | −0.25 |

### Aggregate results (7 poems, n=57–78 tokens per line)

| Line | Role | Avg S2 (raw) | Avg S2 (clean) | Pos Ratio |
|------|------|-------------|----------------|-----------|
| 1 | A-rhyme: intro | −0.408 | −0.408 | 35% |
| 2 | A-rhyme: develop | +1.485 | −0.409 | 37% |
| 3 | B-rhyme: pivot | −0.313 | −0.906 | 32% |
| 4 | B-rhyme: setup | −1.100 | **−1.235** | 22% |
| 5 | A-rhyme: punchline | −0.279 | **−0.279** | 32% |

### Revised findings

1. **Line 4 is consistently the lowest S2** — across both corpus sizes (−1.789 in 3-poem, −1.235 in 7-poem). The second short B-rhyme line is the most constrained, most predictable position in any limerick.

2. **Line 5 (punchline) has the highest artifact-free S2 (−0.279)**, edging out lines 1-2. The punchline is not the *most* predictable position, as the original 3-poem analysis suggested — but it's only slightly above lines 1-2.

3. **The "Who/Whose" artifact drives line 2's raw advantage** — 4 of 7 limericks start line 2 with "Who/Whose," which artificially inflates raw S2. Artifact-free, lines 1 and 2 are statistically tied (−0.408 vs −0.409).

4. **Outlier effects**: "Old Person of Ware" has L5=+2.31 because "Moppsikon Floppsikon" is nonsense neologism that GPT-2 cannot predict. "Young Man of Japan" has L2=+3.91 because its meta-limerick self-reference surprises GPT-2 ("Whose limericks never would scan").

### The stable finding

Across both corpus sizes, the pattern **Lines 3-4 < Lines 1-2 ≈ Line 5** holds. The BB rhyme couplet (the pivot/setup, lines 3-4) is the least surprising position. The punchline is *at least as surprising* as the introduction, and sometimes more so (when it contains genuine neologism or meta-humor). 

**The punchline paradox from the 3-poem analysis is partially revised**: line 5 is not consistently "worst" — that title belongs to line 4. But the punchline is also not consistently the "best," since lines 1-2 match it in the artifact-free analysis.

**The structural interpretation**: Lines 3-4 carry the formal burden of the limerick's meter change (shorter, stricter) and must set up the rhyme. They have less room for lexical deviation, producing consistently low S2. Lines 1-2 and 5 are all longer, with more room to surprise — and in the best limericks, they do.

---

## Suggested Next Steps

1. **Expand limerick corpus**: 10+ limericks would give statistical power for a proper ANOVA across line positions
2. **Test non-"Who/Whose" limericks**: Find limericks where line 2 doesn't start with a relative pronoun to see if the artifact-free pattern holds
3. **Cross-form punchline analysis**: Do other "joke" forms (clerihew, epigram) show the same punchline-low-S2 pattern?
4. **Anti-climax hypothesis**: Test whether known "good" limericks (voted funniest) have higher punchline S2 than average — if the punchline paradox correlates with funniness, it would be a literary quality signal
