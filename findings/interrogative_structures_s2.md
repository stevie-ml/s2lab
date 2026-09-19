# Interrogative Structures in Poetry: The S₂ Profile of Questions

**Date:** 2026-09-19  
**Experiment:** `experiments/interrogative_structures_s2.py`  
**Corpus:** 129 English poems (excluding control prose and German texts)

---

## Research Question

When poets ask questions — from genuine inquiry to rhetorical assertion to existential suspension — how does the information-theoretic profile change? Five hypotheses were tested against the precomputed GPT-2 token data.

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Poems with ≥1 question | 27 / 129 (21%) |
| Total question sentences | 63 |
| Wh-questions found | 33 |
| Non-question wh-words (relative clauses etc.) | 146 |
| Avg S₂ in question sentences | +0.379 |
| Avg S₂ in non-question sentences | +0.201 |
| **S₂ lift from questions** | **+0.178** |

---

## Findings by Hypothesis

### H1 — REJECTED (with twist): Wh-word entropy in vs. out of questions

Counter-intuitively, wh-words in question context have *lower* entropy than in non-question contexts:

| Context | Avg Entropy | Avg S₂ |
|---------|-------------|--------|
| Wh-word in question | 5.479 | **+4.132** |
| Wh-word in relative clause | 5.773 | +2.464 |

The model is slightly more certain about what follows a wh-word in a question than in a relative clause — but the *poet's choice* is far more surprising (S₂ = +4.1 vs +2.5). This suggests poetic questions exploit the model's genre-learned certainty: GPT-2 knows what a "question word" means but doesn't predict what extraordinary thing the poet will actually ask about.

### H2 — WEAKLY SUPPORTED: The token after a wh-word

The token immediately after a question word is slightly more surprising in questions (S₂ = -0.527) vs non-question wh-words (-0.453), but the effect is small. The drama is concentrated in the question word itself, not what follows it.

**S₂ by question word type (in question context):**

| Word | Avg S₂ | n |
|------|--------|---|
| where | +6.70 | 4 |
| what | +4.59 | 17 |
| why | +3.39 | 6 |
| who | +3.21 | 4 |

"Where" and "what" are the highest-S₂ question words. "Where" questions in particular seem to deploy the word in genuinely unexpected contexts — the high std (15.7) shows extreme variance, suggesting a few "where" questions are extraordinarily deviant.

### H3 — PARTIALLY CONFIRMED: Positional distribution

Questions concentrate in the opening and middle of poems, not at the end:

| Position | Count | % | Avg S₂ |
|----------|-------|---|--------|
| Opening (first quarter) | 26 | 42% | +0.241 |
| Middle (middle half) | 26 | 42% | +0.782 |
| Closing (final quarter) | 9 | 14% | -0.163 |

Mid-poem questions have by far the highest S₂ (+0.782), while closing questions have *negative* S₂ (-0.163). This is a striking pattern: **mid-poem questions are informationally bold; closing questions are informationally tame.** This may reflect the rhetorical function — closing questions in classical poetry (think final couplets) follow well-worn formulas, while mid-poem questions interrupt and surprise.

### H4 — CONFIRMED: The "?" token itself

The question mark token has very low S₂ (-1.125), meaning it is more predictable than average, but moderate entropy (4.590). Once you're in a question sentence, GPT-2 expects the "?" to come — it's the *form* that's anticipated. Poets exploit the sentence-internal space for surprise, then land on the expected punctuation.

| Token | Avg S₂ | Avg Entropy | Avg Surprisal |
|-------|--------|-------------|--------------|
| "?" | -1.125 | 4.590 | 3.465 |

### H5 — CONFIRMED: Questions lift overall S₂

Poem-internal question sentences have 88% higher avg S₂ than non-question sentences (+0.379 vs +0.201). Questions generate information-theoretic surprise.

---

## Era Analysis: Who Asks Questions?

