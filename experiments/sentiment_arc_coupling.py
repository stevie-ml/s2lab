"""
S₂ and Sentiment Arc Coupling

Research question: Over the course of a poem, how does the trajectory of
S₂ (information-theoretic surprise) align with or diverge from the
trajectory of emotional valence (sentiment arc)?

Two competing hypotheses:

  H1 — COUPLED: Surprise and emotion co-occur. When a poem builds toward
       an emotional climax, it also builds information-theoretically. S₂
       arc and sentiment arc are positively correlated.

  H2 — DECOUPLED / COMPLEMENTARY: Surprise and emotion are distinct
       resources. A poet can deliver emotional intensity while staying
       syntactically expected (think: "So much depends / upon / a red wheel
       barrow" — surprising word choice, neutral valence). Or they can use
       conventional words to express deep feeling (Keats: familiar,
       emotionally loaded but low-S₂).

Method:
1. Divide each poem into 4 quartiles.
2. For each quartile, compute:
   - mean S₂ (all tokens)
   - mean AFINN valence (matched tokens only)
   - mean |AFINN| intensity (matched tokens only)
3. Across quartiles, compute:
   - Pearson r between S₂ arc and valence arc per poem
   - S₂ trend slope (rising / falling)
   - Valence trend slope (rising / falling / dark / bright)
4. Classify poems into arc-coupling types:
   - SYNCHRONIZED: both S₂ and sentiment rising or both falling
   - ANTI-SYNCHRONIZED: one rises while the other falls
   - DECOUPLED: no significant correlation
5. Group by author and era to find coupling preferences.
"""

import json
import re
import math
import statistics
from collections import defaultdict
from pathlib import Path

