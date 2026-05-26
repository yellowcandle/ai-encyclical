# ai-encyclical

A bilingual (English / Traditional Chinese) study edition of Pope Leo XIV's encyclical *Magnifica Humanitas* (15 May 2026), on safeguarding the human person in the time of artificial intelligence.

**Live site:** <https://yellowcandle.github.io/ai-encyclical/>
**Repository:** <https://github.com/yellowcandle/ai-encyclical>

The page presents the official Vatican English text alongside an **unofficial, AI-assisted** Traditional Chinese study translation rendered in Hong Kong Catholic terminology. Interactive scripture references resolve in both languages: the Berean Standard Bible for English, 思高聖經 (Studium Biblicum Version) for Chinese. The unofficial nature of the Chinese translation is disclosed above the fold, in both languages, and the rendering should not be used for liturgical, magisterial, or scholarly citation.

## Sources

- English text: [vatican.va](https://www.vatican.va/content/leo-xiv/en/encyclicals/documents/20260515-magnifica-humanitas.html). © Libreria Editrice Vaticana.
- Scripture (English): Berean Standard Bible, public domain, via the [HelloAO Bible API](https://bible.helloao.org).
- Scripture (Chinese): 思高聖經 (Studium Biblicum Version), 思高聖經學會, Hong Kong.

## Project shape

- `site/index.html` — the built static page (single file, served by GitHub Pages)
- `data/` — source encyclical, translation blocks, scripture lookups
- `src/build.py`, `src/translate_all.py`, `src/translate_prompt.md` — build and translation pipeline
- `PRODUCT.md`, `DESIGN.md`, `.impeccable/design.json` — design context (impeccable / Stitch format)
- `.github/workflows/deploy.yml` — pushes to `main` redeploy the `site/` folder to GitHub Pages
