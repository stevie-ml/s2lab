# Hapax Legomena and S₂: Two Mechanisms of Poetic Surprise

**Date:** 2026-09-13  
**Experiment:** `experiments/hapax_vs_repeated_s2.py`  
**Corpus:** 106 English poems (2026-09-13 corpus), 3,873 hapax tokens + 2,079 repeated tokens  
**Builds on:** `repetition_and_entropy.md`, `straussian_gap_taxonomy.md`, `vocab_richness_vs_s2.md`

---

## Research Question

Within a single poem, do words used only once (**hapax legomena** — tokens whose alphabetic form appears exactly once in the poem) carry higher S₂ than words the poet uses multiple times? If so, does this hold across eras and genres? And what do the *exceptions* reveal about the two distinct mechanisms that drive the Straussian gap?

---

## Method

- For each English poem (≥20 tokens), counted the frequency of each alphabetic token (length ≥3, lowercased, punctuation stripped).
- **Hapax legomena**: tokens whose normalized form appears exactly once.
- **Repeated words**: tokens whose normalized form appears 2+ times.
- Compared mean S₂ across these two categories, globally and per era.
- Examined reversed-pattern poems (where repeated words have *higher* mean S₂ than hapax) to identify the mechanism.

---

## Results

### Global

| Category | n tokens | Mean S₂ | Std | 
|---|---|---|---|
| **Hapax legomena** | 3,873 | **+1.702** | ±5.133 |
| **Repeated words** | 2,079 | **−0.412** | ±5.675 |
| **Gap (hapax − repeated)** | — | **+2.114** | — |

**97/106 poems (92%) show hapax mean S₂ > repeated mean S₂** — a near-universal pattern.

### By Literary Era (ranked by hapax gap)

| Era | Gap (hapax − rep) | Hapax S₂ | Repeated S₂ | n hapax / repeated |
|---|---|---|---|---|
| beat | +4.753 | +2.727 | −2.025 | 72 / 23 |
| deep_image | +4.305 | +1.964 | −2.341 | 31 / 8 |
| confessional | +3.189 | +2.281 | −0.908 | 59 / 13 |
| language | +2.658 | +1.674 | −0.984 | 65 / 20 |
| new_york_school | +2.632 | +1.217 | −1.415 | 557 / 271 |
| modernist | +2.427 | +2.050 | −0.377 | 564 / 299 |
| haiku | +2.288 | +3.518 | +1.230 | 27 / 8 |
| prose_poetry | +2.016 | +1.228 | −0.788 | 187 / 134 |
| romantic | +1.918 | +1.797 | −0.121 | 433 / 195 |
| **control (prose)** | +1.610 | **−1.491** | **−3.102** | 74 / 26 |
| ballad | +1.426 | +2.677 | +1.250 | 150 / 304 |
| harlem_renaissance | +1.068 | +1.223 | +0.154 | 207 / 80 |
| **oulipo** | **+0.193** | +1.060 | +0.867 | 18 / 6 |

### Poems with Largest Hapax Advantage

| Poem | Hapax S₂ | Repeated S₂ | Gap |
|---|---|---|---|
| Howl (opening) | +3.36 | −4.16 | +7.52 |
| A Route of Evanescence | +3.27 | −3.94 | +7.21 |
| The Convergence of the Twain | +4.91 | −1.08 | +5.99 |
| Sunday Morning (stanza 1) | +1.47 | −4.16 | +5.63 |
| Self-Portrait in a Convex Mirror | +1.48 | −4.05 | +5.53 |

### Reversed Pattern: Repeated Words Outpace Hapax

| Poem | Hapax S₂ | Repeated S₂ | Gap | Mechanism |
|---|---|---|---|---|
| **Harlem** (Hughes) | −0.09 | +11.26 | −11.35 | Anaphoric "Does/Or/like" at line starts |
| **Buffalo Bill 's** (Cummings) | +3.40 | +13.72 | −10.32 | "and" at experimental line beginnings |
| **To a Mouse** (Burns, closing) | +1.95 | +4.55 | −2.60 | "The/But/thou" as stanza-opening refrains |

