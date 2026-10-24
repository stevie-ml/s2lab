# Clerihew vs Limerick: Two Constrained Forms, Opposite S₂ Profiles

**Date:** 2026-10-24  
**Experiment:** `experiments/clerihew_vs_limerick.py`  
**Corpus:** 5 clerihews, 10 limericks  
**Builds on:** `findings/limerick_internal_s2.md`, `findings/repetition_and_entropy.md`, era comparison in researcher reports

---

## The Puzzle

The era comparison table presents a paradox:

| Era | Artifact-free Avg S₂ |
|---|---|
| clerihew | **+0.35** (highest positive among all poetry forms) |
| limerick | **−0.66** (among the lowest — barely above cliché-control) |

Both are highly constrained formal verse. Both require strict rhyme. Both are traditionally humorous. Yet they sit at opposite ends of the S₂ spectrum. Why?

---

## Core Results

*Analysis run on expanded corpus: 10 clerihews (5 original Bentley + 5 new synthetic test cases), 10 limericks.*

### Overall Comparison (artifact-free tokens only)

| Metric | Clerihew | Limerick |
|---|---|---|
| Mean S₂ | **+0.507** | **−0.661** |
| Median S₂ | −0.666 | −1.389 |
| Std S₂ | 4.517 | 3.356 |
| Positive S₂ ratio | 43.5% | 30.0% |
| n poems | 10 | 10 |

**The mean gap is 1.168 bits** — substantial. But note the medians: both forms have *negative* median S₂, meaning the *typical* token in both forms is conformist. The difference is in the **tails** — clerihews have higher-S₂ outlier tokens.

---

## Finding 1: Proper Nouns Are Necessary But Not Sufficient

The clerihew form *requires* including a famous person's full name plus specific biographical facts. These create exactly the tokens GPT-2 never predicts:

| Metric | Clerihew | Limerick |
|---|---|---|
| Proper noun token % | **8.6%** | 3.3% |
| Mean S₂ (proper nouns) | **+3.790** | +2.625 |
| Mean S₂ (all other tokens) | **+0.198** | −0.773 |

With the expanded corpus (n=10), the picture is more nuanced than with n=5. **Non-proper-noun tokens in clerihews have mean S₂ = +0.198** — still positive! The elevated mean is *primarily* but not *entirely* driven by proper nouns.

The additional high-S₂ moments reveal a second mechanism: **biographical factual terms** — specific words that convey the fact the form demands:

