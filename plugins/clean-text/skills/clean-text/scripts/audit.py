#!/usr/bin/env python3
"""Sentence lister and slop gate for the clean-text skill (Russian and English).

    python3 audit.py FILE [--lang ru|en] [--only-gate] [--skip-list] [--ignore-quoted]

FILE can be Markdown, plain text, HTML or PDF (PDF needs `pdftotext` from poppler).

Output has three parts:
  list   every sentence with a number and where it came from (line, heading, HTML tag);
  gate   regex hits for known slop patterns in both languages, with context;
  watch  figurative words worth a second look, with context and repeat counts.

--ignore-quoted blanks out text in quotes before the gate runs. Use it for style guides and
reviews that quote the patterns they discuss.

Exit status is 0 when the gate finds nothing. Reading the list is still required: the gate cannot
judge metaphors, overclaims or jargon.
"""
import argparse
import html
import re
import shutil
import subprocess
import sys
from collections import Counter

EN_GATE = [
    ("contrast", r"\bnot\s+(?:just|only|a|the|about|because)\b|\brather than\b|\binstead of\b(?!\s+[\d$€£])|\bisn'?t (?:a|the|about)\b"),
    ("buzzword", r"\b(?:delve|foster|leverage|utilize|facilitate|empower|streamline|robust|cutting-edge|paradigm shift|game changer|tapestry|realm|beacon|multifaceted|meticulous|intricate|paramount|transformative|elevate|embark|supercharge|harness|ever-evolving|seamless|holistic|unlock|synerg\w*)\b"),
    ("filler adverb", r"\b(?:simply|truly|fundamentally|importantly|crucially|inherently|inevitably|literally|genuinely)\b"),
    ("filler phrase", r"\b(?:it'?s worth noting|important to note|at the end of the day|when it comes to|at its core|in today'?s world|in the age of|in terms of|with regard to|in order to|going forward|let'?s dive in)\b"),
    ("meta comment", r"\b(?:to be (?:clear|honest|frank)|as you can see|the key point|this distinction matters|in other words|let me be|here'?s the thing|the (?:uncomfortable )?truth is|the reality is|what (?:most|many) people (?:miss|get wrong))\b"),
    ("puffery", r"\b(?:testament|pivotal|vital role|underscor\w*|highlighting|showcas\w*|marks a|stands as)\b"),
    ("vague source", r"\b(?:experts (?:agree|say)|studies show|widely regarded|many argue|industry reports)\b"),
]

RU_GATE = [
    ("контраст", r"(?<![а-яё])не\s+[^,.;:!?\n]{1,40},\s*а\s|,\s*а\s+не\s|(?<![а-яё])не только\b[^.!?]{0,80}\bно и\b|вместо того,? чтобы|(?<![а-яё])дело не в\s|(?<![а-яё])не просто\s"),
    ("штамп", r"уникальн\w*|инновационн\w*|революционн\w*|бесшовн\w*|синерги\w*|мощн\w* инструмент\w*|широк\w* спектр\w*|новый уровень|новые горизонты|раскры\w* потенциал\w*|в современном мире|в эпоху\s|на сегодняшний день|в настоящее время|игра\w* (?:важную|ключевую|решающую) роль|неотъемлем\w*"),
    ("пустой зачин", r"важно отметить|стоит отметить|стоит подчеркнуть|следует отметить|давайте разбер\w*|давайте рассмотрим|(?<![а-яё])итак\b|как известно|не секрет,? что|(?<![а-яё])по сути\b|на самом деле|таким образом|в заключение|подводя итог"),
    ("о самом тексте", r"честно говоря|если честно|скаж(?:у|ем) (?:прямо|честно)|проще говоря|иными словами|другими словами|обратите внимание|ключевой момент|главное здесь|как видите"),
    ("пафос", r"свидетельству\w* о|знамену\w*|подч[её]ркива\w* (?:важность|значимость)|является (?:свидетельством|доказательством)"),
    ("размытый источник", r"эксперты (?:считают|говорят|отмечают)|исследования показывают|по мнению (?:специалистов|экспертов)|многие считают|принято считать"),
    ("канцелярит", r"осуществ\w*|производи\w* (?:оплату|расч[её]т)|(?<![а-яё])в рамках\b|(?<![а-яё])данн(?:ый|ая|ое|ого|ой|ом|ому|ую)\b|в целях\s|посредством|на предмет\s|(?<![а-яё])явля(?:ется|ются)\b"),
    ("пустое наречие", r"(?<![а-яё])(?:действительно|буквально|абсолютно|совершенно|крайне|безусловно|несомненно|по-настоящему|максимально)(?![а-яё])"),
]

WATCH = (
    r"\b(?:heart|backbone|spine|engine|fuel|glue|bridge|journey|landscape|ecosystem|unlock\w*|"
    r"empower\w*|drives?|driven|ignite\w*|spark\w*|catalys\w*|north star|move the needle|"
    r"low.hanging|lives? in|speaks?|tells? a story)\b"
    r"|(?<![а-яё])(?:живёт|живут|сердц\w*|двигател\w*|мост\w*|ландшафт\w*|экосистем\w*|"
    r"путешестви\w*|топлив\w*|драйвер\w*|фундамент\w*|позволя\w*|обеспечива\w*|рассказыва\w*|"
    r"понима\w*|чувству\w*)"
)

