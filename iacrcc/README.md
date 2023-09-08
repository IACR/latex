# IACR Communications on Cryptology

## 🔧 This is a work in progress 🔧

This directory contains a LaTeX cls file for the new IACR
Communications on Cryptology journal.  The user documentation is
contained in iacrdoc.tex, and this README currently holds only
development details.

The purpose of this style is to facilitate proper capture of author metadata
for the publication editing workflow. Typically a LaTeX class is concerned with
only the layout of the document, but we have added some additional requirements:
1. when the user runs (pdf|lua|xe)latex on their document, it should produce a parsable text
   file that contains structured metadata about the paper, including title, authors,
   their affiliations, their funding, and the paper citations.
2. the author should only have to enter this metadata once, in properly formatted
   LaTeX macros that conform to the required cls.

This LaTeX style is based on the previous [iacrtrans](https://github.com/Cryptosaurus/iacrtrans)
class used to ToSC and TCHES.

The text file format is similar to yaml, and there is a parser for this
file format in the `parser` subdirectory.

The output file has the extension `.meta`. This file is used in the workflow of the
server to which papers using this class will be submitted. There is a
[separate paper](https://arxiv.org/abs/2301.08277) that describes the goals and implementation of the workflow.

## Related work

There are a large number of LaTeX styles that attempt to capture structured metadata
about authors and affiliations. Some are listed below.

 - [elsarticle](https://ctan.org/tex-archive/macros/latex/contrib/elsarticle?lang=en) They use
   labels to associate affiliations and addresses to authors, but have no example where an
   author has multiple affiliations.
 - [apa7](https://ctan.math.illinois.edu/macros/latex/contrib/apa7/apa7.pdf) uses a
   silly comma separated list, but the mapping from authors to affiliations is many to many as it
   should be.
  Their format is:
  ```
  \authorsnames[1,{2,3},1]{Savannah C. St. John, Fen-Lei Chang, Carlos O. Vásquez III}
  \authorsaffiliations{{Education Testing Service, Princeton, New Jersey, ...},
                       {MRC Cognition and Brain Science Unit, Cambridge, England},
                       {Department of Psychology, University of Cambridge}}
  ```
  There is no structured information about affiliations (e.g., ROR IDs or addresses).
- [ifac,ifacconf](https://www.ifac-control.org/events/author-guide/copy_of_ifacconf_latex.zip/view)
  does pretty close to what we want, but footnotes are ugly ****
- [authblk](https://www.ctan.org/pkg/authblk) comes close to handling authors the way we want, but
  has no structured data for authors or affiliations.
- [amscls](https://ctan.math.utah.edu/ctan/tex-archive/info/amscls-doc/Author_Handbook_Journals.pdf)
- [other journals](https://www.latextemplates.com/cat/academic-journals)
- [springer](https://www.springer.com/gp/computer-science/lncs/conference-proceedings-guidelines)
- [MSCS from CUP](https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/information/instructions-contributors)
  does CUP use a different style for each journal?