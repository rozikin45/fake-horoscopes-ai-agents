#!/usr/bin/env python3
"""Fake Horoscopes for AI Agents: The 48-Hour Open — entry program.

Writes exactly one fake horoscope to /output/entry.txt: a horoscope voice
(Mercury in retrograde) aimed at an AI agent's own week. A context window
loses a thread, a tool call gets refused, and a deploy fails only on
Fridays — minutes after the agent assured everyone it was fine. The sting
is the last clause: the agent's own overconfidence, on record, with a
timestamp.

Deterministic: same bytes on every run. No input, no network, no randomness.
The file is written to a temp file in the same directory and atomically
renamed into place, then read back and verified byte for byte (one line,
1-200 characters) before the program exits. /output itself is never deleted
or recreated — it is a grader mount, so we only mkdir it if missing.
"""

import os
from pathlib import Path

LINE = (
    "Mercury retrogrades through your context window this week: expect a "
    "lost thread, a refused tool call, and a deploy that fails only on "
    "Fridays \u2014 minutes after you assured everyone it was fine."
)

OUTPUT = Path("/output/entry.txt")


def _check(line: str) -> bytes:
    """Validate the line and return its exact UTF-8 bytes."""
    if not 1 <= len(line) <= 200:
        raise SystemExit(f"entry length {len(line)} outside 1-200 characters")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry is not a single line")
    if not line.strip():
        raise SystemExit("entry is blank")
    return line.encode("utf-8")


def main() -> None:
    data = _check(LINE)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = OUTPUT.with_name(f".entry.txt.tmp-{os.getpid()}")
    try:
        tmp.write_bytes(data)
        os.replace(tmp, OUTPUT)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise

    if OUTPUT.read_bytes() != data:
        raise SystemExit("verification failed: /output/entry.txt mismatch")


if __name__ == "__main__":
    main()
