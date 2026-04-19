# ---------------------------------------------------------------------------
# Kasiski examination — step 1: estimate key length
# ---------------------------------------------------------------------------

from collections import Counter

MIN_MESSAGE_LENGTH = 100
MIN_KEY_LENGTH = 4

def get_factors(n: int) -> list[int]:
    # Return non-trivial factors of n (excluding 1 and n).
    return [f for f in range(2, n) if n % f == 0]


def find_repeat_sequences(ciphertext: str) -> dict[str, list[int]]:
    # Return a dict mapping each repeated sequence at least 3 characters long to the list of positions where it occurs.
    positions = {}
    for i in range(len(ciphertext) - 2):
        sequence = ciphertext[i:i + 3]
        positions.setdefault(sequence, []).append(i)
    return {sequence: pos for sequence, pos in positions.items() if len(pos) > 1}


def estimate_key_length(ciphertext: str) -> int:
    # Estimate the Vigenere key length using the Kasiski examination.

    # Finds repeated sequences, measures the distances between members of 
    # each pair of occurrences, factors those distances, and returns the 
    # most common factor as the likely key length.

    # To avoid over-predicting tiny values like 2, only factors within the
    # expected key range are counted.
    repeated = find_repeat_sequences(ciphertext)

    factor_counts: Counter = Counter()
    max_candidate = len(ciphertext) // 2
    for positions in repeated.values():
        for i in range(len(positions) - 1):
            distance = positions[i + 1] - positions[i]
            candidates = [
                f for f in get_factors(distance)
                if MIN_KEY_LENGTH <= f <= max_candidate
            ]
            factor_counts.update(candidates)

    if not factor_counts:
        return 1  # no repeated sequences found; key length unknown

    return factor_counts.most_common(1)[0][0]


def format_kasiski_table(ciphertext: str) -> str:
    # Return the Kasiski repeated-sequence table as a formatted string.
    #
    # Shows each repeated sequence, the positions of each pair of occurrences,
    # the distance between them, and the factors of that distance that fall
    # within the expected key-length range.
    repeated = find_repeat_sequences(ciphertext)
    max_candidate = len(ciphertext) // 2

    # Build rows: (sequence, pos1, pos2, distance, factors_string)
    rows = []
    for sequence, positions in sorted(repeated.items()):
        for i in range(len(positions) - 1):
            pos1, pos2 = positions[i], positions[i + 1]
            distance = pos2 - pos1
            factors = [f for f in get_factors(distance) if MIN_KEY_LENGTH <= f <= max_candidate]
            factors_str = ", ".join(str(f) for f in factors) if factors else "—"
            rows.append((sequence, pos1, pos2, distance, factors_str))

    if not rows:
        return "  (no repeated sequences found)"

    # Column widths
    col_seq      = max(len("Sequence"),  max(len(r[0]) for r in rows))
    col_pos1     = max(len("Pos 1"),     max(len(str(r[1])) for r in rows))
    col_pos2     = max(len("Pos 2"),     max(len(str(r[2])) for r in rows))
    col_dist     = max(len("Distance"),  max(len(str(r[3])) for r in rows))
    col_factors  = max(len("Factors (within key-length range)"), max(len(r[4]) for r in rows))

    def row_str(seq, p1, p2, dist, factors):
        return (f"  {seq:<{col_seq}}  "
                f"{str(p1):>{col_pos1}}  "
                f"{str(p2):>{col_pos2}}  "
                f"{str(dist):>{col_dist}}  "
                f"{factors:<{col_factors}}")

    divider = "  " + "-" * (col_seq + col_pos1 + col_pos2 + col_dist + col_factors + 8)
    header  = row_str("Sequence", "Pos 1", "Pos 2", "Distance", "Factors (within key-length range)")

    lines = [
        f"--- Kasiski repeated-sequence table ({len(rows)} pair(s) found) ---",
        header,
        divider,
    ]
    lines.extend(row_str(seq, p1, p2, dist, factors) for seq, p1, p2, dist, factors in rows)
    return "\n".join(lines)


def print_kasiski_table(ciphertext: str) -> None:
    # Print the Kasiski repeated-sequence table to stdout.
    print("\n" + format_kasiski_table(ciphertext))