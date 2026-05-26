#!/usr/bin/env python3
"""Build site/index.html from the structured encyclical JSON + scripture lookups."""
import json, re, html as html_lib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "site"
SITE.mkdir(exist_ok=True)

doc = json.loads((DATA / "encyclical.json").read_text(encoding="utf-8"))
scr_en = json.loads((DATA / "scriptures_en.json").read_text(encoding="utf-8"))
scr_zh = json.loads((DATA / "scriptures_zh.json").read_text(encoding="utf-8"))

PLACEHOLDER_ZH = '<span class="pending">［中文翻譯進行中 · translation in progress］</span>'

# English book abbreviations (Vatican/Catholic + common Protestant variants).
EN_BOOK_RE = (
    r"Gen|Ex|Lev|Num|Deut|Dt|Josh|Jos|Judg|Jdg|Ruth|Rt|"
    r"1 Sam|2 Sam|1 Kgs|2 Kgs|1 Chron|2 Chron|1 Chr|2 Chr|"
    r"Ezra|Neh|Tob|Jdt|Esth|Est|1 Mac|2 Mac|1 Macc|2 Macc|"
    r"Job|Ps|Prov|Eccl|Qoh|Song|Cant|Wis|Sir|Isa|Is|Jer|Lam|Bar|Ezek|Ez|Dan|"
    r"Hos|Joel|Amos|Am|Obad|Jon|Mic|Mi|Nah|Hab|Zeph|Zep|Hag|Zech|Zec|Mal|"
    r"Mt|Mk|Lk|Jn|Acts|Rom|1 Cor|2 Cor|Gal|Eph|Phil|Phlp|Col|"
    r"1 Thess|2 Thess|1 Tim|2 Tim|Tit|Phlm|Phm|Heb|"
    r"Jas|1 Pet|2 Pet|1 Jn|2 Jn|3 Jn|Jude|Rev|Apoc"
)

# Chinese (思高) book abbreviations, derived from the zh_ref values in scriptures_zh.json
# so additions to the lookup table automatically extend the regex. Longest first so
# "厄下" matches before "厄" (no current collision, but defensive).
#
# Where 思高 numbering differs from the encyclical's Hebrew/English numbering — e.g.
# the Psalter, whose superscription is counted as verse 1 in 思高, shifting every
# Psalm verse by +1 — the zh_ref carries an explanatory parenthetical. We strip
# the parenthetical for matching, and we also synthesise an alias of the form
# "<zh_book> <en_chap_verse>" so the encyclical text (which uses Hebrew numbering)
# still resolves to the lookup key.
def _build_zh_ref_map():
    out = {}
    for key, val in scr_zh.items():
        if key == "_meta" or not isinstance(val, dict) or "zh_ref" not in val:
            continue
        raw = val["zh_ref"]
        canon = re.sub(r"\s*[（(].*", "", raw).strip()
        out[canon] = key
        zh_book = canon.split(" ", 1)[0] if " " in canon else canon
        en_tail = key.split(" ", 1)[1] if " " in key else ""
        if en_tail:
            out.setdefault(f"{zh_book} {en_tail}", key)
    return out


_ZH_REF_TO_KEY = _build_zh_ref_map()
_ZH_BOOKS = sorted({zh_ref.split(" ", 1)[0] for zh_ref in _ZH_REF_TO_KEY}, key=len, reverse=True)
ZH_BOOK_RE = "|".join(re.escape(b) for b in _ZH_BOOKS) if _ZH_BOOKS else r"(?!x)x"  # never matches if empty

