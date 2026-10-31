"""
S2 Surprise Budget Allocation by Part-of-Speech Category

Research question: Where do poets invest their Straussian 'surprise budget'?
Does surprise concentrate in nouns, verbs, adjectives, or function words?
Do poets cluster into distinct 'surprise strategy' types?

Method:
  1. Load corpus_results.json token-level data.
  2. Classify each token into POS using a rule-based system (closed-class
     function words are enumerated explicitly; open-class content words use
     suffix heuristics).
  3. For each poem, the 'surprise budget' = sum of positive S2 values
     (artifact-free tokens only, p(newline) < 0.9).
  4. 'Allocation' = fraction of budget spent on each POS category.
  5. Aggregate by poet (≥3 poems) and era to find systematic strategies.
"""

import json
import re
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Rule-based POS classifier (no external data required)
# ---------------------------------------------------------------------------

FUNCTION_WORDS = {
    # Articles / determiners
    "a", "an", "the", "this", "that", "these", "those", "some", "any",
    "each", "every", "either", "neither", "no", "another", "all", "both",
    "few", "many", "much", "more", "most", "less", "least", "other",
    "such", "what", "which", "whose", "whatever", "whichever",
    # Personal pronouns
    "i", "me", "my", "myself", "mine",
    "you", "your", "yourself", "yours",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "it", "its", "itself",
    "we", "us", "our", "ours", "ourselves",
    "they", "them", "their", "theirs", "themselves",
    "one", "oneself",
    # Relative/interrogative pronouns
    "who", "whom", "whose", "which", "that",
    "whoever", "whomever", "whichever", "whatever",
    # Demonstrative pronouns (standalone)
    # Prepositions
    "in", "on", "at", "by", "for", "from", "to", "into", "onto", "upon",
    "with", "without", "within", "through", "throughout", "across",
    "over", "under", "above", "below", "between", "among", "around",
    "about", "against", "along", "before", "after", "behind", "beside",
    "besides", "beyond", "despite", "during", "except", "inside",
    "near", "of", "off", "out", "outside", "past", "per", "since",
    "than", "till", "toward", "towards", "underneath", "until", "unto",
    "up", "via", "within", "worth",
    # Coordinating conjunctions
    "and", "but", "or", "nor", "for", "yet", "so",
    # Subordinating conjunctions
    "if", "as", "when", "where", "while", "because", "since", "although",
    "though", "unless", "until", "after", "before", "whereas", "whether",
    "how", "lest", "once", "provided", "supposing", "than", "wherever",
    "whenever",
    # Auxiliary verbs
    "is", "am", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having",
    "do", "does", "did", "done", "doing",
    "will", "would", "shall", "should", "may", "might", "must",
    "can", "could", "need", "dare", "ought",
    # Negation
    "not", "n't", "never", "no",
    # Degree adverbs / function adverbs
    "very", "quite", "rather", "too", "so", "just", "also", "even",
    "still", "already", "again", "always", "often", "sometimes", "never",
    "here", "there", "now", "then", "today", "yesterday", "tomorrow",
    "thus", "therefore", "hence", "consequently",
    # Existential there
    "there",
    # Expletive it
    # Infinitive marker
    "to",
}

VERB_SUFFIXES = (
    "ify", "ize", "ise", "ate", "efy", "fy",
    "ened", "ened", "ened",
)

ADJ_SUFFIXES = (
    "ful", "less", "ous", "ious", "eous", "ious", "ive", "ative", "itive",
    "al", "ical", "ial", "able", "ible", "ible", "ic", "ish",
    "like", "ward", "wards", "ern", "most",
)

ADV_SUFFIXES = ("ly",)

