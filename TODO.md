# TODO

## Active: bilingual glossary popovers (Wikipedia-grounded)

Goal: every Catholic/AI key term in the body text becomes a clickable popover
showing a brief bilingual definition + Wikipedia link. Single source of truth
in `data/glossary.json` drives both the (existing) collapsed glossary block at
the top of the page AND the new inline popovers.

### Done

- `data/glossary.json` extracted from commit `21ab984` — 14 entries
  (8 Catholic + 6 AI/tech), each with `term_en`, `term_zh`, `wp_en`, `wp_zh`,
  `def_en`, `def_zh`, `group_en`, `group_zh`. Schema documented in the file's
  `_meta` block.
- Frequency audit complete: ~30 candidate terms found in the body text. See
  `audit notes` below for the ranked list.
- EN Wikipedia summaries fetched into `/tmp/wp_extracts.json` for 21 new
  candidate terms (popes, documents, concepts). Most worked via the
  `?action=query&prop=extracts&exintro=1` MediaWiki API; two need manual
  fallback (`Laudato Si'`, `Dignitas Infinita` — Wiki extract API returns
  empty even though articles exist).

### In progress

- **Write ZH definitions in HK Catholic style** for the ~20 new glossary
  entries. ZH Wikipedia has poor Catholic doctrine coverage (no articles
  for `Gaudium et Spes`, `Laudato Si'`, `Dignitas Infinita`,
  `Synodality`, `Imago Dei`, `Magisterium`, `Common Good`, `Rerum Novarum`),
  and where articles exist they often use mainland (Beijing) transliteration
  rather than HK style (e.g. `尼希米` vs `乃赫米雅` for Nehemiah,
  `约翰保罗二世` vs `若望保祿二世` for John Paul II). User-provided pointers
  for HK style: <https://catholic.org.hk/> (Cloudflare-blocks bots — needs
  manual reference), <https://www.catholiccentre.org.hk/> (bookstore, not a
  glossary). Reachable alternatives: <https://kkp.org.hk/> (公教報) and
  <https://www.vaticannews.va/zh.html> (Vatican News Chinese).

### Outstanding

1. **Finalize `data/glossary.json`** — add ~20 new entries to the existing
   14, with HK Catholic ZH definitions. Suggested new entries:
   - Popes (10): Leo XIV, Leo XIII, Pius XI, Pius XII, Paul VI, John Paul II,
     Benedict XVI, Francis, Augustine of Hippo, Thomas Aquinas
   - Documents (5): Gaudium et Spes, Fratelli Tutti, Laudato Si',
     Populorum Progressio, Dignitas Infinita
   - Concepts (5+): Second Vatican Council, Synodality, Magisterium,
     Imago Dei, Algorithm, Large Language Model
2. **Extend each entry with `surface_forms`** — a list of EN + ZH regex
   alternations that should match in body text. Critical for catching
   variants: `Tower of Babel|Babel` for EN, `巴貝耳塔` + `巴貝耳` for ZH,
   etc. Without this, the wrapper won't match all real occurrences.
3. **Restore `render_glossary()` in `src/build.py`** — render the collapsed
   `<details>` block at the top of the page from glossary.json. This fixes
   the regression I introduced (the original glossary HTML was injected
   directly into `site/index.html` in commit `21ab984` and got wiped when I
   rebuilt for the scripture-popover work). See `git show 21ab984:site/index.html`
   for the visual treatment to match.
4. **Add `wrap_glossary_terms(text, lang)`** in `src/build.py` — scans
   rendered text for glossary terms, wraps the first occurrence per
   paragraph in `<a class="glossary" data-term="<id>">`. Longest-first
   matching to avoid `Leo` eating `Leo XIII`. Case-sensitive for proper
   nouns, case-insensitive for common nouns (AI, common good, algorithm).
5. **Extend the popover JS** to handle `.glossary` anchors. Same popover
   shape as scripture (header + EN + ZH + close button), but the body is
   the definition not the scripture text, and the footer is the Wikipedia
   link(s).
6. **Pipe through `render_en` and `render_zh`** so both columns get the
   inline popovers.
