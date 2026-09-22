# The Word as the Unit of Poetic Surprise: Subword Tokenization and S₂

**Date:** 2026-09-22  
**Experiment:** `experiments/subword_tokenization_s2.py`  
**Corpus:** 140 English-language poems from `results/corpus_results.json`  
**Builds on:** `word_length_vs_s2.md`, `s2_inequality_gini.md`, `second_occurrence_dip.md`

---

## Research Question

GPT-2 uses byte-pair encoding (BPE): common words are single tokens, rare words are split into multiple subword tokens (e.g., "loafe" → "lo" + "afe", "Boomlay" → "B" + "oom" + "lay"). This means every S₂ measurement mixes two fundamentally different populations:

1. **Word-start tokens** — the poet's genuine lexical choice (e.g., " cloud", " wandered")
2. **Continuation tokens** — the predictable unfolding of an already-chosen word (e.g., "inary" in "extraordinary", "oom" in "Boomlay")

If these populations have different S₂ distributions, then previous token-level analyses have been conflating two distinct phenomena. The true "Straussian gap" — the poet's deviation from expectation — should live at word boundaries.

---

## Method

Using sequential context to classify each token:
- **word_start**: begins with ' ' (GPT-2 space prefix, indicating word boundary)
- **line_start**: first token of a new line (no space prefix after '\n')
- **continuation**: no space prefix, not at line start (true subword continuation)
- **special**: newlines and whitespace

For multi-token words (where word-start is followed by continuation tokens), we computed word *complexity* (token count) and the S₂ drop from word-start to first continuation.

---

## Key Findings

### 1. Continuation Tokens Are Informationally Dead Weight

| Token class | n | Mean S₂ | Pos S₂% |
|---|---|---|---|
| **word_start** | 10,570 | **+0.764** | 43.0% |
| **line_start** | 1,619 | **+6.277** | 60.5% |
| **continuation** | 3,707 | **−1.078** | 20.2% |
| special (newlines) | 1,896 | **−1.419** | 14.3% |

**The word-start vs. continuation gap is 1.842 bits.**

Once a poet commits to a word, GPT-2 can predict its continuation tokens with high confidence. The continuation tokens' mean S₂ (−1.078) is close to prose-control territory (−1.939 for word-starts, −1.793 for continuations in prose). This is not where poetic deviation lives.

> **Note on line_start:** The very high S₂ (+6.277) for line-start tokens is the stanza-break artifact identified in `findings/stanza_break_artifact.md` — GPT-2 strongly expects a newline at these positions, so the first word of a new line registers as extremely surprising. This is a formatting artifact, not a poetic signal.

---

### 2. The More Tokens a Word Takes, the More Surprising It Was

Word complexity (number of GPT-2 tokens) is a direct proxy for word rarity. The relationship with S₂ is **monotonic**:

| Word complexity | n words | Mean S₂ at word-start |
|---|---|---|
| 1 token (common) | 7,968 | **−0.498** |
| 2 tokens | 2,143 | **+0.894** |
| 3 tokens | 325 | **+2.492** |
| 4 tokens | 96 | **+2.805** |
| 5 tokens | 26 | **+3.230** |
| 6 tokens | 7 | **+5.070** |

Every level of tokenization depth adds approximately +1 S₂ unit. A word that requires 6 subword tokens averages S₂ = +5.07 — roughly 10× the S₂ of a common 1-token word.

**Interpretation:** S₂ and lexical rarity are aligned but not identical. S₂ measures surprise *given context*, while tokenization depth measures rarity *in pretraining*. The near-monotonic relationship shows these are strongly correlated: unusual words tend to be contextually surprising *and* lexically rare.

The 1-token-word mean (−0.498) being negative is striking: in poetry, the common vocabulary (articles, prepositions, conjunctions, common nouns) is being *over-predicted* by GPT-2. The poem's surprises are concentrated in its unusual words.

---

### 3. The Commitment Drop: S₂ Falls 2.4 Bits When a Word Continues

Across 2,602 word-start + first-continuation pairs:

| Position | Mean S₂ |
|---|---|
| Word-start token | **+1.199** |
| First continuation token | **−1.163** |
| **Δ** | **−2.363** |
| Pairs where S₂ drops | **67.1%** |

The poet "commits" to a word at the word-start token. After that, GPT-2 rapidly narrows its predictions to complete the word it has now half-seen. The S₂ plunges by 2.4 bits on average — from modestly positive to negative in a single token.

This makes the word (not the token) the true *quantum of poetic choice* in information-theoretic analysis.

---

### 4. Era Rankings: Who Uses Rare Words?

Eras with the highest word-start S₂ tend to use vocabulary outside GPT-2's fluent zone:

| Era | WS mean S₂ | Cont mean S₂ | Gap |
|---|---|---|---|
| haiku | +3.687 | −0.704 | +4.391 |
| ballad | +1.723 | −0.819 | +2.542 |
| beat | +1.481 | −0.335 | +1.816 |
| confessional | +1.466 | −1.168 | +2.634 |
| fixed_form | +1.386 | −0.654 | +2.040 |
| modernist | +1.091 | −1.006 | +2.097 |
| *control prose* | *−1.939* | *−1.793* | *−0.146* |

