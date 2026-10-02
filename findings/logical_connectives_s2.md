# Logical Connectives and S₂: How Conditional, Causal, and Concessive Structures Shape Poetic Surprise

**Date:** 2026-10-02  
**Experiment:** `experiments/conditional_causal_s2.py`  
**Corpus:** 175 English poetry texts (control and cliché excluded), 19,780 artifact-free tokens  
**Builds on:** `adversative_turn_s2.md`, `modal_verbs_s2.md`, `negation_and_s2.md`

---

## Research Question

When poets use logical connectives — **conditional** (if/unless), **temporal** (when/while/until), **causal** (because/so/since), **concessive** (yet/though/although/still), and **comparative** (like/as/than) — does the S₂ profile of what follows differ systematically from baseline? 

Different connectives encode different epistemic stances. A causal ("because") closes the logical chain — there must be a reason that fits. A conditional ("if") opens a hypothetical space — anything could follow. A concessive ("yet/though") signals contrast — the expected is about to be contradicted. Can these philosophical differences be measured as information-theoretic differences?

**Three hypotheses going in:**
- **H1:** Conditionals create high entropy (open possibility) → model uncertain → lower actual S₂ (anything goes)
- **H2:** Causals create low S₂ (closed chain must be coherent → conventional choices)
- **H3:** Concessives create higher S₂ (the contrast logic invites unexpected completion)

---

## Method

1. Scan all English poetry tokens for connective words; filter stanza-break artifacts (p_newline ≥ 0.9)
2. Extract S₂ and entropy for the connective itself and the 3 tokens that follow
3. Compare to corpus-wide baseline (mean S₂ = −0.437, mean H = 6.21 bits)
4. Track individual connective words to see within-category variation
5. Era-level breakdown for conditional vs. causal contrast

**Corpus baseline:** N = 19,780 tokens | mean S₂ = −0.437 | median S₂ = −1.224 | mean H = 6.21 bits

---

## Key Results

### 1. Category Summary

| Category | N | H at conn. | H at +1 | S₂ at +1 | ΔS₂ vs. base | +S₂% |
|---|---|---|---|---|---|---|
| **conditional** | 23 | 6.81 | **5.07** | −0.738 | −0.30 | 26.1% |
| temporal | 74 | 6.22 | 5.93 | −0.430 | ≈ 0 | 25.7% |
| causal | 48 | 6.39 | 6.61 | −0.565 | −0.13 | 31.2% |
| **concessive** | 84 | **7.32** | 6.45 | −0.722 | −0.29 | 33.3% |
| comparative | 144 | 6.07 | 6.47 | −0.766 | −0.33 | 36.1% |

**The most striking pattern is entropy at the connective itself:** Concessives ("yet", "though", "still") are reached at moments of maximum model uncertainty (H = 7.32 bits, +1.11 above baseline). The model is most confused when a concessive arrives — these words occur at the most "open" syntactic junctions. But despite this openness, the words that follow are not more surprising than baseline.

**The "entropy compression" effect after conditionals:** After "if", entropy at the next token drops dramatically from 6.81 to 5.07 bits (Δ −1.15). "If" opens a hypothetical frame but immediately constrains the grammar of what follows (verb phrases, noun phrases with determiners). The conditional creates a local prediction paradox: high uncertainty at the connective, then increased constraint at the clause start.

---

### 2. Individual Connective Rankings (by S₂ at +1)

| Word | Category | N | H at word | S₂ at +1 | ΔS₂ | +S₂% |
|---|---|---|---|---|---|---|
| **while** | temporal | 9 | 6.87 | +0.382 | **+0.82** | 33.3% |
| **since** | causal | 5 | 5.21 | +0.035 | +0.47 | 40.0% |
| **until** | temporal | 5 | 4.97 | −0.310 | +0.13 | **60.0%** |
| **so** | causal | 37 | 6.52 | −0.309 | +0.13 | 32.4% |
| **though** | concessive | 21 | 7.24 | −0.085 | +0.35 | 38.1% |
| **yet** | concessive | 28 | 7.00 | −0.278 | +0.16 | 39.3% |
| **when** | temporal | 30 | 6.21 | −0.180 | +0.26 | 23.3% |
| **as** | comparative | 96 | 5.89 | −0.452 | −0.02 | 39.6% |
| **like** | comparative | 35 | 6.57 | −1.008 | −0.57 | 37.1% |
| **after** | temporal | 10 | 6.29 | −1.073 | −0.64 | 20.0% |
| **if** | conditional | 23 | 6.81 | −0.738 | −0.30 | 26.1% |
| **still** | concessive | 24 | **8.57** | −1.681 | **−1.24** | 29.2% |
| **than** | comparative | 13 | 6.03 | −2.433 | **−1.99** | 7.7% |
| **once** | temporal | 6 | 6.57 | −2.238 | −1.80 | 16.7% |
| **because** | causal | 3 | 6.32 | −3.801 | **−3.36** | **0.0%** |

**The individual word variation is enormous** — from "while" (+0.82 delta) to "because" (−3.36 delta). This within-category spread swamps the between-category differences, suggesting that syntactic role within the connective category matters as much as the category itself.

**Most constraining: "because"** (S₂ = −3.80, 0% positive S₂ rate). Every instance in the corpus is followed by a highly predictable word. This confirms the hypothesis that causal explanation closes the logical space maximally — you cannot say "because" and then follow with a wild non-sequitur.

