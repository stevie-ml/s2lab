# Two Roads to Surprise: Oulipo Constraint vs. Surrealist Dream Logic

**Date:** 2026-10-30  
**Experiment:** `experiments/oulipo_vs_surrealist.py` → `results/oulipo_vs_surrealist.json`  
**Corpus:** 4 Oulipo poems, 8 surrealist poems, plus found_poetry (8), language poetry (6), modernist (25), romantic (21) as reference  
**Artifact filter:** p(newline) < 0.9 applied throughout

---

## Research Question

Both Oulipo and Surrealism generate unexpected language — but through opposing mechanisms:

- **Oulipo** applies *formal mathematical constraint* (lipograms, N+7 word substitution, permutations). The poet cannot use certain words; the constraint overrides whatever the language naturally wants to say.
- **Surrealism** applies *automatic writing and dream logic*. The poet follows interior associations, not linguistic convention.

Do these produce different information-theoretic signatures? Specifically:

- Does Oulipo's mechanical constraint create *uniform* high-S2 (the override applies everywhere, systematically)?
- Does Surrealism's dream logic create *spiky* S2 (unexpected bursts embedded in more conventional passages)?
- Does Oulipo override the model *when it's most confident* (the constraint prevents the obvious choice)?
- Does Surrealism extend moments of *natural model uncertainty* (pushing ambiguous moments further into the unexpected)?

---

## Results (N=7 Oulipo, expanded corpus)

| Group | N | Mean S2 | StdDev(S2) | Pos Ratio | Kurtosis | Spike Entropy | Confident Wrong |
|---|---|---|---|---|---|---|---|
| **oulipo** | 7 | **-0.024** | 3.968 | 36.4% | **1.121** | **5.994 bits** | **16.3%** |
| **surrealist** | 8 | **-0.609** | 3.490 | 31.6% | **1.540** | **6.292 bits** | **11.9%** |
| language | 6 | -0.518 | 3.627 | 32.2% | 1.043 | 6.350 bits | 9.6% |
| found_poetry | 8 | -0.621 | 3.126 | 27.1% | 3.657 | 5.304 bits | 18.9% |
| modernist | 27 | -0.427 | 3.760 | 36.2% | 1.231 | 6.779 bits | 8.7% |
| romantic | 21 | -0.496 | 3.606 | 34.6% | 1.358 | 6.929 bits | 8.9% |

**Spike entropy** = mean entropy (model uncertainty) at positions where the poet surprises the model  
**Confident wrong** = fraction of spike positions where model entropy < 3.0 bits (model was highly confident but poet chose differently)

---

## Per-Poem Breakdown

### Oulipo poems (ordered by constraint type)

| Poem | Author | Constraint | Mean S2 | Kurtosis |
|---|---|---|---|---|
| Variations on A (excerpt) | Georges Perec | lipogram (no E) | -0.443 | 1.173 |
| The Lipogram | Georges Perec | lipogram (no E) | -0.597 | 0.100 |
| Eunoia: Chapter A (excerpt) | Christian Bök | univocalic (A only) | +0.063 | 0.586 |
| **Eunoia: Chapter E (excerpt)** | Christian Bök | univocalic (E only) | **+1.772** | **-0.733** |
| If I Told Him | Gertrude Stein | repetition pattern | +0.056 | 2.152 |
| Cent Mille Milliards (Sonnet 1) | Raymond Queneau | combinatorial | -0.749 | 0.026 |
| **S+7: Genesis** | Jean Lescure | N+7 substitution | -0.272 | **4.538** |

### Surrealist poems

| Poem | Author | Mean S2 | Kurtosis |
|---|---|---|---|
| Free Union | André Breton | -0.680 | 1.066 |
| I Have Dreamed of You So Much | Robert Desnos | -0.430 | 1.258 |
| Somnambule Ballad | Federico García Lorca | -0.665 | 2.092 |
| Black Stone Lying on a White Stone | César Vallejo | **+0.234** | **2.719** |
| The Curve of Your Eyes | Paul Éluard | -0.807 | 2.473 |
| Walking Around | Pablo Neruda | -0.132 | 1.269 |
| Departure | Pierre Reverdy | **-1.581** | **-0.169** |
| The Sleeper in the Valley | Arthur Rimbaud | -0.814 | 1.610 |

---

## Key Findings

### 1. Oulipo Is Not One Thing: Constraint Type Governs S2 Shape (Major Finding)

The expanded corpus reveals that "Oulipo" contains at least three distinct information-theoretic profiles:

**Univocalics (Bök)** — *Chapter A*: mean S2=+0.063, kurtosis=0.586. *Chapter E*: mean S2=**+1.772**, kurtosis=**-0.733**  
The Chapter E univocalic achieves the highest mean S2 of any Oulipo poem by far — the model is almost never right — while simultaneously having *platykurtic* distribution (lighter tails than normal). E-only writing creates uniform, sustained high surprise. The constraint is omnipresent and always visible.

**Lipograms (Perec)** — mean S2 ≈ -0.5, kurtosis ≈ 0.1–1.2  
Surprisingly low kurtosis, especially the "Lipogram" (kurtosis=0.100). The lipogram distributes surprise almost uniformly — the most "Gaussian" Oulipo profile. The constraint is pervasive but the violations it forces are spread evenly.

**N+7 Substitution (Lescure)** — mean S2=-0.272, kurtosis=**4.538**  
The most extreme kurtosis in the entire Oulipo group (and among the highest in the whole corpus). N+7 replaces every noun with the seventh noun following it in a dictionary. This occasionally produces wildly unexpected substitutions ("God" → "hebdomad", "evening" → "eviction") while leaving the surrounding structure intact. The result is highly spiky S2: mostly normal text punctuated by occasional extreme surprises.