**Haiku's extreme word-start S₂** (+3.687) is consistent with translation artifacts: Japanese names, place-words, and poetic imagery ("the old pond", "a frog") often require unusual English vocabulary. The gap between word-start and continuation is 4.4 bits — the largest of any era.

**Control prose** near-zero gap (−0.146): prose word-starts and continuations are almost equally predictable. This confirms that the word-boundary surprise advantage is a distinctly poetic phenomenon.

---

### 5. Author Rankings: Word-Start S₂ as Lexical Fingerprint

| Author | WS mean S₂ | WS n | Cont mean S₂ |
|---|---|---|---|
| William Carlos Williams | +6.208 | 42 | −0.776 |
| Gwendolyn Brooks | +6.020 | 23 | −1.833 |
| Matsuo Basho | +4.455 | 36 | −0.813 |
| Kobayashi Issa | +3.895 | 40 | −1.049 |
| Seamus Heaney | +3.284 | 97 | −1.346 |
| E.E. Cummings | +2.656 | 111 | +0.659 |
| Thomas Hardy | +2.481 | 284 | −0.568 |
| Sylvia Plath | +1.968 | 97 | −0.726 |

**Williams and Brooks** lead — extremely high word-start S₂ combined with strongly negative continuation S₂ shows they use a *sparse, precision-engineered* vocabulary: each word is rare and contextually startling, then yields a fully determined completion. Brooks's "We Real Cool" achieves maximum surprise through monosyllabic grammar that refuses to follow GPT-2's syntactic expectations.

**E.E. Cummings** is an outlier: high word-start S₂ AND positive continuation S₂ (+0.659). His visual/typographical distortions create words GPT-2 cannot parse even after seeing their start — continuation tokens stay surprising because the "word" is being invented in real time.

---

### 6. The Genuinely Surprising Continuations: Beyond-Word Surprise

High-S₂ continuation tokens identify words so unusual that even the first subword doesn't resolve GPT-2's uncertainty:

| Word (reconstructed) | Cont token | S₂ | Poet |
|---|---|---|---|
| 'Boomlay' | 'lay' | +18.85 | Vachel Lindsay |
| 'fashes' | 'ashes' | +18.51 | Trad. Scottish ballad |
| 'role-L' | 'L' | +17.73 | John Ashbery |
| 'dois' | 'is' | +17.47 | Trad. Scottish ballad |
| 'time——' | '——' | +16.10 | Sylvia Plath |
| 'loafe' | 'afe' | +12.87 | Walt Whitman |
| 'Abeillard' | 'illard' | +12.07 | D.G. Rossetti |
| 'schip' | 'ip' | +11.69 | Trad. Scottish ballad |

These are the *deepest* lexical deviations in the corpus: invented words ('Boomlay', 'loafe'), archaic/dialect words ('fashes', 'dois', 'schip'), unusual punctuation compounds ('time——'), and proper names from other languages ('Abeillard'). Even after partial tokenization, GPT-2 remains disoriented.

The Scottish ballad tradition appears repeatedly — archaic Scots vocabulary ("fashes" = worries, "dois" = doves, "schip" = ship) consistently produces high continuation-S₂ because these words exist outside GPT-2's primary training distribution.

---

## Summary of Findings

1. **The word, not the token, is the unit of poetic choice.** Word-start tokens average +0.764 S₂; continuation tokens average −1.078. A 1.842-bit gap separates genuine lexical decisions from their predicted completions.

2. **Lexical rarity and S₂ are monotonically linked.** Each additional tokenization split (BPE depth) adds ~+1 S₂ unit to the word-start token. Six-token words average S₂ = +5.07.

3. **The commitment drop.** S₂ falls 2.4 bits from word-start to first continuation token. The poet commits; the model catches up immediately.

4. **Haiku (via translation) and ballad (via dialect) use the rarest vocabulary** relative to GPT-2's prior. Control prose has near-zero word-boundary advantage.

5. **High-S₂ continuation tokens are a lexical exotica detector** — they find invented words, dialect, archaic spelling, and unusual proper names that remain surprising even mid-word.

---

## Methodological Implication

Previous reports in this series measured S₂ at the token level, including continuation tokens. Since roughly 25% of English poetry tokens are continuations (averaging −1.078 S₂), this systematically pulls down reported averages. **A more accurate measure of "poetic surprise" is word-start-only S₂**, which filters out the predictable mechanical unfolding of unusual words and focuses on the poet's actual lexical choices.

The raw poetry vs. prose gap (reported as ~1.3–1.9 bits in earlier findings) remains valid when measured at word-starts: prose word-start mean = −1.939, poetry word-start mean = +0.764. The gap is 2.7 bits — larger than the token-level estimate, because continuations diluted the signal in both directions.

---

## Suggested Next Steps

1. **Reweight all per-poem S₂ scores by word-start-only** to produce "cleaned" author and era rankings.
2. **BPE depth as a poem-level metric**: which poets maximize lexical depth (most multi-token words)? Does Hopkinite compound-invention show up here?
3. **Cross-language comparison**: German poetry (Rilke, Trakl) runs through GPT-2's English BPE vocabulary differently — their word-continuation profiles should diverge markedly from English.
4. **Intentional multi-token wordplay** (Cummings, Ashbery): examine poems where continuation S₂ stays high and reconstruct the visual/typographic effects that cause it.
