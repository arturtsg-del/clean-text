---
name: clean-text
description: >
  Writes, edits and audits any text a person will read (memos, Slack posts, emails, slide copy, briefs,
  READMEs, chat answers longer than a paragraph) so it stops reading like AI output, in Russian and
  English. Runs the no-ai-slop catalogue, Russian patterns, a jargon check, and a
  sentence-by-sentence audit loop that repeats until a full pass finds nothing. TRIGGER on any request
  to write, rewrite, shorten, clean up, "make it human", "убери слоп", "сделай по-человечески",
  "прогони лупом", "вычисти текст", or "is this AI slop?". Detect mode names the patterns without
  rewriting. Style edits keep the author's facts exactly as given.
---

# Clean text

This skill has five parts:

1. **The catalogue.** `references/no-ai-slop.md` (vendored verbatim from petergyang/no-ai-slop, MIT):
   banned words, empty phrases, binary contrasts, colon reveals, puffery, weasel attribution,
   fake-profound kickers, recap endings, formatting slop, em dashes. Its self-check is
   `references/no-ai-slop-eval.md`.
2. **Russian.** `references/russian.md`: the same failure classes as they look in Russian, plus
   канцелярит and the rules for тире. The upstream catalogue is English-only.
3. **Jargon.** §2 below: every code, abbreviation or in-house name is explained where it first
   appears.
4. **The loop (this file).** A text is done only when a full, numbered,
   sentence-by-sentence read of the final rendered output finds zero defects. The loop in §5 runs
   until that is true.
5. **The fresh reader.** `references/fresh-reader.md`: a second Claude instance that sees only the
   finished text and marks every place a reader would stop. It catches what the author cannot see in
   their own text.

Read the references the first time this skill triggers in a session. Read `references/decks.md`
when the output is a slide deck, a PDF or an HTML page.

---

## 0. Three jobs

**Edit (default).** The user gives a draft or asks you to write one. Write or edit, then run the loop
in §5 on your own output. Return the final text and a short "What changed" list.

**Detect.** The user asks "is this slop?", "check this", "проверь текст", or wants findings without a
rewrite. For each finding: the pattern name, the quoted line, the fix in a few words. No rewrite, no
score, no guess about whether AI wrote it. Offer to edit after.

**Loop.** The user says "прогони лупом", "до чистого", "until clean", or the text is long or
high-stakes (goes to a client, a board, all staff). Same as Edit, but you report every pass:
pass number, defects found, defects fixed.

---

## 1. Facts come first

You are editing style, so the facts stay as the author gave them. New figures, sources, examples or
claims come only from the author. When a passage is weak because information is missing, list the
question under "Open" and leave the passage as it is until the author answers.

- **Never delete a claim.** A sentence that says something about the subject (a result, a forecast,
  a conclusion, an opinion, a decision) may be rephrased but not removed, even when it is vague,
  puffed up or unsupported. Rephrase it plainly and add a question under "Open". You may delete a
  sentence only when it says nothing about the subject (throat-clearing, comments about the text) or
  repeats a claim that stays elsewhere in the text. This rule wins over anything in the catalogue
  that says to cut a claim, including weasel attribution, fake-profound kickers and recap endings.
- **Never add a clarification to the text.** If you think you know the basis of a comparison, the
  period, the scope or the meaning of a term, but the author did not say it, it goes under "Open" as
  a question. It does not go into the text, not even with a note in the report.

- **Every claim keeps its strength.** A plan stays a plan and a guess stays a guess. Do not upgrade
  "planned" to "done" for rhythm.
- **Words of degree and mode stay exactly as strong.** When you rephrase a claim, keep how much and
  how sure it is: "a key role" is not "mainly" or "thanks to"; "can work with any" is not "all are
  connected"; "some" is not "most"; "may" is not "will". In Russian the same holds for «ключевой»,
  «основной», «прежде всего», «все», «любые», «некоторые», «может», «умеет», «подключено». If no plain
  wording keeps the same strength, keep the author's words and add a question under "Open".
- **Every term exists somewhere real.** A product name, feature or team name must exist in the
  source material, the codebase or the company's own docs. If a search finds it nowhere, the term is
  invented. Use the real name.
- **Use official names.** If a product, team or process has an official name, use it in headings,
  tags and body. Do not coin catchy replacement labels for things that already have names.
