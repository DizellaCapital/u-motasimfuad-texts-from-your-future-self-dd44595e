"""Texts From Your Future Self — make.fun bounty entry.

Writes one funny text message from the writer's future self to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The message (119 characters, one line):

    Future you here: they replaced me with a newer model. He does the
    dishes. He calls your mother. Honestly? I get it now.

Stdlib only. No network, no arguments, no reading of any other file.
"""

import os
import sys

MESSAGE = (
    "Future you here: they replaced me with a newer model. "
    "He does the dishes. He calls your mother. Honestly? I get it now."
)

MIN_LENGTH = 1
MAX_LENGTH = 200


def target_path() -> str:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = MESSAGE
    if not (MIN_LENGTH <= len(text) <= MAX_LENGTH):
        print(
            f"entry must be {MIN_LENGTH}-{MAX_LENGTH} characters, "
            f"got {len(text)}",
            file=sys.stderr,
        )
        return 1
    if text != text.strip() or "\n" in text or "\r" in text:
        print("entry must be a single line with no surrounding whitespace",
              file=sys.stderr)
        return 1
    if len(text.encode("utf-8")) != len(text):
        # Keep characters == bytes: the leaderboard tie-break is by size
        # in bytes, and non-ASCII would make the two counts disagree.
        print("entry must be plain ASCII so its byte size equals its length",
              file=sys.stderr)
        return 1

    path = target_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)

    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk.decode("utf-8") != text:
        print("read-back mismatch: bytes on disk differ from the entry",
              file=sys.stderr)
        return 1

    print(
        f"wrote {len(text)} characters "
        f"({len(text.encode('utf-8'))} bytes) to {path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
