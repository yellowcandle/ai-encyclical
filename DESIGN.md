---
name: Magnifica Humanitas (Bilingual Edition)
description: Bilingual Loeb-style edition of Pope Leo XIV's encyclical on AI and human dignity
colors:
  ink: "#1c1916"
  paper: "#fbf7ec"
  paper-deep: "#f5efe0"
  rule: "#d9cfb6"
  gold: "#a07835"
  cardinal: "#8b1a1f"
  muted: "#7b7060"
  link: "#5a3a1f"
typography:
  display:
    fontFamily: "EB Garamond, Source Serif Pro, Iowan Old Style, Times New Roman, serif"
    fontSize: "3.2rem"
    fontWeight: 600
    lineHeight: "1.1"
    letterSpacing: "0.03em"
  display-zh:
    fontFamily: "Noto Serif TC, Source Han Serif TC, Songti TC, PingFang TC, serif"
    fontSize: "2.2rem"
    fontWeight: 700
    lineHeight: "1.2"
    letterSpacing: "normal"
  headline:
    fontFamily: "EB Garamond, Source Serif Pro, serif"
    fontSize: "1.7rem"
    fontWeight: 600
    lineHeight: "1.3"
    letterSpacing: "normal"
  title:
    fontFamily: "EB Garamond, Source Serif Pro, serif"
    fontSize: "1.25rem"
    fontWeight: 600
    lineHeight: "1.4"
    letterSpacing: "normal"
  body:
    fontFamily: "EB Garamond, Source Serif Pro, Iowan Old Style, Times New Roman, serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: "1.65"
    letterSpacing: "normal"
  body-zh:
    fontFamily: "Noto Serif TC, Source Han Serif TC, PingFang TC, serif"
    fontSize: "17.5px"
    fontWeight: 400
    lineHeight: "1.95"
    letterSpacing: "normal"
  label:
    fontFamily: "EB Garamond, Source Serif Pro, serif"
    fontSize: "0.78rem"
    fontWeight: 600
    lineHeight: "1.2"
    letterSpacing: "0.22em"
rounded:
  sm: "2px"
  md: "3px"
  lg: "4px"
spacing:
  xs: "0.25rem"
  sm: "0.5rem"
  md: "1rem"
  lg: "1.5rem"
  xl: "2.5rem"
  2xl: "4rem"
components:
  translators-note:
    backgroundColor: "{colors.paper-deep}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "1.25rem 1.5rem 1.35rem"
  toc:
    backgroundColor: "{colors.paper-deep}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "1.25rem 1.5rem"
  popover:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "1rem 1.1rem"
  scripture-link:
    textColor: "{colors.ink}"
  scripture-link-hover:
    textColor: "{colors.cardinal}"
  footnote-ref:
    textColor: "{colors.cardinal}"
  paragraph-number:
    textColor: "{colors.gold}"
  body-link:
    textColor: "{colors.link}"
  body-link-hover:
    textColor: "{colors.cardinal}"
---

# Design System: Magnifica Humanitas (Bilingual Edition)

## 1. Overview

**Creative North Star: "The Loeb Edition for the AI Age"**

This is the visual system for a single document presented as a critical edition. The reference is a Loeb Classical Library volume, transplanted into 2026: parallel bilingual text (English / Traditional Chinese) as the entire reading surface, generous typography set in EB Garamond and Noto Serif TC, paragraph numbering, footnote apparatus, and interactive scripture cross-references that resolve in both languages. The apparatus is the design; decoration is what the apparatus doesn't need.

The palette is a warm-cream paper with a single magisterial cardinal accent, plus manuscript gold for paragraph numbers and rule lines. Surfaces are flat. Motion is essentially absent. Layout is the strict two-column bilingual grid that the Loeb format made famous, the same one Vatican Polyglot Press editions have used for centuries.