# Unified regex: matches either an English-form ref or a Chinese-form ref, in either
# chapter:verse[-verse] or chapter-chapter range form. The EN branch keeps a leading
# word boundary; the ZH branch can't (Han characters aren't \w word chars).
REF_RE = re.compile(
    # English branch
    r"\b(?P<en_book>" + EN_BOOK_RE + r")"
    r"\s+(?:"
    r"(?P<en_chap>\d{1,3})(?::|,\s*)(?P<en_vs>\d{1,3})(?:[–—\-](?P<en_ve>\d{1,3}))?"
    r"|"
    r"(?P<en_c1>\d{1,3})[–—\-](?P<en_c2>\d{1,3})(?![:\d])"
    r")"
    r"|"
    # Chinese branch
    r"(?P<zh_book>" + ZH_BOOK_RE + r")"
    r"\s*(?:"
    r"(?P<zh_chap>\d{1,3})[:：](?P<zh_vs>\d{1,3})(?:[–—\-](?P<zh_ve>\d{1,3}))?"
    r"|"
    r"(?P<zh_c1>\d{1,3})[–—\-](?P<zh_c2>\d{1,3})(?![:：\d])"
    r")"
)


def _ref_to_key(m: "re.Match") -> str | None:
    """Resolve a REF_RE match to the canonical lookup key (English form).
    Returns None if no usable key was produced."""
    if m.group("en_book"):
        book = m.group("en_book")
        if m.group("en_chap"):
            key = f"{book} {m.group('en_chap')}:{m.group('en_vs')}"
            if m.group("en_ve"):
                key += f"-{m.group('en_ve')}"
        else:
            key = f"{book} {m.group('en_c1')}-{m.group('en_c2')}"
        return key
    if m.group("zh_book"):
        book = m.group("zh_book")
        if m.group("zh_chap"):
            zh_ref = f"{book} {m.group('zh_chap')}:{m.group('zh_vs')}"
            if m.group("zh_ve"):
                zh_ref += f"-{m.group('zh_ve')}"
        else:
            zh_ref = f"{book} {m.group('zh_c1')}-{m.group('zh_c2')}"
        return _ZH_REF_TO_KEY.get(zh_ref)
    return None


def wrap_scripture(text: str) -> str:
    """Wrap every recognised scripture ref (EN or ZH) into a popover anchor."""
    out, last = [], 0
    for m in REF_RE.finditer(text):
        out.append(html_lib.escape(text[last:m.start()]))
        key = _ref_to_key(m)
        disp = m.group(0)
        if key and key in scr_en:
            out.append(
                f'<a href="#" class="scripture" '
                f'data-ref="{html_lib.escape(key, quote=True)}" '
                f'role="button">{html_lib.escape(disp)}</a>'
            )
        else:
            out.append(html_lib.escape(disp))
        last = m.end()
    out.append(html_lib.escape(text[last:]))
    return "".join(out)


def wrap_footnote_refs(text: str) -> str:
    """English-column footnote markers. Carries id="fnref-N" so the
    footnote section's backref (↩) can navigate back to this anchor."""
    return re.sub(
        r"\[(\d+)\]",
        lambda m: f'<a href="#fn-{m.group(1)}" id="fnref-{m.group(1)}" class="fnref" role="doc-noteref">[{m.group(1)}]</a>',
        text,
    )


def wrap_footnote_refs_zh(text: str) -> str:
    """Chinese-column footnote markers. Same forward-navigation as the
    English version, but without id="fnref-N" — the EN column already
    owns that id, and HTML disallows duplicates. The single backref in
    the footnote section returns to the EN column; full bilingual
    backref symmetry would need per-language id suffixes plus paired
    backref glyphs and is out of scope for this pass."""
    return re.sub(
        r"\[(\d+)\]",
        lambda m: f'<a href="#fn-{m.group(1)}" class="fnref" role="doc-noteref">[{m.group(1)}]</a>',
        text,
    )


def render_en(text: str) -> str:
    return wrap_footnote_refs(wrap_scripture(text))


def render_zh(text: str) -> str:
    if not text or not text.strip():
        return PLACEHOLDER_ZH
    return wrap_footnote_refs_zh(wrap_scripture(text))


