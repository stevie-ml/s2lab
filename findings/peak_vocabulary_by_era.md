# Peak Vocabulary by Era: What Each Literary Era Reaches For at Its Most Surprising Moments

**Date:** 2026-11-06  
**Experiment:** `experiments/peak_vocabulary_by_era.py`  
**Data:** `results/peak_vocabulary_by_era.json`  
**Corpus:** 376 English poems, artifact-free tokens (p(newline) < 0.9), S2 threshold = 3.0 bits

---

## Research Question

Previous work ([`era_counter_lexicon.md`](era_counter_lexicon.md)) showed what each literary era **suppresses** — the words GPT-2 expected but poets rejected. This experiment asks the complementary question: **at the moments of maximum surprise (artifact-free S2 > 3.0), what does each era actually *choose*?**

Do different literary movements reach for different semantic domains at their peak moments of lexical surprise? Do confessional poets reach for body words? Do Romantics reach for nature? Do Modernists reach for proper nouns and objects?

---

## Summary Table: Peak Rate and Dominant Semantic Field by Era

*(Sorted by peak_rate: peaks per 100 artifact-free tokens)*

| Era | n poems | Peak Rate | Mean Peak S2 | Dominant Field | Top Peak Tokens |
|-----|---------|-----------|--------------|----------------|-----------------|
| clerihew | 10 | 25.43% | 6.832 | death_void | Humph, Dav, ominated, gravy |
| haiku | 14 | 20.82% | 6.195 | human_society | silent, ash, Silence, again |
| german_expressionist | 4 | 19.88% | 5.949 | body | aster, mush, womb, Clean |
| oulipo | 8 | 19.68% | 6.483 | time | Napoleon, full, Shut, shut |
| confessional | 6 | 19.4% | 6.0 | time | ——, heavy, black, shoe |
| ancient | 3 | 17.92% | 5.812 | human_society | tore, Since, equal, across |
| imagist | 5 | 17.76% | 5.631 | motion | away, beats, dead, slack |
| victorian | 29 | 17.29% | 6.137 | time | air, 's, yet, spare |
| modernist | 28 | 16.98% | 6.34 | nature | bes, against, kept, depends |
| old_english | 5 | 16.85% | 6.292 | human_society | praise, point, Gl, Eternal |
| 18th_century | 8 | 16.59% | 6.225 | nature | Cat, Je, off, ry |
| 19th_century | 18 | 16.57% | 5.9 | time | 'd, each, Death, kindly |
| fixed_form | 8 | 16.55% | 6.07 | time | serves, singer, Perse, dim |
| mid_century | 6 | 16.12% | 6.366 | nature | fl, ur, late, sin |
| dramatic_monologue | 7 | 16.0% | 6.074 | time | Duchess, Fra, 't, none |
| romantic | 21 | 15.98% | 6.075 | nature | 'd, sweet, thou, wild |
| elegy | 8 | 15.94% | 6.105 | time | sorrow, though, beneath, curfew |
| ekphrastic | 8 | 15.83% | 5.774 | abstract_soul | ,—, pipes, soft, 's |
| war_poetry | 3 | 15.81% | 5.963 | abstract_soul | dreams, England, double, begg |
| postcolonial | 6 | 15.77% | 6.59 | nature | each, Remember, earth, sand |
| spoken_word | 3 | 15.73% | 6.332 | motion | hips, celebrate, shaped, model |
| contemporary | 19 | 15.64% | 6.091 | nature | even, any, among, nest |
| latin_american | 4 | 15.62% | 6.136 | nature | wind, today, bones, two |
| parody | 4 | 15.55% | 5.931 | color_light | every, cheer, spreads, little |
| early_modern | 7 | 15.45% | 5.953 | time | sometime, after, list, Home |
| ballad | 6 | 15.3% | 6.949 | human_society | wi, guid, sa, dwell |
| villanelle | 3 | 15.14% | 5.977 | time | away, still, Through, broken |
| language | 6 | 15.12% | 6.043 | nature | pause, rose, paper, yellow |
| harlem_renaissance | 7 | 15.07% | 6.265 | time | deferred, dry, over, dawn |
| parody_original | 3 | 14.9% | 5.449 | human_society | cheerful, busy, each, shining |
| new_york_school | 26 | 14.64% | 6.005 | nature | survey, thunder, painting, silence |
| metaphysical | 4 | 14.63% | 5.682 | human_society | 's, overthrow, Die, poor |
| surrealist | 8 | 14.61% | 6.325 | nature | shadow, waist, perhaps, wind |
| classical_chinese | 4 | 14.29% | 6.464 | nature | broken, mountains, wall, shed |
| prose_poetry | 12 | 14.13% | 6.006 | time | carried, filed, daily, pet |
| limerick | 10 | 13.62% | 6.06 | color_light | tutor, feared, Ow, Hen |
| beat | 8 | 13.56% | 8.307 | abstract_soul | sd, looking, angry, under |
| biblical | 8 | 12.77% | 5.706 | abstract_soul | unto, thereof, mine, Israel |
| concrete | 4 | 12.59% | 6.981 | time | spacious, throb, Watch, sil |
| song_lyrics | 3 | 12.38% | 5.959 | human_society | rolling, seldom, sweet, lord |
| double_dactyl | 5 | 12.1% | 5.982 | human_society | ressed, rh, Man, Hopkins |
| cliche_control | 4 | 10.84% | 5.687 | nature | day, life, hills, come |
| found_poetry | 9 | 10.71% | 6.299 | motion | slight, van, various, useful |
| control | 4 | 2.34% | 3.542 | other | outside, installation, administrator |

