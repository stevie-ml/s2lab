# Grammatical Person and S₂: Does Lyric Address Surprise GPT-2?

**Date:** 2026-09-10  
**Experiment:** `experiments/grammatical_person.py`  
**Corpus:** 106 English-language texts from `results/corpus_results.json`  
**Research question:** Does the grammatical person of a poem (1st/2nd/3rd) predict its S₂ profile? And does GPT-2 — trained primarily on 3rd-person prose — find lyric "I" and apostrophic "you" systematically surprising?

---

## Background

Poetry has a distinctive relationship with grammatical person:

- **1st-person lyric** ("I") is the backbone of the Western lyric tradition, from Sappho to confessional poetry.
- **2nd-person address** ("you", "thee") — apostrophe — is a high-rhetoric poetic device, addressing absent, dead, or inanimate entities as if present.
- **3rd-person narration** dominates prose and is less "marked" as poetic.

GPT-2 is trained heavily on Reddit, Wikipedia, and web corpora — all predominantly 3rd-person or impersonal. If the model's prior is calibrated on 3rd-person prose, it should find 1st- and 2nd-person continuations more surprising, producing higher S₂ in poems that foreground the "I" or "you."

---

## Method

1. Classify each English poem by its **dominant grammatical person** using token-level pronoun counting:
   - 1st person: `I, me, my, mine, we, us, our` (and archaic forms)
   - 2nd person: `you, your, thee, thy, thou`
   - 3rd person: `he, him, she, her, they, them, it`
   - Impersonal: no dominant pronoun class

2. Compute avg S₂ at the poem level by person category.

3. At the **token level**, extract S₂ values specifically for pronoun tokens.

4. Detect **person-switch moments** — positions where the poem transitions from one person to another — and measure S₂ at those transitions.

---

## Findings

### 1. Poem-Level S₂ by Dominant Grammatical Person

| Person | n poems | avg S₂ | std S₂ | pos% |
|---|---|---|---|---|
| **1st-person** (I/we) | 41 | **+0.473** | 5.350 | 38.3% |
| **3rd-person** (he/she/they) | 41 | +0.143 | 4.936 | 37.1% |
| **2nd-person** (you/thee) | 7 | +0.011 | 5.073 | 31.4% |
| **Impersonal** | 9 | −0.025 | 4.849 | 31.4% |

**1st-person poems have the highest avg S₂ (+0.473)**, more than 3× the 3rd-person average (+0.143). Impersonal poems sit near zero — the boundary between poetry and prose.

Counterintuitively, 2nd-person poems (the apostrophe tradition) have *lower* S₂ than 1st-person (n=7, so tentative). This may reflect that apostrophic poems tend toward heightened formal diction (Burns, Hardy), which can be structurally predictable in its patterning even when semantically unusual.

### 2. Token-Level S₂ for Pronoun Tokens

| Person | n tokens | avg S₂ | median S₂ | pos% |
|---|---|---|---|---|
| 1st (I/me/my) | 292 | −0.240 | −2.327 | 26.0% |
| 2nd (you/thee/thy) | 102 | −0.846 | −2.354 | 20.6% |
| 3rd (he/she/they) | 220 | −0.558 | −1.585 | 26.4% |

**Surprise finding:** At the token level, pronouns themselves are **low-S₂** — below-average surprise. When a poem uses "I" or "you," these tokens are *less* surprising than the poem's overall mean. This seems paradoxical until you look at the high-S₂ pronoun examples (below).

### 3. The Line-Start Pronoun Effect

At positions where pronouns achieve high S₂ (> +20), the pattern is consistent:

| S₂ | Token | GPT-2 predicted | P(pred) | Context |
|---|---|---|---|---|
| +31.92 | `Our` | `\n` | 99.97% | `…coomb↵` |
| +28.92 | `My` | `\n` | 99.97% | `…ground:↵` |
| +26.87 | `My` | `\n` | 99.96% | `…weight,↵` |
| +25.30 | `My` | `\n` | 99.94% | `…ade,↵` |
| +25.11 | `Your` | `\n` | 99.95% | `…to me↵` |

**The pattern:** GPT-2, having just processed a line break (`\n`), predicts another line break (blank line = poem ending) with 99.9%+ probability. The poet instead begins a new line with a first- or second-person pronoun. The "surprise" is not about the pronoun per se but about the poet's decision to *continue* the poem, starting the next line with lyric address rather than ending.

This is an artifact of GPT-2's training distribution (prose passages end; stanzas continue), but it reveals something real: **continuing to speak — especially in the first person — is informationally marked**.

