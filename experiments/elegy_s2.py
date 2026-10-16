"""
Elegy S2 Analysis
=================
Research question: Do elegies have a distinctive information-theoretic signature?

Elegies are poems of formal mourning. The hypothesis: elegies must work against
consolation — the poem must sustain the wound of loss without resolving it
prematurely. This creates two competing predictions:

  H1 (Suppression hypothesis): Elegies have HIGH positive S2 because the poet
     refuses the conventional grieving script — what GPT-2 predicts ("rest",
     "peace", "gone") is systematically refused in favor of more raw choices.

  H2 (Constraint hypothesis): Elegies use formal conventions (meter, apostrophe,
     classical allusion) that make the language MORE predictable — lower S2
     compared to free verse emotional poetry.

We test by comparing:
  - elegy era (7 poems)
  - romantic/19th-century (life-affirming lyric)
  - confessional (personal/emotional but not elegiac)
  - victorian (formal but various emotional registers)

We also look for "grief words" (death, dead, die, lost, gone, mourn) and ask
whether these specific words have high or low S2 — i.e., are death tokens
surprising or predictable in their contexts?
"""

import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

from corpus.poems import POEMS

# ── model setup ──────────────────────────────────────────────────────────────
print("Loading GPT-2...", flush=True)
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(f"  Using {device}", flush=True)


def compute_s2_tokens(text, max_tokens=512):
    """Returns list of (token_str, s2, surprisal, entropy) for each token."""
    enc = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_tokens)
    input_ids = enc["input_ids"].to(device)
    if input_ids.shape[1] < 3:
        return []

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits[0]  # (seq_len, vocab)

    results = []
    for i in range(1, input_ids.shape[1]):
        log_probs = torch.log_softmax(logits[i - 1], dim=-1)
        probs = log_probs.exp()

        entropy = -(probs * log_probs).sum().item()
        actual_id = input_ids[0, i].item()
        surprisal = -log_probs[actual_id].item()
        s2 = surprisal - entropy

        tok = tokenizer.decode([actual_id])
        results.append((tok, s2, surprisal, entropy))
    return results


def is_artifact(tok, prev_tok):
    """Return True if this token is likely a stanza-break artifact."""
    stripped = tok.strip()
    if not stripped:
        return True
    if tok.startswith("\n") and (not prev_tok or prev_tok.strip() == ""):
        return True
    return False


def analyze_poem(poem):
    tokens = compute_s2_tokens(poem["text"])
    if not tokens:
        return None
    clean = []
    for i, (tok, s2, surprisal, entropy) in enumerate(tokens):
        prev = tokens[i-1][0] if i > 0 else ""
        if not is_artifact(tok, prev):
            clean.append((tok, s2, surprisal, entropy))
    if len(clean) < 5:
        return None
    s2_vals = [x[1] for x in clean]
    return {
        "title": poem["title"],
        "author": poem["author"],
        "era": poem["era"],
        "n": len(clean),
        "mean_s2": sum(s2_vals) / len(s2_vals),
        "tokens": clean,
    }


# ── grief-word analysis ───────────────────────────────────────────────────────
GRIEF_WORDS = {
    "death", "dead", "die", "died", "dying", "grave", "tomb", "mourn",
    "mourning", "loss", "lost", "weep", "wept", "tears", "grief", "sorrow",
    "farewell", "gone", "perish", "perished", "fall", "fallen", "cold",
    "buried", "dust", "ashes", "shadow", "dark", "darkness", "pale",
}

LIFE_WORDS = {
    "live", "living", "life", "birth", "born", "grow", "spring", "joy",
    "light", "sun", "flower", "bloom", "rise", "sing", "bright", "warm",
    "love", "hope", "green", "fresh", "new", "young", "morning",
}


def classify_word(tok):
    w = tok.strip().lower().strip(".,!?;:—\"'")
    if w in GRIEF_WORDS:
        return "grief"
    if w in LIFE_WORDS:
        return "life"
    return None


# ── main analysis ─────────────────────────────────────────────────────────────
target_eras = {"elegy", "romantic", "confessional", "victorian", "19th_century"}
results = {}
grief_s2 = []
life_s2 = []

print("\nAnalyzing poems...", flush=True)
for poem in POEMS:
    if poem.get("language", "en") != "en":
        continue
    era = poem["era"]
    if era not in target_eras:
        continue

    r = analyze_poem(poem)
    if r is None:
        continue

    if era not in results:
        results[era] = []
    results[era].append(r)

    for (tok, s2, surprisal, entropy) in r["tokens"]:
        cat = classify_word(tok)
        if cat == "grief":
            grief_s2.append((tok.strip().lower(), s2, r["title"], era))
        elif cat == "life":
            life_s2.append((tok.strip().lower(), s2, r["title"], era))