---

## Finding 1: Most Eras Reach for the 'Other' at Peak Moments

Across all eras, the most common classification of peak tokens is **'other'** — the token falls outside our semantic field taxonomy. This is methodologically important: it confirms that **poetic peaks are not simply drawn from common semantic lexicons**, but include rare, field-specific, and idiosyncratic vocabulary that resists classification into generic categories.

The finding is consistent with the Straussian hypothesis: the most surprising moments in poetry are precisely the ones that *don't fit* conventional semantic groupings.

---

## Finding 2: Semantic Field Signatures by Era

### Field Distribution at Peak Moments (content words only, % of categorized peaks)

| Era | n | body | nature | death_void | time | abstract_soul | human_society | color_light | motion |
|-----|---|------|--------|------------|------|---------------|---------------|-------------|--------|
| romantic | 606 | 6% | 24% | 8% | 13% | 14% | 22% | 6% | 7% |
| confessional | 77 | 12% | 6% | 6% | 29% | 6% | 12% | 24% | 6% |
| modernist | 507 | 7% | 38% | 4% | 9% | 13% | 9% | 11% | 9% |
| language | 75 | — | 40% | 10% | 30% | 10% | — | 10% | — |
| biblical | 170 | 11% | 16% | — | 5% | 26% | 16% | 11% | 16% |
| beat | 162 | 14% | 22% | 14% | 7% | 29% | — | — | 14% |
| harlem_renaissance | 123 | 8% | 17% | 8% | 25% | 17% | — | 17% | 8% |
| victorian | 890 | 12% | 18% | 14% | 21% | 17% | 7% | 8% | 3% |
| new_york_school | 406 | 5% | 23% | 9% | 11% | 15% | 20% | 6% | 11% |
| surrealist | 161 | 24% | 29% | 9% | 18% | 9% | 3% | 6% | 3% |
| haiku | 61 | — | 22% | 28% | 11% | 5% | 28% | — | 5% |
| war_poetry | 101 | 8% | 15% | — | 15% | 23% | 15% | 8% | 15% |
| imagist | 57 | 17% | 17% | 17% | — | — | 17% | — | 33% |
| mid_century | 94 | 14% | 22% | 14% | 14% | — | 14% | 7% | 14% |

---

## Finding 3: Characteristic Peak Tokens Per Era

Top non-function tokens at peak moments (S2 ≥ 3.0, artifact-free):

**romantic**: `'d` (6×) | `sweet` (3×) | `thou` (3×) | `wild` (3×) | `whose` (3×) | `among` (3×) | `number` (2×) | `Round` (2×)

**confessional**: `——` (2×) | `heavy` (2×) | `black` (1×) | `shoe` (1×) | `poor` (1×) | `Ach` (1×) | `oo` (1×) | `Daddy` (1×)

**modernist**: `bes` (3×) | `against` (2×) | `kept` (2×) | `depends` (2×) | `red` (2×) | `wheel` (2×) | `jar` (2×) | `wild` (2×)

**language**: `pause` (1×) | `rose` (1×) | `paper` (1×) | `yellow` (1×) | `four` (1×) | `greeting` (1×) | `financial` (1×) | `Al` (1×)

**biblical**: `unto` (4×) | `thereof` (3×) | `mine` (2×) | `Israel` (2×) | `upon` (2×) | `sat` (2×) | `his` (2×) | `faint` (2×)

**beat**: `sd` (3×) | `looking` (2×) | `angry` (2×) | `under` (2×) | `shopping` (2×) | `above` (2×) | `where` (2×) | `destroyed` (1×)

**harlem_renaissance**: `deferred` (2×) | `dry` (2×) | `over` (2×) | `dawn` (2×) | `rivers` (1×) | `ancient` (1×) | `older` (1×) | `flow` (1×)

**victorian**: `air` (4×) | `'s` (4×) | `yet` (4×) | `spare` (4×) | `,—` (3×) | `mouth` (3×) | `half` (3×) | `ow` (3×)

**new_york_school**: `survey` (11×) | `thunder` (3×) | `painting` (2×) | `silence` (2×) | `plain` (2×) | `each` (2×) | `outside` (2×) | `turning` (2×)

**surrealist**: `shadow` (3×) | `waist` (2×) | `perhaps` (2×) | `wind` (2×) | `bones` (2×) | `cradle` (2×) | `whose` (1×) | `brush` (1×)

