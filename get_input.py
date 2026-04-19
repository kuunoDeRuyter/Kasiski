#  ---------------------------------------------------------------------------
#  Input collection
#  ---------------------------------------------------------------------------

from pathlib import Path
import re

MIN_MESSAGE_LENGTH = 100
MIN_KEY_LENGTH = 4

SAMPLES_FILE = Path(__file__).resolve().parent / "readability_text_samples.txt"


def load_samples() -> list[str]:
    # Load the sample texts from the samples file.
    raw = SAMPLES_FILE.read_text(encoding="utf-8")
    return [para.strip() for para in raw.split("\n\n") if para.strip()]


def clean_message(raw: str) -> str:
    # Strip non-alpha characters and convert to uppercase.
    return re.sub(r"[^A-Za-z]", "", raw).upper()


def get_message() -> str:
    # Prompt the user for a plaintext message, or let them pick a sample text.

    print("Enter a message containing at least 100 letters to encrypt, or press Enter to choose text from the samples.")
    while True:
        raw = input("Message: ").strip()

        if raw == "":
            samples = load_samples()
            print()
            for i, sample in enumerate(samples, start=1):
                preview = sample[:200].replace("\n", " ")
                print(f"  [{i}] {preview}...\n")
            while True:
                choice = input(f"Choose a sample (1–{len(samples)}): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(samples):
                    return clean_message(samples[int(choice) - 1])
                print(f"  Please enter a number between 1 and {len(samples)}.\n")

        cleaned = clean_message(raw)
        if len(cleaned) >= MIN_MESSAGE_LENGTH:
            return cleaned
        shortage = MIN_MESSAGE_LENGTH - len(cleaned)
        print(f"  Message too short — {len(cleaned)} letters after removing spaces "
              f"and punctuation. Please add at least {shortage} more letter(s).\n")


def get_key() -> str:
    # Prompt the user for an alphabetic keyword of at least 4 letters.
    while True:
        raw = input("Enter a keyword of at least 4 letters: ").strip().upper()
        if not raw.isalpha():
            print("  Keywords must contain only letters. Please try again.\n")
        elif len(raw) < MIN_KEY_LENGTH:
            shortage = MIN_KEY_LENGTH - len(raw)
            print(f"  Keyword too short — {len(raw)} letters. "
                  f"Please add at least {shortage} more letter(s).\n")
        else:
            return raw