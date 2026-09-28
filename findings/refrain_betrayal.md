# Refrain Betrayal: What Happens When a Poet Breaks an Established Copy

**Date:** 2026-09-26
**Experiment:** `experiments/refrain_betrayal.py` → `results/refrain_betrayal.json`
**Corpus:** 184 texts (176 after excluding prose and cliché controls), 18,869 artifact-free tokens
**Corpus changes this run:** 4 new public-domain poems with *varied* refrains (Tennyson: *Tears, Idle Tears*, *Break, Break, Break*, *The Lady of Shalott* Part I; Kipling: *Recessional* st. 1–3). *The Tyger* extended to the full poem, and *The Raven* extended to stanza 8, so both now reach their refrain returns.
**Builds on:** `second_occurrence_dip.md`, `spectral_refrain_null.md`, `repetition_and_entropy.md`, `confidence_trap_analysis.md`

---

## Question

Earlier work showed that repetition makes GPT-2 habituate: second occurrences lose ~2.3 bits of S₂ (`second_occurrence_dip.md`). Refrains show up as impulses, with no periodicity (`spectral_refrain_null.md`). Neither study looked at the moment a poet **starts to repeat and then departs**.

Once a phrase is repeating, a transformer's in-context copying makes it predict the rest of the earlier occurrence with high confidence. A departure at that point should be a confidence trap that the form sets up on purpose: the refrain teaches the model what comes next, and the poet then breaks that expectation.

## Method

For every token *tᵢ*, find the longest suffix of the preceding context (length **L**) that already occurred earlier in the same poem. The token that followed that earlier occurrence is the **copy target**.

- **Honored:** the poet writes the copy target.
- **Betrayed:** the poet writes something else.

Tokens with p(newline) ≥ 0.9 are excluded (the stanza-break artifact). Main analyses use L ≥ 3.

---

## Finding 1: GPT-2 locks onto a refrain after about 4 tokens

| Matched prefix L | n | poet honors copy | model's top-1 = copy | mean entropy | S₂ if honored | S₂ if betrayed |
|---|---|---|---|---|---|---|
| 1 | 4,391 | 15.4% | 25.1% | 6.76 | −2.61 | −0.14 |
| 2 | 1,175 | 25.8% | 42.9% | 6.31 | −2.40 | +0.25 |
| 3 | 435 | 40.5% | 59.5% | 5.28 | −2.08 | +0.37 |
| 4–5 | 310 | 62.3% | 72.3% | 3.98 | −1.74 | +0.87 |
| 6–9 | 227 | 81.5% | 90.3% | 2.42 | −1.44 | +2.64 |
| 10+ | 265 | 89.1% | **96.2%** | **1.61** | −1.08 | **+4.15** |

The lock-in curve is steep and monotonic. By a 10-token match, GPT-2 puts its top guess on the copy 96% of the time, and entropy falls to 1.6 bits (corpus average ≈ 6.3). The cost of betraying the copy rises in step: from −0.14 at L = 1 to +4.15 at L ≥ 10.

The model is also slightly *more* sure of the copy than the poets are faithful to it (96% vs 89% at L ≥ 10). Poets leave themselves room to depart.

## Finding 2: Betrayal is one of the most reliable ways to get positive S₂

| Group (L ≥ 3) | n | mean S₂ | median S₂ | +S₂ rate |
|---|---|---|---|---|
| honored | 790 | −1.55 | −1.06 | **1.3%** |
| betrayed (all) | 447 | +0.96 | +0.22 | 51.2% |
| betrayed while model's top-1 was the copy | 198 | **+2.45** | +1.86 | **63.6%** |
| baseline (all clean tokens) | 18,869 | −0.40 | −1.17 | 34.5% |

An honored copy is almost never positively surprising (1.3%). A betrayed copy, in a context where GPT-2 was actually copying, is positive nearly two times in three. That is 2.85 bits above the baseline mean.

## Finding 3: Extensions are the dramatic case, not substitutions

Betrayals split by what the model expected and what the poet wrote. Whitespace/layout cases (25, almost all from Cummings' *Buffalo Bill 's*) are excluded because they are layout artifacts like the stanza-break one.

| Type | Expected → written | n | mean S₂ | mean S₂ (model copying) | in corpus top-100 | top-100 lift |
|---|---|---|---|---|---|---|
| **extension** | punct/⏎ → word | 14 | **+6.44** | **+9.75** | **4** | **54×** |
| substitution | word → word | 353 | +0.76 | +1.86 | 3 | 2× |
| truncation | word → punct/⏎ | 20 | +0.71 | +1.82 | 0 | — |
| repunctuation | punct → punct | 35 | +0.13 | +1.41 | 0 | — |

**Extension:** the refrain line is expected to end where it ended before, and the poet keeps going. It is rare (14 cases in 184 texts), but 4 of the 14 are among the corpus's 100 highest-S₂ tokens.