# ── AFINN-111 lexicon (same as emotional_valence_s2.py) ──────────────────────
AFINN = {
    "abandon": -2, "abandoned": -2, "abhor": -3, "abhorrent": -3,
    "abominable": -3, "abominably": -3, "abominate": -3, "abomination": -3,
    "abort": -2, "aborted": -2, "aborts": -2, "abrupt": -1,
    "absent": -1, "absorbed": 1, "absurd": -1, "abuse": -3,
    "abused": -3, "abuses": -3, "abusive": -4, "ache": -2,
    "aches": -2, "aching": -2, "afraid": -2, "agony": -3,
    "agree": 1, "agreeable": 2, "aid": 2, "alarm": -2,
    "alarmed": -2, "alienated": -2, "alone": -1, "amazing": 4,
    "angry": -3, "anguish": -3, "annoy": -2, "annoyed": -2,
    "annoying": -2, "appreciate": 2, "approval": 2, "approve": 2,
    "awful": -3, "bad": -3, "beautiful": 3, "beauty": 3,
    "best": 3, "better": 2, "bliss": 3, "blissful": 3,
    "blessing": 3, "bold": 2, "bored": -2, "boredom": -2,
    "brave": 2, "break": -1, "broken": -2, "calm": 2,
    "care": 2, "careful": 2, "caring": 2, "celebrate": 3,
    "cheerful": 2, "clarity": 2, "clean": 2, "comfort": 2,
    "compassion": 2, "confidence": 2, "confused": -2, "corrupt": -3,
    "courage": 2, "create": 1, "creative": 2, "cruel": -3,
    "crush": -2, "cry": -2, "crying": -2, "curious": 1,
    "danger": -2, "dark": -1, "darkness": -1, "dead": -2,
    "death": -2, "defeat": -2, "delight": 3, "delighted": 3,
    "delightful": 4, "depressed": -3, "depression": -3, "desperate": -3,
    "destroy": -3, "devastated": -3, "die": -2, "disaster": -3,
    "disgust": -3, "disgusting": -4, "distress": -3, "doubt": -1,
    "dread": -3, "dreary": -2, "eager": 2, "ecstatic": 4,
    "embarrassed": -2, "embrace": 2, "empathy": 2, "enchant": 3,
    "encourage": 2, "energetic": 2, "enjoy": 2, "enlighten": 2,
    "enormous": 1, "excellent": 3, "excited": 3, "exhausted": -2,
    "failure": -3, "fantastic": 4, "fear": -2, "fearful": -2,
    "fight": -1, "forgive": 2, "free": 2, "freedom": 2,
    "friendly": 3, "frustrated": -2, "funny": 3, "furious": -3,
    "genius": 3, "glad": 3, "gloomy": -2, "glorious": 4,
    "glory": 3, "good": 3, "grace": 3, "graceful": 3,
    "grateful": 3, "great": 3, "grief": -3, "guilty": -3,
    "happiness": 3, "happy": 3, "hate": -3, "help": 2,
    "hopeful": 2, "hopeless": -2, "horror": -3, "humble": 2,
    "hurt": -2, "ideal": 2, "illuminate": 2, "inspire": 3,
    "insult": -3, "intense": 1, "joyful": 4, "kind": 3,
    "kindly": 2, "laugh": 2, "laughter": 3, "light": 1,
    "lonely": -2, "loneliness": -2, "love": 3, "lovely": 3,
    "lucky": 3, "magnificent": 3, "mean": -2, "miserable": -3,
    "misery": -3, "mock": -2, "mourn": -2, "mourning": -2,
    "murder": -3, "need": -1, "neglect": -2, "nervous": -2,
    "nightmare": -3, "noble": 3, "numb": -2, "pain": -2,
    "panic": -3, "peace": 3, "peaceful": 3, "pity": -2,
    "pleasure": 3, "powerful": 2, "pride": 2, "rage": -3,
    "regret": -2, "relief": 2, "sadness": -2, "sad": -2,
    "safe": 2, "shame": -3, "shocked": -2, "sick": -2,
    "silence": -1, "sin": -3, "smile": 2, "sorrow": -2,
    "soul": 1, "spirit": 2, "strength": 2, "suffer": -2,
    "suffering": -3, "sweet": 2, "terrible": -3, "terror": -3,
    "thankful": 3, "thrilled": 4, "torment": -3, "torture": -4,
    "tough": 1, "tragedy": -3, "trouble": -2, "trust": 2,
    "ugly": -3, "unhappy": -3, "useless": -3, "victory": 3,
    "violent": -3, "virtue": 2, "warm": 2, "weak": -2,
    "weep": -2, "weeping": -2, "wisdom": 2, "wonder": 3,
    "wonderful": 4, "worry": -2, "worthy": 2, "wrong": -2,
    "angel": 3, "dark": -1, "death": -2, "die": -2,
    "empty": -1, "fall": -1, "ghost": -1, "god": 2,
    "grave": -2, "heart": 1, "heaven": 3, "hell": -3,
    "hollow": -2, "hope": 2, "hunger": -2, "joy": 3,
    "light": 1, "memory": 0, "mind": 0, "moon": 1,
    "night": -1, "pray": 1, "prayer": 1, "river": 0,
    "ruin": -2, "ruined": -2, "sea": 0, "shadow": -1,
    "silence": -1, "sky": 1, "song": 2, "stone": -1,
    "storm": -2, "sun": 2, "tear": -2, "tears": -2,
    "tree": 0, "truth": 2, "vast": 0, "void": -2,
    "war": -3, "water": 0, "wind": 0, "world": 0,
    "wound": -2, "wrath": -3, "year": 0, "lost": -2,
    "bright": 2, "cold": -1, "silver": 1, "gold": 2,
    "rise": 1, "fall": -1, "born": 1, "dead": -2,
    "black": -1, "white": 0, "red": 0, "blue": 0,
    "deep": 0, "long": 0, "old": 0, "young": 1,
    "little": 0, "small": 0, "great": 3, "high": 1,
    "low": -1, "hard": -1, "soft": 1, "still": 0,
    "gentle": 2, "wild": 1, "true": 2, "false": -2,
    "broken": -2, "whole": 2, "lost": -2, "found": 2,
    "free": 2, "bound": -1, "open": 1, "closed": -1,
    "earth": 0, "fire": 1, "flesh": 0, "soul": 1,
    "blood": -1, "bone": -1, "voice": 1, "hand": 0,
    "eye": 0, "face": 0, "name": 0, "time": 0,
    "beautiful": 3, "ugly": -3, "kind": 3, "cruel": -3,
    "brave": 2, "afraid": -2, "strong": 2, "weak": -2,
    "bright": 2, "dark": -1, "clean": 2, "dirty": -2,
    "sacred": 3, "profane": -2, "holy": 3, "sinful": -3,
    "mercy": 3, "cruelty": -3, "grace": 3, "sin": -3,
    "envy": -2, "greed": -3, "pride": 2, "sloth": -1,
    "wrath": -3, "lust": -1, "gluttony": -2,
    "pure": 2, "corrupt": -3, "innocent": 2, "guilty": -3,
    "alive": 2, "dead": -2, "born": 1, "die": -2,
    "immortal": 2, "mortal": -1, "eternal": 2, "temporal": 0,
    "infinite": 1, "finite": 0, "vast": 0, "small": 0,
    "abyss": -3, "sublime": 2, "terror": -3, "beauty": 3,
    "trembling": -1, "still": 0, "silent": -1, "loud": 0,
    "sudden": 0, "slow": 0, "swift": 1, "heavy": -1,
    "light": 1, "warm": 2, "cold": -1, "fierce": -1,
    "tender": 2, "harsh": -2, "raw": -1, "ripe": 1,
    "withered": -2, "blossoming": 2, "decaying": -2, "growing": 1,
}


