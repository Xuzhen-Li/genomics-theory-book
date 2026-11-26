# Genomics Theory Book（基因组理论之书）

[English](README.md) | 中文

这是一本讲遗传学和基因组演化经典理论、以及每个理论到今天还站不站得住的书。每章写清理论内容和历史、它的预测、支持和反对的证据，并给出地位标签：**已验证**、**部分验证**、**有争议** 或 **被否定**。每章还讨论植物和作物，包括葡萄等克隆繁殖的多年生作物，并说明怎样用公开数据检验这个理论。

- 目录：[INDEX.zh.md](INDEX.zh.md)
- 各理论地位总表：[STATUS.zh.md](STATUS.zh.md)
- 章节：[`chapters/`](chapters/)
- 图：[`figures/`](figures/)，每章一个文件夹；转载的发表图放在 `figures/chNN/published/`
- 作图脚本：[`scripts/`](scripts/)

## 写作规则

- 每篇参考文献都在 Crossref 或 OpenAlex 上核对过题目、作者、年份、期刊和 DOI，并在引用前读过摘要或全文。文中的说法只限于这些来源报告的内容。
- 只要有开放许可（CC BY 或 CC0）的发表图，每章的图 1 就用发表图，原样转载，图注写明作者、年份、题目、期刊、图号、DOI 和许可。没有开放图时，用标明“Redrawn after”出处的重绘图，或本书自绘的示意图和模拟图。
- 自绘图统一风格：字号不小于 6 pt，文字对比度不低于 4.5:1，文字不压边框。每个脚本固定随机种子（20261126），可以重跑。
- 每章都链接到 [`../skills/genomics-theory-mining/theories/`](../skills/genomics-theory-mining/theories/) 中相关的理论短笔记。

## 重新生成图

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
```

需要 Python 3、numpy 和 matplotlib（建议安装 Liberation Sans 字体），输出 PNG 和 SVG。

## 许可

书的文字和自绘图：CC BY 4.0。脚本：MIT，与仓库其余部分相同。转载的发表图保留原许可（见各图注）。详见 [LICENSE.md](LICENSE.md)。