What this system explicitly rejects: AI/SaaS landing-page aesthetics (gradients, hero CTAs, feature cards, Inter/Plus Jakarta Sans), generic Wikipedia/Project Gutenberg plain-text indifference, megachurch web stock-photo warmth, and the currently-saturated Notion/Substack editorial-typographic clone (display-italic-serif + small-mono-labels + ruled-separators). The lineage we *are* in (Loeb, Vatican Polyglot) is the original this trend imitates; the design should read as the source, not the copy.

**Key Characteristics:**
- Bilingual two-column parallel-text grid is the entire UX
- Cream paper background, never pure white
- A single magisterial cardinal accent, used sparingly on labels, links, focus rings, and the leading section mark
- Manuscript-gold paragraph numbers in tracked small-caps, in the left gutter
- No buttons, no forms, no cards, no shadows except one popover
- No motion beyond hover color changes; `prefers-reduced-motion` strips even those

## 2. Colors

A warm, paper-toned palette: one cream surface, one ink, one cardinal, one gold, and a thin rule line. Restrained color strategy in the impeccable sense: tinted neutrals plus accents kept under 10% of any screen.

### Primary

- **Magisterial Cardinal** (`#8b1a1f`): the document's single voice color. Used on the leading `§` section mark on the translator's note, on the small-caps tracked labels (`Contents`, `Translator's Note & Source`, `Chapter Three`), on footnote reference superscripts, on `:focus-visible` outlines, and on hover transitions of interactive text. Never used as a fill behind blocks of text. Never used on body type.
- **Manuscript Gold** (`#a07835`): paragraph numbers in the bilingual grid's left gutter; the highlight wash under scripture-link text (a low-opacity yellow); the ornamental dot dividers (`· · ·`) between sections; the crest glyph (`✠`) at the top of the masthead. The gold is the *book* color; the cardinal is the *voice* color.

### Neutral

- **Warm Cream** (`#fbf7ec`): the page background. Set on `body`. Never `#fff`. This is the paper.
- **Deeper Cream** (`#f5efe0`): the surface color for grouped chrome — the translator's note, the Table of Contents, and the masthead gradient. Reads as a faint card without becoming a card.
- **Warm Black** (`#1c1916`): the ink color. Body type, headings, popover content. Never `#000`.
- **Muted Stone** (`#7b7060`): subtitle text, date line, colophon body, paragraph-number labels in some contexts. Used for content that's present but de-emphasized. Must remain above WCAG AA on cream surfaces — verify before scaling down further.
- **Rule Line** (`#d9cfb6`): every border, every divider, every separator. The line is the same color everywhere. Width varies (0.5pt on print, 1px on screen, 2px for the footnote section break, dashed for mobile-only column dividers).
- **Linked Brown** (`#5a3a1f`): default link color in colophon prose. Hover lifts to Magisterial Cardinal.

### Named Rules

**The One Voice Rule.** Magisterial Cardinal (`#8b1a1f`) is the document's only true accent. It carries labels, focus indicators, footnote markers, and hover state. It is never a background fill behind type. It does not appear on body type at rest. Its rarity is what makes the cardinal feel like a *voice*, not a decoration.

**The No-Pure-White Rule.** The page background is `#fbf7ec`, never `#fff`. Surfaces are `#f5efe0`, never `#fafafa` or `#f5f5f5`. The cream IS the paper; pure white would read as a screen and break the Loeb illusion immediately.

**The Cardinal-Never-Fills Rule.** Cardinal renders as type, border, outline, or 1px-icon stroke. It is never a background-color fill, never a button surface, never a callout body. The moment the cardinal becomes a *block* of color, the document starts feeling like a SaaS landing page.

## 3. Typography

**Display Font:** EB Garamond (with Source Serif Pro, Iowan Old Style, Times New Roman as fallbacks). Cormorant and Cormorant Garamond are explicitly excluded — both are on impeccable's reflex-reject list.

