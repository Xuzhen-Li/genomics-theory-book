# Codon usage: selection-mutation-drift balance

```
Theory: Selection-mutation-drift balance for codon usage
Original paper (year): Ikemura T. 1981. Correlation
  between the abundance of Escherichia coli transfer
  RNAs and the occurrence of the respective codons in
  its protein genes: a proposal for a synonymous codon
  choice that is optimal for the E. coli translational
  system. J Mol Biol 151:389-409. DOI
  10.1016/0022-2836(81)90003-6. Bulmer M. 1991. The
  selection-mutation-drift theory of synonymous codon
  usage. Genetics 129:897-907. DOI
  10.1093/genetics/129.3.897 formalized the balance.
  Grantham et al. 1980 (DOI 10.1093/nar/8.1.197-c) is
  the earlier catalogue and genome hypothesis, not the
  selection-mutation-drift statement. Akashi 1994 (DOI
  10.1093/genetics/136.3.927) and Hershberg and Petrov
  2008 (DOI 10.1146/annurev.genet.42.110807.091442) are
  later tests and reviews.
One-sentence prediction: Preferred synonymous codons
  track tRNA abundance and are more frequent in highly
  expressed genes; the bias is a balance of weak
  selection, mutation and drift, so it is stronger where
  effective size is large.
Assumptions: synonymous sites can be selected;
  expression and tRNA abundance are measured; GC-biased
  gene conversion is distinguished from selection.
Which fail here: GC-biased gene conversion also produces
  preference for GC-ending codons. In grapevine,
  translational selection is detectable, but GC-biased
  gene conversion is the stronger force.
Modern data / statistic: Clément et al. 2017 (DOI
  10.1371/journal.pgen.1006799) found that in grapevine
  the frequency of optimal codons rises with expression,
  and that the direction-of-selection statistic for
  unpreferred-to-preferred changes correlates with
  expression.
What would falsify it: after mutation and GC-biased gene
  conversion are taken into account, codon preference
  does not increase with expression or with tRNA
  abundance.
What we will not claim: that GC-biased gene conversion
  is absent in grapevine. That Ikemura 1981 is a plant
  paper. That codon bias in grapevine is mainly
  translational selection (the chapter says gene
  conversion is stronger).
```

## Later additions
Keep follow-on material in this folder, not in a shared dump:
- `reviews/` — related reviews (not the original paper)
- `research/` — modern tests and follow-ups
- `scripts/` — verification
