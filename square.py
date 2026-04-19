# ---------------------------------------------------------------------------
# Alphabet and Vigenere square
# ---------------------------------------------------------------------------

# The Vigenere square will be exported as a text file to the project root.
# Usage: (key_letter (left column), plain_letter (top row)) → cipher_letter
# e.g., square[('B', 'T')]  → 'U'

import string
from pathlib import Path

alpha = string.ascii_uppercase

square = {
    (alpha[i], alpha[j]): alpha[(i + j) % 26]
    for i in range(26)
    for j in range(26)
}


def build_vigenere_square_text() -> str:
    # Return the Vigenere square as a formatted text table.
    headers = "  ".join(alpha)
    lines = [
        "Vigenere Square",
        "",
        "Row headers (left) are letters from the keyword.",
        "Column headers (top) are letters from the plaintext message.",
        "",
        "    " + headers,
        "   " + "-" * (len(headers) + 2),
    ]
    for key_letter in alpha:
        row = "  ".join(square[(key_letter, plain_letter)] for plain_letter in alpha)
        lines.append(f"{key_letter} | {row}")
    return "\n".join(lines)


def export_vigenere_square() -> Path:
    # Export the Vigenere square as a text file to the project root.
    output_path = Path(__file__).resolve().parent / "vigenere_square.txt"
    output_path.write_text(build_vigenere_square_text() + "\n", encoding="utf-8")
    return output_path