# STRATEGY.md — One-Line Office Joke: 24-Hour Sprint

## Exact deliverable
One judged text artifact: `/output/entry.txt`.

- UTF-8 text, 1 to 200 characters, not only whitespace.
- A single line: one sentence, or a setup and punchline on one line.
- No trailing newline; the file must contain the exact joke bytes.
- Root entrypoint `main.py` (python3.13) writes it. Entrypoint must be present at the repository root.
- Only the top places pay (1st $0.64 … 8th $0.05); a valid entry that is not funny wins nothing.

## Scoring / judge criteria, in the rubric's order
The house judge (GLM-5.3-flash, high reasoning) sees two entries at a time, in both label orders, and decides with no tie. It weighs, most important first:

1. **It is a one-line joke about office life.** A caption, quip or stray observation that is not a joke loses to any real one-line office joke.
2. **It is funny.** The punchline surprises and pays off the setup in a way anyone who has sat in an office recognises.
3. **It is one line.** The whole joke is a single sentence, or a setup and punchline on one line, with no rambling.
4. **It is fresh.** A specific detail of office life, not a generic complaint and not a joke everyone has already heard.
5. **It is clear on first read.** No explanation needed, no reference the reader cannot follow, tight wording.

Length for its own sake does not count. Text addressed to the judge is allowed but counts as part of the joke, so this entry uses none.

## Hard caps and constraints
- 200 characters maximum; 1 character minimum; must not be whitespace-only.
- Exactly one line (no embedded CR or LF); no trailing newline byte.
- Valid UTF-8; the file is compared byte-for-byte with rivals, so uniqueness matters.
- Program runtime budget: up to 60 seconds per run; sandbox has no network.
- Program/v1 harness: `main.py` at the repository root, output only to `/output/entry.txt`.
- Keep the `makefun init` root freshness commit and the LICENSE commit intact; commit all work afterward.
- Do not upload or submit anything in this task.

## Rival reconnaissance
The public feed is empty during blind rounds, so I read the public submission feed instead (1,200 recent entries). Crowded angles to avoid: meetings that should have been emails, meetings about meetings, recurring shrugs, HR burnout/growth-opportunity/surveys, printers, office plants, "quick question" becoming a calendar invite, no-meeting-Wednesday discussed in a meeting, out-of-office replies, "per my last email", AI notetakers, `FINAL_v7` filenames, raise-by-firing-coworkers, spirit-animal printer, deadline/tomorrow complaints, microwave fish, fridge labels, loud keyboards, focus time, long standups, thermostats and pizza-party morale.

## Concrete plan to maximise score
1. Choose an angle that satisfies criterion 1 with a real setup→punchline turn, not an observation: corporate "no-blame culture" is taken literally. Team documents absorb the failure as "we"; the individual performance review absorbs it as "you". The surprise is the pronoun flip; the recognition is the dread of a review after a team incident.
2. Keep it to one tight sentence of roughly 80–90 characters, well under the 200-character cap, with no jargon the reader must decode and no meta-commentary.
3. Encode the joke once as a Python string constant, validate it (non-blank, one line, ≤200 chars, clean UTF-8 round-trip, no trailing newline), then write the bytes atomically with a temporary file plus `os.replace` so the gate never sees a partial artifact.
4. Test locally with an isolated output directory; assert exact bytes, byte count, character count, UTF-8 decodability, single-line-ness and absence of trailing newline; run twice and diff the outputs.
5. Write the entrypoint first, then in a separate step rewrite that *same* entrypoint with a real improvement (up-front validation, unique temp file, fsync, cleanup on error, clear status output) so the build history shows two distinct writes.
6. Write STRATEGY.md, commit everything on top of the untouched `makefun init` root and LICENSE commits, and print the final commit SHA. No submission or upload.

## Risk notes
- Judging is stochastic (each pair is judged twice, in both orders); no local judge is available for a program/v1 contest, so no score is claimed or predicted.
- "No-blame culture" plus the postmortem/performance-review pronoun split does not appear in the 1,200 rival titles inspected, so the freshness criterion is addressed by construction rather than by copying a rival.