CSS = """
:root {
  --ink: #1c1916;
  --paper: #fbf7ec;
  --paper-deep: #f5efe0;
  --rule: #d9cfb6;
  --gold: #a07835;
  --cardinal: #8b1a1f;
  --muted: #7b7060;
  --link: #5a3a1f;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--paper); color: var(--ink); }
body {
  font-family: 'EB Garamond', 'Cormorant Garamond', 'Source Serif Pro', 'Times New Roman', serif;
  font-size: 18px; line-height: 1.65;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--link); }
a:hover { color: var(--cardinal); }

.masthead {
  text-align: center; padding: 3.5rem 1.5rem 2rem;
  border-bottom: 1px solid var(--rule);
  background: linear-gradient(180deg, var(--paper-deep), var(--paper));
}
.crest { font-size: 2rem; color: var(--gold); letter-spacing: .3rem; margin-bottom: .5rem; }
.eyebrow { font-variant: small-caps; letter-spacing: .25em; color: var(--muted); font-size: .8rem; }
.title-en {
  font-family: 'EB Garamond', 'Cormorant Garamond', serif;
  font-size: 3.2rem; font-weight: 600; letter-spacing: .03em;
  font-style: italic; margin: .5rem 0 .25rem;
}
.title-zh {
  font-family: 'Noto Serif TC', 'Source Han Serif TC', 'Songti TC', 'PingFang TC', serif;
  font-size: 2.2rem; font-weight: 700; color: var(--ink);
  margin: .25rem 0 1rem;
}
.subtitle {
  max-width: 56rem; margin: 0 auto; color: var(--muted);
  font-size: 1rem; line-height: 1.5;
}
.subtitle-en { font-style: italic; }
.subtitle-zh { font-family: 'Noto Serif TC', 'Source Han Serif TC', serif; margin-top: .35rem; }
.byline { margin-top: 1.5rem; font-variant: small-caps; letter-spacing: .15em; color: var(--cardinal); font-weight: 600; }
.byline-zh { font-variant: normal; font-family: 'Noto Serif TC', serif; color: var(--cardinal); margin-left: .8rem; }

nav.toc {
  max-width: 70rem; margin: 2rem auto 0; padding: 1.25rem 1.5rem;
  border: 1px solid var(--rule); background: var(--paper-deep);
  border-radius: 4px; font-size: .92rem;
}
nav.toc h2 { font-size: 1rem; font-variant: small-caps; letter-spacing: .2em;
  margin: 0 0 .75rem; color: var(--cardinal); border-bottom: 1px solid var(--rule); padding-bottom: .5rem;}
nav.toc ol { margin: 0; padding-left: 1.2rem; }
nav.toc li { margin: .2rem 0; }
nav.toc .zh { font-family: 'Noto Serif TC', serif; color: var(--muted); margin-left: .5rem; }
nav.toc a { text-decoration: none; }
nav.toc a:hover { text-decoration: underline; }

main { max-width: 90rem; margin: 0 auto; padding: 2rem 1.5rem 4rem; }
.section { margin: 3rem 0 2rem; }
.section-label {
  text-align: center; font-variant: small-caps; letter-spacing: .35em;
  color: var(--gold); font-size: .9rem; margin-bottom: .5rem;
}
.section-title {
  text-align: center; font-size: 1.7rem; color: var(--cardinal);
  font-weight: 600; max-width: 60rem; margin: 0 auto .35rem;
  font-style: italic;
}
.section-title-zh {
  text-align: center; font-family: 'Noto Serif TC', serif;
  font-size: 1.4rem; color: var(--ink); font-weight: 700;
  max-width: 60rem; margin: 0 auto 2rem;
}
.section-divider { text-align: center; color: var(--gold); margin: .5rem 0 2.5rem; letter-spacing: 1rem; }

.subhead {
  margin: 2.5rem auto 1.25rem; max-width: 90rem;
  display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;
  border-top: 1px solid var(--rule); padding-top: 1.5rem;
}
.subhead .en {
  font-style: italic; font-size: 1.25rem; color: var(--cardinal); font-weight: 600;
}
.subhead .zh {
  font-family: 'Noto Serif TC', serif; font-size: 1.2rem; color: var(--ink); font-weight: 700;
}

.bilingual {
  display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem;
  max-width: 90rem; margin: 0 auto;
}
.col-en, .col-zh {
  position: relative; padding: 0 .5rem;
}
.col-zh {
  font-family: 'Noto Serif TC', 'Source Han Serif TC', 'PingFang TC', serif;
  font-size: 17.5px; line-height: 1.95;
}
.para {
  display: grid; grid-template-columns: 2.5rem 1fr; gap: .5rem;
  align-items: baseline; margin-bottom: 1.6rem; scroll-margin-top: 2rem;
}
.para .num {
  text-align: right; color: var(--gold); font-size: .82rem; padding-top: .4rem;
  font-variant: small-caps; letter-spacing: .05em; user-select: none;
}
.para .body { text-align: justify; hyphens: auto; }
.col-zh .para .body { text-align: justify; text-justify: inter-ideograph; }
.continuation { margin-left: 3rem; margin-bottom: 1.6rem; }
.continuation.zh-cont { font-family: 'Noto Serif TC', serif; line-height: 1.95; }

a.scripture {
  text-decoration: none; border-bottom: 1px dotted var(--gold);
  color: var(--ink); cursor: pointer; padding: 0 1px;
  background: linear-gradient(transparent 70%, rgba(160,120,53,.18) 30%);
}
a.scripture:hover { color: var(--cardinal); border-bottom-color: var(--cardinal); }
.popover {
  position: absolute; z-index: 50; max-width: 32rem;
  background: var(--paper); border: 1px solid var(--rule);
  box-shadow: 0 8px 30px rgba(28, 25, 22, 0.18);
  border-radius: 4px; padding: 1rem 1.1rem; font-size: .92rem; line-height: 1.55;
}
.popover .ref-header { font-variant: small-caps; letter-spacing: .15em;
  color: var(--cardinal); font-weight: 600; font-size: .85rem; margin-bottom: .35rem; }
.popover .ref-en { margin-bottom: .75rem; color: var(--ink); font-style: italic; }
.popover .ref-zh { font-family: 'Noto Serif TC', serif; color: var(--ink); }
.popover .ref-zh-header {
  font-family: 'Noto Serif TC', serif; font-variant: normal;
  font-weight: 700; color: var(--cardinal); font-size: .85rem;
  margin: .75rem 0 .25rem; padding-top: .5rem;
  border-top: 1px dashed var(--rule);
}
.popover .close { position: absolute; top: .4rem; right: .6rem; color: var(--muted);
  background: none; border: none; font-size: 1.2rem; cursor: pointer; line-height: 1; }
.popover .close:hover { color: var(--cardinal); }

a.fnref {
  font-size: .7em; vertical-align: super; text-decoration: none;
  color: var(--cardinal); padding: 0 1px;
}
a.fnref:hover { text-decoration: underline; }

.pending {
  color: var(--muted); font-style: italic; font-family: 'Noto Serif TC', serif;
  background: rgba(218, 200, 165, 0.25); padding: 2px 6px; border-radius: 3px;
  font-size: .9em;
}

.footnotes {
  max-width: 70rem; margin: 4rem auto 2rem; padding: 2rem 1.5rem 0;
  border-top: 2px solid var(--rule); font-size: .88rem; color: var(--muted);
}
.footnotes h2 {
  font-variant: small-caps; letter-spacing: .2em; color: var(--cardinal);
  font-size: 1rem; font-weight: 600; margin-bottom: 1rem;
}
.footnotes ol { padding-left: 1.5rem; }
.footnotes li { margin-bottom: .5rem; line-height: 1.5; scroll-margin-top: 1rem; }
.footnotes a.backref { text-decoration: none; color: var(--gold); margin-left: .3rem; }
.footnotes a.backref:hover { color: var(--cardinal); }

footer.colophon {
  max-width: 70rem; margin: 3rem auto 4rem; padding: 2rem 1.5rem;
  border-top: 1px solid var(--rule); text-align: center;
  color: var(--muted); font-size: .85rem; line-height: 1.7;
}
footer.colophon strong { color: var(--ink); }
footer.colophon a { color: var(--cardinal); }

@media (max-width: 900px) {
  .bilingual, .subhead { grid-template-columns: 1fr; }
  .col-zh { border-top: 1px dashed var(--rule); padding-top: 1.5rem; margin-top: 1rem; }
  .title-en { font-size: 2.2rem; }
  .title-zh { font-size: 1.6rem; }
}
"""