---

## Finding

### The Two Mechanisms of the Straussian Gap

The data reveals two distinct pathways through which a poet can register high S₂:

**1. Lexical Novelty (hapax pathway):** The poet chooses a word so unusual — in context — that GPT-2 did not anticipate it. Because this word appears only once, its uniqueness is *both* lexical (rare in the poem's own vocabulary) and statistical (surprising to the model). This is the dominant mechanism in 92% of poems. Beat poetry, deep image, and confessional poetry show the largest gaps — traditions that prize radical lexical freshness.

**2. Structural Recurrence (anaphora pathway):** A poet *repeats* a structural word — "Does", "Or", "like", "and" — at the beginning of lines or stanzas. Each recurrence surprises GPT-2 not for being lexically unusual, but because the model overwhelmingly predicts a *newline* at the end of each question-line, not a continuation word. The repeated anaphoric word defeats this structural expectation each time. Hughes's "Harlem" is the clearest example: "Does" at S₂ = +31.07, "Or" at +28.03, "like" at +27.71 — all highly expected by human readers, all informationally explosive to GPT-2.

The two mechanisms map onto two different registers of surprise:
- **Hapax surprise**: *what* the poet chose (a rare, unexpected word)  
- **Structural surprise**: *where* the poet placed the word (in a position the model expects to be empty)

### Why Oulipo Has the Smallest Gap (+0.19)

Oulipo poetry (e.g., N+7 constraint procedures) generates text by substituting words according to a rule rather than intuitive lexical choice. This systematically disrupts the relationship between lexical uniqueness and semantic intention — words become interchangeable at the level of the constraint. The hapax/repeated distinction loses its meaning: whether a word recurs depends on the constraint algorithm, not on the poet's emphasis. The near-zero gap is diagnostic of procedural rather than intentional composition.

### Haiku: Both Hapax *and* Repeated Are High

Haiku shows high S₂ in both categories (hapax=+3.52, repeated=+1.23). This makes sense: haiku is compact enough that every word is doing maximum work, repeated or not. The few words that *do* repeat (e.g., "the") are still surprising because the entire register is radically compressed.

### The Prose Baseline

Control prose has the same *direction* of effect (hapax gap = +1.61) but at a much lower absolute level: prose hapax words average **−1.49** (still below expectation!), while poetry hapax words average **+1.70** (above expectation). The hapax effect is not unique to poetry — unique vocabulary is generally more surprising — but poetry *amplifies* it: the unique words in a poem are positively surprising (above statistical expectation), while the unique words in prose are merely less conformist than repeated prose words.

---

## Key Numbers to Cite

- **92%** of poems: hapax S₂ > repeated S₂
- Global hapax advantage: **+2.11 S₂ units**
- Hughes's "Harlem": anaphoric "Does" at S₂ = **+31.07** — the highest single-token S₂ via structural (not lexical) surprise
- Beat poetry has the largest hapax-gap (**+4.75**); Oulipo the smallest (**+0.19**)

---

## Suggested Next Steps

1. **Hapax density as a genre signal**: Is type-token ratio correlated with *which* mechanism dominates? Low-TTR poems (repetitive) should rely on structural surprise; high-TTR poems on lexical surprise.
2. **Second-occurrence dip**: For words that appear 2+ times, how does S₂ change from first to second appearance? Does the poet "spend" the surprise the first time?
3. **Structural position of high-S₂ repeated words**: Confirm that high-S₂ repeated words cluster at line beginnings (position=1 within the line) — this would formalize the structural-surprise mechanism.
4. **Apply to prose authors known for repetition** (Hemingway's "and" chains, Woolf's refrains in *The Waves*): does the structural-surprise mechanism generalize outside poetry?
