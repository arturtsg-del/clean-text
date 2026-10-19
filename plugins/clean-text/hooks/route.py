#!/usr/bin/env python3
"""UserPromptSubmit hook: when a prompt asks to write, clean up or check prose, tell Claude to use the
clean-text skill. Skill descriptions alone do not trigger reliably; this makes it deterministic."""
import json
import re
import sys

TRIGGERS = re.compile(
    r"почист|вычист|причеш|слоп|по-человечески|прогони\s+луп|до\s+чистого|"
    r"(?:поправь|отредактируй|перепиши|сократи|проверь|улучши)\s+(?:этот\s+|мой\s+|наш\s+)?"
    r"(?:текст|пост|письмо|сообщение|абзац|анонс|отчёт|отчет|мемо|черновик|слайд\w*|тз)|"
    r"звучит\s+как\s+(?:нейросеть|ии|бот|робот|chatgpt)|"
    r"\bslop\b|sound(?:s)?\s+(?:less\s+like\s+ai|human|like\s+a\s+human)|make\s+(?:it|this)\s+(?:sound\s+)?human|"
    r"clean\s+(?:this|it|the\s+\w+)\s+up|clean\s+up\s+(?:this|the)\s+(?:text|copy|draft|post|email|memo)|"
    r"(?:polish|tighten|rewrite|edit|proofread)\s+(?:this|the|my)\s+(?:text|copy|draft|post|email|memo|message|slides?)|"
    r"fix\s+the\s+copy",
    re.I,
)

HINT = (
    "Before you answer, call the Skill tool with skill \"clean-text:clean-text\" and follow it. This "
    "applies to quick checks too (\"is this slop?\", «это слоп?»): answering from your own judgment "
    "skips the facts check that keeps «позволяет», «ключевой», «давайте», \"key\", \"can\", \"let's\" "
    "and negations intact. Only if the request is about code rather than prose, ignore this note."
)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = data.get("prompt") or data.get("text") or ""
    if TRIGGERS.search(prompt):
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": HINT}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