# ── per-poem results table ────────────────────────────────────────────────────
print("\n=== Per-poem results ===")
all_rows = []
for era, poems in sorted(results.items()):
    for r in poems:
        all_rows.append((r["era"], r["title"][:45], r["author"][:20], r["n"], round(r["mean_s2"], 3)))

all_rows.sort(key=lambda x: (x[0], -x[4]))
for row in all_rows:
    print(f"  [{row[0]:18s}] {row[2]:20s} | {row[1]:45s} | n={row[3]:4d} | S2={row[4]:+.3f}")

# ── era summary ───────────────────────────────────────────────────────────────
print("\n=== Era summary (artifact-free mean S2) ===")
era_summary = {}
for era, poems in results.items():
    vals = [r["mean_s2"] for r in poems]
    era_summary[era] = {
        "n_poems": len(vals),
        "mean_s2": sum(vals) / len(vals),
        "min_s2": min(vals),
        "max_s2": max(vals),
    }

for era, s in sorted(era_summary.items(), key=lambda x: -x[1]["mean_s2"]):
    print(f"  {era:20s}: n={s['n_poems']} mean={s['mean_s2']:+.3f} range=[{s['min_s2']:+.3f}, {s['max_s2']:+.3f}]")

# ── grief vs. life word analysis ──────────────────────────────────────────────
print("\n=== Grief words vs. Life words (S2 analysis) ===")
if grief_s2:
    g_vals = [x[1] for x in grief_s2]
    print(f"  Grief words: n={len(g_vals)} mean_S2={sum(g_vals)/len(g_vals):+.3f}")
    # top grief tokens
    from collections import defaultdict
    grief_by_word = defaultdict(list)
    for tok, s2, title, era in grief_s2:
        grief_by_word[tok].append(s2)
    print("  Top grief word S2 averages:")
    for w, vals in sorted(grief_by_word.items(), key=lambda x: -sum(x[1])/len(x[1]))[:12]:
        print(f"    {w:12s}: mean={sum(vals)/len(vals):+.3f} (n={len(vals)})")

if life_s2:
    l_vals = [x[1] for x in life_s2]
    print(f"\n  Life words: n={len(l_vals)} mean_S2={sum(l_vals)/len(l_vals):+.3f}")

# ── elegy-specific: grief word S2 by era ─────────────────────────────────────
print("\n=== Grief word S2 by era ===")
grief_by_era = defaultdict(list)
life_by_era = defaultdict(list)
for tok, s2, title, era in grief_s2:
    grief_by_era[era].append(s2)
for tok, s2, title, era in life_s2:
    life_by_era[era].append(s2)

for era in sorted(target_eras):
    gv = grief_by_era.get(era, [])
    lv = life_by_era.get(era, [])
    gs = f"{sum(gv)/len(gv):+.3f} (n={len(gv)})" if gv else "n/a"
    ls = f"{sum(lv)/len(lv):+.3f} (n={len(lv)})" if lv else "n/a"
    print(f"  {era:18s} grief_words={gs:20s} life_words={ls}")

# ── elegy internal structure: do elegies peak mid-poem? ──────────────────────
print("\n=== Elegy internal S2 arcs (tercile breakdown) ===")
for r in results.get("elegy", []):
    toks = r["tokens"]
    n = len(toks)
    if n < 12:
        continue
    t1 = toks[: n // 3]
    t2 = toks[n // 3 : 2 * n // 3]
    t3 = toks[2 * n // 3 :]
    s1 = sum(x[1] for x in t1) / len(t1)
    s2m = sum(x[1] for x in t2) / len(t2)
    s3 = sum(x[1] for x in t3) / len(t3)
    print(f"  {r['title'][:50]:50s}: early={s1:+.3f} mid={s2m:+.3f} late={s3:+.3f}")

# ── save results ──────────────────────────────────────────────────────────────
out = {
    "era_summary": era_summary,
    "grief_word_mean_s2": sum(x[1] for x in grief_s2) / len(grief_s2) if grief_s2 else None,
    "life_word_mean_s2": sum(x[1] for x in life_s2) / len(life_s2) if life_s2 else None,
    "grief_by_era": {k: sum(v)/len(v) for k, v in grief_by_era.items()},
    "life_by_era": {k: sum(v)/len(v) for k, v in life_by_era.items()},
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "findings", "elegy_s2.json")
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)
print(f"\nResults saved to {out_path}")