# JS: builds popover purely via createElement + textContent. No innerHTML on user/data strings.
JS = r"""
(function () {
  var scrEN = __SCR_EN__;
  var scrZH = __SCR_ZH__;
  var openPopover = null;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function buildPopover(refKey) {
    var enEntry = scrEN[refKey];
    var zhEntry = scrZH[refKey];
    var pop = el('div', 'popover');
    pop.setAttribute('role', 'dialog');

    var close = el('button', 'close', '×');
    close.setAttribute('aria-label', 'Close');
    close.addEventListener('click', closePopover);
    pop.appendChild(close);

    pop.appendChild(el('div', 'ref-header', refKey + ' — BSB (English)'));
    pop.appendChild(el('div', 'ref-en', enEntry ? enEntry.text : 'Not found.'));

    var zhHeaderText = (zhEntry ? zhEntry.zh_ref : refKey) + ' — 思高聖經';
    pop.appendChild(el('div', 'ref-zh-header', zhHeaderText));
    pop.appendChild(el('div', 'ref-zh', zhEntry ? zhEntry.zh_text : '（思高本未提供）'));
    return pop;
  }

  function makePopover(refKey, anchor) {
    closePopover();
    if (!scrEN[refKey] && !scrZH[refKey]) return;
    var pop = buildPopover(refKey);
    document.body.appendChild(pop);
    var r = anchor.getBoundingClientRect();
    var scrollY = window.scrollY || window.pageYOffset;
    pop.style.top = (r.bottom + scrollY + 6) + 'px';
    var left = r.left + window.scrollX;
    var popW = pop.offsetWidth;
    if (left + popW > window.innerWidth - 16) left = window.innerWidth - popW - 16;
    pop.style.left = Math.max(8, left) + 'px';
    openPopover = pop;
  }

  function closePopover() {
    if (openPopover && openPopover.parentNode) openPopover.parentNode.removeChild(openPopover);
    openPopover = null;
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a.scripture');
    if (a) {
      e.preventDefault();
      makePopover(a.dataset.ref, a);
      return;
    }
    if (openPopover && !e.target.closest('.popover')) closePopover();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePopover(); });
})();
"""


