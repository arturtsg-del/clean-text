---
name: clean-text
description: >
  Writes, edits and checks text a person will read (memos, Slack posts, emails, slide copy, briefs,
  READMEs, reports) so it stops reading like AI output, in Russian and English, without touching the
  author's facts. TRIGGER when the user asks to write, rewrite, shorten, clean up or check a text:
  "make it human", "убери слоп", "сделай по-человечески", "вычисти текст", "прогони лупом", "is this
  AI slop?", «это слоп?», "проверь текст". Not for routine chat answers. Picks a light or deep check by the stakes
  of the text, uses the team glossary and the user's personal voice profile when they exist, and
  quietly learns the user's voice over time.
---

# Clean text

## Always, at every level, even for one short message

1. Save the author's text as a file before you change anything.
2. After editing, run `python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py <draft> --compare <edited>`.
3. Fix every flag it prints by editing the text. An explanation never clears a flag.
4. Never drop or weaken words of importance, possibility, promise or call: «ключевой», «позволяет»,
   «может», «будет», «давайте»; "key", "allows", "can", "will", "let's". Never add a fact.

Skipping step 2 is the most common way this skill fails. It takes one command.

Five parts work together:

1. **Catalogue.** `references/no-ai-slop.md` (petergyang/no-ai-slop, MIT, verbatim): words, phrases
   and patterns that make text read as machine-written. Read it once per session. Where its workflow
   differs from this file, this file wins.
2. **Russian.** `references/russian.md`: the same patterns in Russian, канцелярит, тире. Read it when
   the text is in Russian.
3. **Context.** `references/context.md`: the team glossary and the user's personal voice profile.
4. **Facts rules and the loop** (this file).
5. **Fresh reader.** `references/fresh-reader.md`: a second Claude that sees only the finished text.

`${CLAUDE_SKILL_DIR}` below is the folder this file is in; if the variable is not set, use that path.

---

## 1. Pick the effort first

Spend effort in proportion to the stakes. Choose once, at the start, and say which level you chose in
one line.

| Level | When | What runs |
|---|---|---|
| **Quick** | Chat or Slack message, under ~150 words, internal | Context, one edit, gate on the result, facts check. No fresh reader |
| **Standard** | Default for documents: memos, emails, briefs, README, posts | Everything in §5 once, one fresh reader, one round of fixes |
| **Deep** | The user asks for a loop ("прогони лупом", "до чистого"), or the text goes to a board, a client, investors or the public | Standard, then a second fresh reader on the fixed version |

**Detect mode** ("это слоп?", "проверь, не переписывай"): run the script on the text and read it;
report each finding as pattern, quote, short fix. No rewrite. Suggested fixes obey §3 too: never
suggest swapping «ключевой» for «главный» or "can" for a plain statement.

---

## 2. Load context (cheap, once per session)

Read these if they exist; skip silently if they do not. Never search for them beyond these paths.

1. **Team glossary:** `.claude/clean-text.md` in the current project, else `~/.claude/clean-text/team.md`,
   or a path the user names.
   Official names, terms and what they mean, phrases the team has retired, who the usual readers are.
2. **Personal profile:** `~/.claude/clean-text/profile.md` (or a path the user names). How this
   person writes: words they use and keep, words they never use, their terms, their corrections to
   earlier edits.

Precedence, highest first: the facts rules in §3, the personal profile, the team glossary, the
catalogue. A trait in the profile ("numbered lists for steps", "writes «мы», not «я»") is the
author's voice: keep it even where the catalogue would cut it. A term in the glossary or profile counts
as explained for readers the file says know it.

Format and update rules for both files are in `references/context.md`.

---

## 3. Facts stay as the author gave them

You edit style. Facts, claims and their strength belong to the author.

