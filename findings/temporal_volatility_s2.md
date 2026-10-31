# Temporal Volatility of S₂: How Within-Poem Spread Changes Across Literary History

**Date:** 2026-10-31  
**Experiment:** `experiments/temporal_volatility_s2.py`  
**Results:** `results/temporal_volatility_s2.json`  
**Corpus:** 294 English poems (years 1600–2026), excluding control/parody/light-verse  
**Builds on:** `temporal_evolution_s2.md`, `s2_volatility_signature.md`

---

## Research Question

The `temporal_evolution_s2` study tracked **mean S₂** across literary periods and found an
inverted-U arc peaking at Victorian/Modernist. The `s2_volatility_signature` study showed that
`std_s2` (within-poem spread) is an orthogonal stylometric feature — two poets can have
identical mean S₂ but radically different volatility profiles.

**This study asks:** Does `std_s2` — the volatility of the S₂ signal within a poem —
show its own temporal arc across literary history? Are certain eras characterized by more
uniform surprise, and others by violent spikes against a conventional backdrop?

**Hypothesis:** Modernism would produce high volatility (isolated breaks from convention against
a more regular baseline); Romanticism and Language poetry would show low volatility (either
uniformly elevated uncertainty or uniformly low S₂ respectively).

---

## Method

- English-language poems (1600–2026), N = 294
- Excluded: control prose, parody, clerihew, limerick, double dactyl, found poetry, song lyrics
- Grouped by decade bins (see table)
- Per poem: `std_s2` from `corpus_results.json` summaries (no re-tokenization needed)
- Per era: mean and SD of `std_s2`, mean `avg_s2`, mean `max_s2`
- Linear correlation: Pearson r (year vs `std_s2`)
- Quadrant analysis: global means as thresholds (mean S₂ = 0.359, mean Std_S₂ = 5.165)

---

## Main Findings

### 1. No Linear Trend — But Mid-Century Is the Volatility Peak

| Period | N | Mean S₂ | Mean Std_S₂ | Mean Max_S₂ | SD of Std_S₂ |
|--------|---|---------|-------------|-------------|---------------|
| 17th C | 19 | 0.346 | 4.977 | 20.953 | 1.499 |
| 18th C | 23 | 0.312 | 5.004 | 22.403 | 1.407 |
| Early Romantic | 35 | 0.310 | 5.225 | 25.183 | 1.324 |
| Victorian | 54 | 0.381 | 5.156 | 23.991 | 1.176 |
| **Modernist** | **56** | 0.338 | 5.134 | 23.065 | 1.530 |
| **Mid-Century** | **27** | **0.790** | **5.987** | **26.596** | **2.158** |
| Postmodern | 41 | 0.323 | 5.084 | 21.968 | 1.637 |
| Late/Language | 27 | 0.010 | 4.725 | 23.120 | 1.337 |
| Contemporary | 12 | 0.554 | 5.210 | 21.932 | 1.279 |

**Linear trend:** r = +0.061, slope = +0.001 Std_S₂/year — essentially flat across the
full 1600–2026 range. History does not show a monotone increase or decrease in volatility.

**But the non-linear pattern is clear:** Volatility peaks at Mid-Century (1930–1959),
not Modernist (1900–1929) as hypothesized. Mid-Century is uniquely characterized by
*both* high mean S₂ and high volatility — the only "High S₂, High Volatility" era until
Contemporary. Modernism, despite its reputation for difficulty, sits in the
"Low S₂, Low Volatility" quadrant alongside 17th/18th Century poetry.

### 2. Four Quadrants of S₂/Volatility Space

Using the global means (S₂ = 0.359, Std_S₂ = 5.165) as thresholds:

| Quadrant | Eras | Interpretation |
|----------|------|----------------|
| **High S₂, High Volatility** | Mid-Century, Contemporary | Concentrated spikes; long conformist stretches punctuated by intense ruptures |
| **High S₂, Low Volatility** | Victorian | Sustained elevated surprise; the unusual token appears uniformly throughout |
| **Low S₂, High Volatility** | Early Romantic | Broadly uncertain context but occasional extreme spikes (Keats/Shelley compound nouns, Wordsworth proper nouns) |
| **Low S₂, Low Volatility** | 17th C, 18th C, Modernist, Postmodern, Late/Language | Either uniform conventionality or structural difficulty invisible to GPT-2 |

The **Language poetry** datum (Low S₂ = 0.010, Low Vol = 4.725) is theoretically the
most significant: Language poetry achieves its radical defamiliarization through syntactic
and conceptual disruption that does not register as token-level surprisal. The tokens
themselves are ordinary; their *arrangement* creates difficulty. GPT-2 cannot see this.

### 3. Mid-Century: High Mean AND High Spread

Mid-Century's std_s2 SD across poems (2.158) is the highest of any era — meaning not only
is it the most volatile era on average, but it is also the most *internally diverse*.
Poets within this period vary enormously in their volatility profiles. This is the era of
Confessional poetry (Plath, Lowell), New Criticism, and early New York School — wildly
different aesthetic programs using different volatility strategies:

- **Plath** (mean Std_S₂ = 6.917): high-volatility confessional, violent spikes against
  domestic baseline
