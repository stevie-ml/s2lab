# Instagram Poetry: High Raw S₂, Deeply Predictable Vocabulary

**Date:** 2026-11-16
**New corpus additions:** 3 Instagram-style minimalist poems (`social_media_poetry` era)
**Related:** `findings/found_poetry_intentionality.md`, `findings/stanza_break_artifact.md`

---

## Research Question

Is "Instagram poetry" (Rupi Kaur style: single words per line, maximal whitespace, healing/loss themes, common vocabulary) informationally distinctive? Does it use genuinely surprising language, or does it achieve apparent emotional impact through line-break fragmentation of predictable text?

---

## New Poems Added

Three synthetic poems in the `social_media_poetry` era, exemplifying the dominant style:

1. **Instagram Poem 1** — "you / told me / i was / everything / then left / like i was / nothing"
2. **Instagram Poem 2** — "healing / is not linear / some days you are okay / some days you are not / and both / are allowed"
3. **Instagram Poem 3** — "i miss you / the way you miss / a word / on the tip of your tongue / present / but / unreachable"

---

## Results

| Poem | Raw S₂ | Clean S₂ | Interpretation |
|------|--------|----------|----------------|
| Instagram Poem 1 | **+4.192** | **−0.654** | Extreme raw inflation; vocabulary deeply predictable |
| Instagram Poem 2 | +1.859 | **−1.175** | Raw above lyric average; clean well below prose control |
| Instagram Poem 3 | +1.373 | **−0.974** | Same pattern |
| *Lyric poetry avg* | *(+0.243)* | *(approx −0.4)* | *Reference* |
| *Control prose avg* | *(−1.663)* | *(−1.663)* | *Reference* |

**Instagram Poem 1** has the highest raw S₂ in the new sample — apparently more "surprising" than experimental Oulipo. But its **clean S₂ of −0.654** is *lower than the average lyric poem and approaching prose control*.

---

## Key Finding: The Line-Break Illusion

Instagram poetry achieves its apparent informational richness entirely through **stanza-break artifacts** — the high-S₂ tokens are almost exclusively line-break violations (tokens that follow newlines when GPT-2 expected another newline).

**How it works:**
- One word per line creates a maximum-density newline structure
- GPT-2 after a newline strongly predicts another newline (poem is "done")
- Each new word violates that expectation → massive surprisal spike
- S₂ = surprisal − entropy → positive spike whenever the model was confidently wrong

**After removing artifact tokens (p_newline < 0.90):**
- Instagram Poem 1: −0.654 (more predictable than the typical lyric poem)
- Instagram Poem 2: −1.175 (between control prose and found poetry)
- Instagram Poem 3: −0.974 (between control prose and found poetry)

The vocabulary of Instagram poetry — "you", "i", "was", "everything", "healing", "linear", "okay", "allowed", "miss", "tongue", "present", "unreachable" — is exactly the kind of common, emotionally legible language that GPT-2 handles most confidently.

---

## Comparison with Other New Poems

| Poem | Era | Raw S₂ | Clean S₂ |
|------|-----|--------|----------|
| Instagram Poem 1 | social_media_poetry | +4.192 | −0.654 |
| Instagram Poem 2 | social_media_poetry | +1.859 | −1.175 |
| Instagram Poem 3 | social_media_poetry | +1.373 | −0.974 |
| N+7: Death Poem (Dickinson) | oulipo | +0.921 | **+0.159** |
| Diamond Concrete Poem | concrete | +0.618 | −0.307 |
| Lipogram Without A | oulipo | +0.347 | −0.231 |
| Homophonic Translation (Catullus) | oulipo | +0.167 | −0.549 |
| Acrostic: SILENCE | oulipo | −0.534 | −0.771 |
| Line Palindrome | oulipo | −1.501 | **−1.516** |

**The N+7 substitution (Dickinson → "Deacon" for "Death", "Carrot" for "Carriage") achieves genuine positive S₂ even in clean form (+0.159)** — the nonsense substitutions create real surprisal that isn't artifact.

**The Line Palindrome hits −1.516 clean** — the second most negative in the entire corpus (after control prose at −1.663). After the palindrome's midpoint, GPT-2 has seen all the words and predicts them perfectly in the second half, creating near-zero surprisal throughout.

---

## Theoretical Implication: S₂ Exposes the Line-Break Illusion

This finding has implications for how we evaluate contemporary "accessible" poetry:

**Instagram poetry aesthetics** — sparse lines, common vocabulary, universal themes — creates the subjective experience of emotional impact through **typography** (white space, fragmentation), not through lexical surprise. The line break physically isolates ordinary words, making them feel weightier. But the information content is demonstrably lower than any canonical poetry movement.

**What this means for the Straussian gap:** Instagram poetry has *nothing* in the gap between what language expected and what the poet chose. The vocabulary IS what language expected — "healing", "okay", "you", "left". The only surprise is typographic: the line break tells you something is about to be revealed, and then a very ordinary word appears.

This is the inverse of the Straussian reading: canonical poets suppress expected language and substitute unexpected language. Instagram poets suppress *nothing* — they deliver exactly what is expected, but delay it typographically.

---

## Suggested Next Steps

1. **Add real Rupi Kaur poems** (fair-use excerpts) for direct measurement — do commercially published Instagram poems follow the same pattern as synthetic examples?
2. **Typography control**: Reformat these poems as prose (remove line breaks) and re-measure — does clean S₂ change further?
3. **Emotional vs. informational impact**: This dissociation (low S₂, high perceived emotional resonance) suggests S₂ and emotional impact are orthogonal. What predicts emotional resonance if not S₂?
4. **Social media corpus**: Add tweets, Instagram captions, text messages — build a "below poetry" baseline to anchor the bottom of the S₂ scale.