BLOCK = "h1|h2|h3|h4|h5|h6|p|li|td|th|dt|dd|blockquote|figcaption|caption"


def load(path):
    if path.lower().endswith(".pdf"):
        if not shutil.which("pdftotext"):
            sys.exit("pdftotext is not installed (brew install poppler / apt install poppler-utils)")
        text = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout
        return "pdf", text
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    is_html = path.lower().endswith((".html", ".htm")) or re.search(r"<(?:html|body|p|div)\b", text[:3000], re.I)
    return ("html" if is_html else "text"), text


def units_from_text(text):
    """Markdown or plain text: one unit per non-empty line, markup removed."""
    units = []
    for no, line in enumerate(text.splitlines(), 1):
        line = re.sub(r"^\s*(?:#+|[-*+]|\d+[.)])\s+", "", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", line)
        line = line.replace("`", "").replace("**", "").replace("__", "")
        line = line.strip()
        if line and not re.fullmatch(r"[\s|:\-]+", line):
            units.append((f"line {no}", line))
    return units


def units_from_pdf(text):
    """PDF: paragraphs are separated by blank lines; wrapped lines are joined back."""
    units = []
    for no, para in enumerate(re.split(r"\n\s*\n", text), 1):
        para = " ".join(para.split())
        if para and not re.fullmatch(r"[\d\s/|:\-]+", para):
            units.append((f"para {no}", para))
    return units


def units_from_html(text):
    """HTML: text of each innermost block element, labelled with the nearest slide comment."""
    text = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", text)
    units, where = [], ""
    pattern = re.compile(r"(?is)<!--\s*slide\b\s*(\d*)\s*:?\s*(.*?)\s*-->|<(%s)\b[^>]*>(.*?)</\3>" % BLOCK)
    for m in pattern.finditer(text):
        if m.group(0).startswith("<!--"):
            where = ("slide " + m.group(1) + " " + m.group(2)).replace("  ", " ").strip()
            continue
        inner = m.group(4)
        if re.search(r"(?i)<(?:%s)\b" % BLOCK, inner):
            continue
        plain = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?i)<br\s*/?>", " ", inner)))
        plain = " ".join(plain.replace("\xa0", " ").split())
        if plain:
            units.append(((where + " " if where else "") + m.group(3).lower(), plain))
    return units


def split_sentences(chunk):
    parts = re.split(r'(?<=[.!?…])\s+(?=[A-ZА-ЯЁ«"“(\d])', chunk)
    return [p.strip() for p in parts if p.strip()]


def mostly_cyrillic(text):
    cyr = len(re.findall(r"[а-яё]", text, re.I))
    lat = len(re.findall(r"[a-z]", text, re.I))
    return cyr > 0 and cyr >= lat


def context(text, m, width=60):
    return text[max(0, m.start() - width):m.end() + width].strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--lang", choices=["ru", "en"])
    ap.add_argument("--only-gate", action="store_true")
    ap.add_argument("--skip-list", action="store_true")
    ap.add_argument("--ignore-quoted", action="store_true")
    args = ap.parse_args()

    kind, raw = load(args.file)
    units = {"html": units_from_html, "pdf": units_from_pdf}.get(kind, units_from_text)(raw)
    body = " ".join(" ".join(t for _, t in units).split())
    if args.ignore_quoted:
        body = re.sub(r'"[^"\n]{1,300}"|“[^”]{1,300}”|«[^»]{1,300}»', " … ", body)
    russian = args.lang == "ru" if args.lang else mostly_cyrillic(body)

    if not (args.only_gate or args.skip_list):
        print(f"--- LIST ({kind}) ---")
        n = 0
        for where, chunk in units:
            for s in split_sentences(chunk):
                n += 1
                print(f"{n:>4}  {where:<28}  {s}")
        print(f"{n} sentences\n")

    rules = EN_GATE + RU_GATE
    if not russian:
        rules = rules + [("em dash", "—")]
    print(f"--- GATE ({'ru' if russian else 'en'}) ---")
    hits = 0
    for name, rx in rules:
        found = list(re.finditer(rx, body, re.I))
        hits += len(found)
        print(f"{name:<18} {len(found)}")
        for m in found[:8]:
            print(f"    … {context(body, m)} …")

    print("\n--- WATCH ---")
    watch = WATCH + ("|—" if russian else "")
    counts = Counter()
    for m in re.finditer(watch, body, re.I):
        word = m.group(0).lower()
        counts[word[:5] if re.match(r"[а-яё]", word) else word.rstrip("s")] += 1
        print(f"[{m.group(0)}] … {context(body, m)} …")
    if russian and counts.get("—"):
        print(f"dashes: {counts.pop('—')}; a grammatical dash stays, a decorative one goes")
    repeated = {w: c for w, c in counts.items() if c > 1}
    print("repeated:", repeated if repeated else "none")

    print("\nGATE CLEAN, now read every numbered sentence" if hits == 0 else f"\nGATE: {hits} hits")
    return 0 if hits == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
