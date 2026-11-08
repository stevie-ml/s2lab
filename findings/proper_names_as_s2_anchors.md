# Proper Names as S2 Anchors in Poetry

**Date:** 2026-11-08  
**Experiment:** `experiments/proper_names_s2.py`  
**Data:** `results/proper_names_s2.json` (411 poems, ~49,000 tokens)

---

## Research Question

Do proper nouns — personal names, place names, mythological figures — carry
systematically higher S2 than common nouns in poetry? If so, what does GPT-2
expect *instead* of a proper name, and what does that tell us about the
"nominal anchor" function of proper referents in verse?

---

## Method

Tokens were classified by capitalization (excluding sentence-initial positions)
and matched against lexicons for:
- **PROPER_PERSON**: personal names, historical figures, biblical characters
- **PROPER_PLACE**: geographic locations, mythological geography
- **PROPER_MYTHOLOGICAL**: personifications (Muse, Fate, Death, Love, etc.)
- **PROPER_OTHER**: capitalized tokens not in any lexicon (the largest category)
- **COMMON_NOUN**, **FUNCTION**, **PUNCT** as comparison baselines

---

## Results

### Category S2 Summary

| Category            |      N | Mean S2 | Median S2 |
|---------------------|-------:|--------:|----------:|
| PROPER_MYTHOLOGICAL |     31 |   2.576 |     1.904 |
| PROPER_OTHER        |    938 |   2.634 |     2.123 |
| PROPER_PLACE        |     39 |   2.007 |     1.434 |
| PROPER_PERSON       |    103 |   1.367 |     0.591 |
| COMMON_NOUN         | 25,526 |   1.469 |     0.131 |
| FUNCTION            | 15,655 |  -0.386 |    -1.911 |
| PUNCT               |  7,060 |  -1.625 |    -2.058 |

### Key Gradients

The proper-name S2 hierarchy (descending):
1. **PROPER_OTHER** (2.634) — unknown-to-lexicon proper names; these catch
   GPT-2 most off-guard, often unique place names, invented terms, or rare names.
2. **PROPER_MYTHOLOGICAL** (2.576) — personifications like Muse, Fate, Death,
   Love; abstract forces raised to proper-noun status.
3. **PROPER_PLACE** (2.007) — geographic anchors; rivers, cities, regions.
4. **PROPER_PERSON** (1.367) — close to COMMON_NOUN (1.469); see discussion.

### The Personal-Name Anomaly

Surprisingly, personal names have *lower* S2 than place names and mythological
personifications, landing near common nouns. Two possible explanations:

1. **Conventional slot**: Poetry has a long tradition of direct address (apostrophe
   to Keats, invocation of the Muse). These personal names appear in highly
   predictable syntactic positions ("O Keats!", "To —"). The model has
   seen "O [Proper Name]" enough that it's not shocked.
2. **Pronoun substitution**: GPT-2 expects a pronoun ("I", "he", "you") in many
   positions where poets put a personal name. The name *is* surprising, but
   the semantic category (human referent) overlaps with what the model predicted.

Place names and mythological personifications, by contrast, appear in positions
where the model expects concrete nouns or abstract nouns — a larger class with
higher entropy, so the specificity of the proper name constitutes a stronger
"reality anchor."

---

## What GPT-2 Suppresses When a Proper Name Appears

### Top 15 Suppressed Alternatives

| Token     | Freq | Category     |
|-----------|-----:|--------------|
| "the"     |  291 | FUNCTION     |
| ","       |  172 | PUNCT        |
| "I"       |  131 | FUNCTION     |
| "" (eos)  |  120 | OTHER        |
| "a"       |  114 | FUNCTION     |
| "and"     |   77 | FUNCTION     |
| "."       |   40 | PUNCT        |
| "my"      |   39 | FUNCTION     |
| "man"     |   35 | COMMON_NOUN  |
| "'s"      |   33 | PUNCT        |
| "his"     |   30 | FUNCTION     |
| "The"     |   28 | FUNCTION     |
| "God"     |   28 | PROPER_PERSON|
| "Lord"    |   28 | PROPER_PERSON|
| "of"      |   26 | FUNCTION     |

### Suppressed Alternative Categories

| Category    | Count |   % |
|-------------|------:|----:|
| COMMON_NOUN | 1,945 | 58% |
| FUNCTION    |   986 | 30% |
| PUNCT       |   282 |  8% |
| OTHER       |   120 |  4% |

**Reading**: When a poet writes a proper name, GPT-2 most often expected a
*common noun* (58%) — meaning proper names substitute for generic referents.
"Mississippi" appears where the model expected "river"; "Keats" where it
expected "poet" or "man". The article "the" is the single most suppressed token
(291 cases), often meaning the proper name appears where the model would start
a noun phrase: "the [river]" → "Mississippi".

The appearance of "God" and "Lord" (28 each) in the suppressed list is striking:
when a proper name appears, the model frequently predicts another divine referent.
This reveals a **divine register cluster** in the corpus — proper names cluster
in contexts saturated with religious vocabulary.