| Era | Q-density (/100 tokens) | S₂ lift in questions | n |
|-----|--------------------------|---------------------|---|
| romantic | 6.60 | n/a | 1 |
| harlem_renaissance | 5.41 | +1.668 | 3 |
| prose_poetry | 4.05 | -0.523 | 1 |
| spoken_word | 2.20 | +1.010 | 1 |
| contemporary | 1.90 | +0.392 | 2 |
| new_york_school | 1.57 | +1.375 | 5 |
| ballad | 1.52 | +0.019 | 3 |
| metaphysical | 1.09 | +0.196 | 2 |
| victorian | 0.81 | -0.070 | 5 |
| modernist | 0.43 | +0.709 | 1 |

**Harlem Renaissance poetry** stands out: highest question density (5.41/100 tokens) AND the strongest S₂ lift from questions (+1.668). Langston Hughes is a key driver. The rhetorical question as a form of accusatory power is informationally visible in the data.

**New York School** also shows high question density with a strong S₂ lift (+1.375). Ashbery's questions deliberately avoid coherence; they open semantic space without answering it.

---

## Most Surprising Questions in the Corpus

| Rank | Author | Text (excerpt) | S₂ |
|------|--------|-----------------|-----|
| 1 | Langston Hughes | "Or fester like a sore— / And then run?" | +3.727 |
| 2 | William Blake | "On what wings dare he aspire?" | +3.239 |
| 3 | G.M. Hopkins | "Why do men then now not reck his rod?" | +3.095 |
| 4 | Langston Hughes | "Or crust and sugar over— / like a syrupy sweet?" | +2.878 |
| 5 | Langston Hughes | "Does it stink like rotten meat?" | +2.522 |

Hughes's "Harlem" / "A Dream Deferred" dominates the top of this list. The poem is *structurally* a series of questions — each more viscerally unexpected than the last. The model cannot predict "fester like a sore" or "syrupy sweet" in the context of dreaming; the S₂ values confirm that the poem achieves sustained rhetorical escalation through a chain of high-surprise questions.

## Most Expected (Low-S₂) Questions

| Rank | Author | Text (excerpt) | S₂ |
|------|--------|-----------------|-----|
| 1 | John Ashbery | "And what about / The parents?" | -2.279 |
| 2 | Shakespeare | "Shall I compare thee to a summer's day?" | -1.975 |
| 3 | Mary Oliver | "Who made the grasshopper?" | -1.774 |
| 4 | Baudelaire | "—Your country?" | -1.684 |

Shakespeare's most famous question has negative S₂ — GPT-2 finds "compare thee to a summer's day" statistically expected given the opening. The sonnet tradition has so thoroughly saturated language that the model anticipates it. This could be read as: **canonical poetry becomes informationally invisible; its surprise has been absorbed into the model's prior.**

---

## Core Finding

**Questions in poetry are informationally bold — but selectively.** The S₂ lift from questions (+0.178) confirms they are devices for generating linguistic surprise. The wh-question word itself carries the surprise (S₂ = +4.1 in question context vs +2.5 in relative clauses), while what follows the question word is comparatively expected. Mid-poem questions are the most surprising (S₂ = +0.782); closing questions are the least (S₂ = -0.163), supporting the intuition that final rhetorical questions are formulaic closures while mid-poem questions are genuine disruptions.

The Harlem Renaissance anomaly is striking: questions are both more frequent and more surprising there than in any other era, consistent with the tradition's use of the rhetorical question as a form of accusatory power — a linguistic mode that makes the reader feel the force of the unanswered.

---

## Suggested Next Steps

1. **Anaphoric questions in Hughes**: Model the full S₂ trajectory of "Harlem" — does S₂ escalate with each sequential question?
2. **"The rhetorical question trap"**: Identify closing questions that have negative S₂ (the formula problem) and examine whether they use different vocabulary than opening questions.
3. **Question chains vs isolated questions**: Are poems that ask multiple consecutive questions more or less surprising than poems with a single central question?
4. **Expand to German corpus**: Does the German tradition show the same mid-poem peak? Rilke's *Duino Elegies* are driven by questions ("Wer, wenn ich schriee...").
5. **Apostrophe and vocative as question-adjacent devices**: The "O" apostrophe (Blake's "O Tyger!") may show similar S₂ profiles to question words — both open a semantic void.
