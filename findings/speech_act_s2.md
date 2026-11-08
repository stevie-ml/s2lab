# Speech Act S2: Performative vs. Constative Verbs in Poetry

**Date:** 2026-11-08  
**Experiment:** `experiments/speech_act_s2.py`  
**Data:** `findings/speech_act_s2.json` (411 poems, ~49,000 tokens)

---

## Research Question

Do performative speech act verbs — Austin's illocutionaries — carry higher S2
than constative verbs in poetry? When a poet writes "swear", "bless", "curse",
or "proclaim", is GPT-2 more surprised than when they write "see", "feel", or
"think"?

**Hypothesis**: Performative verbs enact reality rather than describe it. In
Austin's terms, to say "I swear" is to swear; to say "I curse thee" is to curse.
These are moments of maximum linguistic commitment. GPT-2, trained on descriptive
prose, doesn't anticipate performatives where it expects ordinary descriptors.

---

## Austin's Speech Act Taxonomy

| Category | Definition | Examples |
|----------|------------|---------|
| **Commissive** | Speaker commits to future action | swear, vow, promise, pledge |
| **Expressive** | Expresses sincere psychological state | bless, curse, celebrate, welcome, abhor |
| **Declaration** | Changes institutional reality | declare, proclaim, crown, name |
| **Directive** | Attempts to get hearer to act | implore, beseech, summon, bid, command |
| **Constative: mental** | Describes internal states (control) | see, feel, know, think, believe |
| **Constative: action** | Describes physical actions (control) | walk, stand, rise, move, hold |

---

## Results

### S2 Summary Table

| Category | N | Mean S2 | Median S2 | Pos% | Max S2 |
|----------|---|---------|-----------|------|--------|
| Commissive (vow/promise) | 8 | **+1.483** | +1.694 | 75.0% | 5.41 |
| Expressive (bless/curse) | 38 | **+2.207** | +2.274 | 65.8% | 12.08 |
| Declaration (proclaim) | 31 | **-0.221** | -0.672 | 38.7% | 9.94 |
| Directive (implore/bid) | 44 | **+2.216** | +2.609 | 70.5% | 10.70 |
| Constative: mental | 291 | **-0.543** | -0.982 | 38.1% | 11.68 |
| Constative: action | 625 | **+0.551** | -0.167 | 48.5% | 13.08 |

---

## Key Findings

### 1. Expressives and Directives Are the Biggest Straussian Gaps

**Expressive** and **directive** verbs both average +2.2 S2, dramatically above
all other categories. This is the core finding: when poets bless, curse,
implore, or command — when they DO something with language — GPT-2 is most
surprised.

The practical implication: the highest-S2 moments in poetry often coincide with
the moments of greatest affective stakes. Poetry does not merely describe
emotion; it *performs* it.

### 2. Mental Constatives Are the Most Predictable Verbs

Mental constative verbs ("see", "feel", "know", "think", "believe") average
**-0.543** S2 — the lowest category, more predictable even than action verbs.
These are the workhorse verbs of lyric subjectivity, and GPT-2 knows them
perfectly well. The model is well-calibrated to expect "I see", "I feel",
"I think" in poetic positions.

**Implication**: When poets rely on mental state verbs, they are speaking
in language that the model already anticipates — the "said" that suppresses
no "unsaid."

### 3. Declarations Are Surprisingly Low — The "Formal Slot" Effect

Declarations ("declare", "proclaim", "name") average **-0.221** S2 despite
being performative. Why?

These verbs tend to appear in highly predictable syntactic positions:
- "The heavens **declare** the glory of God" (Psalm 19) — GPT-2 expects something
  after "heavens" and "declare" fits a known grammatical slot
- "I do hereby **declare**..." — formal/legal collocations are well-represented
  in GPT-2's training data

This reveals a *syntactic constraint*: declarations are performatives that have
been syntactically conventionalized. They appear in formulaic frames that GPT-2
recognizes.

### 4. Best Individual Examples

**Highest expressive S2:**
- `'abhor'` (S2=**12.08**) — Robert Browning, *Soliloquy of the Spanish Cloister*  
  GPT-2 expected: "going" / "broken" / "in"  
  *Analysis*: Browning's obsessive speaker uses a Latinate dysphemism where
  the model expected continuation of description. The abrupt expressive pivot
  registers as maximum surprise.

