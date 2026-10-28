# On-Map vs. Off-Map Deviation: Two Geometries of Poetic Surprise

**Date:** 2026-10-28  
**Experiment:** `experiments/on_map_off_map_deviation.py`  
**Corpus:** 369 texts analyzed with GPT-2 (S₂ threshold: 1.0, map boundary: rank ≤ 10)  
**Builds on:** `straussian_gap_taxonomy.md`, `entropy_conditioned_deviation.md`, `rank_pos_deviation.md`

---

## Research Question

When a poet writes a token with high S₂ (more surprising than entropy warrants), there are two structurally different situations:

- **On-map deviation** (rank ≤ 10): GPT-2's top-10 predictions *included* the poet's choice — but it was less likely than something else. The model "imagined" this word; the poet just picked the less-traveled option.
- **Off-map deviation** (rank > 10): GPT-2's top-10 predictions *did not include* the poet's choice. The word was essentially outside the model's considered alternatives.

These represent two different creative geometries: choosing the unexpected *from within* a known horizon vs. departing the map entirely.

---

## Key Finding

The overwhelming majority of poetic surprise is **off-map**:

| Type | Count | % of high-S₂ | Avg S₂ | Avg Entropy | Avg Word Length | Longer than alt? |
|---|---|---|---|---|---|---|
| **On-map** (rank ≤ 10) | 1,249 | 9.8% | 2.77 | 3.02 | 2.54 | 42.3% |
| **Off-map** (rank > 10) | 11,541 | 90.2% | 4.62 | 7.27 | 4.22 | 65.1% |

**90.2% of all high-S₂ moments are off-map.** Poetry does not primarily deviate by selecting from the model's known alternatives — it departs the map entirely.

### The Entropy Asymmetry

The most important structural difference: **off-map tokens occur in high-entropy contexts** (avg entropy 7.27 bits) while **on-map tokens occur in low-entropy contexts** (avg entropy 3.02 bits). 

This reveals a **complementary division of labor**:
- When the model is uncertain (many options), poets go *further off the map* than the model imagined
- When the model is confident (clear expectations), poets sometimes choose a *near alternative* (on-map) rather than radical departure

This makes intuitive sense: a poet who writes something truly unexpected when the model is confident (low entropy) cannot rely on the context to "explain" the surprise — the word must justify itself semantically. Such on-map deviations are subtle defiances of a clear prediction.

### Off-Map Tokens Are Longer Words

Off-map tokens average 4.22 characters vs. 2.54 for on-map. This aligns with the finding from `word_length_vs_s2.md` — longer, less-common words push further off the model's map.

Off-map tokens are also **longer than the top-predicted alternative 65.1%** of the time (vs. 42.3% for on-map). Poets tend to choose longer words over what the model expected.

---

## By Era: Which Genres Are Most "On-Map"?

| Era | On-Map % | n high-S₂ |
|---|---|---|
| triolet | 32% | 22 |
| concrete | 32% | 19 |
| **control** (prose) | **25%** | 20 |
| found_poetry | 24% | 192 |
| oulipo | 23% | 145 |
| prose_poetry | 18% | 359 |
| biblical | 17% | 276 |
| villanelle | 15% | 47 |
| song_lyrics | 14% | 91 |
| language | 13% | 122 |
| nursery_rhyme | 13% | 55 |
| new_york_school | 13% | 477 |
| modernist | 10% | ~500 |
| surrealist | ~8% | ~100 |
| beat | ~7% | ~200 |

**Control prose ranks 3rd most on-map**, just below concrete and triolet. Prose deviation tends to stay within the model's imaginable alternatives — even when prose surprises, it selects from familiar vocabulary.

**Found poetry and Oulipo** (constraint-based writing like N+7, lipograms) have high on-map rates — their rule-governed substitutions often replace one grammatically similar word with another, staying within the model's horizon.

**Beat poetry, surrealism, and early modernism** cluster at the bottom — these movements systematically depart the model's map entirely.

---

## By Author: On-Map Extremes

### Most On-Map Authors
| Author | On-Map % | n | Style |
|---|---|---|---|
| Thomas Jefferson (found text) | 56% | 18 | Documentary prose |
| Emmett Williams | 43% | 14 | Concrete/Oulipo |
| Arthur Symons | 42% | 12 | Victorian Symbolist |
| Anonymous (found text) | 32% | 76 | Found documents |
| Killarney Clary | 30% | 37 | Prose poetry |
| Kenneth Koch | 29% | 41 | New York School |
| Gertrude Stein | 21% | 145 | Language / prose |