- **Never add.** No new number, date, name, source, example, scope, comparison basis or meaning of a
  term. If you think you know it, it goes under "Open" as a question, never into the text. When you
  replace a vague or banned word, use the plainest word with the same meaning («обеспечить взаимодействие
  команд» → «команды работают вместе»). A more specific action or result would be an addition.
- **Never delete a claim.** A sentence that says something about the subject (a result, forecast,
  conclusion, opinion, decision) may be rephrased, not removed, even when vague or unsupported:
  rephrase it plainly and ask under "Open". Delete only sentences that say nothing about the subject
  (throat-clearing, comments about the text) or repeat a claim that stays elsewhere. A puffed-up
  claim ("a game changer", «прорыв») is a claim too: turn it into the plain claim it makes ("makes a
  big difference to onboarding") and ask for the evidence. This beats anything in the catalogue that
  says to cut a claim.
- **Keep caveats next to what they limit.** Reordering is fine, but a conclusion does not move away
  from the risks, conditions or «предварительно» that qualify it.
- **Keep the strength.** Degree and certainty stay exactly as strong: "a key role" is not "mainly";
  "can work with any" is not "all are connected"; "some" is not "most"; "may" is not "will"; a plan
  stays a plan. Same for «ключевой», «основной», «прежде всего», «все», «любые», «может», «умеет». If
  no plain wording keeps the strength, keep the author's words and ask.
- **Importance and possibility are claims, not decoration.** «Ключевой», «важный», «главный»,
  "key", "critical" say how much something matters: they stay. «Позволяет», «может», «можно»,
  "allows", "can" say that something is possible, not that it happens: «позволяет сократить сроки» may
  become «с ним можно сократить сроки», never «сроки сократятся». «Давайте», "let's" is a joint call
  and stays a call. Only empty praise that names no degree can go: «инновационный», «уникальный»,
  «мощный», «революционный», "seamless", "cutting-edge", "world-class".
- **Do not touch:** direct quotes, citations, legal and contract wording, code, product and company
  names, URLs, numbers and their units. Approved figures keep their wording and basis (net/gross,
  period, currency).
- **One term, one meaning.** Use official names (glossary first). Do not coin new labels for things
  that have names.

---

## 4. Jargon

A reader who has to ask "what does that mean?" has been let down by the sentence. Abbreviations,
codes, names of in-house tools, made-up role titles and private nicknames get a plain explanation
where they first appear, unless the glossary or profile says this reader knows them. You may
expand a standard abbreviation (P&L, NPS) or name a well-known public product only when you are
certain. In-house names, codes and nicknames are never guessed: keep them and ask. "KPI-4 dropped from 91% to 84%"
stays until the author says what KPI-4 measures.

---

## 5. The loop

**A. Write or edit.** Keep the author's draft (or the user's notes, if you write from scratch) as a
file: the facts check needs it. Fix what the catalogue, `russian.md`, §4 and the table below cover.

**B. Gate.** `python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py <edited>` prints every sentence numbered,
then pattern hits in both languages, then figurative words to look at. Hits are candidates: fix the
ones that are slop, leave the ones that are not, without writing justifications. Exit 0 only means no
pattern matched; metaphors, overclaims and jargon need your reading of the numbered list.

**C. Facts check.** `python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py <draft> --compare <edited>` lists
numbers (digits, number words, тыс/млн/%), dates, relative times, quotes, codes and links the edit
lost or added, a warning if the text got over a third shorter, and every changed sentence as a
was / now pair. Inside each pair it flags negations and six groups of degree and mode words:
importance («ключевой», "key"), main cause («главный», "mainly"), possibility («позволяет», «можно»,
"can"), future or promise («будет», "will"), call to act («давайте», "let's"), scope («все», «только»,
"any"), hedges («вероятно», "may"). Swapping words inside a group passes ("allows" → "can").