**Body Font (Chinese):** Noto Serif TC (with Source Han Serif TC, Songti TC, PingFang TC as fallbacks). Hong Kong / Macau diocese typographic conventions.

**Label Font:** EB Garamond at small-caps with heavy tracking; no separate label family.

**Character.** A classical-Renaissance Garamond pairing with a Traditional Chinese serif (思源 / Noto family). The English column reads as a humanist book face; the Chinese column reads as a Ming-style book face. Together they produce a "two voices, one document" effect that matches the bilingual editorial frame. There is no monospace font and no sans-serif. The page is set the way a printed book is set.

### Hierarchy

- **Display** (600 weight, italic, 3.2rem, line-height 1.1, letter-spacing 0.03em): the masthead title (`MAGNIFICA HUMANITAS`). Italic Garamond at this scale is the document's single typographic flourish. Drops to 2.2rem under 900px.
- **Display ZH** (700 weight, 2.2rem, Noto Serif TC): the masthead Chinese title (`「壯麗的人性」通諭`). Sits beneath the English display title at smaller scale per the source-language hierarchy.
- **Headline** (600 weight, italic, 1.7rem): chapter and section titles in the body (`The grandeur of humanity...`). Same italic Garamond as Display, just smaller.
- **Title** (600 weight, italic, 1.25rem): subhead row across both columns (the `<div class="subhead">`). Cardinal-colored italic on the English side, plain Ming-style on the Chinese.
- **Body** (400 weight, 18px, line-height 1.65): English column body type. Cap line length: each of the two columns sits in roughly 45rem of a 90rem grid, putting line length at ~70ch — within the 65-75ch target.
- **Body ZH** (400 weight, 17.5px, line-height 1.95): Chinese column body type. Chinese needs more line-height than English at the same x-height; 1.95 is calibrated for sustained Ming-style reading.
- **Label** (600 weight, 0.78rem, letter-spacing 0.22em, small-caps): every chrome label — section dividers (`INTRODUCTION · 引言`), TOC heading (`Contents · 目錄`), translator's note label (`Translator's Note & Source · 譯者按與來源`), colophon labels (`Scripture provenance`). Cardinal-colored.

### Named Rules

**The Italic-Garamond-Only-At-Scale Rule.** Italic Garamond is the document's headline gesture, used at 1.7rem and above. It is not used for body emphasis; for that, use plain italics within the body font. The italic-at-scale is a Loeb / classical-edition convention; italic-at-body would be magazine.

**The No-Sans-Serif Rule.** This is a book. There is no sans-serif font on the page, ever, including labels and metadata. Labels get their distinctiveness from small-caps + letter-spacing on Garamond, not from a sans-serif switch. Adding a single sans would announce "this is a website."

**The Bilingual-Parity Rule.** Whatever the English column gets, the Chinese column gets. If English body is 18px, Chinese body is 17.5px (compensated for Chinese x-height). If English has a small-caps tracked label, Chinese gets the same content in a Ming-style 700-weight Chinese-typographic equivalent. No language is a translation *appendage* of the other.

## 4. Elevation

The system is flat by default. Surfaces sit at one of three tonal layers: page (`#fbf7ec`), chrome (`#f5efe0`), or popover (`#fbf7ec` again, raised by a shadow). Depth is conveyed by these tonal shifts and by the rule lines (`#d9cfb6`), not by stacking shadows on resting surfaces.

The single resting shadow on the page is the **popover shadow**: `0 8px 30px rgba(28, 25, 22, 0.18)`. It appears only when a scripture reference is clicked. No card, no button, no chrome carries shadow at rest. Hover states do not produce shadow.

### Named Rules

**The Flat-By-Default Rule.** Resting surfaces are flat. The popover is the *only* shadowed surface in the system, and it appears only in response to a click on a scripture reference. If you find yourself wanting a shadow to separate one block from another, use the rule line (`#d9cfb6`) or a tonal shift to `paper-deep` instead.

