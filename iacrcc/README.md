# IACR Communications on Cryptology

## 🔧 This is a work in progress 🔧

This directory contains a LaTeX cls file for the new IACR
Communications on Cryptology journal.  The user documentation is
contained in example.tex, and this README currently holds only
development details.

The purpose of this style is to facilitate proper capture of author metadata
for the publication editing workflow. Typically a LaTeX class is concerned with
only the layout of the document, but we have added some additional requirements:
1. when the user runs pdflatex on their document, it should produce a parsable text
   file that contains structured metadata about the paper, including title, authors,
   their affiliations, and the paper citations.
2. the author should only have to enter this metadata once, in properly formatted
   LaTeX macros that conform to the required cls.

This LaTeX style is based on the previous [iacrtrans](https://github.com/Cryptosaurus/iacrtrans)
class used to ToSC and TCHES. These may be unified in the future.

While the file we generate appears to be `yaml`, it's not guaranteed
to be parsable as a `yaml` file because of special characters like {
or \ or ". For this reason we use a custom parser that looks only at
the tags on the line to decide what the structure is. The format of
the file is hierarchical, and is perhaps best illustrated with an
example in which there are three authors show share three affiliations.

```
title: How to break {RSA} digital signatures
author:
  name: Ronald Rivest
  inst: 1
author:
  name: Adi Shamir
  inst: 2
  orcid: zzzz-yyyy-zzzz-yyyy
  email: shamir@weizman.ac.il
author:
  name: Leonard M. Adleman
  inst: 1,3
  orcid: xxxx-yyyy-zzzz-wwww
  email: len@usc.edu
affil:
  name: MIT
  ror: ljl2j543
affil:
  name: Weizmann Institute
affil:
  name: University of Southern California
  ror: 2342342xy
citation:
  title: The best algorithm never exists
  authors: Alfred Alliant and David Dumbo
  doi: 10.1007/2122_133
citation:
  title: Is it funny if you have to explain it?
  authors: Ralph Bunch and Ida Lupino
```
The specification of metadata requirements is hopefully readily apparent
from this example. The structure is designed to fulfill the requirements
for consumers of metadata about papers, which is described in a
[separate document](METADATA.md).

## Related work

There are a large number of LaTeX styles that attempt to capture strucutred metadata
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