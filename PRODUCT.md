# Product

## Register

brand

## Users

Two primary reading audiences, distinct enough that the design has to hold both without alienating either:

1. **Bilingual Hong Kong Catholic readers** — lay faithful, clergy, students at Catholic schools. The 思高聖經 alignment and Hong Kong Catholic terminology (天主, 聖神, 教宗, 通諭, 思高 numbering) are calibrated to this audience. Reading is intentional, often slow, sometimes liturgical-adjacent.
2. **AI-ethics curious general readers** — people drawn by the encyclical's subject (the human person in the time of artificial intelligence) who would not otherwise read a papal document. They arrive from blog posts, tech newsletters, or academic syllabi rather than from a parish. They read in English, with the Chinese column serving as cultural texture and a check on translation choices.

Both audiences read on desktop or tablet for sustained sessions, not in 30-second bursts. Older readers are the implicit calibration point: type size, contrast, and keyboard navigation are designed for someone over 50 reading at length, even at the cost of "tighter" visual moves.

## Product Purpose

A bilingual (English / Traditional Chinese) study edition of Pope Leo XIV's encyclical *Magnifica Humanitas* (15 May 2026), presenting the official Vatican English text alongside an unofficial, AI-assisted Hong Kong Catholic Chinese translation, with interactive scripture references that resolve in both languages (BSB for English, 思高聖經 for Chinese).

It exists because no official Chinese translation is available yet (and may not be for months) and because the encyclical's subject — AI and human dignity — invites a wider audience than papal documents normally reach. The AI-assisted nature of the translation is disclosed up front, in both languages.

Success, six months out: a small, well-made artifact, shared in trusted niches (a handful of HK Catholic readers, a few AI-ethics syllabi, a few blog mentions). No growth ambitions. The bar is craft, not reach.

## Brand Personality

**Reverent · scholarly · durable.**

The reference register is the *critical edition* — a Loeb Classical Library volume, a Cambridge or Oxford parallel-text edition, the Vatican's own polyglot editions. The thing the reader should feel within five seconds is: *this is set with care, by someone who respects the source*.

Voice across UI copy: deferential to the source, plain about its own limits, never marketing-warm. The translator's note says what is true (unofficial, AI-assisted, not for citation) and stops there. No persuasion, no FOMO, no asks.

## Anti-references

What this must not look like, in priority order:

1. **AI/SaaS landing page aesthetic.** The trap closest at hand: bright gradients, hero CTAs, three-column feature cards, Inter / Plus Jakarta Sans, breezy marketing copy. The category reflex an AI-themed document could fall into because of its subject. The page about AI must not look like a page *by* an AI startup.
2. **Generic Wikipedia / Project Gutenberg plain-text.** "Just put the text up" — functional but uncared-for. Times New Roman, default margins, blue links, no typographic decisions.
3. **Megachurch / evangelical web style.** Wrong denomination AND wrong register: stock photos of crowds and skies, casual sans, conversational copy.
4. **Algorithmic editorial-typographic clone.** Display-serif-italic + small-mono-labels + ruled-separators in the currently-saturated Notion/Substack-adjacent mode. The Loeb / Vatican lineage carves out this aesthetic family legitimately (it's the source the trend imitates), but the design should read as *that lineage*, not as the trend that copies it.

## Design Principles

1. **Apparatus over decoration.** What makes this trustworthy is the visible apparatus: parallel translation, paragraph numbering, footnote density, scripture cross-references that resolve in both languages, sources cited up-front. Polish goes into the apparatus. Decorative flourishes that don't serve scholarship get cut.
2. **Bilingual symmetry is the design.** The two-column parallel-text grid isn't a feature; it's the entire UX. Both columns get equal visual weight, equal typographic care, and equal access to chrome (warnings, disclaimers, popovers). A Chinese-only reader and an English-only reader see the same product.
3. **Disclose what AI did, in both languages, up front.** Given the encyclical's subject (the human person in the age of AI) and the translation's provenance (AI-assisted), transparency about the AI-translation status is itself a design value. It belongs above the fold, not in the footer, and in both languages, not just English.
4. **Reverence is calm, not loud.** Authority comes from restraint and care. The Loeb page commands respect by being utterly composed; large display moments, dramatic color shifts, and motion are not in this register. When in doubt, take a step out, not in.
5. **Older eyes are the calibration point.** Comfortable body type (≥18px), high contrast, generous line-height, strong keyboard focus indicators, no surprise motion. The Catholic-reader audience overlaps strongly with readers over 50; designing for them costs nothing for the younger AI-curious audience and serves the primary use case (sustained reading).

## Accessibility & Inclusion

- **WCAG AA** is the floor. Body text meets contrast at all times; muted secondary text is permitted only above contrast minimums.
- **Keyboard navigation** is first-class: every interactive element (scripture popovers, footnote refs, backrefs, TOC entries, disclaimer links) shows a visible `:focus-visible` indicator in the brand's cardinal red.
- **Older readers** are the calibration point for type size and contrast even though no specific reader need has been declared.
- **`prefers-reduced-motion`** is respected; the design has very little motion to begin with, but transitions and animations are explicitly disabled when the user prefers it.
- **Print** is a real use case (study, liturgical preparation, distribution within parishes), so a print stylesheet ships with the page.
- **Bilingual screen-reader behavior** is acceptable but not aggressively engineered. `lang="en-zh"` on the root is a deliberate hybrid declaration; individual columns are not separately `lang`-tagged, which is a known trade-off favoring reading flow over per-paragraph language switching.