**Combinatorial (Queneau)** — mean S2=-0.749, kurtosis=0.026  
Near-zero kurtosis — the most perfectly uniform surprise distribution. The "Hundred Thousand Billion Poems" is a matrix of interchangeable sonnet lines. No position is systematically more or less surprising than others.

### 2. The "Confident Wrong" Asymmetry

**Oulipo's confident-wrong rate (16.3%) exceeds Surrealism's (11.9%).**

At high-S2 positions, Oulipo more often surprises the model when it was highly confident (entropy < 3.0 bits). This confirms the Oulipo mechanism: constraint overrides the model's strong predictions. Surrealism, by contrast, tends to surprise the model at positions where it was already uncertain (spike entropy = 6.29 vs Oulipo's 5.99 bits).

### 3. Surrealism is Spikier Than Average Oulipo (Kurtosis)

**Surrealism group kurtosis (1.540) > Oulipo group (1.121).**

This contradicts the original hypothesis that Oulipo would be more uniform. But the group average masks huge within-Oulipo variation: N+7 (kurtosis=4.538) far exceeds any surrealist poem, while lipograms and combinatorial poetry are flatter than surrealism. Oulipo is *more heterogeneous* in kurtosis than surrealism.

### 4. Oulipo Has Higher Mean S2 

**Oulipo mean S2 (-0.024) is much less negative than Surrealism (-0.609).**

The constraint produces more globally elevated deviation on average; surrealism produces lower baseline but occasionally higher spikes. Oulipo is globally more surprising; surrealism is locally more extreme.

### 5. The Outlier: Found Poetry

**Found poetry has the highest kurtosis (3.657) among all genre groups.**

Found poetry repurposes non-poetic text as poetry: mostly conventional language punctuated by extreme S2 spikes from recontextualized juxtapositions. It shares the "spiky flat landscape" profile with N+7 — both are *appropriation aesthetics* that keep most language normal while producing occasional extreme surprises.

### 6. The Gertrude Stein Anomaly

**"If I Told Him" has kurtosis 2.152, closer to surrealist spikiness than classical Oulipo.**

Stein (who predates Oulipo) is sometimes called proto-Oulipian. Informationally, her repetition-with-variation creates a surrealist-style S2 profile: not the uniform override of lipogram or combinatorial, but spiky moments embedded in repetitive base. Her work may represent a third category — *rhythmic constraint* rather than lexical constraint.

---

## Interpretation: A Taxonomy of Constrained Surprise

The data suggests not two but *at least four* distinct information-theoretic strategies for generating unexpected language:

**Strategy 1 — Uniform constraint (lipogram, combinatorial)**  
Surprise is spread evenly across the text. Low kurtosis, moderate mean S2. The constraint is always present and its effects are always visible. (*Perec lipogram, Queneau combinatorial*)

**Strategy 2 — Escalating constraint (univocalic)**  
High mean S2, platykurtic distribution. The single-vowel constraint creates globally elevated deviation that doesn't spike — there's no "normal" baseline to spike from. (*Bök Eunoia Chapter E*)

**Strategy 3 — Substitutive rupture (N+7, found poetry)**  
Low to moderate mean S2 but very high kurtosis. The surrounding text is relatively normal; isolated substitutions create extreme spikes. Surprise is local and dramatic. (*Lescure S+7, found poetry*)

**Strategy 4 — Uncertainty extension (surrealism)**  
Moderate kurtosis, lower mean S2, spike entropy higher than other groups. Surprise occurs at positions of model uncertainty — the poet extends and amplifies ambiguity rather than overriding confidence. (*Breton, Éluard, Lorca*)

These map onto aesthetic philosophies:
- Lipogram/combinatorial: surprise as *omnipresent structural constraint*
- Univocalic: surprise as *complete alternative universe* (every word is wrong by conventional standards)
- N+7/found poetry: surprise as *rupture* in an otherwise ordinary landscape
- Surrealism: surprise as *deep following* of language's own uncertainties

---

## Limitations

1. Small N for Oulipo (4 poems) — findings should be treated as preliminary
2. The "Oulipo" group is heterogeneous: Perec (lipogram), Stein (repetition), Bök (univocalics) use very different constraints
3. Gini coefficient computation has a sign error in the current implementation — not reported here
4. Translations of surrealist poets (Lorca, Neruda, Vallejo, Éluard) introduce an additional source of S2 variation from translation choices

---

## Suggested Next Steps

1. **The S+7 token catalog**: At the N+7 high-S2 spikes, what specific substitutions (e.g., "God"→"hebdomad", "evening"→"eviction") are most extreme? Can we detect the dictionary-offset mechanism from S2 patterns alone?
2. **Stein as category**: Is "repetition-with-variation" consistently somewhere between Oulipo and Surrealism in information space? Test with Gertrude Stein's other works.
3. **The Reverdy singularity**: Reverdy (kurtosis=-0.169) is the only platykurtic surrealist. His imagist-adjacent prose poems may be a bridge genre. Investigate whether prose poetry generally has platykurtic S2.
4. **Constraint specificity**: Test whether different lipogram lengths (avoiding A vs. E vs. a rare letter) produce different S2 levels — does frequency of avoided letter predict strength of deviation?
5. **The Bök E/A contrast**: Eunoia Chapter A (kurtosis=0.586, mean S2=+0.063) vs Chapter E (kurtosis=-0.733, mean S2=+1.772) is striking. E is a more common vowel, so avoiding it is harder → higher S2. Verify: does E-vowel constraint produce higher surprisal because GPT-2 expects E more often?
