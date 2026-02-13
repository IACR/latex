# The metacapture package

The `metacapture` package provides a mechanism for authors to express
their metadata in a way that separates it from the styling of the
page.  It is intended primarily for use by LaTeX document class
designers, but may also be useful for authors who may wish to change
their document class in the future.

When a document that loads `metacapture.sty` is compiled, it produces
a yaml-like text file containing all metadata from the document. The
`metacapture` package accomplishes this by providing replacements for
the generic macros `\title`, `\author` and `\maketitle` macros that
have traditionally been used by document classes. The `metacapture`
package also provides several implementations of the `\maketitle` in
different styles, partly as a way to demonstrate how to separate
metadata capture from styling of front matter. Document class designers
can also write their own implementation of `\maketitle` with their
preferred styling using the dictionary-like data structures used
to hold author metadata.

The documentation for the `metacapture` package is contained in the
`metacapture-doc.tex` file (along with the `metacapture-doc.pdf` file).
There is also a `metacapture-sample.tex` file that demonstrates
the many uses of the `metacapture` package.

The `metacapture` package was developed for use in the `iacrj.cls`
document class that is used for IACR journals, but may be used by
others. There is also a companion open source project for a LaTeX
workflow located at a separate [github repository](https://github.com/IACR/latex-submit).
Further information about this can be found at two articles that were
published by the authors:

* [An article in arXiv](https://arxiv.org/abs/2504.10424): https://arxiv.org/abs/2504.10424 
* [An article in TUGboat](https://tug.org/TUGboat/tb46-3/tb144bos-workflow.html): https://tug.org/TUGboat/tb46-3/tb144bos-workflow.html

Bugs on this can be filed at the [github repository](https://github.com/IACR/latex)