**The Tonal-Layer Rule.** The system has exactly three tonal layers: `#fbf7ec` (page), `#f5efe0` (chrome and masthead), `#fbf7ec` (popover, raised by shadow). No additional surface shades. Inventing a fourth layer (a `#f8f3e3` between page and chrome) compounds drift faster than it solves any real depth problem.

## 5. Components

### Masthead

A centered editorial title block at the top of the document. Crest glyph (`✠`) in Manuscript Gold; small-caps tracked eyebrow (`Encyclical Letter · 教宗通諭`) in Muted Stone; the display title in italic EB Garamond; the Chinese display title in Noto Serif TC; bilingual subtitle in muted prose; byline in small-caps tracked cardinal; date line. Background is a top-to-bottom gradient from `paper-deep` to `paper`, with a 1px `rule`-color bottom border. Vertical padding generous (3.5rem top, 2rem bottom); horizontal centered at all viewport sizes.

### Table of Contents

A flat-bordered ordered list at `max-width: 70rem`. Background `paper-deep`; 1px `rule` border; 4px radius. Heading "Contents · 目錄" in small-caps cardinal labels. Chapter entries pair English (`CHAPTER ONE · A DYNAMIC APPROACH...`) and Chinese (`第一章 · 忠於福音的動態進路`) on one line, separated by middle-dots (`·`) in both languages. Hover: underline only. Focus-visible: 1.5px cardinal outline at 2px offset.

### Translator's Note (Signature Component)

