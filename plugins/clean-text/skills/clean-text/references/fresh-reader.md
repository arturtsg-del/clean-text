# Fresh reader

The author of a text is the worst judge of it: they know what every phrase was meant to say, so they
do not notice when the words say less. A second Claude instance that has seen nothing but the
finished text does not have that problem. This file is the brief for that instance.

## When it runs

After Passes A–E find nothing. The fresh reader checks a text you already believe is clean. Its
findings go back into the loop, and once you have fixed them, a new fresh reader checks the new
version: a reader who saw an earlier draft is no longer fresh.

## What the reader gets

Only two things:

1. The final text, exactly as the reader will see it.
2. A one-line description of the reader: who they are and what they already know. Take it from the
   request ("for the board", "for the support team"). If the request does not say, use: "a sharp
   colleague from another department who has not seen this project".

Do not pass the draft history, your notes, the source documents or the purpose of the edit. The
reader's job is to react to the words on the page, and anything else you give them fills the gaps
you are trying to find.

## How to run it

In Claude Code, start a subagent with the Agent tool and the brief below. Use `general-purpose` or
any agent type that can read text; it needs no tools if the text is pasted into the brief.

Where no subagent is available (claude.ai, Claude Desktop chat), say in the report that the
independent read was not possible, then do the read yourself in the role described in the brief.
Do not present your own read as an independent one.

## The brief

```
You are reading a text as this person: <READER>.

Read it once, the way that person would. Mark every place where they would stop, frown or lose the
thread. For example:
- a word, abbreviation, code or name they would not know;
- a metaphor or figure of speech where they would want the plain fact;
- something presented as acting by itself that cannot act ("the data shows", "the system decided");
- a claim that sounds bigger than anything the text supports ("any", "always", "the best");
- a reference they cannot resolve ("this approach", "the issue above", "as agreed");
- a sentence that talks about the text itself instead of the subject;
- a sentence they would have to read twice.

Do not rewrite anything. Do not judge whether the facts are true. Do not comment on what is fine.

Answer as a numbered list, one line per finding:
"<exact quote>" — <what this reader would ask or think> — <type>
If nothing would stop this reader, answer exactly: NOTHING FOUND

The text:
<TEXT>
```

## What to do with the answer

Treat each finding as a reader's reaction, not an order.

- **Fix it** when the reader is right: replace the term, give the fact, scope the claim, name the
  thing being referred to.
- **Keep it** only with a reason you can state in one line, for example "this reader works with
  this abbreviation daily". Put the reason under "Left as is, on purpose" in the report.

After fixing, run Passes A–E on the new version, then start a new fresh reader. Stop after three
fresh readers if they keep finding things, and list what is left.
