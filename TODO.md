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
- **`data/glossary.json` finalized** — 14 → 35 entries. 21 new entries
  added with HK Catholic-style ZH definitions, grounded in actual paragraph
  references from the encyclical body (verified against `data/encyclical.json`).
  Two new groups introduced for cleaner organization: `教會文獻與大公會議`
  (6 entries: Vatican II, Gaudium et Spes, Populorum Progressio, Laudato Si',
  Fratelli Tutti, Dignitas Infinita) and `教宗與教會人物` (10 entries:
  Leo XIV/XIII, Pius XI/XII, Paul VI, John Paul II, Benedict XVI, Francis,
  Augustine, Aquinas). Algorithm + LLM added to AI group. Magisterium,
  Synodality, Imago Dei added to Catholic terms group. All definitions use
  HK conventions (`良`/`庇護`/`保祿`/`若望保祿`/`本篤`/`方濟各`/`奧斯定`/
  `多瑪斯`/`牧職憲章`/`眾位弟兄`/`願祢受讚頌`/`民族發展`/`無限尊嚴`/
  `演算法`).

### In progress

- **Visual verification + deploy**. The build pipeline is wired up and
  `python3 src/build.py` produces a 537 KB `site/index.html` with the
  expected anchor counts; the user should open the page locally to
  confirm the glossary styling and popover behavior look right before
  pushing.

### Outstanding

1. ~~**Finalize `data/glossary.json`**~~ — DONE 2026-05-27.
2. ~~**Extend each entry with `surface_forms`**~~ — DONE 2026-05-27.
3. ~~**Restore `render_glossary()` in `src/build.py`**~~ — DONE 2026-05-27.
   Visual treatment matches commit `21ab984`: paper-deep background,
   1px rule border, cardinal small-caps summary, rotating ▸ disclosure
   mark, dashed-rule h3 group headers, bilingual two-column definition.
   Generates 35 entries across 4 groups directly from `data/glossary.json`.
4. ~~**Add `wrap_glossary_terms(text, lang)`**~~ — DONE 2026-05-27.
   Implementation in `src/build.py`: builds one alternation regex per
   language over all 35 entries&rsquo; surface forms (longest-first by
   pattern length), runs *after* `wrap_scripture` and only operates on
   plain-text segments between existing anchors (so it can&rsquo;t
   wrap inside a scripture anchor or break attribute markup). Per-block
   `seen` sets enforce first-occurrence-per-paragraph. Case-insensitive
   throughout; embedded `\b` boundaries handle the proper-noun overlap
   cases that needed care.
5. ~~**Extend the popover JS**~~ — DONE 2026-05-27. Two popover builders
   share positioning + close + Escape handling. Glossary definitions are
   pre-tokenized server-side into `[["t", "text"], ["em", "Magnifica
   Humanitas"], …]` and rendered with `createElement` + `textContent` —
   **no `innerHTML` anywhere** on dynamic data, per the
   `security-guidance` hook&rsquo;s recommendation. The static collapsed
   glossary block emits raw HTML (entities + `<em>`) directly, which is
   fine because it&rsquo;s server-rendered, not parsed at runtime.
6. ~~**Pipe through `render_en` and `render_zh`**~~ — DONE 2026-05-27.
   Both functions now take an optional `seen_gloss: set` parameter;
   `render_section` allocates fresh sets per paragraph or continuation
   block so a term can repeat once per block in each column.
7. ~~**Rebuild + verify**~~ — partially done. Build output:
   - 62 `a.scripture` anchors (unchanged ✓)
   - 582 `a.glossary` anchors (across 228 paragraphs in two columns)
   - 35 entries in the collapsed glossary block, in 4 groups
   - 394 footnote refs (unchanged)
   - `node --check` confirms JS parses cleanly
   - No placeholder leaks (`__SCR_EN__`, `__GLOSSARY__` all substituted)
   - No `innerHTML` calls in JS (only references in comments)
   Visual verification in a browser still pending.

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
