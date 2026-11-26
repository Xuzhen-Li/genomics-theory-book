# Genomics Theory Book

English | [中文](README.zh.md)

A book about classic theories in genetics and genome evolution, and how well each one has held up. Every chapter states the theory and its history, lists what it predicts, weighs the evidence for and against, and gives a status label: **Verified**, **Partly verified**, **Contested** or **Rejected**. Each chapter also covers plants and crops, including grapevine and other clonally propagated perennials, and explains how to test the theory with public data.

- Contents: [INDEX.md](INDEX.md)
- Status of each theory: [STATUS.md](STATUS.md)
- Chapters: [`chapters/`](chapters/)
- Figures: [`figures/`](figures/), one folder per chapter; reproduced published figures are in `figures/chNN/published/`
- Figure scripts: [`scripts/`](scripts/)

## How the book is written

- Every reference was checked against Crossref or OpenAlex (title, authors, year, journal, DOI), and its abstract or full text was read before it was cited. Claims are limited to what those sources report.
- Figure 1 of a chapter is a published figure where an openly licensed one exists (CC BY or CC0). It is reproduced unchanged, with authors, year, title, journal, figure number, DOI and licence in the caption. Where no open figure exists, the book uses a redrawing marked “Redrawn after” its source, or its own schematic or simulation.
- Own figures follow one house style: text at least 6 pt, text contrast at least 4.5:1, and no text on borders. Each script fixes its random seed (20261126) and can be rerun.
- Each chapter links to the related short theory notes in [`../skills/genomics-theory-mining/theories/`](../skills/genomics-theory-mining/theories/).

## Rerunning the figures

```bash
cd book/scripts
python -B ch01_mendel_figures.py ../figures/ch01
python -B ch02_hwe_figures.py ../figures/ch02
python -B ch03_neutral_figures.py ../figures/ch03
python -B ch04_nearly_neutral_figures.py ../figures/ch04
```

Needs Python 3 with numpy and matplotlib (Liberation Sans font recommended). Outputs are PNG and SVG.

## Licence

Book text and the book’s own figures: CC BY 4.0. Scripts: MIT, as for the rest of the repository. Reproduced published figures keep their original licence (stated in each caption). See [LICENSE.md](LICENSE.md).