- **Brooks** (mean Std_S₂ = 9.835): extreme volatility, consistent with compression of
  complex urban imagery into tight formal structures

### 4. Most Volatile Poets by Std_S₂

| Author | N | Mean Std_S₂ | Mean Avg_S₂ | Era |
|--------|---|-------------|-------------|-----|
| William Carlos Williams | 4 | 10.116 | 3.103 | modernist |
| Gwendolyn Brooks | 2 | 9.835 | 2.181 | mid_century |
| Carl Sandburg | 2 | 7.950 | 2.540 | modernist |
| E.E. Cummings | 3 | 7.816 | 1.577 | modernist |
| Kobayashi Issa | 3 | 7.513 | 1.153 | haiku |
| Langston Hughes | 3 | 7.152 | 1.085 | harlem_renaissance |
| Sylvia Plath | 2 | 6.917 | 0.947 | confessional |

**William Carlos Williams** tops the list (10.116 mean Std_S₂) — despite being classified
as "modernist," his observed volatility makes him individually a Mid-Century-style writer.
This is consistent with his aesthetic: "no ideas but in things" — concrete imagism creates
sudden high-surprisal specific nouns against a plain prose syntax. The strategy is
*juxtaposition*, and juxtaposition shows up as volatility.

### 5. Most Stable Poets

| Author | N | Mean Std_S₂ | Mean Avg_S₂ | Era |
|--------|---|-------------|-------------|-----|
| Russell Edson | 2 | 3.200 | −0.387 | prose_poetry |
| Christopher Smart | 2 | 3.370 | −0.348 | 18th_century |
| William Shakespeare | 3 | 3.514 | −0.618 | victorian (era label) |
| Georges Perec | 2 | 3.587 | −0.310 | oulipo |
| Charles Bernstein | 2 | 3.728 | −0.607 | language |
| Alexander Pope | 3 | 3.959 | −0.225 | 18th_century |

Stable-low (low Std_S₂, negative avg_S₂): Shakespeare, Pope, Bernstein — the predictably
structured, the formally rigorous, and the language-experimental all converge here.
**Russell Edson** (prose poetry) is the most stable: his deadpan surrealism relies on
narrative grammar that GPT-2 follows smoothly; the surrealism is conceptual, not lexical.

---

## Theoretical Implications

### The Mid-Century Volatility Paradox

Modernism (1900–1929) was expected to show maximum volatility based on its reputation for
difficulty. Instead, it scores near the global mean. The real peak is **Mid-Century**
(1930–1959). Why?

One interpretation: High Modernism (Eliot, Pound, H.D.) achieves difficulty through
*cultural allusion and intertextuality* — devices that raise surprisal and entropy together
(yielding moderate or low S₂). Mid-Century poets (Brooks, Plath, WCW) achieve difficulty
through *lexical specificity* — naming things (diseases, neighborhoods, tools, brands) in
contexts where GPT-2 was confident about something more generic. This creates high S₂ and
high volatility because the model is briefly confident, then violently wrong.

### GPT-2 Cannot Measure Language Poetry

The Language poetry finding (Low S₂ = 0.010, Low Std_S₂ = 4.725) confirms what the
temporal_evolution study suggested: Language poetry's defamiliarization operates at a
level GPT-2 is blind to. The tokens are common; the syntax is disrupted. This is a **floor
effect** for information-theoretic literary analysis using autoregressive LMs — they measure
lexical surprise, not syntactic surprise at the level Language poetry operates on.

### Volatility as a Dimension of Poetic Style

The orthogonality of mean_S₂ and std_S₂ holds temporally: eras high in one are not
necessarily high in the other. Victorian poetry is the clearest example — high mean S₂
but below-median volatility, suggesting a *sustained* rather than *punctuated* approach
to deviation. Mid-Century is the opposite of Language poetry: both mean and std are maximal.

This 2D (mean, volatility) space may be the right stylometric representation, improving
on mean S₂ alone.

---

## Suggested Next Steps

1. **Regression: Std_S₂ ~ Era + Form**: Control for poetic form (sonnet vs. free verse
   vs. prose poem) within era — is Mid-Century's volatility due to the poets, or to the
   forms they used?

2. **Intra-poem volatility arc**: Does std_S₂ *within* a poem (computed over sliding
   windows) show structure? Opening volatility → settling → spike at closure?

3. **WCW case study**: Williams's 10.116 mean Std_S₂ is exceptional even among modernists.
   A close reading of his S₂ profiles poem by poem would reveal whether this is image-
   driven (red wheelbarrow style) or syntactic.

4. **The Language poetry blind spot**: Test with a model explicitly trained on experimental
   poetry (if available) or with GPT-2 medium/large to see if the scale of the model
   captures more Language poetry surprise.

5. **Max_S₂ as a period fingerprint**: Mean max_S₂ (the highest single S₂ token per poem)
   shows a distinct pattern: Early Romantic peaks at 25.183 (Keats compounds), Mid-Century
   at 26.596. The highest-ever single surprises occur in these two eras.

---

## Data

Full results: `results/temporal_volatility_s2.json`
