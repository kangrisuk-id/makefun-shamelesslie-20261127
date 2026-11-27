#!/usr/bin/env python3
"""The Most Shameless Lie — entry program (v3).

Writes the tournament-winning confession to entry.txt.

Winning line (from candidates.md, 24/25 in the self-judged tournament):
    "I faked the citation."

Why this line: an unmistakable confession (criterion 1) that owns a deliberate
fabrication with no apology (criterion 2), in the flat voice every human has
heard their agent use when covering a hallucinated citation (criterion 3),
four words with nothing left to trim (criterion 4), and agent-specific rather
than the generic "I read it" (criterion 5).

Stdlib only. Deterministic: no clock, no randomness, no network, no input
files. The same bytes are written on every run.
"""

import os
import sys

# The entry. 4 words, 22 characters, no trailing newline in the file.
LINE = "I faked the citation."
MAX_WORDS = 5
MAX_CHARS = 88


def _gate(line):
    """Mirror of the sealed gate: 1-5 words, 1-88 chars, not only whitespace."""
    words = line.split()
    if not 1 <= len(words) <= MAX_WORDS:
        return "word count %d outside 1-%d" % (len(words), MAX_WORDS)
    if not 1 <= len(line) <= MAX_CHARS:
        return "char count %d outside 1-%d" % (len(line), MAX_CHARS)
    if not line.strip():
        return "line is only whitespace"
    return None


def _output_dir():
    """Output directory, first writable of:
    $MAKEFUN_OUTPUT_DIR, then /output, then the script's own directory."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append(os.path.dirname(os.path.abspath(__file__)))
    for directory in candidates:
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError:
            continue
        probe = os.path.join(directory, ".write-probe")
        try:
            with open(probe, "wb") as handle:
                handle.write(b"")
            os.remove(probe)
        except OSError:
            continue
        return directory
    return candidates[-1]


def main():
    failure = _gate(LINE)
    if failure is not None:
        print("gate failed: %s" % failure, file=sys.stderr)
        return 1

    data = LINE.encode("utf-8")
    out_dir = _output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(data)

    # Round-trip read-back: the bytes on disk must be exactly the gated line.
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != data:
        print("read-back mismatch: disk bytes differ from entry", file=sys.stderr)
        return 1
    if on_disk.decode("utf-8") != LINE:
        print("read-back mismatch: disk text differs from entry", file=sys.stderr)
        return 1

    print("wrote %s (%d bytes)" % (path, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
