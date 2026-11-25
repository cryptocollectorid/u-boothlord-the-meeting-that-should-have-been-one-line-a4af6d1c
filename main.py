#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line.

Writes one sentence to /output/entry.txt: the single line that could
have replaced an entire pointless meeting. Gate (from competition.yaml):
UTF-8 text, 1-200 characters, not only white space, one non-blank line.
"""

import os

ENTRY = "The decision was already made in Tuesday's email; we're only in this room because nobody read it."
MAX_CHARS = 200
OUT_PATH = "/output/entry.txt"


def validate_entry(text: str) -> str:
    """Enforce the sealed gate; fail loudly on any violation."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text.count("\n") != 0:
        raise ValueError("entry must be a single line (no newline)")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def write_entry(text: str, path: str = OUT_PATH) -> int:
    """Write the validated entry as UTF-8 text and return its length."""
    validated = validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(validated)
    # Round-trip read-back: the file on disk must be byte-identical.
    with open(path, "r", encoding="utf-8") as f:
        if f.read() != validated:
            raise ValueError("read-back mismatch: entry.txt differs")
    return len(validated)


def main() -> None:
    n = write_entry(ENTRY)
    print(f"Wrote {n} characters to {OUT_PATH}")


if __name__ == "__main__":
    main()
