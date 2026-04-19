# ---------------------------------------------------------------------------
# Kasiski examination — step 2: frequency analysis to recover the key
# ---------------------------------------------------------------------------

from collections import Counter
import string


alpha = string.ascii_uppercase
# Expected letter frequencies in English text (A–Z), expressed as
# proportions.  Source: standard English monograph frequencies.
ENGLISH_FREQUENCIES = [
    0.08167,  # A
    0.01492,  # B
    0.02782,  # C
    0.04253,  # D
    0.12702,  # E
    0.02228,  # F
    0.02015,  # G
    0.06094,  # H
    0.06966,  # I
    0.00153,  # J
    0.00772,  # K
    0.04025,  # L
    0.02406,  # M
    0.06749,  # N
    0.07507,  # O
    0.01929,  # P
    0.00095,  # Q
    0.05987,  # R
    0.06327,  # S
    0.09056,  # T
    0.02758,  # U
    0.00978,  # V
    0.02360,  # W
    0.00150,  # X
    0.01974,  # Y
    0.00074,  # Z
]


def split_into_groups(ciphertext: str, key_length: int) -> list[str]:
    # Split ciphertext into groups by key position.

    # Group 0 contains every character at positions 0, key_length, 2*key_length, …
    # Group 1 contains every character at positions 1, key_length+1, 2*key_length+1, …
    # and so on.

    # Each group was encrypted with a single Caesar shift (one letter of the
    # key), so standard frequency analysis can recover that letter.
    groups = [""] * key_length
    for i, char in enumerate(ciphertext):
        groups[i % key_length] += char
    return groups


def chi_squared_score(observed_counts: Counter, total: int, shift: int) -> float:
    # Score a candidate Caesar shift using the chi-squared statistic.

    # For a given shift, we ask: "If this group was shifted by `shift`,
    # how well do the resulting letter frequencies match English?"

    # Lower scores indicate a better match to English.

    # The formula for each letter position p is:
    #     (observed[p] - expected[p])^2 / expected[p]

    # where observed[p] is how many times the letter at position (p + shift) % 26
    # appears in the group, and expected[p] is how many times we'd expect letter p
    # to appear in English text of this length.
    
    score = 0.0
    for i in range(26):
        expected = ENGLISH_FREQUENCIES[i] * total
        # After undoing the shift, position i in plaintext corresponds
        # to position (i + shift) % 26 in the ciphertext group.
        observed = observed_counts.get(alpha[(i + shift) % 26], 0)
        if expected > 0:
            score += (observed - expected) ** 2 / expected
    return score


def recover_key_letter(group: str) -> str:
    # Determine which key letter (Caesar shift) was used to encrypt a group.
    #
    # Tries all 26 possible shifts and returns the one whose chi-squared
    # score against English letter frequencies is lowest — i.e., the shift
    # that makes the group look most like normal English.

    counts = Counter(group)
    total = len(group)

    best_shift = 0
    best_score = float("inf")
    for shift in range(26):
        score = chi_squared_score(counts, total, shift)
        if score < best_score:
            best_score = score
            best_shift = shift

    return alpha[best_shift]


def recover_key(ciphertext: str, key_length: int) -> str:
    # Recover the full key by applying frequency analysis to each group.
    groups = split_into_groups(ciphertext, key_length)
    return "".join(recover_key_letter(group) for group in groups)