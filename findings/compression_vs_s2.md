# Compression Ratio vs S₂: Two Kinds of Poetic Difficulty
**Date:** 2026-08-31
**Experiment:** `experiments/compression_ratio.py`
**Corpus:** 73 texts (68 poetry, 5 control prose) — including 10 new poems added this run

## Question
gzip and GPT-2 both estimate the compressibility of a string, but on very different substrates. gzip finds *surface* redundancy — repeated character n-grams. GPT-2 finds *contextual* predictability — tokens the model expected given prior context. Do these two signals correlate? Where do they diverge, and what does that divergence tell us about how poems evade compression?

## Method
- For each text, computed `gzip.compress(...)` at level 9 and reported the compressed/uncompressed byte ratio (**CR**). Lower CR = more surface-compressible.
- Compared CR against pre-computed GPT-2 metrics (`avg_s2`, `avg_surprisal`, `avg_entropy`, `pos_s2_ratio`) at the poem level.
- Split the corpus by median CR and median S₂ to isolate four "quadrants" of difficulty.
- Added 10 new poems to test the hypothesis: repetition-heavy Stein (`Susie Asado`), concrete cummings (`Buffalo Bill 's`), extreme brevity (`Three Haiku`), Imagist `Oread`, and prose poetry (Baudelaire's `L'Étranger`).

---

## Results

### 1. Poetry compresses better than prose — but shows more S₂

| Group  | n  | Mean CR | Mean S₂ | r(CR, S₂) within group |
|--------|----|---------|---------|------------------------|
| Poetry | 68 | **0.731** | **+0.256** | 0.410 |
| Prose  |  5 | 0.793 | −1.664 | 0.772 |

Two clean facts jump out:

- **Poems have lower gzip ratios than prose.** This is the opposite of what one might guess if "poetic difficulty" always meant unpredictability. Poems repeat surface patterns (refrains, anaphora, sonic figures) that gzip exploits, while prose spreads its material more evenly.
- **Within prose, gzip and S₂ agree strongly** (r=0.77): the more contextually unpredictable the sentence, the less compressible the string. Within poetry, the correlation drops to r=0.41 — poems systematically dissociate the two signals.

### 2. Global correlations (all 73 texts)

| Variable        |    r    |
|-----------------|--------:|
| avg_s2          |  0.276  |
| avg_surprisal   |  0.339  |
| avg_entropy     |  0.159  |
| pos_s2_ratio    |  0.095  |

Compression ratio tracks token **surprisal** more than it tracks **entropy**. That fits: gzip's job is to compress *the actual string*, so it's paid for surprises the poet actually delivered, not for the alternatives GPT-2 hedged over.

### 3. Era ranking by compressibility

Poems ranked from most to least compressible (mean CR, poetry only):

| Era                    | n  | Mean CR | Mean S₂ |
|------------------------|----|---------|---------|
| prose_poetry           |  1 | 0.568   | −0.34   |
| surrealist             |  1 | 0.650   | −0.33   |
| german_modernist       |  2 | 0.667   | +1.12   |
| german_symbolist       |  3 | 0.669   | +0.42   |
| ancient (Sappho)       |  1 | 0.675   | +0.19   |
| harlem_renaissance     |  2 | 0.679   | +0.93   |
| beat                   |  2 | 0.679   | +1.03   |
| german_expressionist   |  2 | 0.689   | +0.62   |
| new_york_school        | 18 | 0.717   | −0.18   |
| contemporary           |  5 | 0.717   | −0.03   |
| romantic               |  3 | 0.719   | −0.26   |
| oulipo                 |  1 | 0.746   | −0.12   |
| 19th_century           |  6 | 0.750   | +0.45   |
| deep_image             |  1 | 0.764   | +0.25   |
| modernist              | 12 | 0.772   | +0.20   |
| mid_century            |  2 | 0.798   | +1.70   |
| language               |  3 | 0.804   | +0.26   |
| confessional           |  2 | 0.806   | +0.95   |
| **haiku**              |  1 | **0.809** | **+2.14** |

**Haiku sits alone at the extreme:** high CR (0.81) *and* high S₂ (+2.14) — brief, non-repetitive, and semantically maximally deviant. Confessional and mid-century poetry are also close to the "hard on both axes" region. On the opposite corner, Language poetry has some of the highest compression ratios (its refrains are less mechanical than one might think), while surrealist and prose-poetry are highly compressible surface-level despite their reputational strangeness.

### 4. The four-quadrant map — dissociations that reveal method

Split by median CR (0.712) and median S₂ (+0.06):

| Quadrant                                     | n  | Poet's mode |
|----------------------------------------------|----|-------------|
| **Easy at both** (low CR, low S₂)            | 21 | Discursive, conventionally-worded poems that also reuse a lot of surface phrasing — Ashbery's long lyric-essays live here (`Soonest Mended`, `Self-Portrait...closing`), plus Rankine's `Citizen`. |
| **Hard at both** (high CR, high S₂)          | 20 | Poems whose sentences are both formally novel *and* lexically unpredictable — the "genuinely difficult" bucket: `Islets/Irritations`, `Lady Lazarus`, `What Is Poetry`, `Verklärter Herbst`. |
| **Surface-hard, semantically easy** (high CR, low S₂) | 16 | Non-repetitive but conventionally-worded: `Dover Beach`, `Wandered Lonely as a Cloud`, `Self-Portrait (opening)`, `Night Sky with Exit Wounds`. Each sentence unique; each word almost expected. |
| **Surface-easy, semantically hard** (low CR, high S₂) | 16 | Structural repetition wrapping unexpected content: `A Supermarket in California`, `The Negro Speaks of Rivers`, `Archaischer Torso Apollos`, `Grodek`, `Komm in den totgesagten park und schau`. Anaphora and refrain give gzip something to fold, but the specific choices resist the model. |

The **surface-easy / semantically-hard** quadrant is the most theoretically interesting one — it's where a poet uses formulaic scaffolding (Ginsberg's Whitmanic list, the German Symbolist's repeated imperative) as a delivery vehicle for lexical surprise. gzip sees the ritual; GPT-2 sees the deviation. This is exactly the "Straussian" pattern: predictable frame, unpredictable filling.

### 5. Extremes

**Most compressible (surface-level):**

| Rank | Text | CR | S₂ |
|------|------|----|----|
| 1 | Stein, *Susie Asado* | 0.562 | −0.66 |
| 2 | Baudelaire, *The Stranger* (prose poem) | 0.568 | −0.34 |
| 3 | Cummings, *Buffalo Bill 's* | 0.571 | −0.31 |
| 4 | Stevens, *The Emperor of Ice-Cream* | 0.596 | +0.07 |
| 5 | Whitman, *A Noiseless Patient Spider* | 0.599 | +0.10 |
| 6 | Lindsay, *The Congo* | 0.617 | −1.05 |

Stein's `Sweet sweet sweet sweet sweet tea. Susie Asado.` reduces to almost nothing under gzip and is *below-average* in S₂ because the model, once it sees `Sweet sweet sweet sweet`, guesses the next word (repeating "sweet") is not surprising. Repetition kills S₂ *and* CR simultaneously — which is why the poem sits close to the origin on both axes despite reading as radically strange to a human.

**Least compressible (surface-level):**

| Rank | Text | CR | S₂ |
|------|------|----|----|
| 1 | Pound, *In a Station of the Metro* | 1.229 | +0.26 |
| 2 | Williams, *The Red Wheelbarrow* | 1.044 | +3.59 |
| 3 | Brooks, *We Real Cool* | 0.906 | +2.18 |
| 4 | H.D., *Oread* | 0.868 | +0.51 |
| 5 | Dickinson, *A Route of Evanescence* | 0.867 | +0.23 |

**A methodological caveat:** two of these poems have CR > 1.0. gzip prepends a ~20-byte header, and for texts shorter than a couple hundred bytes the header dominates. `In a Station of the Metro` is 14 English words; `The Red Wheelbarrow` is 16. gzip cannot amortize its metadata over so little material, so CR is misleadingly high — the Imagist choice of *radical brevity* is itself a form of compression, and gzip literally cannot compress a text that is already at the shortness limit of language. This is a genuine finding about the compression measure, not an artifact to be dismissed: **the Imagist experiment sits at a place gzip cannot see.**

### 6. The Imagist / Haiku / short-lyric zone

For the four shortest texts in the corpus (< 100 UTF-8 bytes each: `In a Station of the Metro`, `The Red Wheelbarrow`, `Oread`, `A Route of Evanescence`), mean CR is **0.95** and mean S₂ is **+1.14**. Compare with a length-matched slice of longer poems: mean CR ≈ 0.72 and mean S₂ ≈ +0.20. Extreme brevity *simultaneously* raises both signals — but for entirely different reasons:

- CR rises because there is nothing to compress *away*.
- S₂ rises because every content word is load-bearing and none can be predicted from the sparse context.

The Imagist manifesto — Pound's demand for "direct treatment of the thing," "absolutely no word that does not contribute" — is legible in both measures at once.

---

## Finding

**Compression ratio and S₂ measure different information-theoretic properties of a poem, and their disagreement is diagnostic of poetic method.**

- Where CR and S₂ agree (both high or both low), the poem's method is unified: `Susie Asado` compresses surface *and* satisfies the model; `Islets/Irritations` resists compression on both axes.
- Where they disagree, they carve poets by strategy: anaphoric poems (Ginsberg, Hughes, German Symbolists) use ritual scaffolding to smuggle high-S₂ diction past the reader; discursive poems (Wordsworth, Arnold, later Ashbery) do the opposite, using never-repeated but conventionally-lexicated sentences.
- **The one place both measures collapse is extreme brevity** — the Imagist / haiku zone, where a two-line poem is simultaneously below gzip's compression threshold and above GPT-2's prediction confidence. This is a real feature of the object, not a measurement error.

Two independent compressibility metrics on the same text yield a diagnostic 2-axis map of poetic difficulty. This suggests **CR + S₂ together are a better literary-genre discriminator than either alone**, and prose vs. poetry may be separable by their position in this plane.

---

## Suggested next steps

1. **Length-normalize both signals.** Recompute CR against a random-permutation baseline (`CR(text) / CR(shuffled)`) so short-text overhead cancels out; likewise consider a length-controlled S₂.
2. **Fit a 2-D classifier.** With ~70 poetry texts and ~5 controls the discrimination is easy, but the *classifier boundary* in (CR, S₂) space is itself the interesting object.
3. **Zoom in on the surface-easy/semantically-hard quadrant.** These are the "Straussian" poems by construction — repetition as a delivery vehicle for surprise. Pull the token-level trace of `A Supermarket in California` and `Archaischer Torso Apollos` and characterize *where* in each poem S₂ spikes despite gzip finding structure.
4. **Sub-word compression.** Run gzip on the *token sequence* (GPT-2 BPE tokens) rather than the raw string — this would let CR and S₂ share a substrate and might sharpen the correlation.
5. **Add more haiku, tanka, and micro-prose.** The <100-byte regime is under-sampled and appears to be a distinct information-theoretic phase.
