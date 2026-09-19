# Apostrophe and S₂: The Frame Effect of Direct Address

**Date:** 2026-09-19  
**Experiment:** `experiments/apostrophe_s2.py`  
**New poems added:** 5 (Ode to the West Wind, The Sick Rose, To Autumn, To a Skylark, O Captain! My Captain!)  
**Corpus:** 146 texts (5 up from previous run)

---

## Research Question

Apostrophe — the rhetorical figure of directly addressing an absent person, a dead person, or a personified abstraction ("O Death", "O wild West Wind", "O Rose thou art sick") — is one of poetry's oldest devices. When a poet turns from the world to address the ineffable, how does the information-theoretic profile change?

We tested three tiers of apostrophic signal:
- **T1 (STRONG):** Vocative "O" / "Oh" / "Hail" / "Hark"
- **T2 (MEDIUM):** Archaic 2nd-person pronouns: thou, thee, thy, thine
- **T3 (WEAK):** Modern direct address "you/your"

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Apostrophic poems (T1 or T2 present) | 38 / 146 (26%) |
| Non-apostrophic poems | 108 / 146 |
| T1 vocative markers found | 55 |
| T2 archaic pronoun tokens found | 52 |
| Avg S₂ of vocative "O"/"Oh" | **+2.502** |
| Avg S₂ of token immediately after "O" | **-0.920** |
| Avg S₂ of archaic thou/thee/thy | **-0.929** |
| Avg S₂ of modern "you/your" | -0.647 |
| Avg S₂ of baseline pronouns (I/he/she) | -0.590 |
| S₂ lift for apostrophic vs. non-apostrophic poems | -0.009 |

---

## Hypotheses — Results

### H1 ✓ SUPPORTED: The vocative "O"/"Oh" is high-S₂

The vocative marker itself is dramatically surprising to GPT-2:

| Marker | n | Avg S₂ |
|--------|---|--------|
| oh | 10 | **+4.037** |
| o (vocative) | 45 | **+2.161** |

"Oh" is more surprising than "O" — probably because lowercase "o" appears in many non-vocative contexts (letter "O", parts of tokens), while "oh" is more distinctively an interjection. Both dwarf the corpus average S₂ of ~0.2.

At the 55 vocative positions, GPT-2 expected:
- Other content word: 53%
- Punctuation (comma, period): 27%
- Function word: 20%

GPT-2 did not predict apostrophe at any of these moments — it was expecting the poem to continue with content or to pause, never to pivot into direct address.

### H2 ✗ NOT SUPPORTED (Revealing Inversion): Post-vocative token

The token IMMEDIATELY AFTER "O" has avg S₂ = **-0.920** — well below the poem average.

**This is the frame effect.** The vocative "O" pays the information-theoretic cost upfront, establishing an apostrophic frame that makes what follows more predictable, not less.

However, the outliers are spectacular:

| Phrase | S₂ | Poem |
|--------|-----|------|
| "O **haste**" | +8.40 | *Barbara Allen* (Traditional ballad) |
| "O **snail**" | +7.78 | Kobayashi Issa, *Three Haiku* |
| "Oh **Mr**" | +6.39 | *Frankie and Johnny* |
| "O **stolz**" | +5.11 | Georg Trakl, *Grodek* |
| "O **kins**men" | +4.83 | Claude McKay, *If We Must Die* |
| "O **heart**" | +4.16 | Whitman, *O Captain!* |

These high-S₂ post-vocative cases are poems that address something genuinely unexpected: a snail, kinsmen in battle, a dying heart. The folk ballads show the highest surprise — they invoke "O" to introduce urgent, specific, surprising appeals.

The canonical Romantic apostrophes ("O wild West Wind", "O Rose", "O Death") address *what you'd expect* in an apostrophic context (grand abstractions, symbolic entities). The folk ballads address whatever the narrative demands at that moment — hence higher post-vocative S₂.

### H3 ✗ NOT SUPPORTED (Crucial Insight): Archaic pronouns are NOT more surprising

| Pronoun | n | Avg S₂ |
|---------|---|--------|
| thou (subject) | 24 | -0.630 |
| thee (object) | 16 | -1.096 |
| thy (possessive) | 12 | -1.303 |

**All archaic pronouns are negative S₂** — meaning they are *more expected* than GPT-2's entropy suggests. This is a key finding: in their natural context (Shakespeare sonnets, Donne, Burns, Shelley), archaic pronouns are predictable. Once you've established an archaic register, GPT-2 can anticipate the next archaic form.

