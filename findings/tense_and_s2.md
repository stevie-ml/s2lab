# Tense and S₂: The Grammar of Time in Poetic Surprise

**Date:** 2026-09-15  
**Experiment:** `experiments/tense_and_s2.py`  
**Corpus:** 128 English poems (123 with classifiable tense tokens)  
**Builds on:** `straussian_gap_taxonomy.md`, `hapax_legomena_s2.md`, `temporal_evolution_s2.md`

---

## Research Question

Do verb tense and tense transitions correlate with S₂ patterns in poetry? When a poem shifts between past and present tense, does GPT-2 register that transition as surprise — producing a measurable S₂ spike?

The **Temporal Straussian Gap hypothesis**: GPT-2, trained predominantly on prose and online text where present tense is the statistical default, treats present tense as the "expected" mode. When poets use past tense — especially narrative or confessional past — they deviate from the model's temporal expectation, creating high S₂. Conversely, the "lyric present" so celebrated by critics may be statistically unsurprising: the model already expected it.

---

## Method

- Classified each token as `past`, `present`, `future`, or `modal` using:
  - A lexicon of ~120 irregular past forms (was, went, felt, sang…)
  - Regular past detection: tokens ending in `-ed` (length > 4)
  - Present forms: is, are, has, have, do, does, seem, feel, stand…
  - Future markers: will, shall
  - Modal markers: would, could, might, should, must, may
- For each tense token, checked whether GPT-2's top-3 alternatives belong to the same tense category (**tense match**) or a different one (**tense mismatch**)
- Tracked tense sequences within each poem to identify **transition points** (consecutive tense tokens belonging to different tense categories) vs **sustained** same-tense stretches
- Analyzed by era using the corpus's existing era metadata

---

## Results

### 1. Tense Category S₂

| Tense    | n tokens | Mean S₂  | Median S₂ | Std  |
|----------|----------|----------|-----------|------|
| past     | 417      | **+1.189** | +0.067  | 4.56 |
| modal    | 40       | +0.310   | −0.880    | 4.14 |
| present  | 488      | −0.993   | −1.945    | 4.21 |
| future   | 23       | −1.307   | −1.323    | 2.16 |

**Key finding:** Past tense tokens have mean S₂ = **+1.189** — more than 2 nats above present tense (−0.993). Future tense is the most "expected" (−1.307), consistent with "will" and "shall" being statistically common in conditional contexts GPT-2 has seen.

The large spread on past (std = 4.56) signals that past tense produces both very surprising and very unsurprising moments — it is not uniformly high S₂, but has a heavy right tail of extreme surprises.

### 2. The Tense Mismatch Effect

When GPT-2 predicts a different tense from what the poet actually uses:

| Condition | n   | Mean S₂ |
|-----------|-----|---------|
| Tense match (predicted = actual tense) | 558 | **−1.847** |
| Tense mismatch (predicted ≠ actual tense) | 115 | **+0.434** |

The **temporal Straussian gap** = 2.28 nats. Tense mismatches are not rare accidents — they are 115 events across the corpus — and they consistently produce higher S₂ than tense matches. Whenever the poet uses a tense that the model did not expect, surprise rises dramatically.

### 3. Tense Transitions Within Poems

Tracking consecutive tense-marked tokens within each poem:

| Condition | n   | Mean S₂ |
|-----------|-----|---------|
| Tense transition (prev tense ≠ current) | 347 | **+0.410** |
| Sustained (prev tense = current)        | 621 | **−0.239** |

Transition points average 0.65 nats higher S₂ than sustained same-tense stretches. The grammar of temporal switching is itself a source of surprise.

### 4. Transition Type Breakdown

Not all transitions are equal. The most striking asymmetry:

| Transition      | n   | Mean S₂ |
|-----------------|-----|---------|
| future→past     | 2   | **+14.315** |
| present→past    | 134 | **+1.795** |
| present→modal   | 14  | +0.604  |
| modal→past      | 13  | −0.220  |
| **past→present**| 118 | **−0.492** |
| present→future  | 11  | −0.589  |
| modal→present   | 19  | −1.072  |
| past→future     | 5   | −1.228  |
| future→present  | 14  | −1.288  |
| past→modal      | 16  | **−1.431** |

**The critical asymmetry:** `present→past` transitions produce mean S₂ = **+1.795**, while `past→present` transitions produce mean S₂ = **−0.492**. 

This is counter-intuitive for literary critics: the "lyric present" — the present tense moment so often analyzed as a mark of poetic intensity — is the *low-S₂* direction. GPT-2 already expects the lyric present. The model's training on present-tense-dominant text means present tense is the unmarked default. What surprises the model is *staying in or shifting to past* when it expects present.

### 5. Top Tense-Mismatch Moments (Temporal Straussian Gap Instances)

These are the moments where tense choice most surprised the model:

| S₂     | Poem / Author | Token | Actual | Predicted | GPT-2 alt |
|--------|--------------|-------|--------|-----------|-----------|
| +13.89 | O'Hara (1957) | 'needed' | past | present | 'is' |
| +9.36  | Traditional (1899) | 'saw' | past | future | 'will' |
| +8.06  | Rankine (2014) | 'let' | past | future | 'can' |
| +7.28  | Ginsberg (1955) | 'walked' | past | present | 'am' |
| +7.08  | Browning (1842) | 'pictured' | past | present | 'I' |
| +5.46  | T.S. Eliot (1922) | 'kept' | past | present | 'is' |
| +5.39  | Ashbery (1956) | 'did' | past | modal | 'could' |
| +5.35  | Millay (1923) | 'sang' | past | present | 'is' |
| +5.35  | Hardy (1912)  | 'planned' | past | present | 'is' |

