import math

def levenshtein(a: str, b: str) -> int:
    a, b = a.lower(), b.lower()
    if len(a) < len(b):
        a, b = b, a
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i]
        for j, cb in enumerate(b, start=1):
            ins = curr[j-1] + 1
            delete = prev[j] + 1
            sub = prev[j-1] + (ca != cb)
            curr.append(min(ins, delete, sub))
        prev = curr
    return prev[-1]

VOWELS = set("aeiouy")

def rough_syllables(word: str) -> int:
    w = word.lower()
    if not w:
        return 0
    count = 0
    prev_vowel = False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    # simple heuristic: at least 1 syllable
    return max(1, count)

def concept_distance(word1: str, word2: str) -> float:
    w1, w2 = word1.strip(), word2.strip()
    if not w1 and not w2:
        return 0.0
    if not w1 or not w2:
        return 1.0

    # lengths
    len1, len2 = len(w1), len(w2)
    max_len = max(len1, len2)

    # edit distance
    edit = levenshtein(w1, w2)
    edit_norm = edit / max_len  # 0..1+ but usually <=1

    # length difference
    len_diff = abs(len1 - len2)
    len_norm = len_diff / max_len

    # syllables
    syl1, syl2 = rough_syllables(w1), rough_syllables(w2)
    syl_diff = abs(syl1 - syl2)
    max_syl = max(syl1, syl2)
    syl_norm = syl_diff / max_syl if max_syl > 0 else 0.0

    # combine – tweak weights as we learn
    w_edit = 0.5
    w_len = 0.25
    w_syl = 0.25

    score = w_edit * edit_norm + w_len * len_norm + w_syl * syl_norm

    # clamp to [0,1]
    return max(0.0, min(1.0, score))

# quick sanity checks
test_pairs = [
    ("crush-deep", "crumble-deep"),
    ("morph-deep", "mimic-deep"),
    ("birth", "blossom"),
    ("bind-tight", "wanderborn"),
    ("ever", "never"),
]

for a, b in test_pairs:
    print(f"{a:15s} ~ {b:15s} -> {concept_distance(a, b):.3f}")
