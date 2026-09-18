# The Adversative Turn: S₂ Dynamics After Contrastive Conjunctions

**Date:** 2026-09-18  
**Experiment:** `experiments/adversative_turn.py`  
**Corpus:** 128 texts (English-language poems, excluding prose control), 87 adversative tokens identified  
**Builds on:** `negation_and_s2.md`, `volta_and_s2.md`, `grammatical_person_s2.md`

---

## Research Question

When poets use adversative conjunctions — "but", "yet", "though", "although", "whereas" — they signal a **semantic reversal**: the current line of argument gives way to its opposite. The classical "volta" in sonnet tradition is the most famous example, but all poetry uses these pivot words.

Does the adversative turn show a distinctive information-theoretic signature? Three competing hypotheses:

- **H1 (Pre-spent)**: The surprise lives in the adversative itself; what follows is normalized and predictable (the pivot *is* the event)
- **H2 (Post-activation)**: The adversative opens a high-entropy window that poets exploit; the tokens *after* it are maximally surprising
- **H3 (Neutral)**: Adversatives are conventional markers and carry no distinctive S₂ signal either side

---

## Key Finding: The Pivot Itself Is the Surprise

The data strongly supports **H1**:

| Window | n | mean S₂ | pos% |
|--------|---|---------|------|
| Post-adversative (+1 to +5) | 427 | **−0.418** | 33.0% |
| Pre-adversative (−5 to −1) | 435 | −0.274 | 32.9% |
| Global baseline | 12,190 | **+0.188** | 35.5% |
| **Adversative token itself** | 87 | **+1.987** | — |

**Adversative conjunctions have S₂ 10× higher than the global baseline** (+1.987 vs +0.188). But the tokens following them are *below* baseline (−0.418). **The pivot word carries the surprise, not the reversal it introduces.**

This is a striking literary insight: when Keats writes "But being too happy in thine happiness," the surprise registers on **"but"** — GPT-2 was not expecting the turn — not on what the turn says.

---

## By Conjunction Type

| Category | n | S₂(self) | H(self) | post-window S₂ | lift |
|----------|---|---------|---------|---------------|------|
| Coordinating (but, yet, still) | 61 | +1.485 | 5.93 | −0.589 | **−0.371** |
| Subordinating (though, while, whereas) | 23 | +3.386 | 5.91 | −0.037 | **+0.434** |
| Conjunctive (however, nevertheless) | 3 | +1.453 | 5.08 | −0.575 | −0.658 |

**Subordinating adversatives are twice as surprising as coordinating ones** (S₂ = +3.39 vs +1.49). When a poet inserts "though" or "whereas," that choice is more informationally charged than a simple "but." And crucially, subordinating adversatives show a *positive lift* in post-window S₂ (+0.434), meaning "though" actually does open a surprise-enabling window.

---

## Per-Conjunction Detail

| Word | n | S₂(self) | H(self) | post-1 | post-2 | post-3 |
|------|---|---------|---------|--------|--------|--------|
| "but" | 37 | +1.54 | 5.00 | −0.50 | +0.66 | −0.64 |
| "yet" | 15 | +1.40 | 6.79 | **+0.43** | −1.04 | −0.34 |
| "though" | 11 | **+2.68** | 6.39 | **+1.73** | +0.21 | +0.49 |
| "still" | 9 | +1.40 | **8.31** | −1.34 | −1.50 | −3.21 |
| "while" | 9 | **+3.87** | 5.40 | −1.37 | +1.19 | −0.53 |
| "whereas" | 3 | **+4.52** | 5.65 | +0.10 | −3.69 | −1.18 |

**"Though" is the most productive adversative** for post-turn surprise: S₂(self) = +2.68, and the very next word averages +1.73 — well above baseline. A poet who writes "though" is both making a surprising choice and setting up a genuinely unpredictable continuation.

**"Still" has the highest entropy** (8.31 bits) — GPT-2 is most uncertain about what direction "still" will take. But what follows is deeply predictable (post-window S₂ = −1.34), suggesting "still" is deployed in highly conventional syntactic frames.

---

## Line-Initial vs. Medial Adversatives

| Position | n | S₂(adv) | H(adv) | post-window S₂ |
|----------|---|---------|--------|---------------|
| Line-initial | 81 | +1.64 | 5.98 | −0.49 |
| Medial | 6 | **+6.67** | 4.69 | +0.17 |

**Medial adversatives are 4× more surprising than line-initial ones.** A "but" placed in the middle of a line — rather than at the conventional line start — registers as a radical choice. This matches the classical rhetoric of *antistrophe*: the adversative placed inside the metrical unit creates maximum resistance.

---

## The Most Surprising Post-Adversative Moments

| S₂ | Adv | Word chosen | Expected | P(expected) | Source |
|----|-----|-------------|---------|------------|--------|
| **+12.53** | yet | "turning" | "," | 0.19 | Rossetti |
| **+10.43** | though | "speech" | "they" | 0.23 | Ashbery |
| **+6.11** | but | "barely" | "a" | 0.36 | Scottish ballad |
| **+4.65** | though | "before" | "we" | 0.23 | Claude McKay |
| **+4.49** | yet | "well" | "I" | 0.24 | Shakespeare |
| **+3.91** | yet | "knowing" | "I" | 0.12 | Robert Frost |
| **+2.87** | though | "dead" | "we" | 0.37 | Claude McKay |