def render_section(s):
    parts = []
    label_en = s.get("en_label", "")
    label_zh = s.get("zh_label", "")
    title_en = s.get("title_en", "")
    title_zh = s.get("title_zh", "")
    if label_en or title_en:
        parts.append('<section class="section">')
        if label_en:
            parts.append(f'<div class="section-label">{html_lib.escape(label_en)} · {html_lib.escape(label_zh)}</div>')
        if title_en:
            parts.append(f'<h2 class="section-title">{html_lib.escape(title_en)}</h2>')
        if title_zh:
            parts.append(f'<h3 class="section-title-zh">{html_lib.escape(title_zh)}</h3>')
        parts.append('<div class="section-divider">· · ·</div>')
        parts.append('</section>')
    for blk in s["blocks"]:
        if blk["type"] == "subheading":
            zh_val = blk.get("zh") or ""
            zh_html = html_lib.escape(zh_val) if zh_val else PLACEHOLDER_ZH
            parts.append(
                f'<div class="subhead"><div class="en">{html_lib.escape(blk["en"])}</div>'
                f'<div class="zh">{zh_html}</div></div>'
            )
        elif blk["type"] == "paragraph":
            n = blk["num"]
            en_html = render_en(blk["en"])
            zh_html = render_zh(blk.get("zh", ""))
            parts.append(
                '<div class="bilingual">'
                f'<div class="col-en"><div class="para" id="p-{n}">'
                f'<div class="num">¶ {n}</div><div class="body">{en_html}</div></div></div>'
                f'<div class="col-zh"><div class="para"><div class="num">¶ {n}</div>'
                f'<div class="body">{zh_html}</div></div></div>'
                '</div>'
            )
        elif blk["type"] == "continuation":
            en_html = render_en(blk["en"])
            zh_html = render_zh(blk.get("zh", ""))
            parts.append(
                '<div class="bilingual">'
                f'<div class="col-en"><div class="continuation">{en_html}</div></div>'
                f'<div class="col-zh"><div class="continuation zh-cont">{zh_html}</div></div>'
                '</div>'
            )
    return "\n".join(parts)


