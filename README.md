# clean-text

Скилл для Claude, который пишет и проверяет тексты так, чтобы они не читались как ответ нейросети.
Работает с русским и английским.

Основа скилла — каталог [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) (лицензия MIT,
файлы скопированы без изменений). Сверху добавлено пять вещей:

1. **Русский язык.** Исходный каталог только английский. Здесь те же ошибки по-русски, плюс
   канцелярит («осуществлять контроль», «в рамках», «данный») и правила тире.
2. **Проверка жаргона.** Каждое сокращение, код и внутреннее название объясняется там, где появляется
   впервые.
3. **Цикл проверки.** Скрипт нумерует каждое предложение текста, Claude читает и исправляет каждое,
   потом проверяет уже исправленный текст. Цикл повторяется, пока полный проход не найдёт ноль ошибок
   (максимум пять проходов, потом Claude перечисляет, что осталось).
4. **Свежий читатель.** Когда Claude считает текст чистым, его читает отдельный экземпляр Claude,
   который не видел ничего, кроме готового текста и описания читателя. Он отмечает каждое место, где
   читатель споткнётся: незнакомое слово, метафору вместо факта, утверждение без опоры. Работает в
   Claude Code; в claude.ai Claude честно напишет, что независимого прочтения не было.
5. **Факты автора не трогаются.** Новые цифры, источники и примеры берутся только от автора. Если
   абзацу не хватает информации, Claude оставит его как есть и задаст вопрос.

## Установка в Claude Code

В сессии Claude Code:

```
/plugin marketplace add arturtsg-del/clean-text
/plugin install clean-text@clean-text
```

Обновить до новой версии:

```
/plugin marketplace update clean-text
```

Без системы плагинов можно скопировать скилл вручную:

```bash
git clone https://github.com/arturtsg-del/clean-text.git && clean-text/tools/install-local.sh
```

## Установка в claude.ai и Claude Desktop (вкладка чата)

1. Скачайте `clean-text.zip` со страницы Releases этого репозитория или соберите сами:
   `tools/build-zip.sh`.
2. Settings → Capabilities → Skills → Upload skill, выберите zip.
3. Должен быть включён Code execution and file creation: без него скрипт проверки не запустится, и Claude проверит текст
   только чтением.

## Как пользоваться

Скилл включается сам, когда вы просите написать или поправить текст. Явные формулировки:

| Что сказать | Что произойдёт |
|---|---|
| «Напиши пост для команды про …» | Claude пишет, затем прогоняет цикл проверки по своему тексту |
| «Убери слоп», «сделай по-человечески» + текст | Правка с минимальными изменениями и список того, что поменялось |
| «Прогони лупом до чистого» | То же, но с отчётом по каждому проходу: сколько нашёл, сколько исправил |
| «Это слоп?», «проверь текст, не переписывай» | Список типовых ошибок с цитатой и коротким вариантом исправления, без переписывания |

В Claude Code скилл можно вызвать явно: `/clean-text:clean-text`.

Скрипт проверки можно запустить и без Claude, на любом `.md`, `.txt`, `.html` или `.pdf`:

```bash
python3 plugins/clean-text/skills/clean-text/scripts/audit.py draft.md
```

Код выхода 0 значит только, что регулярные выражения ничего не нашли. Метафоры, преувеличения и
непонятные термины видно лишь при чтении, поэтому чтение каждого предложения в цикле обязательно.

## Если у автора есть свой стиль

Если у вас есть собственное руководство по стилю или скилл голоса, в спорных местах побеждает оно. Всё
остальное из clean-text продолжает действовать.

## Состав

```
.claude-plugin/marketplace.json          каталог плагинов для Claude Code
plugins/clean-text/
  .claude-plugin/plugin.json
  skills/clean-text/
    SKILL.md                             порядок работы, цикл, критерий готовности
    scripts/audit.py                     нумерация предложений и проверка регулярными выражениями
    references/no-ai-slop.md             каталог из petergyang/no-ai-slop (без изменений)
    references/no-ai-slop-eval.md        его чек-лист
    references/russian.md                типовые ошибки по-русски, канцелярит, тире
    references/decks.md                  слайды, PDF и HTML: проверка по готовому файлу
    references/fresh-reader.md           задание для свежего читателя
tests/                                   примеры текстов для проверки скрипта
tools/test.sh                            проверка скрипта на примерах
tools/build-zip.sh                       сборка zip для claude.ai
tools/pull-upstream.sh                   обновление каталога из исходного репозитория
```

## Как предложить правку

Нашли ошибку, которую скилл пропускает: добавьте её в `references/russian.md` или в таблицу §3
`SKILL.md`, допишите регулярное выражение в `scripts/audit.py`, положите пример в `tests/slop_*.md` и
запустите `tools/test.sh`. Файлы `no-ai-slop*.md` руками не меняйте, их обновляет
`tools/pull-upstream.sh`.

---

**English.** A Claude skill that writes and audits text so it stops reading like AI output, in Russian
and English. It bundles the [no-ai-slop](https://github.com/petergyang/no-ai-slop) catalogue (MIT,
verbatim), adds Russian patterns, a jargon check and a numbered sentence-by-sentence audit
loop that repeats until a full pass finds nothing. Install in Claude Code with
`/plugin marketplace add arturtsg-del/clean-text` and `/plugin install clean-text@clean-text`, or
upload `clean-text.zip` in claude.ai under Settings → Capabilities → Skills.