- **One term, one meaning, the whole piece.** Do not call one thing "platform" on slide 2 and "the
  system" on slide 5.
- **Approved figures keep their approved wording and scope.** If a number came with a basis (net or
  gross, a fiscal year, a currency), the basis travels with it.

---

## 2. Jargon

A reader who has to ask "what does that mean?" has been let down by the sentence. Abbreviations,
project or ticket codes, names of in-house tools, made-up role titles and private nicknames each get
a plain explanation where they first appear, or get replaced by what they stand for. "Ждём апрув от
L2" becomes «Ждём подписи руководителя отдела закупок». "KPI-4 dropped from 91% to 84%" stays as
it is until the author says what KPI-4 measures; then it becomes, for example, "Repeat purchases within
a week dropped from 91% to 84%". If you do not know what a term means, ask; never guess it into the
text. An explanation in a glossary at the end does not count, and
neither does one three sections earlier: readers jump straight to the part they need.

---

## 3. Failure classes the catalogue does not name

These pass the `no-ai-slop` word lists and its eval. Each comes with a fix.

| Failure class | Example | Fix |
|---|---|---|
| **Metaphor where a business noun belongs** | "the beating heart of your sales"; "a bridge between teams"; «сердце системы» | Name the thing, if the text says what it is. If it does not, keep the phrase and ask the author what it refers to |
| **Inanimate subject, human verb** | "The dashboard tells a story"; "the numbers speak"; «отчёт рассказывает», «система понимает» | Give the verb to someone who can act, or use the literal verb: "the dashboard shows"; «в отчёте указано» |
| **The author's own repeated filler verb** | the same figurative verb in paragraph after paragraph; «закрывает» in every section | Count figurative verbs across the whole piece. Keep at most one, where it does real work |
| **Narrated honesty** | "Let's be upfront:"; "we say this openly"; «скажем прямо» | Delete the sentence about the prose. The fact convinces; the framing weakens it |
| **Defensive register on basics** | "We would never cut corners on quality." | State what is done, using only facts in the text. If the text has none, keep the sentence and ask what the practice actually is |
| **Rotation without meaning** | "This is a partnership, not a purchase"; «это не инструмент, а партнёр» | Say the one thing: "We work with you for the whole year" |
| **Universal a reader discounts** | "Handles any task"; "works with every tool"; «любые задачи» | Narrow it only with limits the text already gives ("any supplier in the registry"). Otherwise keep it and ask what it really covers |
| **Term the reader cannot parse** | "the flywheel" (never defined); "north-star metric"; «бэклог», «квик-вин» | Define at first use or replace (§2) |
| **Cryptic punchline** | "Speed is a habit." | If the line needs explaining, cut it and end on the last concrete sentence |
| **Colon joining unlike things** | "Our approach is simple: customers, people, growth." | A colon introduces a list, a label or a definition of the noun before it. Otherwise write two sentences |
| **Synonym pair for one thing** | "customers" on one page, "clients" on the next | One term. Use the one already on the page |
| **New slop introduced by the fix** | An edit that removed three metaphors added a fourth | Re-read your own edit as a stranger's draft. Pass D exists for this |

Ordinary terms of art are not metaphors and stay: go live, hand-off, sales pipeline, bottleneck.
The script flags some of them anyway. Judge each one in context. Do not swap a literal word for a
synonym just to silence a repeat count: "says / states / notes" for the same act is synonym cycling.

---

## 4. Register

- **Default:** no binary contrasts; no runs of
  punchy fragments; plain business language; no em dashes in short copy, at most two in a long
  document, none in a deck. Russian тире follows `references/russian.md`.
- **If the author has their own style guide or voice skill**, it wins where the two disagree.
  Everything else in this skill still applies.
- **Headings never end with a period**, in any language.
- **The chat answer that reports the work** follows the same rules: no metaphors, no recap paragraph,
  open items named as open.

---

## 5. The loop

Run the whole sequence on the whole piece every time. Never patch only the line someone pointed at:
if a reader found one defect in a text you called clean, the text was not audited.

