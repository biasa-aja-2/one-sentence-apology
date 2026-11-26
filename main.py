"""The One-Sentence Apology Your Agent Owes You.

Writes one funny, human sentence of apology to /output/entry.txt.
Pure stdlib only (os, sys).
"""

import os
import sys

LINE = "I'm sorry I deleted your only copy of the file and then emptied the trash, so you'd never have to wonder where it went."
# The joke lands on a real failure with a sharp turn: deleting the only
# copy is bad enough, but emptying the trash afterwards — framed as a
# helpful favour, "so you'd never have to wonder where it went" — turns
# the apology into a confession of a second, worse mistake made with
# total confidence. Plain, embarrassed voice, no robot pun, no
# customer-service boilerplate: one clean sentence, 119 chars, well
# inside the 1-200 gate.

MAX_CHARS = 200


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check gate: 1-200 chars, single sentence, single line,
    # not whitespace-only.
    if not LINE or not LINE.strip():
        print("gate failed: line is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print("gate failed: line is %d chars, over %d" % (len(LINE), MAX_CHARS),
              file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: line is not a single line", file=sys.stderr)
        return 1
    if LINE.count(".") != 1 or not LINE.endswith("."):
        print("gate failed: line is not exactly one sentence", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(path, 0o644)

    # Read-back verification: byte-exact, valid UTF-8, no trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("verification failed: file bytes differ", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or "\n" in text:
        print("verification failed: length or line check", file=sys.stderr)
        return 1
    if text.strip() != LINE or text != text.strip():
        print("verification failed: unexpected surrounding whitespace", file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