**Thomas Jefferson's "Declaration of Independence"** — repurposed as found poetry — is the most on-map text in the corpus. Political/legal prose deviates in modest, grammatically predictable ways.

### Most Off-Map Authors (0% on-map)
| Author | Style |
|---|---|
| H.D. (Hilda Doolittle) | Imagist |
| Vachel Lindsay | Oral/performance |
| Andrew Marvell | 17th-century metaphysical |
| Homer (trans. Pope) | Classical epic in heroic couplets |
| Anonymous (Old English, trans.) | Alliterative verse |
| Adelaide Crapsey | Cinquain (compressed form) |
| Li Bai, Wang Wei, Cui Hao | Classical Chinese (in translation) |

The zero-on-map cluster is striking in its diversity: it includes translated texts, archaic English, classical Chinese poetry, and imagism. **What unites them is vocabulary foreignness** — either historically archaic (Marvell, Old English), linguistically distant (Chinese translation), or semantically extreme (imagism's concrete-noun accumulation). GPT-2 simply never predicted these words in these contexts.

### The Cummings-Stein Contrast
- **E.E. Cummings**: 3% on-map — his typographic and syntactic experiments place him almost entirely off GPT-2's map. His surprise is radical and structural.
- **Gertrude Stein**: 21% on-map — her repetition-based deviations stay more within the model's imagination. Her surprises are more "grammatically considered" — she uses ordinary words in odd combinations that the model at least contemplated.

---

## Notable Examples

### On-Map Examples (High S₂ Within Model's Horizon)
| Token | S₂ | Rank | Expected | Context |
|---|---|---|---|---|
| `"ads"` | 11.68 | 9 | `"adow"` | Romantic poem mid-word (tokenization split) |
| `" you"` | 11.37 | 8 | `" her"` | "but he done..." (song lyric gender flip) |
| `" could"` | 10.83 | 8 | `" would"` | Modal substitution (parody) |
| `" again"` | 9.79 | 8 | `" different"` | "and will be..." |

The on-map examples reveal **near-substitutions**: gender pronouns swapped, modal verbs exchanged, grammatically parallel alternatives chosen over the model's preference.

### Off-Map Examples (Complete Departure)
| Token | S₂ | Rank | Expected | Era |
|---|---|---|---|---|
| `" gro"` | 36.66 | 15,997 | `" "` | Beat |
| `" climbs"` | 28.25 | 38,430 | `" "` | Beat |
| `" pour"` | 27.73 | 1,574 | `"'m"` | Spoken word |
| `" glass"` | 25.63 | 2,667 | `" "` | Modernist |
| `" whenever"` | 25.60 | 13,167 | `" "` | Beat |

---

## Interpretation: A Two-Mode Theory of Poetic Surprise

The data supports a **two-mode model** of poetic deviation:

1. **On-map mode** (Low entropy context → poet picks rank 2-10 alternative):  
   The model was confident. The poet defies that confidence but stays within a nearby space — choosing a semantically parallel alternative. This is subtle defamiliarization: the unexpected but understandable word.

2. **Off-map mode** (High entropy context → poet picks rank 11+):  
   The model was already uncertain. The poet doesn't pick from its shortlist at all — they go somewhere else entirely. This is radical departure: the word that wasn't even on the table.

The finding that **90.2% of high-S₂ moments are off-map** suggests that poetry's primary mechanism is not "choosing the wrong word from a known set" but "choosing a word from outside the set." This aligns with Jakobson's equivalence principle: poetry's selections break the model's paradigmatic axis entirely.

---

## Suggested Next Steps

1. **Entropy-conditioned on/off-map split**: For tokens with entropy < 2 bits (high model confidence), what % are on-map vs. off-map? This would isolate the "true Straussian" on-map moves.
2. **Semantic analysis of on-map deviations**: Are on-map high-S₂ tokens semantically *related* to the expected token (synonyms, near-synonyms) or syntactically parallel (same POS, different meaning)?
3. **On-map rate as a poetic register fingerprint**: Can the ratio on_map/(on_map+off_map) distinguish literary registers more cleanly than raw S₂?
4. **Trajectory**: Does on-map ratio change across the length of a poem? Do poets "warm up" into off-map territory or use it strategically at specific structural points?
