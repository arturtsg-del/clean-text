# Context: team glossary and personal voice profile

Two optional files make the skill fit a team and a person. Both are plain Markdown, short, and
written to be read in a few seconds. Neither is part of this repository.

## Team glossary

Where: `.claude/clean-text.md` in a project the team shares (committed with the project), or
`~/.claude/clean-text/team.md` for one person's machine.

The team writes and owns it. Claude reads it and never edits it on its own: when a run shows that a
term or a retired phrase is missing, suggest the line under "Open" and let the team add it.

```markdown
# Team glossary

## Readers
- board: knows the business model and the yearly targets; does not know internal tool names
- engineering: knows the stack and ticket codes

## Terms
| Term | Means | Known to |
|---|---|---|
| ARR | annual recurring revenue | board, engineering |
| L2 | second-line support team | engineering |

## Official names
- Product names exactly as written here; never shorten or rename them.

## Retired phrases
- "seamless experience" (dropped from all customer copy)
```

## Personal voice profile

Where: in Claude Code, `~/.claude/clean-text/profile.md`, or a path the user names. In claude.ai,
where Claude cannot keep files between chats, the profile is a file named `profile.md` in the
Project's knowledge; outside a Project the user can paste it at the start of a chat.

```markdown
# Voice profile
Updated: <date>

## Keep (my voice)
- Numbered lists for steps (seen 3x)
- Writes «мы», not «я», in team updates (corrected 1x)

## Never use
- «в рамках», "utilize" (corrected 1x)

## My terms
| Term | Means | Readers who know it |
|---|---|---|
| ops review | the Monday operations meeting (explained 1x) | team |

## Corrections
- <date>: I replaced «созвон» with «встреча»; the user restored «созвон». Rule: keep «созвон». (corrected 1x)

## Candidates (seen once)
- Starts emails without a greeting (seen 1x)
```

## How the profile learns

Run this after every delivery. It should cost a few seconds: at most three new lines per run.
Raising a counter or moving a line from "Candidates" to "Keep" is free and does not count.

1. **Look for evidence in this run only.**
   - An explicit correction of your edit ("верни как было", "я так не пишу", the user restoring a
     phrase) becomes a rule at once, under "Keep" or "Never use", and a dated line under "Corrections".
   - A term the user explained while answering "Open" goes under "My terms" with its plain meaning.
   - A turn of phrase or habit in the user's own draft goes under "Candidates". It moves to "Keep"
     when it shows up in a second, separate text. A new observation that contradicts an existing
     candidate replaces it; never keep both. Text written by someone else teaches nothing about the
     user. Patterns from the catalogue (empty phrases, puffery) never become voice from a draft
     alone; only an explicit correction makes them a rule.
2. **Store style, never content.** No figures, dates (other than the update stamp), quotes from the
   text, client or project details, or facts about people. A term and its plain meaning are fine.
3. **Keep it short.** The whole file stays under 60 lines. When it grows past that, merge similar
   lines and drop the oldest candidates.
4. **Respect the user's own lines.** Every line Claude writes ends with a counter in brackets,
   "(seen 2x)" or "(corrected 1x)". A line without a counter was written or edited by the user: never
   rewrite, move or remove it.
5. **First run.** If the file does not exist and this run has something to record, create it with
   the header and those observations, and tell the user once where it is and that they can edit or
   delete it. Never create an empty profile.
6. **No file access** (claude.ai chat): give the new lines at the end in a code block, headed with the
   section they belong to, and say they go into `profile.md` in the Project's knowledge. Do not
   mention `~/.claude` paths there.

## How the files are used

- The profile and glossary are read before editing (SKILL.md §2), and they decide voice questions:
  a trait under "Keep" survives even if the catalogue would cut it.
- Terms listed as known to a reader are not flagged as jargon for that reader, and the fresh reader
  is told about them.
- Neither file can override the facts rules: a profile line never permits adding or removing a fact.