COMMON_VERBS = {
    "said", "says", "say", "told", "tells", "tell",
    "came", "come", "comes", "go", "goes", "went", "gone",
    "see", "sees", "saw", "seen", "look", "looks", "looked",
    "know", "knows", "knew", "known", "think", "thinks", "thought",
    "feel", "feels", "felt", "seem", "seems", "seemed",
    "make", "makes", "made", "take", "takes", "took", "taken",
    "give", "gives", "gave", "given", "keep", "keeps", "kept",
    "stand", "stands", "stood", "fall", "falls", "fell", "fallen",
    "rise", "rises", "rose", "risen", "break", "breaks", "broke",
    "hold", "holds", "held", "turn", "turns", "turned",
    "grow", "grows", "grew", "grown", "lead", "leads", "led",
    "move", "moves", "moved", "pass", "passes", "passed",
    "run", "runs", "ran", "walk", "walks", "walked",
    "live", "lives", "lived", "die", "dies", "died",
    "find", "finds", "found", "leave", "leaves", "left",
    "begin", "begins", "began", "begun", "end", "ends", "ended",
    "call", "calls", "called", "put", "puts", "hear", "heard",
    "let", "lets", "set", "sets", "play", "plays", "played",
    "write", "writes", "wrote", "written", "read", "reads",
    "sing", "sings", "sang", "sung", "draw", "draws", "drew",
    "lie", "lies", "lay", "lain", "sit", "sits", "sat",
    "stand", "stood", "bear", "bears", "bore", "born",
    "bring", "brings", "brought", "build", "builds", "built",
    "buy", "buys", "bought", "catch", "catches", "caught",
    "cast", "casts", "cut", "cuts", "drink", "drinks", "drank",
    "drive", "drives", "drove", "eat", "eats", "ate", "eaten",
    "fight", "fights", "fought", "fly", "flies", "flew", "flown",
    "forget", "forgets", "forgot", "forgotten",
    "hang", "hangs", "hung", "hide", "hides", "hid", "hidden",
    "hit", "hits", "hurt", "hurts", "keep", "kept",
    "lose", "loses", "lost", "meet", "meets", "met",
    "pay", "pays", "paid", "ride", "rides", "rode", "ridden",
    "send", "sends", "sent", "shoot", "shoots", "shot",
    "show", "shows", "showed", "shown", "shut", "shuts", "shut",
    "sleep", "sleeps", "slept", "speak", "speaks", "spoke", "spoken",
    "spend", "spends", "spent", "spread", "spreads",
    "steal", "steals", "stole", "stolen", "strike", "strikes", "struck",
    "sweep", "sweeps", "swept", "swing", "swings", "swung",
    "teach", "teaches", "taught", "throw", "throws", "threw", "thrown",
    "understand", "understands", "understood", "wake", "wakes", "woke",
    "wear", "wears", "wore", "worn", "win", "wins", "won",
    "wish", "wishes", "wished", "wonder", "wonders", "wondered",
    "wait", "waits", "waited", "watch", "watches", "watched",
    "want", "wants", "wanted", "need", "needs", "needed",
    "ask", "asks", "asked", "answer", "answers", "answered",
    "open", "opens", "opened", "close", "closes", "closed",
    "carry", "carries", "carried", "pull", "pulls", "pulled",
    "push", "pushes", "pushed", "rise", "rises",
    "follow", "follows", "followed", "remain", "remains", "remained",
    "return", "returns", "returned", "reach", "reaches", "reached",
    "remember", "remembers", "remembered", "forget", "forgot",
    "change", "changes", "changed", "use", "uses", "used",
    "try", "tries", "tried", "help", "helps", "helped",
    "appear", "appears", "appeared", "happen", "happens", "happened",
    "allow", "allows", "allowed", "become", "becomes", "became",
    "create", "creates", "created", "show", "shows",
    "fall", "feel", "fill", "fills", "filled",
    "gather", "gathers", "gathered", "scatter", "scatters",
    "wake", "waken", "rise", "shone", "shine", "shines", "shined",
    "flow", "flows", "flowed", "blow", "blows", "blew", "blown",
}

COMMON_ADJ = {
    "good", "great", "new", "old", "high", "large", "small", "long",
    "big", "little", "young", "own", "last", "first", "next", "same",
    "right", "left", "far", "near", "open", "free", "full", "hard",
    "clear", "white", "black", "red", "green", "blue", "dark", "light",
    "bright", "warm", "cold", "hot", "cool", "soft", "sweet", "deep",
    "wide", "thin", "thick", "strong", "weak", "dead", "alive", "true",
    "false", "real", "bare", "pure", "fresh", "raw", "wild", "calm",
    "still", "quiet", "loud", "slow", "fast", "low", "high",
    "heavy", "dry", "wet", "empty", "whole", "round", "flat",
    "sharp", "smooth", "rough", "clean", "dirty",
    "happy", "sad", "glad", "glad", "mad", "bad", "evil", "holy",
    "sacred", "divine", "mortal", "immortal", "eternal", "temporal",
    "ancient", "modern", "strange", "familiar", "distant", "close",
    "alone", "lonely", "lost", "found", "born", "dead", "alive",
    "simple", "complex", "single", "double", "triple",
    "human", "divine", "earthly", "heavenly", "natural", "unnatural",
}