The internal hierarchy is also informative: "thou" (subject) is least negative, while "thy" (possessive) is most negative. The possessive is the rarest archaic form and the hardest for GPT-2 to predict even within the archaic frame.

Comparison:
- Archaic pronouns: S₂ = -0.929
- Modern "you/your": S₂ = -0.647
- Baseline "I/he/she": S₂ = -0.590

Archaic pronouns are MORE expected (lower S₂) than modern "you" in poetry. This runs completely against naive intuition but makes perfect sense: archaic pronouns only appear in contexts where they're already established as the register.

### H4 ✗ NOT SUPPORTED: Apostrophic poems don't have higher overall S₂

Apostrophic poems: avg S₂ = 0.198 ± 0.690  
Non-apostrophic: avg S₂ = 0.253 ± 0.983  
Lift: **-0.009** (negligible)

Apostrophe does not make a poem more information-theoretically surprising overall. Its effect is strictly local — the vocative marker itself — not distributed through the poem.

---

## The Frame Effect of Apostrophe

The central finding is what we call the **Frame Effect**:

1. The vocative "O"/"Oh" pays a large surprise cost (S₂ ≈ +2.5 to +4.0)
2. This immediately establishes an apostrophic frame
3. Within that frame, subsequent tokens become MORE predictable (negative S₂)
4. The overall poem is not more surprising than non-apostrophic poetry

Apostrophe is an **information front-loader**: one high-S₂ gesture purchases a window of predictability. Compare this to:
- **Adversative turns** ("but", "yet"): distributed lift, whole window +0.15 higher
- **Interrogative structures**: lift of +0.178 throughout the question
- **Apostrophe**: spike on the marker, then drop below average

This makes rhetorical sense. The "O" signals a complete change of mode — once the reader is repositioned as overhearing a direct address, the content of that address (grand abstractions, beloved entities) becomes the expected poetic thing to do.

---

## Poems with Most Apostrophic Content

The highest-density apostrophic poems show a paradox:

| Poem | Author | Density | Avg S₂ |
|------|--------|---------|--------|
| Death, Be Not Proud | Donne | 0.063 | **-0.641** |
| The Sick Rose | Blake | 0.062 | **-0.951** |
| To a Mouse | Burns | 0.048 | +0.517 |
| To a Skylark | Shelley | 0.047 | +0.999 |
| Sonnet 18 | Shakespeare | 0.037 | -0.452 |

The most apostrophe-dense poems (Donne, Blake, Shakespeare) have **negative average S₂** — they are overall more conformist to statistical expectation than prose! This is because dense archaic-register poetry with abundant thou/thee/thy is highly predictable within its established frame.

Meanwhile the lower-density apostrophic poems (Burns' *To a Mouse*, Shelley's *To a Skylark*) have positive S₂ — suggesting that occasional apostrophe, used sparingly, achieves higher surprise than dense apostrophe.

---

## Finding

**Apostrophe is an information front-loader.** The vocative "O" is one of the highest-S₂ tokens in the corpus (avg S₂ = +2.5), but it immediately establishes a frame that makes subsequent address language *more* predictable, not less. Poems dense with archaic 2nd-person language (Donne, Shakespeare, Blake) have *negative* average S₂ — they conform to statistical expectation overall, having spent their surprise budget on the rhetorical gesture.

The most surprising apostrophes are not in canonical Romantic odes but in folk ballads, where "O" introduces a sudden urgent appeal whose content (a haste, a kinsman) GPT-2 genuinely could not predict.

---

## Suggested Next Steps

1. **Invocation vs. apostrophe**: Distinguish between invoking a Muse ("O Muse!") and apostrophizing a present object — do they differ informationally?
2. **Apostrophe position effects**: Does apostrophe at the poem's opening (Shelley's West Wind) vs. middle vs. end produce different S₂ patterns?
3. **Second-person poem types**: Compare the apostrophic "you" (addressing the absent) with the intimate "you" of direct-address love poems — does register change the information signature?
4. **Hail/Hark extended analysis**: The T1 markers "hail" and "hark" appeared rarely; expanding the corpus with more invocation-heavy poems could test their S₂ profiles.
5. **Cross-language apostrophe**: German "O" apostrophes in Rilke/Trakl — does GPT-2's German model show the same pattern?
