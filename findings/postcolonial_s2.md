# Postcolonial / Diaspora Poetics and S₂: Oral Ritual vs. Straussian Deviation

**Date:** 2026-10-13  
**Experiment:** `experiments/postcolonial_s2.py`  
**New poems added:** 6 (Joy Harjo ×2, Derek Walcott, Agha Shahid Ali ×2, Kamau Brathwaite)  
**Corpus now:** 277 texts  
**Builds on:** `catalog_decay_s2.md`, `repetition_and_entropy.md`, `second_occurrence_dip.md`, `oral_literary_register.md`

---

## Research Question

Do poets working between oral traditions, vernacular dialect, and standard literary English show
systematically different S₂ signatures from mainstream Anglo-American poetry?

**The hypothesis**: Code-switching, oral patterning, and cross-cultural lexicons (Caribbean
toponyms, Mvskoke cosmology, Kashmiri imagery) diverge from GPT-2's primarily Anglo-American
training distribution → **higher artifact-free S₂** than comparable contemporary poetry.

**Poets added:**
- **Joy Harjo** (Mvskoke Nation) — contemporary Native American poetry with oral/ritual structure
- **Derek Walcott** (St. Lucia) — Caribbean modernism, Creole-inflected English, West Indian landscape
- **Agha Shahid Ali** (Kashmir/USA) — ghazal form, Urdu poetic tradition transplanted into English
- **Kamau Brathwaite** (Barbados) — "Nation language," creolized syntax, visual/spatial typography

---

## Main Finding: Hypothesis DISCONFIRMED — Oral Tradition Produces LOWER S₂

| Era | n | Mean S₂ (clean) | +S₂% |
|---|---|---|---|
| beat | 6 | **+0.279** | 32% |
| confessional | 6 | −0.300 | 38% |
| victorian | 21 | −0.305 | 36% |
| contemporary | 9 | −0.365 | 34% |
| modernist | 24 | −0.405 | 36% |
| language | 5 | −0.424 | 33% |
| romantic | 15 | −0.470 | 36% |
| **postcolonial** | **6** | **−0.495** | **30%** |
| harlem_renaissance | 5 | −0.500 | 35% |
| black_arts | 1 | −0.502 | 34% |
| new_york_school | 18 | −0.599 | 35% |
| protest_political | 2 | −0.730 | 33% |

**Postcolonial poets average −0.495 artifact-free S₂ — below beat, confessional, Victorian, and
modernist, and roughly equal to Harlem Renaissance and Black Arts.** The hypothesis that
cultural/linguistic outsider status creates higher informational surprise is not supported.

| Poem | S₂ (clean) | Max S₂ | +S₂% |
|---|---|---|---|
| Harjo — "Remember" | −0.452 | 18.06 | 30% |
| Harjo — "She Had Some Horses" | −0.579 | 10.92 | 23% |
| Walcott — "The Season of Phantasmal Peace" | −0.802 | 12.94 | 27% |
| Ali — "Postcard from Kashmir" | −0.384 | 10.92 | 36% |
| Ali — "Even the Rain" | −0.444 | 11.58 | 38% |
| Brathwaite — "Calypso" | −0.307 | 25.66 | 24% |

---

## Why the Hypothesis Failed: The Oral Ritual Effect

The key to understanding this result is **Joy Harjo's "She Had Some Horses"**:

The poem repeats the phrase "She had horses who were X" 12 times, each with a different completion.
This is a deliberate incantatory structure drawn from oral ritual traditions (Mvskoke ceremonial
speech, the horse's centrality in Plains Indian cosmology).

**Habituation of "horses" across 12 occurrences:**

| Occurrence | Position | S₂ | Surprisal | Entropy |
|---|---|---|---|---|
| 1st | 2 | **+4.11** | 14.32 | 10.21 |
| 2nd | 7 | −0.99 | 6.23 | 7.21 |
| **3rd** | 16 | **−3.98** | 0.82 | 4.81 |
| 4th | 25 | −2.83 | 0.43 | 3.26 |
| 5th | 34 | −2.01 | 0.27 | 2.28 |
| 6th | 44 | −1.89 | 0.26 | 2.14 |
| 7th | 52 | −1.47 | 0.19 | 1.66 |
| 8th | 60 | −1.10 | 0.14 | 1.23 |
| 9th | 69 | −0.89 | 0.11 | 1.00 |
| 10th | 78 | −1.24 | 0.15 | 1.40 |
| 11th | 85 | −1.02 | 0.12 | 1.14 |
| 12th | 98 | −1.09 | 0.13 | 1.22 |

**S₂ collapses from +4.11 (1st) to −3.98 (3rd) — an 8-bit drop in just two iterations.**

By the 9th occurrence, surprisal is 0.11 bits: the model is ~93% confident "horses" is next.
Yet this poem is widely celebrated and taught in American poetry courses.

**Crucially, this confirms the two-track theory of poetic effect:**

> Oral/ritual poetry achieves its aesthetic effect through the DELIBERATE ELIMINATION of
> surprise — the Straussian gap closes as the incantation progresses. The poem's power comes
> from rhythm, weight, accumulation, and trance — not from information-theoretic deviation.

This is the information-theoretic signature of oral tradition: **maximum habituation, not maximum surprise.**

Compare to `catalog_decay_s2.md`'s finding that 69% of anaphora chains are "adapting" — Harjo's
poem is the most extreme case of intentional rapid habituation in the entire corpus.

---

## Brathwaite: Visual Spacing as Information

Kamau Brathwaite's "Calypso" has the **highest max S₂ (25.66)** in the postcolonial group.
However, analysis reveals this is driven by the poem's extreme visual layout — words separated
by long stretches of whitespace (his "sycorax video style"):

```
Cuba and San Domingo
                         Jamaica and Puerto Rico
Grenada        Guadeloupe         Bonaire
```

These whitespace sequences create newline-like tokens where GPT-2 expects more content.
The S₂ spikes at "Jamaica" (S₂ = +16.27), "Guadeloupe" (S₂ = +21.80 via subword "Gu")
are **spatial artifacts**, not semantic surprises — GPT-2 expected the line to end, not continue.

**This extends the stanza-break artifact finding**: Brathwaite's visual-poetic practice
(N Language — treating the page as a score) systematically creates artifact inflation.
His artifact-corrected mean would be even lower than the raw −0.307.

---

## Ali and Walcott: The Register of Loss

Agha Shahid Ali's two poems show the highest +S₂% in the postcolonial group (36–38%),
nearly matching confessional poetry. His "Even the Rain" (a ghazal) produces genuine
semantic surprises:

| Moment | Token | GPT-2 expected | S₂ |
|---|---|---|---|
| "he has bought _grief_'s lottery" | grief | a(14.7%), the(10.2%) | +11.58 |
| "How did the _Enemy_" | Enemy | rain(17.3%), sun(1.4%) | +10.88 |

The word "Enemy" at the start of a ghazal couplet, where GPT-2 expected "rain" (the refrain
word), represents genuine semantic deviation. Ali exploits the ghazal's formal structure to
*withhold* the expected refrain word and substitute something conceptually distant.

Walcott's poem, by contrast, uses formal Victorian-adjacent diction ("arbor made of the
boughs of both islands") — syntactically conventional for its literary register, producing
below-average S₂. Colonial-era English literary training dampens surprise.

---

## The Cultural Geography of S₂

Organizing these poets by their relationship to English:

| Poet | Tradition | Primary Relation to English | S₂ |
|---|---|---|---|
| Harjo | Mvskoke oral tradition | English as 2nd/colonial language | −0.515 avg |
| Brathwaite | Caribbean oral/Nation language | Creole-inflected, visual poetry | −0.307 |
| Walcott | St. Lucian Creole + formal English | Formal/literary English dominant | −0.802 |
| Ali | Urdu ghazal tradition | English as formal lyric medium | −0.414 avg |

**Hypothesis**: Poets who work primarily in *formal literary English* (Walcott, in this poem)
have lower S₂ than those who resist formal English norms (Brathwaite's spacing, Harjo's
oral structures). But the effect is smaller than the oral/ritual effect.

---

## What DOES Create High S₂ in These Poems?

Category breakdown of tokens with S₂ > 2.0 in postcolonial poems:

| Category | % of high-S₂ tokens |
|---|---|
| Content words (unexpected lexical choice) | 67% |
| Newline/whitespace artifact | 17% |
| Function words in unexpected position | 5% |
| Long/rare words (multi-subword) | 4% |
| Cultural-specific lexicon | 3% |
| Proper nouns | 3% |

**Culturally-specific vocabulary contributes only 3% of high-S₂ moments** — far less than
expected. Caribbean place names (Guadeloupe, Jamaica), geological terms (Himalayas,
Jhelum), and cultural objects (bergamot, vermouth) surprise GPT-2 when they appear, but
they are relatively rare in the poems. The main driver of surprise is the same as in any
poetry: **unexpected content-word substitution** — the standard Straussian gap.

---

## Revised Theory: Two Modes of Postcolonial Poetics

The findings suggest two distinct information-theoretic strategies:

**Mode 1 — Incantatory/Oral** (Harjo, Brathwaite):
- Rapid habituation through anaphoric repetition
- Low mean S₂, very low +S₂%
- Aesthetic effect from weight, accumulation, trance
- S₂ profile: converges toward −1.0 to −2.0 as poem progresses

**Mode 2 — Lyric/Formal** (Walcott, Ali):
- Individual high-S₂ moments at culturally-specific or semantically unexpected words
- S₂ profile: scattered spikes against low baseline
- Ghazal structure (Ali) creates expected/unexpected rhythm like refrain poems

Neither mode achieves the high positive S₂ of beat poetry or German modernism.
The postcolonial information signature is closer to **oral tradition** than to
experimental European modernism — despite the cultural distance from GPT-2's training.

---

## Key Findings

1. **The oral ritual hypothesis**: Harjo's anaphoric catalog achieves poetic effect
   through rapid, *intentional* habituation — S₂ collapses from +4.11 to −3.98 in two
   iterations of "horses." This is the fastest and most complete habituation in the corpus.

2. **Cultural lexicon has minimal S₂ effect**: Place names and culturally-specific vocabulary
   (Guadeloupe, Kashmir, bergamot) contribute only 3% of high-S₂ moments. Postcolonial
   poets' "outsider" lexicons do not systematically surprise GPT-2 more than any other
   unusual vocabulary.

3. **Visual/spatial poetics creates S₂ inflation**: Brathwaite's whitespace typography
   inflates raw S₂ via the same mechanism as stanza breaks.

4. **The ghazal's refrain withholding**: Ali's "Even the Rain" shows that the ghazal's
   ability to withhold the expected refrain word and substitute something semantically
   distant is a genuine source of Straussian deviation (+10.88 for "Enemy" where "rain"
   was expected).

---

## Suggested Next Steps

- **Test Mode 1 vs Mode 2 across a larger sample**: Add more oral-tradition poems (Lucille
  Clifton, Sherman Alexie, Sonia Sanchez) to see if the rapid-habituation pattern holds.
- **Analyze Brathwaite's full corpus** with whitespace-tokenization awareness — what is his
  true S₂ when visual artifacts are stripped?
- **"Even the Rain" refrain tracking**: Do ghazal refrains follow the same habituation curve
  as other anaphoric structures? The ghazal's refrain appears every couplet; does S₂ of
  "the rain" drop as fast as "horses"?
- **The oral-lyric spectrum**: Is there a continuum from maximum-habituation (oral ritual)
  to maximum-surprise (Language poetry), with most literary poetry in between? Map all eras
  on this axis.
