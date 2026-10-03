# Information Feet: Do S2 Sequences Form Iambic, Trochaic, or Anapestic Patterns?

**Date:** 2026-10-03  
**Experiment:** `experiments/information_feet.py`  
**Corpus:** 187 poems (filtered to ≥20 artifact-free tokens)  
**Builds on:** `s2_spectral_periodicity.md` (FFT periodicity), `s2_markov_transitions.md` (state transitions)

---

## Research Question

In classical prosody, syllable stress organizes into "feet": iambs (da-DUM), trochees
(DUM-da), anapests (da-da-DUM), dactyls (DUM-da-da). If we map S2 to
**information stress** (H = S2 > 0.5, L = S2 ≤ 0.5), do poems have characteristic
bigram and trigram patterns — information feet — analogous to metrical feet?

**Three hypotheses tested:**
1. *H1 (Iambic Default)*: English poetry, predominantly iambic, should show more LH
   (iamb-like) than HL (trochee-like) patterns in information space.
2. *H2 (Era Differentiation)*: Metrical eras should show stronger iambic information
   patterns than free verse eras.
3. *H3 (Anapestic Ballad)*: Ballads with anapestic meter should show more LLH trigrams.

**All three hypotheses are rejected.** The actual findings are more interesting.

---

## Finding 1: Poetry Is Near-Symmetric; Prose Is Trochaic

At threshold S2 > 0.5, the global bigram distribution is:

| Bigram | Observed | Null (independence) | Deviation |
|--------|----------|--------------------:|----------:|
| LH (iamb-like) | 20.7% | 21.2% | −0.5% |
| HL (trochee-like) | 21.0% | 21.2% | −0.2% |
| LL (pyrrhic-like) | 48.6% | 48.5% | +0.1% |
| HH (spondee-like) | 9.6% | 9.2% | **+0.4%** |

**Key finding**: Poetry shows almost zero iambic-vs-trochaic asymmetry (iambic dominance
= 0.981). The biggest deviation from independence is in HH — S2 spikes cluster
together slightly more than chance.

| Group | Mean Iambic Dominance | H rate |
|-------|-----------------------|--------|
| Prose control | **0.855** | ~20% |
| All poetry | **0.981** | 30.4% |
| Metrical eras | 0.988 | 30.6% |
| Free verse eras | 0.984 | 30.4% |

The crucial comparison is **prose vs. poetry**:
- Prose shows strongly **trochaic** information structure (HL 17% more common than LH)
- Poetry approaches **symmetric** information rhythm

Under independence, the iambic dominance is always 1.0 regardless of H rate.
Prose's deviation to 0.855 is therefore a genuine structural signal: prose **front-loads**
information (content words / stressed positions come first in phrases, then decay),
creating trochaic information patterns. **Poetry neutralizes this asymmetry.**

---

## Finding 2: Metrical Tradition Does Not Predict Information Rhythm

All three prosodic hypotheses fail:

**H1 rejected**: Poetry is slightly *trochaic* (0.981), not iambic. Traditional meter
does not map onto information structure.

**H2 rejected**: Metrical eras (0.988) and free verse eras (0.984) are virtually
identical in iambic dominance. The 0.004 difference is smaller than the within-era
standard deviations.

**H3 rejected**: Ballads show *lower* LLH (anapest-like) proportion (0.1209) than
most poetry eras, not higher.

**Interpretation**: Poetic meter organizes syllable stress, but it does not determine the
**information pattern** of word choice. A poem can be metrically regular (alternating
stressed and unstressed syllables) while its S2 pattern follows different rules —
because S2 is driven by semantic/pragmatic unexpectedness, not by syllabic position.

---

## Finding 3: The Most Iambic and Trochaic Poems

### Most Iambic Information Structures (LH/HL ratio > 1.0)

| Author | Title | Iamb Dom | Era |
|--------|-------|----------|-----|
| W.C. Williams | The Red Wheelbarrow | 1.250 | modernist |
| Kobayashi Issa | Three Haiku (translated) | 1.111 | haiku |
| Austin Dobson | In After Days (rondeau) | 1.100 | fixed_form |
| Elizabeth Bishop | One Art | 1.083 | mid_century |
| Langston Hughes | Harlem | 1.077 | harlem_renaissance |
| Langston Hughes | A Dream Deferred | 1.077 | harlem_renaissance |
| Matthew Arnold | Dover Beach | 1.067 | 19th_century |
| T.S. Eliot | Prufrock (opening) | 1.062 | modernist |
| Claudia Rankine | Citizen (excerpt I) | 1.050 | prose_poetry |

### Most Trochaic Information Structures (LH/HL ratio < 0.9)