- `'celebrate'` (S2=**9.99**) — Lucille Clifton, *Won't You Celebrate With Me*  
  Context: "...hand; come **celebrate**"  
  GPT-2 expected: "," / "to" / "on"  
  *Analysis*: After "come", the model expects a preposition or comma; instead
  Clifton issues a direct exhortation to joy.

- `'welcome'` (S2=**8.03**) — Emma Lazarus, *The New Colossus*  
  GPT-2 expected: "," / "the" / "."  
  *Analysis*: The Statue's famous declarative welcome — "I lift my lamp beside
  the golden door" — is performed in a verb slot where GPT-2 expected punctuation
  or grammatical completion.

**Highest directive S2:**
- `'commands'` (S2=**10.70**) — Robert Browning, *My Last Duchess*  
  Context: "...I gave **commands**"  
  GPT-2 expected: "" / "her" / "it"  
  *Analysis*: Browning's most chilling line. After "I gave", the model expects
  a direct object ("her", "it") — Browning's choice of the noun "commands" (here
  functioning as direct object) creates maximum S2.

- `'call'` (S2=**9.85**) — Christina Rossetti, *Goblin Market*  
  Context: ...'Come buy,' **call**  
  GPT-2 expected: "Laura" / "said" / "she"  
  *Analysis*: After the goblins' cry, the model expects a speaker name;
  Rossetti repeats the performative verb itself.

---

## What GPT-2 Suppresses at Performative Positions

Top tokens GPT-2 expected when poets wrote performative verbs:

| Rank | GPT-2 Expected | Count |
|------|---------------|-------|
| 1 | "the" | 21 |
| 2 | "," | 19 |
| 3 | "" (line boundary) | 11 |
| 4 | "name" | 10 |
| 5 | "a" | 9 |
| 6 | "are" | 9 |
| 7 | "be" | 8 |
| 8 | "have" | 7 |
| 9 | "not" | 6 |
| 10 | "is" | 6 |
| 11 | "see" | 6 |
| 12 | "word" | 6 |

**Core pattern**: GPT-2 overwhelmingly expects **grammatical tokens** (the, a,
be, is, are) at positions where poets write performative verbs. The model fills
these slots with structural glue; poets fill them with world-making action.

Notably, "see" (rank 11) is itself a constative verb — GPT-2 substitutes the
*most predictable* lyric verb at positions where poets use the *most committed*
illocutionary verbs.

---

## Theoretical Synthesis

This experiment provides information-theoretic evidence for a claim that
speech act theory implies but hasn't measured: **performative language in
poetry creates genuine Straussian gaps**.

The data supports a hierarchy of illocutionary force vs. predictability:

```
        HIGH S2 (unpredictable)
        ↑
        Expressive / Directive (+2.2)
        Commissive (+1.5)
        Constative: action (+0.6)
        Declaration (-0.2)    ← conventionalized
        Constative: mental (-0.5)
        ↓
        LOW S2 (predictable)
```

The key insight: **the more a verb enacts an emotional or interpersonal reality
(rather than describing it), the more it surprises GPT-2**. The exception —
declarations — reveals that when performatives become formulaic (legal, liturgical,
institutional), they lose their gap-generating power.

---

## Limitations

- Sample sizes for commissives (n=8) and expressives (n=38) are small; the
  corpus may underrepresent these verb forms
- Crude lemmatization (stripping trailing "s") may misclassify some tokens
- First-person constraint analysis was data-limited; most performatives in
  the corpus appear without an explicit "I" subject

---

## Suggested Next Steps

1. **Expand the lexicon**: Include inflected forms ("swears", "blessed", "cursing",
   "proclaimed") to increase sample size
2. **Performative context**: Compare bare performatives vs. 1st-person performatives
   ("I swear" vs. a character "swearing") — are canonical speech acts more
   surprising than reported ones?
3. **Embedding distance**: Does the semantic distance between a performative verb
   and its following object correlate with S2?
4. **Lyric vs. dramatic**: Do performatives in dramatic monologues (Browning) differ
   systematically from those in lyric poems (Clifton)?
5. **Historical arc**: Did poets use more performative language before or after
   the Romantic shift to interiority? (Early modern "I curse thee" vs. Romantic
   "I feel the dark...")