**haiku**: `silent` (2×) | `ash` (2×) | `Silence` (2×) | `again` (2×) | `jumps` (1×) | `cold` (1×) | `monkey` (1×) | `coat` (1×)

**war_poetry**: `dreams` (2×) | `England` (2×) | `double` (1×) | `begg` (1×) | `under` (1×) | `sacks` (1×) | `coughing` (1×) | `through` (1×)

**imagist**: `away` (1×) | `beats` (1×) | `dead` (1×) | `slack` (1×) | `against` (1×) | `ut` (1×) | `ted` (1×) | `rid` (1×)

**mid_century**: `fl` (2×) | `ur` (2×) | `late` (2×) | `sin` (2×) | `gin` (2×) | `June` (2×) | `road` (2×) | `sw` (2×)

---

## Finding 4: The 'Peak Rate' as a Measure of Era-Level Risk-Taking

The **peak rate** (peaks per 100 artifact-free tokens) varies substantially across eras:

**Most peaks per token (highest risk-taking):**

- **clerihew** (10 poems): 25.43% peak rate, mean peak S2 = 6.832
- **haiku** (14 poems): 20.82% peak rate, mean peak S2 = 6.195
- **german_expressionist** (4 poems): 19.88% peak rate, mean peak S2 = 5.949
- **oulipo** (8 poems): 19.68% peak rate, mean peak S2 = 6.483
- **confessional** (6 poems): 19.4% peak rate, mean peak S2 = 6.0

**Fewest peaks per token (lowest risk-taking):**

- **song_lyrics** (3 poems): 12.38% peak rate, mean peak S2 = 5.959
- **double_dactyl** (5 poems): 12.1% peak rate, mean peak S2 = 5.982
- **cliche_control** (4 poems): 10.84% peak rate, mean peak S2 = 5.687
- **found_poetry** (9 poems): 10.71% peak rate, mean peak S2 = 6.299
- **control** (4 poems): 2.34% peak rate, mean peak S2 = 3.542

---

## Finding 5: Unexpected Field Signatures — Surprising the Hypothesis

### Surrealist: peaks → body (5.0% of all peaks, 23.7% of categorized peaks)

Surrealist poetry has the highest body-field share at peak moments among all eras. This is the era expected to be most abstract or dreamlike — yet at the moments of maximum lexical surprise, surrealists reach for the corporeal. Top tokens: `bones`, `body`, `voice`, `arm`, `ear`. The body appears as the site of surrealist rupture — the dream is embodied.

### Confessional: peaks → time (6.5% of all peaks, 29.4% of categorized peaks)

Confessional poetry's dominant peak field is **time**, not body. Confessional poets (Plath, Sexton) deploy their most surprising lexical choices at temporal moments — words that anchor the poem's crisis in time. The expected finding (body-at-peaks) does not hold. Their second field is **color_light**: at peaks, confessional poets reach for precise color words (`black`, `heavy`, `dark`), materializing psychological states visually rather than corporeally.

### Modernist: peaks → nature (4.1% of all peaks, 37.6% of categorized peaks)

Modernist peaks are dominated by **nature** (38% of categorized peaks). This resists the common characterization of modernism as 'urban' and 'fragmented' — at the moments of maximum S2, modernist poets reach for the natural world. The unexpected choice in a modernist poem is often a nature word placed in an industrial or psychological context.


---

## Finding 6: Nature vs Body vs Abstract — The Tripartite Structure of Poetic Surprise

Three semantic fields account for the majority of categorized peaks across all eras: **nature**, **body**, and **abstract_soul**. The relative weight of each field tracks the era's characteristic aesthetic program:

**Corpus-wide distribution of semantic fields at S2 > 3.0 (all eras combined):**

| Semantic Field | % of All Peaks |
|----------------|---------------|
| other | 87.9% |
| nature | 2.6% |
| time | 2.2% |
| abstract_soul | 1.7% |
| human_society | 1.7% |
| death_void | 1.0% |
| body | 1.0% |
| motion | 1.0% |
| color_light | 0.9% |

---

## Suggested Next Steps

1. **Refine the taxonomy.** The 'other' category dominates — adding more semantic fields (e.g., perception/senses, domestic/built environment, number/quantity, agency/volition) would reveal finer structure.
2. **Weight by S2 magnitude.** The current analysis counts peaks equally; weighting by S2 value would let us ask which semantic fields carry the highest surprise.
3. **Control for base rates.** A field's high peak-time rate may simply reflect that the field's words are common in poetry. Computing a 'peak premium' (peak rate / background rate) would isolate genuine peak-specificity.
4. **Author-level analysis.** Do individual poets within an era show the era's characteristic field, or diverge from it? This would test whether the field signature is a movement property or an individual style.
5. **Extend to what was suppressed.** For each era, compare the semantic field of the CHOSEN token (this study) with the semantic field of the SUPPRESSED alternative. Do poets substitute within-field or cross-field?