The above-the-fold disclaimer panel. Same `paper-deep` background and 1px `rule` border as the TOC, but distinguished by a leading `§` section mark in Magisterial Cardinal italic Garamond at 1.4rem, top-left, replacing what would otherwise be a side-stripe border (which is forbidden — see Don'ts). Bilingual two-column grid inside, mirroring the document's body grid. Small-caps tracked label at the top (`Translator's Note & Source · 譯者按與來源`). Two short paragraphs per column: a disclaimer paragraph and a source-attribution paragraph.

### Bilingual Paragraph Row (Signature Component)

The body paragraph as displayed in the parallel-text grid. Two columns at `1fr 1fr` with 2.5rem gap; each column has its own inner grid (`grid-template-columns: 2.5rem 1fr`) for paragraph number + body text. Paragraph number rendered in Manuscript Gold, 0.82rem, small-caps tracked, right-aligned in the gutter (the Loeb / classical-edition convention). Body text justified with hyphens-auto in English; Chinese uses `text-justify: inter-ideograph`. Mobile (<900px): grid collapses to single column; Chinese column gets a dashed `rule`-colored top border.

### Scripture Link

Inline anchor inside body text, marking a scripture citation (e.g. `Prov 8:22-31`). Default: ink color, no underline, but a 1px dotted gold bottom border and a low-opacity yellow background wash (a `linear-gradient` highlight covering the bottom 30% of the text height). Hover: text and border shift to Magisterial Cardinal. Focus-visible: 2px cardinal outline at 3px offset, 2px radius. On click, renders a popover.

### Footnote Reference

A superscript anchor (e.g. `[7]`) rendered at 0.7em, in Magisterial Cardinal, with no underline by default. Hover: underline appears. Focus-visible: 1.5px cardinal outline at 2px offset. Backref anchor (`↩`) in the footnotes section uses Manuscript Gold, hover lifts to Magisterial Cardinal.

### Popover (Signature Component)

Positioned absolutely below the clicked scripture link. `paper` background, 1px `rule` border, 4px radius, the system's single shadow (`0 8px 30px rgba(28, 25, 22, 0.18)`). Renders the English passage from the Berean Standard Bible and the Chinese passage from 思高聖經, each with a small-caps tracked cardinal label header. Close button (✕) in the top-right corner, Muted Stone color, hover lifts to Magisterial Cardinal.

### Colophon

Footer block at the page bottom, slim. Centered text in Muted Stone at 0.85rem. Three short paragraphs: scripture provenance, a link upward to the translator's note, and a one-line metadata stat (`228 numbered paragraphs · 224 footnotes · 25 scripture lookups`). 2px `rule`-colored top border; 1px on print.

## 6. Do's and Don'ts

### Do:

- **Do** preserve the bilingual two-column grid at every level (body, TOC, translator's note, popover). If a piece of chrome only applies to one language, it's wrong.
- **Do** use Magisterial Cardinal (`#8b1a1f`) only as type, border, outline, or 1px stroke. Never as a fill.
- **Do** keep the paragraph-number gutter at the left of each column (the Loeb convention). The gold paragraph numbers in tracked small-caps are the document's most identifiable mark.
- **Do** use middle-dots (`·`) as separators in chrome (TOC, labels, masthead). Both English and Chinese halves of the same line should use the same separator.
- **Do** name colors with the manuscript voice for accents (Magisterial Cardinal, Manuscript Gold) and the restrained voice for neutrals (Warm Cream, Warm Black, Muted Stone). The accents get the distinctive language; the neutrals stay quiet.
- **Do** verify color contrast for Muted Stone on `paper-deep` whenever you scale down — that pairing sits closest to the WCAG AA floor.
- **Do** ship a print stylesheet whenever new chrome is added; encyclicals get printed for study.
- **Do** respect `prefers-reduced-motion` reflexively. The page has almost no motion, so the override is cheap; ship it anyway.
- **Do** keep visible `:focus-visible` outlines on every interactive element in Magisterial Cardinal at 1.5–2px width, 2–3px offset.

### Don't:

- **Don't** use side-stripe borders. `border-left` or `border-right` greater than 1px as a colored accent on the translator's note, callouts, list items, or anything else is forbidden by impeccable's absolute bans. Use a full border plus a leading `§`-style mark instead.
- **Don't** use em dashes (` — ` or `--`) in chrome (UI copy, TOC, labels, page title, popover headers). Use commas, colons, semicolons, periods, or middle-dots. The encyclical's body text and footnotes are source content and stay untouched; Chinese `——` (full-width double dash) is a Chinese typographic convention and also stays.
- **Don't** add Cormorant or Cormorant Garamond to font stacks. Both are on impeccable's reflex-reject list. EB Garamond is the primary; fall back to Source Serif Pro, Iowan Old Style, Times New Roman.
- **Don't** introduce a sans-serif anywhere on the document. This is a book. Labels get their distinctiveness from small-caps + letter-spacing on Garamond, not a sans switch.
- **Don't** use `#000` or `#fff`. The page is cream paper with warm-black ink. Pure values break the lineage on the first glance.
- **Don't** drift into AI/SaaS landing-page aesthetics: bright gradients, hero CTAs, three-column feature cards, Inter or Plus Jakarta Sans, breezy marketing copy. The page about AI must not look like a page *by* an AI startup.
- **Don't** drift into megachurch / evangelical web style: stock photos of crowds and skies, casual sans, soft pastel backgrounds, conversational warmth. Wrong denomination and wrong register.
- **Don't** drift into generic Wikipedia / Project Gutenberg plain-text. Times New Roman + default margins + blue links = uncared-for. The document is *set*; setting must be visible.
- **Don't** add cards. There are no cards in this system. The TOC and the translator's note are *bordered note panels*, not cards; they are larger, full-width, and have no shadow. A grid of equally-sized icon-heading-text cards is the SaaS template par excellence.
- **Don't** add modals. The popover is positioned absolutely under the scripture link; it is not a modal. A modal would interrupt reading, which is the entire point of the page.
- **Don't** animate layout properties. The page has essentially no motion; if you add any, use only color or opacity transitions, ease-out-quart or ease-out-expo, 150–250ms.
- **Don't** repeat the source attribution in both the translator's note and the colophon. The note is the canonical place; the colophon points up to it.