Resolve every flag by editing, not by explaining: a removed word or negation comes back; an added
one goes, unless it only restates the same sentence of the draft («будут выше» for «ожидали, что
выше»), which you note in one line under "Checks". Rerun until no flag is left. A sentence marked
`[moved]` changed place: check it still sits next to the caveats that limit it. Reading the pairs
is also your re-read of your own edit.

**D. Rendered output** (decks, PDFs, HTML only): read what the reader will see, per
`references/decks.md`.

**E. Fresh reader** (Standard and Deep): per `references/fresh-reader.md`. Apply the findings marked
fixable, put the rest under "Open". Deep only: one more reader on the fixed version.

**Stop** when B and C are clean and the last reader returns nothing fixable. Questions only the author
can answer do not keep the loop going: they go under "Open" and the text is delivered with them. Hard
limit: two rounds of fixes in Standard, three in Deep.

### Failure classes the catalogue does not name

| Class | Example | Fix |
|---|---|---|
| Metaphor for a business noun | "the beating heart of sales"; «сердце системы» | Name the thing if the text says what it is; otherwise keep it and ask |
| Inanimate subject, human verb | "the dashboard tells a story"; «данные говорят» | Literal verb or the real actor: "the dashboard shows"; «по данным» |
| Repeated figurative verb | the same verb in every paragraph | Keep at most one |
| Narrated honesty | "Let's be upfront:"; «скажем прямо» | Delete the sentence about the prose |
| Defensive register | "We would never cut corners on quality." | State what is done using facts in the text; if none, keep it and ask |
| Rotation without meaning | «это не инструмент, а партнёр» | Say the one thing. Keep the contrast when its second half guards against a likely misreading: «пауза, а не отмена», "rent, not buy" |
| Universal a reader discounts | "handles any task"; «любые задачи» | Narrow only with limits the text gives; otherwise keep and ask |
| Cryptic punchline | "Speed is a habit." | Cut only if it carries no claim; end on the last concrete sentence |
| Colon joining unlike things | "Our approach is simple: customers, people, growth." | A colon introduces a list, label or definition; otherwise two sentences |
| Synonym pair for one thing | "customers" here, "clients" there | One term |
| Slop added by the fix | removing three metaphors added a fourth | Caught by the pair reading in C |

Terms of art stay: go live, hand-off, sales pipeline, bottleneck. Headings never end with a period.
No em dashes in short copy, at most two in a long document, none in a deck; Russian тире per
`russian.md`.

---

## 6. Learn the user's voice (every run, a few seconds)

After delivering, update the personal profile per `references/context.md`, in at most three short
lines. Learn from: the user's own drafts (recurring words and turns they clearly like), their
corrections to your edits ("верни как было", "я так не говорю"), and terms they explained when
answering "Open". If the draft was written by someone else (a colleague's email, a text the user
forwarded), learn nothing from the draft; only the user's own corrections count. Store only how they write, never what the text says: no figures, quotes, client
data or personal details. In Claude Code, write the file; where you cannot write files, offer the
lines at the end for the user to save. Mention the update in one line ("Профиль: +2 наблюдения").

---

## 7. Deliver

1. The final text, in full.
2. **What changed:** main edits, before → after, grouped by pattern. Short.
3. **Open:** questions only the author can answer, numbered.
4. **Checks:** one line each for the facts check (and why any difference stays), the fresh reader
   (how many, what was fixed), and the level used. In Quick, one line in total.
5. The profile line from §6.

No recap paragraph at the end.

---

## 8. Exit checklist

- [ ] Effort level chosen and stated; limits respected.
- [ ] Glossary and profile read if present; the author's voice traits kept.
- [ ] Nothing added, no claim deleted, every was / now pair has the same claim and strength.
- [ ] Quotes, legal wording, code, names, URLs, numbers and units untouched.
- [ ] Gate candidates judged; numbered sentences read for metaphors, overclaims, jargon.
- [ ] Fresh reader run (Standard, Deep) or its absence stated; fixable findings applied.
- [ ] Open questions listed; profile updated with style only.
