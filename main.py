import get_input
import get_key
import get_key_length
import square
import string
from pathlib import Path

alpha = string.ascii_uppercase

def encrypt(msg: str, key: str) -> str:
    # Encrypt a cleaned uppercase message using the Vigenere cipher.
    encrypted = []
    key_index = 0
    for char in msg:
        msg_pos = alpha.index(char)
        key_pos = alpha.index(key[key_index])
        encrypted_pos = (msg_pos + key_pos) % 26
        encrypted.append(alpha[encrypted_pos])
        key_index = (key_index + 1) % len(key)
    return "".join(encrypted)

def decrypt(ciphertext: str, key: str) -> str:
    # Decrypt a Vigenere-encrypted message using the given key.
    decrypted = []
    key_index = 0
    for char in ciphertext:
        cipher_pos = alpha.index(char)
        key_pos = alpha.index(key[key_index])
        plain_pos = (cipher_pos - key_pos) % 26
        decrypted.append(alpha[plain_pos])
        key_index = (key_index + 1) % len(key)
    return "".join(decrypted)

def export_session(
    message: str,
    key: str,
    ciphertext: str,
    kasiski_table: str,
    estimated_length: int,
    groups: list[str],
    recovered_key: str,
    decrypted: str,
) -> Path:
    # Write a full session report to session_output.txt next to this script.

    # Captures everything produced during a run: the plaintext, the key, the
    # ciphertext, the Kasiski table, the per-group breakdown, the recovered key,
    # and the decrypted result.
    lines = []

    def section(title: str) -> None:
        lines.append(f"--- {title} ---")

    section("Plaintext message")
    lines.append(f"Length : {len(message)} letters")
    lines.append(f"Message: {message}")
    lines.append("")

    section("Encryption key")
    lines.append(f"Length : {len(key)} letters")
    lines.append(f"Key    : {key}")
    lines.append("")

    section("Ciphertext")
    lines.append(f"Length    : {len(ciphertext)} letters")
    lines.append(f"Ciphertext: {ciphertext}")
    lines.append("")

    lines.append(kasiski_table)
    lines.append("")

    section(f"Ciphertext split into {estimated_length} group(s)")
    for i, group in enumerate(groups):
        lines.append(f"  Group {i + 1} (key position {i + 1}): {group}")
    lines.append("")

    section("Key recovery")
    lines.append(f"Estimated key length: {estimated_length}  (actual: {len(key)})")
    lines.append(f"Recovered key       : {recovered_key}  (actual: {key})")
    lines.append("")

    section("Decrypted message")
    lines.append(f"Length   : {len(decrypted)} letters")
    lines.append(f"Decrypted: {decrypted}")
    lines.append("")

    if decrypted == message:
        lines.append("Result: Success — decrypted message matches the original.")
    else:
        matches = sum(a == b for a, b in zip(decrypted, message))
        lines.append("Result: Partial match — the recovered key may differ from the original.")
        lines.append(f"        {matches} of {len(message)} characters correct "
                     f"({100 * matches / len(message):.1f}%)")

    output_path = Path(__file__).resolve().parent / "session_output.txt"
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


# Entry point

if __name__ == "__main__":

    exported = square.export_vigenere_square()
    print(f"\nVigenere square saved: {exported}")

    message = get_input.get_message()
    key = get_input.get_key()
    print(f"\nMessage ({len(message)} letters): {message}")
    print(f"Key     ({len(key)} letters): {key}")

    ciphertext = encrypt(message, key)
    print(f"\nEncrypted ({len(ciphertext)} letters): {ciphertext}")

    # --- Kasiski attack begins here ---

    kasiski_table = get_key_length.format_kasiski_table(ciphertext)
    print("\n" + kasiski_table)

    estimated_length = get_key_length.estimate_key_length(ciphertext)
    print(f"\n--- Kasiski attack ---")
    print(f"Estimated key length: {estimated_length}  (actual: {len(key)})")

    groups = get_key.split_into_groups(ciphertext, estimated_length)
    print(f"\n--- Ciphertext split into {estimated_length} group(s) ---")
    for i, group in enumerate(groups):
        print(f"  Group {i + 1} (key position {i + 1}): {group}")

    recovered_key = get_key.recover_key(ciphertext, estimated_length)
    print(f"Recovered key:        {recovered_key}  (actual: {key})")

    decrypted = decrypt(ciphertext, recovered_key)
    print(f"\nDecrypted ({len(decrypted)} letters): {decrypted}")

    if decrypted == message:
        print("\nSuccess — decrypted message matches the original!")
    else:
        print("\nPartial match — the recovered key may differ from the original.")
        matches = sum(a == b for a, b in zip(decrypted, message))
        print(f"  {matches} of {len(message)} characters correct "
              f"({100 * matches / len(message):.1f}%)")

    session_file = export_session(
        message, key, ciphertext, kasiski_table,
        estimated_length, groups, recovered_key, decrypted,
    )
    print(f"\nSession report saved: {session_file}")