**Rossetti's "yet turning" is the single most surprising post-adversative word in the corpus** (S₂ = +12.53). After "yet," GPT-2 expects a comma (19% probability mass) — the conventional syntactic completion; "turning" is an unexpected gerund that opens a new temporal frame.

McKay appears three times in the top examples, suggesting his adversative strategy is distinctive: he uses "though" and "yet" to set up genuinely unexpected continuations.

---

## Era Patterns: Adversative Density

| Era | n poems | adv/poem | post-adv S₂ | baseline S₂ |
|-----|---------|---------|------------|------------|
| Song lyrics | 3 | **1.67** | +0.042 | +0.092 |
| Harlem Renaissance | 4 | **1.50** | +0.339 | +0.436 |
| Romantic | 9 | 1.33 | −0.344 | +0.171 |
| Victorian | 13 | 1.08 | +0.081 | +0.337 |
| Ballad | 6 | 0.67 | +0.879 | +0.814 |
| Modernist | 18 | 0.44 | −0.649 | +0.370 |
| Prose poetry | 9 | 0.33 | −1.492 | −0.156 |

**Song lyrics and Harlem Renaissance poetry use adversatives most densely.** This aligns with the antithetical rhetoric of both traditions: lyric song structure depends on the turn/counter-turn pattern, and Harlem Renaissance poetry (McKay, Hughes) frequently employs irony and reversal for political effect.

**Ballad poetry** has both relatively high adversative density *and* positive post-adversative S₂ (+0.879) — suggesting ballad tradition uses these pivots as genuine surprise-generators.

---

## What Does GPT-2 Expect Instead?

When poets write "but," GPT-2's top predictions were:
1. `[newline]` — 17.3% (GPT-2 expects the line to end)
2. `"but"` itself — 13.8% (once calibrated to poetry, it expects the pivot)
3. `"and"` — 3.9%

When poets write "yet":
1. `[newline]` — 9.5%
2. `"And"` — 4.4%
3. `"."` — 4.0%

When poets write "though":
1. `[newline]` — 11.0%
2. `"if"` — 6.1%  ← GPT-2 expects conditionals, not concessives
3. `"the"` — 2.8%

The "if" expectation after "though" is particularly telling: **GPT-2 conflates subordinating adversatives with conditionals**, treating "though" as if it were "if." Poets who write "though" are not just making an unexpected word choice — they're exploiting a genuine model confusion between concession and condition.

---

## Poet Fingerprints

| Author | adv count | post-adv S₂ | corpus S₂ |
|--------|-----------|------------|----------|
| Traditional (Scottish ballad) | 4 | **+0.879** | +0.756 |
| Claude McKay | 5 | **+0.603** | −0.046 |
| Traditional (American folk) | 5 | +0.042 | −0.738 |
| John Ashbery | 13 | −0.534 | −0.284 |
| Robert Burns | 7 | −1.025 | +0.391 |
| William Shakespeare | 4 | −1.324 | −0.618 |

**Surprise**: Shakespeare and Burns show *negative* post-adversative S₂ (−1.32 and −1.03). Their reversals land on highly predictable language — the "but" surprises, but the reversal itself is conventional. This is the hallmark of virtuosic traditional poetry: the turn is expected *in general* (we know a Shakespearean couplet reverses the octave) but comes at the *right* formal moment.

**McKay**, by contrast, uses adversatives to introduce genuinely unexpected language (+0.60 post-adv S₂), consistently surprising even after establishing the pivot.

---

## Synthesis: A Two-Phase Model of the Adversative Turn

The data supports a **two-phase model**:

1. **Phase 1 — The Pivot Signal** (the adversative token itself): High S₂ (+1.99 average). The poet's choice to turn is itself informationally significant. GPT-2 expects continuation, not reversal.

2. **Phase 2 — The Reversal Content** (what follows): Typically lower S₂ than baseline (−0.42). Having signaled the turn, poets often deploy familiar language to execute it — the vocabulary of reversal is often conventional ("death," "still," "wait," "far," "well").

**The adversative junction spends its informational budget on signaling the turn, then recovers toward predictability in the execution.**

The exception is "though," which maintains elevated S₂ in both phases, suggesting it functions differently: not as a cheap pivot marker, but as a genuine semantic operator that opens unpredictable territory.

---

## Suggested Next Steps

1. **Concessive vs. adversative**: Distinguish pure adversatives ("but I will not") from concessives ("though I will not, I know that..."). Do they produce different S₂ profiles?

2. **Adversative + line break**: When "but" or "yet" falls at a line break (enjambment into a new line), does the combined effect amplify S₂?

3. **Historical drift**: Is the adversative turn becoming less surprising over time as GPT-2's training data skews modern? (The era data hints at this: romantic/Victorian adversatives may be less surprising to GPT-2 than modernist ones.)

4. **Expand corpus**: Add more ballad tradition poems (Child Ballads) and Harlem Renaissance texts to test the adversative-density/surprise connection more rigorously.
