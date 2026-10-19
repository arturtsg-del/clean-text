# Slides, PDFs and web pages

People read the finished file, not its source, so the check runs on the finished file.

- **PDF.** `python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py report.pdf` extracts the text with
  `pdftotext` and rebuilds whole sentences. Also open the pages you changed and look at them: a word
  stranded alone on a line, text spilling into the footer, an empty half-page.
- **HTML.** Run the script on the `.html` file. If slides are marked with comments like
  `<!-- slide: Results -->`, each sentence is labelled with its slide.
- **After an edit.** Confirm the new wording appears in the exported file before you send it. When
  searching a PDF for a phrase, flatten line breaks first, because a phrase split across two lines
  will not match.
- **Slide text.** Titles are short descriptions or official names. No period at the end of a title.
  No em dashes except in number ranges.