7. **Rebuild + verify** — confirm 62 existing scripture anchors unchanged,
   collapsed glossary block restored, sample terms (`Fratelli Tutti`,
   `John Paul II`, `artificial intelligence`) wrap to popover anchors in
   both EN and ZH columns. Also visually check the page so the glossary
   styling matches the original (paper-deep background, rule border,
   cardinal small-caps labels, rotating ▸ disclosure mark).

### Open questions

- **First-occurrence-per-paragraph or all occurrences?** Wrapping every
  occurrence will visually clutter the prose (`AI` appears 76+ times).
  First-per-paragraph is the encyclopedia convention. Going with that
  unless told otherwise.
- **`AI` as a standalone abbreviation needs `\b` boundaries** — without
  them, case-insensitive matching catches `said`, `aim`, `again`, `details`,
  `main`, etc. (Audit showed 412 false positives.)
- **HK Catholic ZH terminology divergence from Wikipedia** — already
  noted in commit `21ab984`'s message: 巴別塔 vs 巴貝耳塔, 尼希米 vs 乃赫米雅,
  道成肉身 vs 聖言成了血肉. The glossary entries should use HK style.

## Background: blocked on GitHub Pages deploy

Local `f9df3d9` (bilingual scripture popovers + chapter-range citations,
yellowcandle-authored) is on `origin/main` but not deployed.
GitHub Actions outage (2026-05-26 UTC) prevented the workflow from running;
status was still showing `degraded_performance` for Actions when this
session paused. Once Actions recovers:

```
gh run rerun 26448128506 --repo yellowcandle/ai-encyclical
```

— or push any new commit. Verify deploy by hard-reloading
<https://yellowcandle.github.io/ai-encyclical/?v=8> and clicking a Chinese
scripture ref like `(默 21:2)` to confirm the popover appears.

## Audit notes (frequency-ranked candidate terms)

From `data/encyclical.json` body text, after fixing case-sensitivity:

| EN pattern | EN | ZH | ZH surface forms |
|---|---:|---:|---|
| common good | 74 | 77 | 公益 |
| Catholic Social Teaching | 0 | 67 | 教會社會訓導 / 社會訓導 |
| magisterium | 6 | 55 | 訓導 |
| Subsidiarity | 20 | 25 | 輔助性原則 / 輔助性 |
| algorithm | 19 | 18 | 演算法 |
| Pope Francis | 18 | 18 | 方濟各 |
| John Paul II | 15 | 15 | 若望保祿二世 |
| Tower of Babel / Babel | 13 | 13 | 巴貝耳塔 / 巴貝耳 |
| Nehemiah | 11 | 9 | 乃赫米雅 |
| Second Vatican Council | 10 | 10 | 梵蒂岡第二屆大公會議 |
| Paul VI | 9 | 9 | 保祿六世 |
| Encyclical | 7 | 10 | 通諭 |
| Rerum Novarum | 4 | 11 | 《新事》 / 新事 |
| Leo XIII | 7 | 7 | 良十三世 |
| Augustine | 4 | 8 | 聖奧斯定 / 奧斯定 |
| transhumanism | 5 | 6 | 超人類主義 |
| Incarnation | 4 | 5 | 聖言成了血肉 / 降生成人 |
| technocratic paradigm | 5 | 2 | 科技至上 |
| Fratelli Tutti | 2 | 4 | 《眾位弟兄》 |
| Laudato Si' | 2 | 4 | 《願祢受讚頌》 |
| synodality | 2 | 4 | 共議性 |
| Benedict XVI | 2 | 2 | 本篤十六世 |
| Thomas Aquinas | 1 | 3 | 多瑪斯·阿奎那 / 聖多瑪斯 / 阿奎那 |
| Gaudium et Spes | 2 | 2 | 牧職憲章 |
| Populorum Progressio | 1 | 2 | 《民族發展》 |
| Imago Dei | 0 | 3 | 天主的肖像 |
| Pius XII | 1 | 1 | 庇護十二世 |
| large language model | 1 | 1 | 大型語言模型 |
| lethal autonomous weapons | 0 | 1 | 自主武器系統 |
| Leo XIV | 0 | 1 | 良十四世 |
| Pius XI | 1 | 0 | — |
| Dignitas Infinita | 1 | 0 | — |

Note: AI is 76+77 (huge) but must use `\bAI\b` to avoid 412 false positives.