def classify_pos(token_str: str) -> str:
    """Return broad POS category for a GPT-2 token string."""
    raw = token_str.strip().lstrip()  # remove leading space

    # Punctuation / newline
    if not raw or raw in {"\n", " ", "\t"}:
        return "PUNCT"
    if all(c in r""".,;:!?'"()-–—…/\|@#$%^&*+=[]{}""" for c in raw):
        return "PUNCT"

    # Numeric
    if re.match(r"^-?[\d,\.]+$", raw):
        return "NUM"

    word = raw.lower()

    # Explicit function word list
    if word in FUNCTION_WORDS:
        return "FUNC"

    # -ing suffix: gerund/present participle (verb-like)
    if word.endswith("ing") and len(word) > 4:
        return "VERB"

    # -ed suffix: past tense/participle
    if word.endswith("ed") and len(word) > 3:
        return "VERB"

    # Common verbs
    if word in COMMON_VERBS:
        return "VERB"

    # Adverb: -ly suffix
    if word.endswith("ly") and len(word) > 4:
        return "ADV"

    # Adjective suffixes
    for sfx in ADJ_SUFFIXES:
        if word.endswith(sfx) and len(word) > len(sfx) + 2:
            return "ADJ"

    # Common adjectives
    if word in COMMON_ADJ:
        return "ADJ"

    # Verb-forming suffixes
    for sfx in VERB_SUFFIXES:
        if word.endswith(sfx) and len(word) > len(sfx) + 2:
            return "VERB"

    # Proper noun heuristic: capitalized token not at start (preceded by space and capitalized)
    if token_str.startswith(" ") and raw[0].isupper():
        return "PROPN"

    # Default: treat as common noun / content word
    return "NOUN"


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------

def load_corpus(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)


ARTIFACT_THRESHOLD = 0.9  # p(newline) < 0.9 = artifact-free


def analyze_poem(poem: dict) -> dict | None:
    """Compute POS budget allocation for one poem."""
    tokens = poem.get("tokens", [])
    if not tokens:
        return None

    meta = poem.get("metadata", {})
    era = meta.get("era", "unknown")
    author = meta.get("author", "Unknown")
    title = meta.get("title", "")

    # POS-bucket accumulators
    pos_budget = defaultdict(float)   # total positive S2 per category
    pos_count = defaultdict(int)       # token count per category
    pos_s2_sum = defaultdict(float)    # total S2 (pos+neg) per category

    total_budget = 0.0
    total_tokens = 0

    for tok in tokens:
        p_nl = tok.get("p_newline", 0)
        if p_nl >= ARTIFACT_THRESHOLD:
            continue  # skip artifact tokens

        s2 = tok.get("s2", 0)
        token_str = tok.get("token", "")
        pos = classify_pos(token_str)

        pos_count[pos] += 1
        pos_s2_sum[pos] += s2
        total_tokens += 1

        if s2 > 0:
            pos_budget[pos] += s2
            total_budget += s2

    if total_budget == 0 or total_tokens < 10:
        return None

    # Normalize to fractions
    pos_frac = {pos: v / total_budget for pos, v in pos_budget.items()}

    return {
        "era": era,
        "author": author,
        "title": title,
        "total_budget": total_budget,
        "total_tokens": total_tokens,
        "budget_per_token": total_budget / total_tokens,
        "pos_frac": dict(pos_frac),
        "pos_count": dict(pos_count),
        "pos_avg_s2": {pos: pos_s2_sum[pos] / pos_count[pos]
                       for pos in pos_count if pos_count[pos] > 0},
    }


ALL_POS = ["FUNC", "NOUN", "VERB", "ADJ", "ADV", "PROPN", "PUNCT", "NUM", "OTHER"]