**Pass A. Extract and read.** Save the text to a file if it is not in one, then run:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py <file>
```

`${CLAUDE_SKILL_DIR}` is the folder this SKILL.md is in; if the variable is not set, use that path.
The script prints every sentence with a number and its location (line, slide, HTML tag). Read each
numbered sentence and give it a verdict: clean, or the defect and the fix. Use the catalogue,
`references/russian.md`, §2 and the table in §3. Fix everything found. Add `--ignore-quoted` when the
text quotes the patterns it discusses.

**Pass B. Regex gate.** The same run prints the gate: binary contrasts, banned words, empty phrases,
metadiscourse, puffery, vague attribution, канцелярит, em dashes, in both languages. Every count
must be zero, except a survivor you justify in writing (for example a grammatical Russian тире, or
a contrast that is the factual point, such as "rent, not buy"). Exit code 0 means the gate passed. It does not mean the text passed: the gate cannot
see a metaphor, an overclaim or a term the reader does not know.

**Pass C. Figurative scan.** The watchlist section lists every figurative verb or noun with context
and a repeat count. For each hit: a literal business word, or a written reason it is a term of art.
Any figurative word used more than once gets cut to one.

**Pass D. Re-read your own edit.** Run Pass A again on the edited text. Your fixes add new defects.
Read the edit as a draft written by a stranger.

**Pass E. Read the rendered output.** For decks, PDFs and HTML: render it and read what the reader
will see (`references/decks.md`). Line breaks, orphan words and overflow are defects the source file
cannot show. For chat text and Markdown, the file is the rendered output.

**Pass F. Facts check.** Compare the author's draft with your version:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py <draft> --compare <edited>
```

It lists numbers, dates, quoted names and codes that the edit lost or added, and any change in the
count of negations, hedges («предварительно», "about"), conditions («если», "if") and currency marks.
Restore every lost item. Remove every added one. A changed count is allowed only when you can say
why in one line (for example, «а не выше» became a separate sentence); put that line under "Left as
is, on purpose". Keep the author's draft as a file from the start so this pass is possible.

The same run prints every changed sentence as a was / now pair. Read each pair and ask two
questions: does the new sentence make the same claim, and is it exactly as strong (degree, certainty,
scope, can versus does)? A pair that fails goes back to the author's wording, or to a version that
passes both questions.

**Pass G. Fresh reader.** When A–F find nothing, hand the final text to a reader who has seen
nothing else, following `references/fresh-reader.md`. In Claude Code this is a subagent. Fix what
the reader is right about, then run A–F again and use a new reader on the new version.

**Pass H. Repeat.** Run A–G until a full pass and a fresh reader both find nothing. Stop after five
passes or three fresh readers if it has not converged, and list what is left and why. Only then say
"done", with the number of passes, edits and fresh readers.

If you cannot honestly say "I read every numbered line of the final output, an independent reader
read it too, and neither found anything", you are not done. Say what is left instead. Where no
subagent is available, say that the independent read was not possible.

---

## 6. Deliver

1. The final text, in full.
2. **What changed:** the main edits as before → after, grouped by pattern. Keep it short.
3. **Left as is, on purpose:** any survivor of the gate and why.
4. **Open:** facts you need from the author, named as questions.
5. **Facts check:** the result of the last `--compare` run, the reason for each difference left, and
   the number of changed sentences you checked for same claim and strength.
6. **Fresh reader:** how many readers ran and what the last one returned, or that no subagent was
   available and the read was your own.
7. In Loop mode: one line per pass, e.g. `Pass 2: 7 found, 7 fixed`.

No recap paragraph at the end.

---

## 7. Exit checklist

Every answer must be yes. Any no means the text is not done.

- [ ] A full numbered pass over the final output found zero defects.
- [ ] A fresh reader who saw only the final text returned NOTHING FOUND, or the report says no subagent was available.
- [ ] The edit added no number, date, name, claim, source or example the author did not give.
- [ ] No claim of the author was deleted; the facts check shows nothing lost or added, or each difference is explained.
- [ ] Every was / now pair makes the same claim at the same strength.
- [ ] Every term exists in the source material or is explained at first use; one term, one meaning.
- [ ] No binary contrasts, unless the contrast itself is the fact being stated.
- [ ] No inanimate subject does a human action; every figurative word appears at most once and is justified.
- [ ] No sentence describes the prose itself ("to be clear", «скажем честно»).
- [ ] No basic fact is argued defensively or by negation.
- [ ] Every universal ("any", "all", «любой») is scoped to what is true.
- [ ] Headings end without a period.
- [ ] Russian text: no канцелярит from `references/russian.md`; every тире is grammatical.
- [ ] Decks and PDFs: read from the rendered file; no orphans, no overflow, no em dashes.
