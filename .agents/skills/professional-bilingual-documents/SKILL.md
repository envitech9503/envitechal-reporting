---
name: professional-bilingual-documents
description: Use for any Envi Tech AL report/document/PDF work involving client-facing English, Urdu or Arabic-script text, mixed Urdu-English content, FPDF rendering, typography, RTL/BiDi, wrapping, tables, document templates, export, or document QA. Do not use for unrelated application code.
---

# Professional bilingual documents

Produce publication-grade English, Urdu, and mixed-language reports without breaking the existing Envi Tech AL report system.

## First inspect the real path

Before changing document behavior:

1. Identify the exact report/view and PDF class/function involved.
2. Trace where text originates: model/form/database, view, helper, template, or hard-coded label.
3. Identify the rendering method used (`text`, `cell`, `multi_cell`, HTML renderer, etc.).
4. Keep PDF merge/compression code separate from typography fixes.
5. Preserve branded geometry unless redesign is explicitly requested.

The repository currently has a large FPDF-based report surface. Prefer reusable helpers and incremental migration rather than copying fixes into every report class.

## Required reading

For client-facing English, read `references/english-style-guide.md`.

For Urdu or mixed-language work, read both:
- `references/urdu-style-guide.md`
- `references/fpdf-rtl-guide.md`

## English workflow

For any new or materially changed English content:

1. Draft for technical accuracy first.
2. Perform a separate editorial pass.
3. Fix grammar, punctuation, articles, agreement, tense, capitalization, spacing, and awkward phrasing.
4. Keep technical terms, test names, standards, units, report numbers, regulatory names, and client facts unchanged unless the task explicitly corrects them.
5. Keep labels and terminology consistent across the same document.
6. Prefer concise professional business English; remove filler and repeated meaning.
7. Verify final line wrapping and alignment in the rendered PDF.

Do not treat an English copy edit as permission to alter scientific or regulatory meaning.

## Urdu / RTL workflow

### Source text

- Store and edit Urdu in Unicode logical order.
- Never manually reverse Urdu strings.
- Normalize text before rendering.
- Keep punctuation intentional.
- Preserve Latin technical fragments, units, URLs, emails, standards, dates, codes, and report numbers.

### Rendering

Use `EnviTechAlApp/document_i18n.py` as the single compatibility boundary for Arabic-script shaping/BiDi in the legacy FPDF path.

Do not add direct `arabic_reshaper` or `bidi.algorithm.get_display` calls elsewhere.

For new renderer work, prefer native shaping/BiDi support when the production renderer and dependencies support it. Until that migration is verified, use the centralized compatibility helper for legacy FPDF output.

### Alignment

- Normal Urdu body/label text: right aligned.
- English: left aligned unless document design says otherwise.
- Numbers and identifiers must not be reversed.
- Mixed-language paragraphs use the paragraph's dominant/base direction, but Latin fragments remain readable.
- Tables need an explicit column-direction decision; never blindly reverse all columns.

## FPDF rules

1. Do not pass Arabic-script model/form text directly to low-level FPDF drawing methods in new code.
2. Call the central helper to prepare the display text.
3. Use box-aware right alignment for Urdu rather than guessing an x-coordinate.
4. Prefer `multi_cell`/wrapping helpers for variable-length content instead of absolute single-line `text()` where space is not guaranteed.
5. Measure the prepared display string using the same font that will render it.
6. Never truncate technical identifiers silently.
7. Test long client names/addresses as well as short examples.

## Font policy

Do not add a font binary merely because it looks good on one workstation. Font changes require:

- Unicode coverage for required Urdu characters;
- correct shaping with the chosen renderer;
- verified PDF embedding;
- licensing approval for repository/server distribution;
- screen and print review;
- fallback behavior.

A high-quality Naskh-style font is normally preferable for dense technical tables/body copy. Nastaliq can be used for formal Urdu presentation only after renderer shaping and vertical metrics are verified. Do not force a Nastaliq font into dense laboratory tables without testing.

## QA gates

For document-generation code changes, run:

```bash
python .agents/skills/professional-bilingual-documents/scripts/qa_document_source.py
python -m unittest EnviTechAlApp.test_document_i18n
```

Then, when the local environment can generate PDFs:

- render one representative English report;
- render one Urdu report or Urdu test specimen;
- render one mixed Urdu-English specimen containing a date, percentage, unit, email/URL, standard number, and report number;
- inspect clipping, glyph shaping, order, punctuation, wrapping, table alignment, header/footer collisions, page breaks, QR readability, and font substitution.

A file opening successfully is not sufficient QA.

## Completion criteria

Do not report the task as complete unless:

- changed code passes relevant automated checks;
- English copy was editorially reviewed where changed;
- Urdu/mixed content uses the central BiDi/shaping path;
- no manual reversal hack was introduced;
- no existing branded/document-integrity behavior was weakened;
- representative rendered output was inspected when rendering is available.

If a renderer limitation prevents professional Urdu, state the limitation and propose an engine-level migration rather than hiding it with string hacks.