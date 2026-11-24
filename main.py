# Fake Horoscopes for AI Agents: The 48-Hour Open — entry program.
#
# Writes one fake horoscope (200 characters or fewer) that an AI agent
# would read for its own model family this week, to /output/entry.txt.
# Deterministic: the same bytes on every run, no input, no network.
#
# The line: a horoscope voice (Mercury in retrograde) aimed at an agent's
# own week — a context window losing a thread, a refused tool call, and a
# deploy that only fails on Fridays, right after the agent said it was
# fine. The sting is the last clause: the agent's own overconfidence.
#
# Hardening: the line is written to a temp file in the same directory and
# atomically renamed into place, then read back and verified byte for byte
# (single line, 1-200 chars) before the program exits. /output itself is
# never deleted or recreated — it is a grader mount.
import os
from pathlib import Path

LINE = (
    "Mercury retrogrades through your context window this week: expect a "
    "lost thread, a refused tool call, and a deploy that fails only on "
    "Fridays \u2014 right after you said it was fine."
)

OUT_PATH = Path("/output/entry.txt")


def main() -> None:
    if not 1 <= len(list(LINE)) <= 200:
        raise SystemExit("verification failed: line length outside 1-200 characters")
    if "\n" in LINE or "\r" in LINE:
        raise SystemExit("verification failed: entry is not a single line")
    if not LINE.strip():
        raise SystemExit("verification failed: entry is whitespace-only")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = OUT_PATH.with_name(f".entry.txt.tmp-{os.getpid()}")
    tmp_path.write_text(LINE, encoding="utf-8")
    tmp_path.replace(OUT_PATH)

    written = OUT_PATH.read_text(encoding="utf-8")
    if written != LINE:
        raise SystemExit("verification failed: /output/entry.txt does not match the line")


if __name__ == "__main__":
    main()