def render_toc(doc):
    items = []
    for s in doc["sections"]:
        if not s.get("en_label"): continue
        label = s["en_label"]
        title = s.get("title_en", "")
        zh = s.get("zh_label", "") + ((" · " + s.get("title_zh", "")) if s.get("title_zh") else "")
        items.append(
            f'<li><strong>{html_lib.escape(label)}</strong>'
            + (f' — <em>{html_lib.escape(title)}</em>' if title else "")
            + (f'<span class="zh">{html_lib.escape(zh)}</span>' if zh else "")
            + '</li>'
        )
    return '<nav class="toc"><h2>Contents · 目錄</h2><ol>' + "\n".join(items) + "</ol></nav>"


def render_footnotes(doc):
    parts = ['<section class="footnotes"><h2>Notes · 附註</h2><ol>']
    for fn in doc["footnotes"]:
        n = fn["num"]
        parts.append(
            f'<li id="fn-{n}">{html_lib.escape(fn["en"])}'
            f' <a class="backref" href="#fnref-{n}" aria-label="back to text">↩</a></li>'
        )
    parts.append('</ol></section>')
    return "\n".join(parts)


page = f"""<!doctype html>
<html lang="en-zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Magnifica Humanitas · 偉大的人類 · Encyclical Letter of Pope Leo XIV</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Noto+Serif+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<header class="masthead">
  <div class="crest">✠</div>
  <div class="eyebrow">Encyclical Letter · 教宗通諭</div>
  <h1 class="title-en">{html_lib.escape(doc['title']['en'])}</h1>
  <h2 class="title-zh">{html_lib.escape(doc['title']['zh'])}</h2>
  <p class="subtitle subtitle-en">{html_lib.escape(doc['title']['subtitle_en'])}</p>
  <p class="subtitle subtitle-zh">{html_lib.escape(doc['title']['subtitle_zh'])}</p>
  <div class="byline">His Holiness Pope Leo&nbsp;XIV<span class="byline-zh">教宗良十四世</span></div>
  <div class="byline" style="font-size:.78rem;margin-top:.5rem;color:var(--muted)">
    {html_lib.escape(doc['title']['date_en'])} · {html_lib.escape(doc['title']['date_zh'])}
  </div>
</header>

{render_toc(doc)}

<main>
{"".join(render_section(s) for s in doc['sections'])}
</main>

{render_footnotes(doc)}

<footer class="colophon">
<p><strong>Source</strong> · English text: <a href="https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html" target="_blank" rel="noopener">vatican.va</a> (official). © Libreria Editrice Vaticana.</p>
<p><strong>Chinese translation</strong> · <em>Unofficial study translation</em> rendered in Hong Kong Catholic terminology. Not a magisterial text. For liturgical or scholarly citation please await the official translation from the Holy See.</p>
<p><strong>Scripture quotations</strong> · English passages from the <a href="https://bible.helloao.org" target="_blank" rel="noopener">Berean Standard Bible</a> via HelloAO Bible API. Chinese passages from <strong>思高聖經 (Studium Biblicum Version)</strong> — published by the 思高聖經學會, Hong Kong.</p>
<p style="margin-top:1rem">{sum(1 for s in doc['sections'] for b in s['blocks'] if b['type']=='paragraph')} numbered paragraphs · {len(doc['footnotes'])} footnotes · {len(scr_en)} scripture lookups</p>
</footer>

<script>
{JS.replace('__SCR_EN__', json.dumps(scr_en, ensure_ascii=False)).replace('__SCR_ZH__', json.dumps(scr_zh, ensure_ascii=False))}
</script>
</body>
</html>
"""

(SITE / "index.html").write_text(page, encoding="utf-8")
print(f"Wrote {SITE / 'index.html'} ({len(page):,} bytes)")