The dominant pattern: **model predicts 'is'/'am' (present), poet writes past tense**. This is the lyric present bias made quantitative — GPT-2 expects poems to stay in present tense and registers past tense as deviation.

A sub-pattern: **model predicts 'will'/'can' (future/modal), poet writes past** — as in the Traditional ballad and Rankine's *Citizen*. These are contextually unusual past-tense constructions where the model's probability mass has flowed to anticipatory or conditional mood.

### 6. Era Analysis

Mean S₂ per tense category by poetic era:

| Era | Past S₂ | Present S₂ | Modal S₂ | Future S₂ |
|-----|---------|-----------|---------|----------|
| surrealist | **+9.488** | −3.402 | — | — |
| haiku | — | **+7.935** | — | — |
| romantic | +1.099 | +2.103 | **+7.113** | −2.875 |
| beat | **+4.690** | +0.141 | — | — |
| mid_century | +3.681 | +0.733 | — | −3.499 |
| harlem_renaissance | +2.517 | +0.509 | −0.406 | — |
| new_york_school | +1.922 | −0.798 | +0.895 | +0.368 |
| language | +0.620 | **+2.364** | — | — |
| modernist | +1.346 | −1.891 | −1.928 | +0.634 |
| **confessional** | **−0.861** | −2.293 | — | — |
| victorian | +1.381 | −0.732 | −0.776 | −1.460 |
| 19th_century | +0.702 | −0.402 | −1.023 | −0.008 |

**Notable patterns:**

- **Surrealist past S₂ = +9.488**: The highest past-tense surprise. Surrealist poems (Lorca, Neruda, Char) use past tense in dreamlike contexts where it is maximally unexpected. The surrealist past is a temporal rupture.

- **Haiku present S₂ = +7.935**: Haiku's compressed present tense is so syntactically unusual that GPT-2 finds it very surprising even though it's "present tense" — the tokens following haiku context are among the most unexpected in the corpus.

- **Romantic modal S₂ = +7.113**: Keats, Wordsworth, and Blake use modal verbs (would, could, might) in positions GPT-2 strongly did not predict. The Romantic subjunctive—"I could not stop for Death"—is a genuine grammatical surprise.

- **Beat past S₂ = +4.690**: Ginsberg's catalogue-past (walking, seeing, knowing in long enumerations) violates the model's expectations repeatedly.

- **Confessional past S₂ = −0.861** (the only NEGATIVE past S₂): Plath, Sexton, Lowell — whose poetry is intensely narrative and autobiographical — use past tense in ways that GPT-2 expects. Confessional past is "readable" past: direct, sequential, prose-like. The most intimate tense is, paradoxically, the least surprising.

- **Language poetry present S₂ = +2.364**: Language poetry's fragmented present tense (Hejinian, Silliman, Perelman) is surprising even to GPT-2, which cannot predict the disjunctive syntax.

---

## Interpretation: The Lyric Present Bias

The central finding inverts a common literary-critical assumption. Critics have long analyzed the "lyric present" — poetry's tendency to use present tense to create immediacy and universality — as a mark of heightened poetic intensity. One might expect it to be computationally *surprising* for the same reason it seems rhetorically striking.

Instead, the data show the opposite: **present tense is the model's default prediction for poetry**. GPT-2, trained on a corpus where present tense dominates (news, social media, essays), treats present as the unmarked, expected choice. The lyric present is informationally cheap — it is what the model already predicts.

It is **past tense that surprises**. When poets anchor their work in specific remembered events — Ginsberg's "I saw the best minds," O'Hara's "I needed something," Eliot's "Winter kept us warm" — they choose the temporal mode that GPT-2 did not expect. Past tense in poetry is a choice against the model's prior, a grammatical Straussian gap.

This has implications for literary history. The confessional poets, who grounded their work in specific autobiographical past, produced *prose-like* past tense that the model found unsurprising — their transparency was real, not just claimed. Surrealists, by contrast, deployed past tense as part of their defamiliarization of time, producing the highest-S₂ past tense in the corpus.

---

## Limitations

1. Tense classification is lexical, not syntactic — we cannot distinguish between the past form "let" (past tense) and the imperative/modal "let" (as in "let us go"), which inflates some past-tense counts.
2. GPT-2 tokenization sometimes splits verb forms across multiple tokens (e.g., "walk" + "ed"), which this method may miss.
3. Era sample sizes are unequal; surrealist (n=1?) and haiku (small n) results should be treated cautiously.
4. "Tense sequence" within a poem doesn't account for intervening non-tense tokens — transitions may be many tokens apart.

---

## Suggested Next Steps

1. **Resolve the "let" ambiguity** using a lightweight POS tagger (spaCy) to distinguish past from imperative forms — would sharpen the confessional vs surrealist contrast.
2. **Stratify by narrative mode**: does the confessional/lyric distinction in tense S₂ hold within poets who write both narrative and lyric poems (e.g., compare Plath's "Lady Lazarus" vs "Morning Song")?
3. **Cross with emotional valence**: are high-S₂ past-tense moments (like Ginsberg's "walked") also emotionally charged? Test whether the temporal Straussian gap and the affective gap co-occur.
4. **Tense and the volta**: do tense transitions within poems correlate with `volta_and_s2.md` findings? Is the volta a tense shift as well as a rhetorical turn?
5. **Add more confessional poems** to test whether the negative past-tense S₂ is stable across the genre, or specific to the few poems currently in the corpus.