| S₂ | Context (⏎ = newline) | model expected | poet wrote | Poet |
|---|---|---|---|---|
| 15.80 | `And fare thee weel` | `,` (0.94) | **awhile** | Burns, *A Red, Red Rose* |
| 15.07 | `Susie Asado` | `.` (0.91) | **which** | Stein, *Susie Asado* |
| 14.31 | `I've known rivers` | `:` (0.52) | **ancient** | Hughes, *The Negro Speaks of Rivers* |
| 10.24 | `Tyger Tyger` | `,` (0.82) | **burning** | Blake, *The Tyger* |

Hughes' "I've known rivers: / I've known rivers **ancient** as the world" is a textbook example. The model has learned from the first line that the phrase ends with a colon, and Hughes turns the fragment into a longer clause.

**Substitution** (swapping a word inside a known frame) raises S₂ reliably but modestly. At +1.86 it clears the baseline, but only 3 cases reach the top-100. Word-for-word variation, such as Tennyson's "So sad, so *fresh*" → "So sad, so *strange*", scores −2.15. When the refrain frame is broken by a word, the model's uncertainty spreads across plausible alternatives, so the substitute is often one it already ranked highly.

## Finding 4: GPT-2 recovers immediately after a substitution

| Token after a betrayal | n | mean S₂ | model's top-1 was the resumption |
|---|---|---|---|
| poet resumes the earlier line | 51 | **−2.47** | **86%** |
| poet keeps diverging | 372 | −0.88 | 5% |

When a poet swaps one word and then returns to the refrain, GPT-2 usually predicts the return (86%). The copy survives a one-token perturbation, which matches known induction-head behavior. So a departure costs surprise only at the point of departure, not afterwards.

**The exception is instructive: Blake's "Could → Dare".**

```
What immortal hand or eye,⏎      p(⏎)=0.95
D·are                            S₂ = 18.45  (p(⏎)=0.999 → artifact-filtered; runner-up alt: "Could")
 frame                           S₂ = 14.78  (model expected " thy" 0.94)
 thy fearful symmetry?           S₂ ≈ 0
```

The substitution itself sits on a position where GPT-2 wrongly expected a blank line, so the artifact filter removes it. The resumption ("frame") is where the surprise lands. After "Dare", GPT-2 puts 0.94 on " thy". That matches neither the stanza-1 continuation (" frame") nor the stanza-4 one ("Dare *its*"). The model has dropped both copies and parses "Dare" as a fresh transitive verb ("Dare thy…"). "Dare" is a verb that takes a direct object, whereas "Could" is a modal that needs a verb, so Blake's one-word revision changes the grammar of the line. That breaks the copy in a way a word of the same class (like Tennyson's "fresh" → "strange") does not. This is a single case, but it suggests a testable rule: **a substitution that changes the grammatical category of the word breaks the refrain copy, while one within the same category does not.**

---

## Limitations

1. **Betrayals at the start of a refrain are invisible to this method.** Kipling's "*Judge of the Nations*, spare us yet" (for "*Lord God of Hosts*, be with us yet") and Tennyson's "*At the foot of thy crags*, O Sea!" depart at the refrain's first word. Nothing before them sets up a copy, so they are not detected. The method only measures departures in the *middle* of a refrain.
2. **The artifact filter hides some real betrayals.** Line-initial substitutions sit exactly where GPT-2 misplaces newline mass ("Dare" above). A renormalized S₂ (surprise conditional on "not a newline") would recover them, but `engine.py` stores only the top-10 alternatives, so this can't be computed from the current results file.
3. **Small n for extension** (14). The 54× lift is robust in direction but not in size.
4. Folk/oral texts (*Oh Shenandoah*, *Lord Randal*, *Frankie and Johnny*) dominate the event counts because they have the most repetition. Ballad-heavy results may reflect oral-formulaic variation rather than a written poet's deliberate choice.

## Hypothesis

> **Refrains are how a poem teaches its own reader what to expect, and a refrain that changes is how the poem cashes that in.** Repetition drives GPT-2's in-context confidence to ~96% within about ten tokens. The poem gets its largest surprises not from new words but from **extending a line the reader thinks is finished**. That move is roughly 50× over-represented among the corpus's extreme S₂ tokens. Swapping a word inside the frame is surprising but cheap, and the model recovers from it at once.

This refines `second_occurrence_dip.md`. Repetition lowers S₂ (habituation), but it also sets up the strongest confidence traps in the corpus. The repetition sets up the surprise, and a poet cashes it in by extending a line the model thinks is finished.

## Suggested next steps

1. **Store `p_nonnewline`-renormalized surprisal in `engine.py`** (surprisal of the actual token given "not a newline"). This would remove the stanza-break artifact without discarding positions, and would recover line-initial betrayals like "Dare".
2. **Detect refrain-head substitutions** by aligning *lines* (edit distance over token sequences) instead of prefix matching, so "Judge of the Nations" is scored against "Lord God of Hosts".
3. **Cross-model check:** GPT-2 medium/large have stronger induction heads. Does the lock-in curve steepen, and does the cost of extension grow?
4. **Test the part-of-speech rule from the "Dare" case:** among word → word substitutions, compare re-entry S₂ when the substitute has the same vs a different POS than the copy target.
5. **Complete the truncated villanelles** (Robinson, Henley, Dowson, Wilde are all excerpts). The final quatrain, where both refrains combine, is the case this method measures best.
