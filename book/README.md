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
python -B ch05_coalescent_figures.py ../figures/ch05
python -B ch06_molecular_clock_figures.py ../figures/ch06
python -B ch07_recombination_ld_figures.py ../figures/ch07
python -B ch08_linked_selection_figures.py ../figures/ch08
python -B ch09_sweeps_figures.py ../figures/ch09
python -B ch10_genetic_load_figures.py ../figures/ch10
python -B ch11_muller_ratchet_figures.py ../figures/ch11
python -B ch12_introgression_figures.py ../figures/ch12
python -B ch13_fisher_geometric_figures.py ../figures/ch13
python -B ch14_population_structure_figures.py ../figures/ch14
python -B ch15_c_value_figures.py ../figures/ch15
python -B ch16_junk_dna_figures.py ../figures/ch16
python -B ch17_selfish_dna_figures.py ../figures/ch17
python -B ch18_drift_barrier_figures.py ../figures/ch18
python -B ch19_duplication_figures.py ../figures/ch19
python -B ch20_gene_balance_figures.py ../figures/ch20
python -B ch21_polyploidy_figures.py ../figures/ch21
python -B ch22_fractionation_figures.py ../figures/ch22
python -B ch23_gbgc_figures.py ../figures/ch23
python -B ch24_codon_usage_figures.py ../figures/ch24
python -B ch25_centromere_drive_figures.py ../figures/ch25
python -B ch26_sex_chromosome_figures.py ../figures/ch26
python -B ch27_dmi_figures.py ../figures/ch27
python -B ch28_epigenetic_inheritance_figures.py ../figures/ch28
python -B ch29_pangenome_figures.py ../figures/ch29
python -B ch30_missing_heritability_figures.py ../figures/ch30
python -B appA_status_figures.py ../figures/appA
```

Needs Python 3 with numpy and matplotlib (Liberation Sans font recommended). Outputs are PNG and SVG.

## Licence

Book text and the book’s own figures: CC BY 4.0. Scripts: MIT, as for the rest of the repository. Reproduced published figures keep their original licence (stated in each caption). See [LICENSE.md](LICENSE.md).
