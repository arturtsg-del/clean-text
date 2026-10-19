# Fresh reader

The author of a text is the worst judge of it: they know what every phrase was meant to say, so they
do not notice when the words say less. A second Claude instance that has seen nothing but the
finished text does not have that problem. This file is the brief for that instance.

## When it runs

Standard: once, after the gate and the facts check are clean. Deep: once more on the fixed version,
because a reader who saw an earlier draft is no longer fresh. Quick: never, unless the user asks.

## What the reader gets

1. The final text, exactly as the reader will see it.
2. One line about the reader: who they are. Take it from the request ("for the board"); otherwise use
   "a sharp colleague from another department who has not seen this project".
3. The terms this reader already knows, from the team glossary or the personal profile (SKILL.md §2),
   so they are not flagged again. Leave the list out if there is none.

Nothing else: no draft history, notes, sources, or purpose of the edit. Those fill exactly the gaps
the reader is there to find.

## How to run it

In Claude Code, start one subagent with the Agent tool and the brief below; it needs no tools.
Where no subagent is available (claude.ai, Claude Desktop chat), say in the report that the
independent read did not happen, and do the read yourself in the role from the brief. Never present
your own read as an independent one.

## The brief

```
You are reading a text as this person: <READER>.
They already know these terms: <TERMS or "none listed">.

Read it once, the way that person would. Mark every place where they would stop, frown or lose the
thread: a word or code they would not know; a figure of speech where they want the plain fact;
something presented as acting by itself that cannot act; a claim bigger than anything the text
supports; a reference they cannot resolve ("this approach", "as agreed"); a sentence about the text
itself; a sentence they would have to read twice.

Do not rewrite anything. Do not judge whether facts are true. Do not comment on what is fine.

Answer as a numbered list, one line per finding:
"<exact quote>" | <what this reader would ask or think>
If nothing would stop this reader, answer exactly: NOTHING FOUND
```

Then the text, after a blank line.

## What to do with the answer

Sort each finding into one of two groups. Do not ask the reader to sort; you know what the author gave.

- **Fixable now:** the fix needs nothing new. Reorder, split a sentence, use a fact already in the
  text, name a thing the text names elsewhere, replace a figure of speech whose meaning the text
  makes clear. Apply these, then rerun the gate and the facts check on the changed text.
- **Needs the author:** the fix needs information the text does not have (what a term means, the basis
  of a number, the real scope of a claim). Add it under "Open" unless an existing question already
  covers it. Leave the passage as it is.

A reader's findings that all need the author mean the text is done for now: deliver it with the
questions. Do not start another reader to confirm that.