| Token | S₂ | Type |
|---|---|---|
| " gravy" | +18.41 | absurd rhyme word (Davy / gravy) |
| " raven" | +15.83 | literary allusion (Poe's raven) |
| " sums" | +13.31 | factual term (Newton → mathematics) |
| " pige" | +12.87 | biographical detail (Tesla's pigeon obsession) |
| " alternating" | +11.82 | technical term (alternating current) |
| " sodium" | +11.52 | scientific discovery (Davy's discovery) |

**The clerihew's high S₂ is driven by content specificity**: both proper nouns AND the specific technical/biographical vocabulary the form's factual obligation requires.

---

## Finding 2: What Makes Clerihew Proper Nouns So Surprising

The top S₂ moments in clerihews are a window into the form's mechanism:

| Token | S₂ | Context | GPT-2 predicted | Note |
|---|---|---|---|---|
| " gravy" | +18.41 | "Abominated" | [by, in, for] | Abominable → rhyme |
| " Tay" | +11.84 | "His" | [name, first, father] | River/bridge allusion |
| " sodium" | +11.52 | "Of having discovered" | [the, a, \n] | Scientific fact |
| " mild" | +11.30 | "Wilde" | [I, the, you] | Rhyme pivot: Wilde/mild |
| " McG" | +10.51 | "Topaz" | [,, -, \n] | Surname fragment |
| " Mew" | +8.86 | "otte" | [,, 's, "] | Obscure poet name |
| " rather" | +8.67 | "Was known as" | [the, a, '] | Biographical evaluation |

**Three mechanisms drive clerihew S₂:**
1. **Biographical facts**: "sodium" (Humphrey Davy discovered it), "Tay Bridge" (McGonagall's famous disaster poem)
2. **Absurd rhyme pivots**: After "Wilde", the model expects connectives — but the form demands "mild", creating a pure Straussian gap
3. **Rare/obscure proper names**: "Charlotte Mew" is obscure enough that GPT-2 hallucinates continuations of "Charlotte" rather than expecting a surname

---

## Finding 3: Limericks' Low S₂ Has Two Sources

| Limerick feature | Effect on S₂ |
|---|---|
| Anapestic meter | Rhythmic slots constrain token length/stress → model predicts syllabic patterns |
| AABBA rhyme scheme | Double-constrained rhyme positions create anticipable endings |
| Traditional subject matter | Predictable narrative arc (person → situation → absurd outcome) |

Even the highest S₂ limerick moments are structurally interesting:

| Token | S₂ | Context | GPT-2 predicted | Note |
|---|---|---|---|---|
| " scan" | +14.18 | "icks never would" | [have, be, 've] | *Meta-limerick about limericks!* |
| "pps" | +12.48 | "'s a Mo" | [at, -, ose] | Lear's invented word "Moppsikon" |
| " plac" | +9.49 | ", Who" | [was, had, ,] | Unusual post-relative verb |
| " Ware" | +9.41 | "Old Person of" | [the, God, Light] | Place name: GPT-2 expected abstract noun |

**The highest-S₂ moment in all limericks is meta**: "limericks never would scan" (a limerick about limericks that intentionally *doesn't* scan) creates genuine conceptual surprise. This is the Straussian gap at the level of form itself.

---

## Finding 4: Edward Lear vs Traditional Limericks

| Subtype | n | Mean artifact-free S₂ |
|---|---|---|
| Edward Lear | 3 | **−0.324** |
| Traditional/anonymous | 7 | **−0.797** |

Lear's limericks are significantly higher-S₂ than traditional ones (+0.47 advantage). The mechanism: **invented vocabulary**. Words like "Moppsikon Floppsikon" and "Pobble" are completely outside GPT-2's training distribution, creating high-surprisal moments even within an otherwise highly constrained form.

This mirrors the proper noun effect in clerihews: *unusual lexical material* (whether proper nouns or invented words) generates the Straussian gap, regardless of formal constraint.

---

## Finding 5: Both Forms Peak Early

Positional S₂ profiles (artifact-free):

| Position | Clerihew | Limerick |
|---|---|---|
| Opening (0–25%) | +0.639 | −0.405 |
| Early middle (25–50%) | +0.149 | −0.641 |
| Late middle (50–75%) | +0.519 | −0.999 |
| Closing (75–100%) | +0.113 | −0.606 |

Both forms have their *highest* S₂ in the opening position — which makes sense: the first token of a short poem is the most contextually unconstrained. Clerihews, however, remain positive throughout, while limericks stay negative. Limericks are *deepest* in the late-middle (the C rhyme couplet, AA**BB**A), where the double rhyme maximally constrains the model's expectations.

---

## Synthesis: The Proper Noun Paradox of Formal Verse

The clerihew and limerick invert conventional assumptions about constraint and surprise:

**The limerick is MORE constrained** (meter + rhyme) and achieves **lower S₂** — formal constraint suppresses the Straussian gap.

**The clerihew is LESS formally constrained** (rhyme only, no meter) but achieves **higher S₂** — because the *content constraint* (must name a real person and assert biographical facts) forces tokens that no purely formal constraint would require.

This points to a theoretical distinction:
- **Form-level constraint** (meter, rhyme scheme): makes token selection more predictable → *lowers S₂*
- **Content-level constraint** (biographical reference, specific allusion): forces rare tokens → *raises S₂*

The clerihew shows that **content obligation can be more informatively disruptive than formal structure**. What constrains the *subject* (you must write about sodium, about the Tay Bridge) can override what constrains the *syntax* in producing surprisal.

---

## Next Steps

1. **Test with more clerihews**: n=5 is small. Add 10 more clerihews to confirm the proper noun mechanism.
2. **Dissect the limerick meter effect**: Compare metered vs unmetered poems at positions that *should* be rhyme slots. Does the model learn to anticipate rhyme?
3. **Control experiment**: Rewrite the clerihew subjects as functional descriptions (e.g., replace "Humphrey Davy" with "The chemist") — does mean S₂ drop to limerick levels?
4. **Oulipo poems** (another constrained form at −0.15) make an interesting intermediate case: severe formal constraint but usually no biographical proper nouns.