| Author | Title | Iamb Dom | Era |
|--------|-------|----------|-----|
| Blake | The Sick Rose | 0.909 | romantic |
| E. Williams | For Spacious Skies | 0.900 | concrete |
| Wordsworth | I Wandered Lonely as a Cloud | 0.889 | romantic |
| Bruce Andrews | Islets/Irritations | 0.889 | language |
| Gwendolyn Brooks | We Real Cool | 0.857 | mid_century |
| Prose controls | (3 examples) | 0.667–0.857 | control |
| Eugen Gomringer | silencio | 0.500 | concrete |

**Pattern in iambic poems**: Short, compressed, image-based poems with deliberate
syntactic compression (Wheelbarrow, haiku, Hughes). These poems withhold their
key content word until after establishing context — building toward revelation.

**Pattern in trochaic poems**: Poems that open immediately with strong content words
("I wandered", "The Sick Rose", "We Real Cool", "silencio"). The information peak
hits first, then the poem explains or expands. This is the "front-loaded statement"
structure that also characterizes prose.

---

## Finding 4: Haiku Is the Most Iambic and Anapestic Tradition

| Group | Mean Iamb Dom | P(LLH) anapest-like |
|-------|---------------|---------------------|
| Haiku | **1.037** | **0.180** |
| Metrical eras (avg) | 0.988 | 0.143 |
| Free verse eras (avg) | 0.984 | 0.141 |
| Control | 0.855 | 0.072 |

Haiku — with 5-7-5 syllable structure — is the one tradition showing both:
1. More LH (iamb) than HL (trochee) bigrams
2. Highest LLH (anapest-like) trigram rate

The haiku structure may naturally create LLH patterns because:
- The kigo (season word) and kireji (cutting word) tend to appear late in the 5-7-5 sequence
- Two low-S2 establishment tokens precede the high-S2 "cut" moment
- This is the information-theoretic version of the haiku's traditional "juxtaposition"

---

## Finding 5: Robustness Across Thresholds

The near-symmetry of poetry is robust across all thresholds:

| Threshold | Iamb Dom | % poems > 1.0 |
|-----------|----------|----------------|
| S2 > −1.0 | 0.987 | 9.6% |
| S2 > −0.5 | 0.983 | 7.5% |
| S2 > 0.0 | 0.981 | 5.3% |
| **S2 > 0.5** | **0.981** | **5.9%** |
| S2 > 1.0 | 0.985 | 5.9% |
| S2 > 2.0 | 0.986 | 2.7% |

The trochaic bias is always present (< 1.0), and always small (≤ 0.02 from neutral).
The prose deficit (0.855) is robust and large by comparison.

---

## Theoretical Interpretation

The core finding — **prose is trochaic, poetry is neutral** — has a natural explanation
in information theory:

**Prose follows topic-comment structure**: Subject → predicate → modifier.
The *subject* (topic) tends to be the most predictable part (often re-mentioned, given
information). The *new information* comes in the predicate or complement. But in
sentence-initial position, GPT-2 is often more uncertain (high entropy) at the start
of a new clause, meaning even a "given" subject can have moderate S2. After the subject,
the verb/predicate can be more predictable (HL = trochee).

Actually, the simpler explanation: prose sentences begin with their main content word
(the "subject" = content word = high S2), followed by function words and modifiers
(low S2). This creates front-loaded, trochee-like patterns.

**Poetry disrupts this front-loading**: By inverting syntax (postpositive adjectives,
unexpected line breaks, delayed main verbs), poetry delays or defers the information
peak. The result is that L and H tokens are distributed more symmetrically — neither
consistently rising nor falling.

The most "iambic" poems — Williams, Hughes, Bishop — are those that most dramatically
withhold their key word: "a red wheel / barrow" holds the key noun across a line break;
"Harlem" ends with the explosive "explode" after much qualification.

---

## Implications for the S2 Framework

1. **Information feet ≠ metrical feet**: S2 rhythm is decoupled from traditional prosody.
   The two capture different dimensions of poetic structure.

2. **Prose's trochaic signature** is a new discriminator: beyond mean S2, the *direction*
   of S2 change within bigrams separates prose from poetry more cleanly for short texts.

3. **The "iambic information poem"**: A new sub-category worth tracking — poems where
   information stress builds rather than falls. These tend to be compressed, late-revelation
   poems (haiku, imagist, confessional).

4. **HH clustering** (spondee-like): The slight excess of HH over the null model confirms
   that S2 spikes cluster. Surprise is not isolated but comes in small bursts.

---

## Next Steps

- **Within-line information foot analysis**: Does the metrical foot (iambic pentameter)
  correspond to LH patterns within the line, even if the poem-level average is neutral?
- **Syntax-aware analysis**: Does iambic dominance correlate with subject-final word order
  (more typical of poetry: adjective-noun, object-verb inversions)?
- **Reader experience modeling**: Iambic information poems may feel "more satisfying"
  because each H moment arrives as a resolution; test with reader-response data.
- **Cross-linguistic expansion**: Do Japanese haiku (originally in Japanese) show stronger
  LLH patterns than translated haiku?