---

## Most Frequent Proper Names in Corpus

| Name      | Count | Notes                                   |
|-----------|------:|-----------------------------------------|
| God       |    43 | Most common — religious saturation      |
| Captain   |    12 | Whitman's "O Captain! My Captain!"      |
| Death      |    12 | Personified, often mythological         |
| LORD      |    10 | Biblical, all-caps distinguishes divine |
| Father    |    10 | Religious / familial                   |
| Lamb      |     7 | Blake's "The Lamb"; also Christ figure  |
| Napoleon  |     7 | Most common historical proper name      |
| Love      |     7 | Personified Love (Donne, Herbert)       |
| William   |     9 | Multiple poets addressed/named         |

The dominance of **religious vocabulary** is the clearest corpus signal: God,
LORD, Father, Lamb, Lord, Captain (the Lincoln elegy) — the corpus is heavily
weighted toward 19th-century religious poetry and elegiac verse.

---

## Poems with Highest Proper-Name S2 Lift

(Lift = proper_avg_s2 − common_avg_s2)

| Lift   | Poem                                            | Author              |
|--------|-------------------------------------------------|---------------------|
| +16.61 | Inversnaid                                      | Gerard Manley Hopkins|
| +13.52 | Anecdote of the Jar                             | Wallace Stevens     |
| +12.66 | Wet Casements                                   | John Ashbery        |
| +12.57 | Driving Toward the Lac Qui Parle River          | Robert Bly          |
| +11.76 | Proverbs of Hell (excerpt)                      | William Blake       |
| +11.51 | The World                                       | Henry Vaughan       |
| +10.67 | Carmel Point                                    | Robinson Jeffers    |
| +10.46 | For a Venetian Pastoral by Giorgione            | Dante Gabriel Rossetti|

**Pattern**: Poems with high proper-name lift tend to be *place-centered*:
"Inversnaid" (a Scottish waterfall), "Anecdote of the Jar" ("Tennessee"),
"Driving Toward the Lac Qui Parle River" (Lakota place name), "Carmel Point"
(Jeffers' coastal California). The specific place name punctures the statistical
flow in a way that common nouns cannot — it forces maximum specificity.

---

## Findings

### Finding 1: Proper Names Are Information-Theoretic Anchors

Proper names (excluding personal names) have S2 roughly double that of common
nouns (2.0–2.6 vs. 1.5 mean). They function as **reality anchors** — tokens
that tie the poem to a specific, unrepeatable entity — and this anchoring is
visible in the S2 signature.

### Finding 2: The Personal-Name Paradox

Personal names are *less* surprising than place names (1.37 vs 2.01). Despite
being equally specific referents, they appear in conventionally predictable
positions (apostrophe, dedication, address) that GPT-2 has learned. The place
name resists domestication; the personal name fits into a known poetic slot.

### Finding 3: Proper Names Suppress Generic Nouns

58% of GPT-2's suppressed alternatives at proper-name positions are common nouns.
Poets use proper names where language naturally tends toward the generic. The
"Straussian gap" here is: *Mississippi* where language says *river*; *Keats*
where language says *poet*; *Lac Qui Parle* where language says *the river*.

### Finding 4: The Divine Cluster

"God" and "Lord" appear in the suppressed alternatives (28 each), not because
God appears as a proper name but because the positions *around* proper names are
saturated with divine vocabulary. Proper names cluster in religiously-toned
contexts — the corpus reveals this as its structural backbone.

---

## Hypothesis

**The nominal anchor hypothesis**: Place names have higher S2 than personal
names because place names occupy positions where the statistical texture of
the sentence expects class-level (not instance-level) reference. The specificity
of a place forces the reader to instantiate a singular world; the specificity
of a person name fits into an already-abstract social-deictic slot that poetry
has normalized.

This predicts: in poems with more landscape imagery, proper place names should
carry higher S2 lift than in poems with social/dramatic content.

---

## Limitations

- The lexicons are incomplete; PROPER_OTHER (938 tokens) is a catch-all for
  capitalized words not recognized — it may include false positives (line-initial
  words captured despite filtering, artifacts of German poems in the corpus).
- The corpus has German poems analyzed with the English model — their tokens
  will show anomalous S2 values (confirmed by "Verklärter Herbst" at high
  proper-name density).
- Personal names are under-counted by the lexicon approach.

---

## Suggested Next Steps

1. **NER-based classification**: Replace the lexicon heuristic with spaCy NER to
   get cleaner PERSON/LOC/ORG tags and reduce PROPER_OTHER noise.
2. **Place names by specificity**: Compare rivers → cities → countries → mythological
   places — does S2 increase with geographic obscurity?
3. **Proper names by poetic function**: Apostrophe ("O —"), simile ("like —"),
   catalogue — are there positional S2 differences by rhetorical function?
4. **Filter German poems**: Exclude non-English poems from future proper-name
   analysis to remove model-language mismatch artifacts.
5. **Historical trend**: Do Romantic poets (heavy on classical proper names) use
   proper names differently from Modernists (concrete, local proper names)?