### 4. Person-Switch Moments

| | n tokens | avg S₂ |
|---|---|---|
| Switch pronoun tokens | 212 | −0.735 |
| Non-switch pronoun tokens | 402 | −0.306 |
| **Difference** | | **−0.428** |

Person switches on average have *lower* S₂ than non-switch pronouns. However, individual high-S₂ switches are striking:

| From → To | S₂ | Context | Author |
|---|---|---|---|
| 1st → 3rd | +32.18 | `give me↵they were` | William Carlos Williams |
| 1st → 2nd | +25.11 | `to me↵Your face` | Thomas Hardy |
| 3rd → 1st | +20.33 | `it.↵I heard` | Langston Hughes |
| 1st → 3rd | +17.65 | `creatures where↵They dw` | Thomas Hardy |
| 1st → 3rd | +17.21 | `Death –↵He kindly` | Emily Dickinson |
| 2nd → 1st | +11.23 | `id,↵My de` | Traditional (Scottish ballad) |

Dickinson's `Because I could not stop for Death — / He kindly stopped for me` is the standout: the poem shifts from 1st-person speaker to 3rd-person Death (personified), a S₂ = +17.21 moment that enacts the grammatical estrangement of dying — "I" yielding to "He."

Williams's `give me / they were` in "This Is Just to Say" (S₂ = +32.18) switches from a direct-address "give me" to a subordinate-clause "they were" — another of this poem's repeatedly high-S₂ line-start moments.

### 5. Grammatical Person by Era

| Era | n | %1st | %2nd | %3rd | Dominant |
|---|---|---|---|---|---|
| confessional | 3 | 100% | 0% | 0% | 1st |
| beat | 2 | 100% | 0% | 0% | 1st |
| romantic | 7 | 71% | 14% | 14% | 1st |
| contemporary | 7 | 71% | 14% | 14% | 1st |
| harlem_renaissance | 4 | 50% | 0% | 50% | 1st |
| 19th_century | 9 | 56% | 0% | 44% | 1st |
| victorian | 9 | 44% | 0% | 56% | 3rd |
| modernist | 18 | 33% | 11% | 44% | 3rd |
| new_york_school | 18 | 28% | 11% | 61% | 3rd |
| ballad | 6 | 33% | 0% | 67% | 3rd |
| language | 3 | 0% | 0% | 67% | 3rd |
| control | 4 | 0% | 0% | 25% | impersonal |

The Romantic and confessional eras are dominantly 1st-person. Modernist and New York School poetry — known for deflecting lyric "I" — skew 3rd-person. The Language poetry poets show 0% 1st-person in this sample, consistent with their anti-lyric poetics.

---

## Interpretation

**Finding 1:** 1st-person poems have the highest average S₂ (+0.473), supporting the hypothesis that lyric "I" correlates with more informationally marked choices — though this is partly confounded with era (confessional, romantic poetry is both 1st-person and stylistically distinctive).

**Finding 2:** The bulk of high-S₂ pronoun moments occur at line starts, where GPT-2 strongly predicts poem termination (blank line) and the poet instead begins a new line with "I", "My", or "You." The S₂ spike measures the poet's decision to *continue speaking*, not the pronoun itself.

**Finding 3:** Person-switch moments are on average *less* surprising than stable-person pronoun use, but individual switches can be highly marked. Dickinson's person-switch at "Death — / He kindly" is among the most formally significant in the corpus.

**Finding 4:** The 2nd-person surprise is structural: "you" tokens have the *lowest* avg S₂ (-0.846) at the token level. When a poem has established a pattern of direct address, further "you" tokens are predictable. The S₂ for apostrophe accrues in the *initial establishment* of the address mode.

---

## Suggested Next Steps

1. **Isolate the line-start effect**: Separately compute S₂ for mid-line vs. line-start pronouns to disentangle the "decision to continue" signal from the person effect per se.

2. **Person purity vs. fluidity**: Do poems that maintain a single grammatical person throughout have lower S₂ than poems that shift freely? Measure standard deviation of person assignment across a poem.

3. **Address vs. narrative**: Categorize 2nd-person instances as true apostrophe (addressing absent/inanimate things) vs. conversational (addressing a present interlocutor). Do they differ in S₂?

4. **Anti-lyric poets**: Compare Language poetry (0% 1st-person) directly against confessional poetry (100% 1st-person). Both have moderate S₂ — but for different reasons? Language poems may have high S₂ through semantic disruption; confessional poems through emotional intensity and non-normative syntax.
