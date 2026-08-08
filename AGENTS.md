# Repository guidance for Codex

## Document-generation rule

When a task creates, edits, previews, exports, validates, or refactors a report, PDF, document template, document renderer, font rule, English client-facing text, Urdu text, or mixed Urdu-English content, use the repository skill:

`$professional-bilingual-documents`

The skill is stored at `.agents/skills/professional-bilingual-documents/SKILL.md`.

## Non-negotiable document standards

- Treat document formatting as renderer behavior, not prompt decoration.
- Keep semantic content separate from layout and rendering logic.
- Do not solve Urdu/RTL problems by reversing strings manually.
- Centralize Arabic-script shaping and BiDi handling in `EnviTechAlApp/document_i18n.py`; do not add new ad-hoc `arabic_reshaper` or `bidi` calls in report modules.
- Preserve Unicode logical-order source text in models/forms/database values. Convert to display order only at the legacy FPDF rendering boundary when required.
- For mixed Urdu-English text, preserve Latin identifiers, numbers, dates, units, URLs, email addresses, model numbers, report numbers, and standard references in readable order.
- Do not introduce new font binaries or production dependencies without an explicit dependency/licensing review. `requirements.txt` represents the production environment and must not be casually edited.
- Preserve existing branded report geometry unless the task explicitly requests redesign.
- Never weaken report verification, signatures, QR verification, password protection, or document integrity while changing formatting.

## English quality

Any new or materially edited client-facing English must receive an editorial pass for grammar, punctuation, terminology consistency, capitalization, dates, units, labels, and professional business tone. Do not change technical or regulatory meaning merely to improve prose.

## Urdu quality

Any Urdu or Arabic-script output must be treated as RTL content. Use Unicode text, normalize it, shape/reorder only at the renderer boundary if the renderer needs that fallback, and right-align ordinary Urdu body text unless the design requires another alignment.

## Required checks for document changes

Run these checks when touching document-generation code:

```bash
python .agents/skills/professional-bilingual-documents/scripts/qa_document_source.py
python -m unittest EnviTechAlApp.test_document_i18n
```

If a representative PDF can be generated in the local environment, render and visually inspect at least one English sample and one Urdu/mixed-language sample before declaring the task complete.

## Current renderer architecture

The legacy laboratory-report path is primarily FPDF-based and contains absolute-position drawing. Prefer small, reusable renderer helpers and regression-safe migration over broad layout rewrites. PDF merge/compression is a separate concern and must not be used to repair text direction or typography defects.