def main():
    corpus_path = Path(__file__).parent.parent / "results" / "corpus_results.json"
    corpus = load_corpus(str(corpus_path))

    poem_results = []
    for poem in corpus:
        r = analyze_poem(poem)
        if r:
            poem_results.append(r)

    print(f"Analyzed {len(poem_results)} poems with budget data\n")

    # ---- Era-level aggregation ----
    era_data = defaultdict(list)
    for r in poem_results:
        era_data[r["era"]].append(r)

    # For each era, compute mean fraction of budget in each POS
    era_summary = {}
    for era, items in era_data.items():
        if len(items) < 2:
            continue
        fracs = defaultdict(list)
        bpw = []
        for it in items:
            for pos in ALL_POS:
                fracs[pos].append(it["pos_frac"].get(pos, 0))
            bpw.append(it["budget_per_token"])
        era_summary[era] = {
            "n": len(items),
            "mean_bpt": sum(bpw) / len(bpw),
            "mean_frac": {pos: sum(fracs[pos]) / len(fracs[pos]) for pos in ALL_POS},
        }

    # Sort eras by NOUN fraction (descending)
    print("=== ERA-LEVEL SURPRISE BUDGET ALLOCATION ===")
    print("(fraction of positive S2 budget allocated to each POS)\n")
    print(f"{'Era':<22} {'N':>3} {'FUNC':>6} {'NOUN':>6} {'VERB':>6} {'ADJ':>6} {'ADV':>6} {'PROPN':>6} {'PUNCT':>6}")
    print("-" * 72)

    sorted_eras = sorted(era_summary.items(), key=lambda x: x[1]["mean_frac"]["NOUN"], reverse=True)
    for era, es in sorted_eras:
        mf = es["mean_frac"]
        print(f"{era:<22} {es['n']:>3}  "
              f"{mf['FUNC']:>5.1%}  {mf['NOUN']:>5.1%}  {mf['VERB']:>5.1%}  "
              f"{mf['ADJ']:>5.1%}  {mf['ADV']:>5.1%}  {mf['PROPN']:>5.1%}  {mf['PUNCT']:>5.1%}")

    # ---- Poet-level aggregation ----
    print("\n\n=== POET-LEVEL SURPRISE BUDGET ALLOCATION ===")
    print("(poets with ≥3 poems; sorted by VERB fraction)\n")

    poet_data = defaultdict(list)
    for r in poem_results:
        poet_data[r["author"]].append(r)

    poet_summary = {}
    for author, items in poet_data.items():
        if len(items) < 3:
            continue
        fracs = defaultdict(list)
        bpw = []
        for it in items:
            for pos in ALL_POS:
                fracs[pos].append(it["pos_frac"].get(pos, 0))
            bpw.append(it["budget_per_token"])
        poet_summary[author] = {
            "n": len(items),
            "era": items[0]["era"],
            "mean_bpt": sum(bpw) / len(bpw),
            "mean_frac": {pos: sum(fracs[pos]) / len(fracs[pos]) for pos in ALL_POS},
        }

    print(f"{'Poet':<30} {'N':>3} {'Era':<18} {'FUNC':>6} {'NOUN':>6} {'VERB':>6} {'ADJ':>6} {'ADV':>6}")
    print("-" * 90)

    sorted_poets = sorted(poet_summary.items(), key=lambda x: x[1]["mean_frac"]["VERB"], reverse=True)
    for author, ps in sorted_poets:
        mf = ps["mean_frac"]
        print(f"{author:<30} {ps['n']:>3}  {ps['era']:<18} "
              f"{mf['FUNC']:>5.1%}  {mf['NOUN']:>5.1%}  {mf['VERB']:>5.1%}  "
              f"{mf['ADJ']:>5.1%}  {mf['ADV']:>5.1%}")

    # ---- Extremes analysis: which poets concentrate surprise most narrowly? ----
    print("\n\n=== SURPRISE CONCENTRATION ANALYSIS ===")
    print("Poets who allocate >35% of surprise budget to a single POS category\n")

    for author, ps in sorted(poet_summary.items()):
        mf = ps["mean_frac"]
        for pos in ALL_POS:
            if mf[pos] > 0.35:
                print(f"  {author:<30} {pos}: {mf[pos]:.1%}  (era: {ps['era']}, n={ps['n']})")

    # ---- Top-line statistics ----
    all_fracs = defaultdict(list)
    all_bpt = []
    for r in poem_results:
        for pos in ALL_POS:
            all_fracs[pos].append(r["pos_frac"].get(pos, 0))
        all_bpt.append(r["budget_per_token"])

    print("\n\n=== CORPUS-WIDE AVERAGE BUDGET ALLOCATION ===")
    for pos in ALL_POS:
        vals = all_fracs[pos]
        if vals:
            print(f"  {pos:<8}: {sum(vals)/len(vals):.1%} (max {max(vals):.1%})")
    print(f"\n  Mean budget/token: {sum(all_bpt)/len(all_bpt):.4f} bits")

    # ---- Save results ----
    results = {
        "corpus_poems": len(poem_results),
        "era_summary": {
            era: {
                "n": es["n"],
                "mean_bpt": round(es["mean_bpt"], 4),
                "mean_frac": {pos: round(v, 4) for pos, v in es["mean_frac"].items()},
            }
            for era, es in era_summary.items()
        },
        "poet_summary": {
            author: {
                "n": ps["n"],
                "era": ps["era"],
                "mean_bpt": round(ps["mean_bpt"], 4),
                "mean_frac": {pos: round(v, 4) for pos, v in ps["mean_frac"].items()},
            }
            for author, ps in poet_summary.items()
        },
        "corpus_avg_frac": {pos: round(sum(all_fracs[pos]) / len(all_fracs[pos]), 4) for pos in ALL_POS if all_fracs[pos]},
    }

    out_path = Path(__file__).parent.parent / "results" / "s2_pos_budget.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return results


if __name__ == "__main__":
    main()