**Most constraining surprise trap: "still"** — The model is maximally uncertain when "still" arrives (H = 8.57 bits, the highest in the table). Yet the token that follows has S₂ = −1.68, far below baseline. "Still" appears at open syntactic junctions but is immediately followed by conventional words. The model's uncertainty is not exploited.

**Highest positive S₂ rate: "until"** (60.0%). With only 5 instances, this is a small sample, but "until" consistently precedes surprising completions — likely because temporal endpoints in poetry are often unexpected images.

**The "like/as" divergence:** Within comparative, "as" (S₂ = −0.45) and "like" (S₂ = −1.01) are both simile markers but behave very differently. "As" is more open; "like" constrains more strongly. This extends `simile_structure_s2.md`: the specific simile connector matters.

---

### 3. Hypothesis Tests

| Hypothesis | Prediction | Finding | Verdict |
|---|---|---|---|
| **H1:** Conditionals → high entropy → low S₂ | Higher H, lower S₂ at +1 | H at connective higher (+0.60), but entropy at +1 is LOWER (−1.15), and S₂ also lower | **H1 PARTIALLY CONFIRMED** — The conditional does have higher initial uncertainty, but the grammar constrains what follows more strongly than expected |
| **H2:** Causals → closed chain → low S₂ | Lower S₂ at +1 | S₂ = −0.565 < baseline −0.437. "Because" is S₂ = −3.80. | **H2 CONFIRMED** |
| **H3:** Concessives → contrast → high S₂ | Higher S₂ at +1 | S₂ = −0.722, worse than baseline | **H3 NOT CONFIRMED** — but concessives DO have higher entropy at the connective itself |

The key unexpected finding is the **entropy-surprise decoupling at concessives.** High entropy (7.32 bits) does not produce high S₂ (+1 position). Poets reach "yet/though/still" at moments of maximum model uncertainty, but they do NOT systematically use that uncertainty to place unexpected words. This suggests concessives function more as **structural signals** (marking a turn) than as **surprise mechanisms** — the surprise in concessive structures is conceptual (the contrast between the clauses), not token-level.

---

### 4. Era Comparison: Conditional vs. Causal Contrast

| Era | Cond. S₂ | Causal S₂ | Gap |
|---|---|---|---|
| **Victorian** | **+1.37** | **−1.40** | **+2.77** |
| New York School | — | −2.72 | — |
| Early Modern | — | −0.41 | — |

Victorian poetry shows the largest gap between conditional and causal contexts. Victorian poets use "if" as a vehicle for genuine surprise (+1.37 mean S₂) while their causal constructions ("because", "so") close into conventional formulations. This fits the Victorian aesthetic of **conditional space** — the elaborate hypothetical ("If thou could'st see what I see") followed by a surprising specific that fills the conditional frame.

---

### 5. Most Striking Individual Moments

**Conditionals:**
- Shakespeare: "If [snow]" — S₂ = 9.27, entropy at "If" = 7.47. The specific image fills the hypothetical.
- T.S. Eliot: "if [at]" — S₂ = 4.92. Conditional used to place a structural word in an unusual position.

**Causals:**
- E.E. Cummings: "so [floating]" — S₂ = 13.06, entropy at "so" = only 3.29 bits. The model is CONFIDENT about what comes after "so" (a very constrained position), but Cummings places an unusual participle. This is a classic Cummings move: break the causal constraint with a sensory verb.

**Concessives:**
- Christina Rossetti: "yet [turning]" — S₂ = 12.53. "Yet" followed by an action verb instead of an expected adjective or noun phrase.
- John Ashbery: "though [speech]" — S₂ = 10.43. Noun phrase where a clause is expected.

**Temporal:**
- Langston Hughes: "when [Abe]" — S₂ = 13.01. "When" triggers expectation of a common temporal phrase; "Abe" (Lincoln) is a specific proper name that creates enormous surprise.

---

## Summary Finding

Logical connectives do not uniformly create or constrain surprise. The clearest result is a **continuum of constraint**:

**Most constraining** (low S₂): `because` (−3.80) > `than` (−2.43) > `once` (−2.24) > `like` (−1.01) > `still` (−1.68)

**Most open** (near or above baseline): `while` (+0.38) > `since` (+0.04) > `until` (−0.31) ≈ `so` (−0.31) > `when` (−0.18)

The philosophical hypothesis that **causals constrain more than conditionals** is partially supported: "because" is the single most constraining word in the corpus. But the conditional "if" is also quite constraining — the IF-clause structure is grammatically rigid.

The deepest finding is the **"still" paradox**: the word in the corpus most often reached under high model uncertainty (H = 8.57 bits) is immediately followed by highly predictable words. Poets seem to use "still" as a structural pivot that arrives at open syntactic junctions but then returns to conventional register — a form of **"earned predictability"** that uses concessive logic to signal surprise at the conceptual level while remaining conventional at the token level.

---

## Suggested Next Steps

1. **Expand to subordinate clause structure**: look at S₂ across the full subordinate clause (10+ tokens) following each connective type
2. **Conditional + imagery**: when conditionals are followed by high-S₂ images (like Shakespeare's "If snow"), classify the semantic domain of those images
3. **"Because" in prose vs. poetry**: run the same analysis on the prose controls — is "because" even MORE constraining in prose?
4. **Era-stratified analysis of "still"**: Is the "still" paradox universal or concentrated in specific eras? Victorian and Romantic poets use this heavily