def stem(word):
    """Minimal stemming for AFINN lookup."""
    w = word.lower()
    for suffix in ("ing", "edly", "edly", "edly", "edly", "ed", "ly", "er", "est", "ness", "s"):
        if len(w) > len(suffix) + 2 and w.endswith(suffix):
            base = w[: -len(suffix)]
            if base in AFINN:
                return base
    return w


def afinn_score(token):
    """Return AFINN valence or None if not in lexicon."""
    t = re.sub(r"[^a-z]", "", token.lower())
    if not t or len(t) < 2:
        return None
    if t in AFINN:
        return AFINN[t]
    stemmed = stem(t)
    if stemmed in AFINN:
        return AFINN[stemmed]
    return None


def pearson_r(xs, ys):
    """Compute Pearson r between two equal-length lists."""
    n = len(xs)
    if n < 3:
        return None
    xm = sum(xs) / n
    ym = sum(ys) / n
    num = sum((xs[i] - xm) * (ys[i] - ym) for i in range(n))
    sx = math.sqrt(sum((x - xm) ** 2 for x in xs))
    sy = math.sqrt(sum((y - ym) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    return num / (sx * sy)


def linear_slope(values):
    """Return slope of best-fit line, x normalized to [0,1]."""
    n = len(values)
    if n < 2:
        return 0.0
    xs = [i / max(1, n - 1) for i in range(n)]
    xm = sum(xs) / n
    ym = sum(values) / n
    num = sum((xs[i] - xm) * (values[i] - ym) for i in range(n))
    den = sum((xs[i] - xm) ** 2 for i in range(n))
    return num / den if den > 0 else 0.0


def quartile_arcs(token_list):
    """
    Divide tokens into 4 quartiles and compute mean S₂ and mean valence per quartile.
    Returns (s2_arc [4 floats], val_arc [4 floats or None], val_intensity_arc [4 floats or None]).
    A quartile's valence is None if fewer than 2 matched tokens.
    """
    n = len(token_list)
    if n < 4:
        return None, None, None

    q_size = n / 4
    q_s2 = [[] for _ in range(4)]
    q_val = [[] for _ in range(4)]

    for i, tok in enumerate(token_list):
        q = min(3, int(i / q_size))
        q_s2[q].append(tok.get("s2", 0.0))
        v = afinn_score(tok.get("token", ""))
        if v is not None:
            q_val[q].append(v)

    s2_arc = [statistics.mean(q) if q else 0.0 for q in q_s2]
    val_arc = [statistics.mean(q) if len(q) >= 2 else None for q in q_val]
    val_intensity_arc = [
        statistics.mean(abs(x) for x in q) if len(q) >= 2 else None for q in q_val
    ]
    return s2_arc, val_arc, val_intensity_arc


def classify_coupling(s2_arc, val_arc):
    """
    Return coupling label given 4-point arcs.
    s2_arc: list of 4 floats
    val_arc: list of 4 floats|None — skip poems with too few valence matches
    """
    val_clean = [v for v in val_arc if v is not None]
    if len(val_clean) < 3:
        return "insufficient_valence"

    # Use only quartiles where valence is available
    s2_pairs = [s2_arc[i] for i, v in enumerate(val_arc) if v is not None]
    val_pairs = val_clean

    r = pearson_r(s2_pairs, val_pairs)
    s2_slope = linear_slope(s2_arc)
    val_slope = linear_slope(val_pairs)

    if r is None:
        return "insufficient_valence"

    if r >= 0.7:
        return "synchronized"
    elif r <= -0.7:
        return "anti_synchronized"
    elif -0.3 <= r <= 0.3:
        return "decoupled"
    else:
        # Moderate correlation — use slopes to sub-classify
        if (s2_slope > 0) == (val_slope > 0):
            return "weak_synchronized"
        else:
            return "weak_anti_synchronized"


def run():
    results_path = Path("results/corpus_results.json")
    if not results_path.exists():
        print("corpus_results.json not found — run engine.py first")
        return

    with open(results_path) as f:
        corpus = json.load(f)

    # Fields are nested under 'metadata' in corpus_results.json
    for p in corpus:
        meta = p.get("metadata", {})
        p["author"] = meta.get("author")
        p["title"] = meta.get("title")
        p["era"] = meta.get("era")
        p["year"] = meta.get("year")
        p["language"] = meta.get("language", "en")

    # Filter to English poems with sufficient token count
    poems = [p for p in corpus if p.get("language", "en") == "en" and len(p.get("tokens", [])) >= 20]
    print(f"Analyzing {len(poems)} English poems...\n")

    # ── Per-poem arc analysis ──────────────────────────────────────────────────
    poem_arcs = []
    for poem in poems:
        tokens = poem["tokens"]
        s2_arc, val_arc, val_int_arc = quartile_arcs(tokens)
        if s2_arc is None:
            continue

        coupling = classify_coupling(s2_arc, val_arc)
        val_clean = [v for v in (val_arc or []) if v is not None]
        val_pairs = val_clean if val_clean else []
        s2_pairs = [s2_arc[i] for i, v in enumerate(val_arc or []) if v is not None] if val_arc else []

        r = pearson_r(s2_pairs, val_pairs) if len(s2_pairs) >= 3 else None
        s2_slope = linear_slope(s2_arc)
        val_slope = linear_slope(val_pairs) if val_pairs else None

        poem_arcs.append({
            "title": poem.get("title"),
            "author": poem.get("author"),
            "era": poem.get("era"),
            "year": poem.get("year"),
            "s2_arc": s2_arc,
            "val_arc": val_arc,
            "val_int_arc": val_int_arc,
            "coupling": coupling,
            "r": r,
            "s2_slope": s2_slope,
            "val_slope": val_slope,
            "avg_s2": statistics.mean(s2_arc),
            "n_tokens": len(tokens),
        })

    # ── Coupling distribution ──────────────────────────────────────────────────
    coupling_counts = defaultdict(int)
    for p in poem_arcs:
        coupling_counts[p["coupling"]] += 1

    total = len(poem_arcs)
    print("=" * 60)
    print("Arc Coupling Distribution")
    print("=" * 60)
    for label, count in sorted(coupling_counts.items(), key=lambda x: -x[1]):
        pct = 100 * count / total if total else 0
        print(f"  {label:<30} {count:3d}  ({pct:.1f}%)")
    print()

    # ── Coupled vs decoupled poems: who are the extremes? ─────────────────────
    coupled = [p for p in poem_arcs if p["coupling"] == "synchronized" and p["r"] is not None]
    anti = [p for p in poem_arcs if p["coupling"] == "anti_synchronized" and p["r"] is not None]
    decoupled = [p for p in poem_arcs if p["coupling"] == "decoupled" and p["r"] is not None]

    if coupled:
        coupled_sorted = sorted(coupled, key=lambda x: -x["r"])
        print("=" * 60)
        print(f"Most SYNCHRONIZED poems (S₂ arc ≈ sentiment arc, n={len(coupled)})")
        print("  [surprise and emotion co-occur]")
        print("=" * 60)
        for p in coupled_sorted[:8]:
            print(f"  r={p['r']:+.2f}  {str(p['author'] or '')[:30]:<30}  \"{str(p['title'] or '')[:40]}\"")
        print()

    if anti:
        anti_sorted = sorted(anti, key=lambda x: x["r"])
        print("=" * 60)
        print(f"Most ANTI-SYNCHRONIZED poems (S₂ ↑ as sentiment ↓, n={len(anti)})")
        print("  [poet surprises by going AGAINST emotional grain]")
        print("=" * 60)
        for p in anti_sorted[:8]:
            print(f"  r={p['r']:+.2f}  {str(p['author'] or '')[:30]:<30}  \"{str(p['title'] or '')[:40]}\"")
        print()

    if decoupled:
        print("=" * 60)
        print(f"Most DECOUPLED poems (r ≈ 0, n={len(decoupled)})")
        print("  [surprise and emotion are independent resources]")
        print("=" * 60)
        for p in sorted(decoupled, key=lambda x: abs(x["r"]))[:8]:
            print(f"  r={p['r']:+.2f}  {str(p['author'] or '')[:30]:<30}  \"{str(p['title'] or '')[:40]}\"")
        print()

    # ── S₂ arc shapes: are rising-S₂ poems more common? ─────────────────────
    s2_rising = [p for p in poem_arcs if p["s2_slope"] > 0.5]
    s2_falling = [p for p in poem_arcs if p["s2_slope"] < -0.5]
    s2_flat = [p for p in poem_arcs if abs(p["s2_slope"]) <= 0.5]

    val_rising = [p for p in poem_arcs if p["val_slope"] is not None and p["val_slope"] > 0.3]
    val_falling = [p for p in poem_arcs if p["val_slope"] is not None and p["val_slope"] < -0.3]

    print("=" * 60)
    print("S₂ Arc Shape Distribution")
    print("=" * 60)
    print(f"  Rising S₂ (front-loaded conventional → back-loaded surprise): {len(s2_rising)} ({100*len(s2_rising)/total:.1f}%)")
    print(f"  Falling S₂ (front-loaded surprise → back-loaded convention):  {len(s2_falling)} ({100*len(s2_falling)/total:.1f}%)")
    print(f"  Flat S₂:                                                        {len(s2_flat)} ({100*len(s2_flat)/total:.1f}%)")
    print()
    print("  [Previous finding: information_arcs_s2.md shows poems front-load surprise]")
    print()

    print("Sentiment Arc Shape Distribution")
    print("=" * 60)
    print(f"  Rising valence (poem brightens):  {len(val_rising)} ({100*len(val_rising)/total:.1f}%)")
    print(f"  Falling valence (poem darkens):   {len(val_falling)} ({100*len(val_falling)/total:.1f}%)")
    print()

    # ── Cross-tabulation: S₂ arc x Valence arc ──────────────────────────────
    print("=" * 60)
    print("S₂ arc × Sentiment arc cross-tabulation")
    print("=" * 60)
    types = {
        ("rising", "rising"):   "S₂↑ & sentiment↑  (intensifying)   ",
        ("rising", "falling"):  "S₂↑ & sentiment↓  (dark surprise)  ",
        ("falling", "rising"):  "S₂↓ & sentiment↑  (bright resolve) ",
        ("falling", "falling"): "S₂↓ & sentiment↓  (dark calm)      ",
    }
    counts = defaultdict(int)
    for p in poem_arcs:
        if p["val_slope"] is None:
            continue
        s2_dir = "rising" if p["s2_slope"] > 0.2 else ("falling" if p["s2_slope"] < -0.2 else "flat")
        val_dir = "rising" if p["val_slope"] > 0.2 else ("falling" if p["val_slope"] < -0.2 else "flat")
        if s2_dir != "flat" and val_dir != "flat":
            counts[(s2_dir, val_dir)] += 1

    for k, label in types.items():
        n = counts.get(k, 0)
        print(f"  {label}: {n}")
    print()

    # ── By era: which eras tend toward which coupling? ───────────────────────
    era_coupling = defaultdict(lambda: defaultdict(int))
    era_r = defaultdict(list)
    era_s2_slope = defaultdict(list)
    era_val_slope = defaultdict(list)

    for p in poem_arcs:
        era = p["era"] or "unknown"
        era_coupling[era][p["coupling"]] += 1
        if p["r"] is not None:
            era_r[era].append(p["r"])
        era_s2_slope[era].append(p["s2_slope"])
        if p["val_slope"] is not None:
            era_val_slope[era].append(p["val_slope"])

    eras_by_poems = sorted(era_r.keys(), key=lambda e: -len(era_r[e]))

    print("=" * 60)
    print("Era-level arc coupling statistics")
    print("=" * 60)
    header = f"  {'Era':<25} {'n':>4}  {'mean r':>7}  {'S₂ slope':>9}  {'val slope':>9}  {'dominant coupling'}"
    print(header)
    print("  " + "-" * 85)
    for era in eras_by_poems:
        rs = era_r[era]
        ss = era_s2_slope.get(era, [])
        vs = era_val_slope.get(era, [])
        mean_r = statistics.mean(rs) if rs else 0
        mean_ss = statistics.mean(ss) if ss else 0
        mean_vs = statistics.mean(vs) if vs else 0
        dom = max(era_coupling[era].items(), key=lambda x: x[1])[0] if era_coupling[era] else "—"
        print(
            f"  {era:<25} {len(rs):>4}  {mean_r:>+7.3f}  {mean_ss:>+9.3f}  {mean_vs:>+9.3f}  {dom}"
        )
    print()

    # ── By author: coupling tendencies ───────────────────────────────────────
    author_data = defaultdict(list)
    for p in poem_arcs:
        if p["r"] is not None:
            author_data[p["author"]].append(p)

    author_stats = {}
    for author, plist in author_data.items():
        if len(plist) < 2:
            continue
        rs = [p["r"] for p in plist if p["r"] is not None]
        author_stats[author] = {
            "n": len(plist),
            "mean_r": statistics.mean(rs) if rs else 0,
            "mean_s2_slope": statistics.mean(p["s2_slope"] for p in plist),
        }

    print("=" * 60)
    print("Author arc-coupling tendencies (≥2 poems)")
    print("=" * 60)
    print(f"  {'Author':<30} {'n':>3}  {'mean r':>7}  {'S₂ slope':>9}")
    print("  " + "-" * 60)
    for author, stats in sorted(author_stats.items(), key=lambda x: -x[1]["mean_r"]):
        a = str(author or "")
        print(f"  {a[:30]:<30} {stats['n']:>3}  {stats['mean_r']:>+7.3f}  {stats['mean_s2_slope']:>+9.3f}")
    print()

    # ── Case studies: most extreme examples ──────────────────────────────────
    print("=" * 60)
    print("Case studies: extreme arc patterns")
    print("=" * 60)

    # Poem with strongest synchronized arc
    best_sync = max(
        (p for p in poem_arcs if p["r"] is not None), key=lambda x: x["r"], default=None
    )
    # Poem with strongest anti-synchronized arc
    best_anti = min(
        (p for p in poem_arcs if p["r"] is not None), key=lambda x: x["r"], default=None
    )

    if best_sync:
        print(f"\nStrongest synchronized (r={best_sync['r']:+.3f}):")
        print(f"  \"{best_sync['title']}\" by {best_sync['author']}")
        print(f"  S₂ arc:       {['%.2f' % x for x in best_sync['s2_arc']]}")
        val_str = [('%.2f' % x if x is not None else 'N/A') for x in (best_sync['val_arc'] or [None]*4)]
        print(f"  Valence arc:  {val_str}")
        print(f"  Reading: as S₂ rises/falls, sentiment rises/falls in lockstep.")

    if best_anti:
        print(f"\nStrongest anti-synchronized (r={best_anti['r']:+.3f}):")
        print(f"  \"{best_anti['title']}\" by {best_anti['author']}")
        print(f"  S₂ arc:       {['%.2f' % x for x in best_anti['s2_arc']]}")
        val_str = [('%.2f' % x if x is not None else 'N/A') for x in (best_anti['val_arc'] or [None]*4)]
        print(f"  Valence arc:  {val_str}")
        print(f"  Reading: most surprising moments are least emotionally charged, and vice versa.")

    # ── Grand mean coupling r ────────────────────────────────────────────────
    all_r = [p["r"] for p in poem_arcs if p["r"] is not None]
    if all_r:
        grand_mean_r = statistics.mean(all_r)
        median_r = statistics.median(all_r)
        pos_r = sum(1 for r in all_r if r > 0) / len(all_r)
        print(f"\n{'='*60}")
        print("Grand summary: S₂ arc ↔ sentiment arc coupling")
        print(f"{'='*60}")
        print(f"  Mean Pearson r:    {grand_mean_r:+.4f}")
        print(f"  Median Pearson r:  {median_r:+.4f}")
        print(f"  % poems with r > 0 (synchronized): {100*pos_r:.1f}%")
        print()
        if abs(grand_mean_r) < 0.1:
            print("  → S₂ and sentiment arcs are LARGELY INDEPENDENT across the corpus.")
            print("    Poetic surprise and emotional charge operate as distinct registers.")
        elif grand_mean_r > 0:
            print("  → S₂ and sentiment arcs are WEAKLY POSITIVE across the corpus.")
            print("    Emotional intensity and informational surprise tend to co-occur.")
        else:
            print("  → S₂ and sentiment arcs are WEAKLY ANTI-CORRELATED across the corpus.")
            print("    Surprising moments tend to be emotionally cooler; emotional climaxes tend to be conventional.")

    return poem_arcs


if __name__ == "__main__":
    import os
    os.chdir(Path(__file__).parent.parent)
    run()
