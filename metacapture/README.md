# The metacapture package and iacrj document class

This contains the source code for two LaTeX components:

## The `metacapture.sty` package

This provides a mechanism for authors to express their metadata in a
way that separates it from the styling of the page. When a document
that loads `metacapture` is compiled, it produces a yaml-like text
file containing all metadata from the document.  The `metacapture`
package accomplishes this by providing replacements for the generic
macros `\title`, `\author` and `\maketitle` macros that have
traditionally been used by document classes.  The `metacapture`
package also provides several implementations of the `\maketitle` in
different styles, partly as a way to demonstrate how to separate
metadata capture from styling of front matter. Document class authors
can also write their own implementation of `\maketitle` with their
preferred styling.

The documentation for the `metacapture` package is contained in the
`metadoc.tex` with the [`metadoc.pdf`](metadoc.pdf) file.  There
is also a `sample.tex` file that demonstrates
the many uses of the `metacapture` package.

## The `iacrj.cls` document class

The `iacrj` document class is an implementation of a document class on top
of the `metacapture` package. It is intended to be used for three IACR
journals:
* [IACR Transactions on Symmetric Cryptology](https://tosc.iacr.org/)
* [IACR Transactions on Cryptographic Hardware and Embedded Systems](https://tches.iacr.org)
* [IACR Communications in Cryptology](https://cic.iacr.org)

The documentation for the `iacrj.cls` is contained in `iacrdoc.tex`
and [`iacrdoc.pdf`](iacrdoc.pdf). There is additionally a sample file
in `template.tex` to be used in creating articles for the journals.

The `iacrj.cls` document class is a replacement for both `iacrcc.cls`
and `iacrtrans.cls` that were previously used for the IACR journals.
