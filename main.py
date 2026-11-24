#!/usr/bin/env python3
"""Write the judged one-line office joke to /output/entry.txt, atomically.

The gate requires UTF-8 text of 1..200 characters, not only whitespace, with
no trailing newline. Every check runs *before* the atomic replace, so a bad
build can never leave a partial or invalid artifact in /output.
"""

from __future__ import annotations

import os
import tempfile

JOKE = "In our no-blame culture, the postmortem says 'we' and my performance review says 'you.'"
OUTPUT_FILE = "entry.txt"
MAX_CHARS = 200


def entry_bytes() -> bytes:
    """Validate the joke and return its exact UTF-8 bytes."""
    if not isinstance(JOKE, str) or not JOKE.strip():
        raise ValueError("entry must be non-blank text")
    if "\n" in JOKE or "\r" in JOKE:
        raise ValueError("entry must be a single line")
    if len(JOKE) > MAX_CHARS:
        raise ValueError(f"entry exceeds {MAX_CHARS} characters")
    data = JOKE.encode("utf-8")
    # A clean round-trip proves the text is well-formed UTF-8; the explicit
    # newline check keeps the artifact free of a trailing byte.
    if data.decode("utf-8") != JOKE or data.endswith(b"\n"):
        raise ValueError("entry must be valid UTF-8 with no trailing newline")
    return data


def write_atomically(data: bytes) -> str:
    """Write bytes to a private temp file in the output dir, then replace."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, OUTPUT_FILE)
    fd, tmp = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=out_dir)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, dest)
    except BaseException:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
        raise
    return dest


def main() -> None:
    data = entry_bytes()
    dest = write_atomically(data)
    print(f"wrote {dest}: {len(data)} bytes, {len(JOKE)} chars")


if __name__ == "__main__":
    main()
