# Migrating from `iacrtrans` to `iacrcc`

Converting a paper from the `iacrtrans` LaTeX style file (as used by the [*IACR Transactions on Symmetric Cryptology*](http://tosc.iacr.org/) and the [*IACR Transactions on Cryptographic Hardware and Embedded Systems*](http://tches.iacr.org/)) means adjusting how some of the meta-data is provided. Concretely, the biggest change involves adjusting the title, author and affiliation information. This guide doesn't cover every detail, and the full documentation is [located here](https://publish.iacr.org/iacrcc).

### Our starting point

Let’s use a slightly adjusted version of the `iacrtrans` [template](https://github.com/Cryptosaurus/iacrtrans/blob/master/template.tex) as an example:

```latex
\documentclass{iacrtrans}
\usepackage{orcidlink}
\author{Jane Doe\,\orcidlink{0000-1111-2222-3333}\inst{1,2} \and John Doe\,\orcidlink{1111-2222-3333-4444}\inst{1}}
\institute{
  Institute A, City, Country, \email{jane@institute}
  \and
  Institute B, City, Country, \email{john@institute}
}
\title{My New Paper}
\begin{document}
\maketitle
\keywords{Something \and Something else}
\begin{abstract}
  In this paper we prove that the One-Time-Pad has perfect security.
\end{abstract}
\section{Introduction}
We use RSA~\cite{RSA78}.
\bibliographystyle{alpha}
\bibliography{mybibliography}
\end{document}
```
Where we assume a file mybibliography.bib exists which contains:

```
@article{RSA78,
  author    = {Ronald L. Rivest and Adi Shamir and Leonard M. Adleman},
  title     = {A Method for Obtaining Digital Signatures and Public-Key Cryptosystems},
  pages     = {120--126},
  year      = {1978},
  journal   = {Communications of the {ACM}},
  volume    = {21},
  number    = {2},
  publisher = {ACM New York, NY, USA},
  doi       = {10.1145/359340.359342},
}
```

### Document class

The conversion starts by changing the `iacrtrans` document class to the `iacrcc`
document class. Simply change

```latex
\documentclass{iacrtrans}
```
to
```latex
\documentclass{iacrcc}
```

### Title

The title and related information should be provided in the same way (although `iacrcc` supports various optional parameters). If macros (or math) are used in the title then make sure to provide a plaintext version using the `plaintext` option on `\title`.

### Author and affiliations

Author and affiliation information are provided one at-a-time. The `iacrtrans` code

```latex
\author{Jane Doe\,\orcidlink{0000-1111-2222-3333}\inst{1,2} \and John Doe\,\orcidlink{1111-2222-3333-4444}\inst{1}}
\institute{
  Institute A, City, Country, \email{jane@institute}
  \and
  Institute B, City, Country, \email{john@institute}
}
```
needs to be converted into

```latex
\addauthor[inst={1,2},
           email={jane@institute},
           orcid={0000-1111-2222-3333}]{Jane Doe}
\addauthor[inst=1,
           email={john@institute},
           orcid={1111-2222-3333-4444}]{John Doe}
```
and the affiliations become
```latex
\addaffiliation[city={City},
                country={Country}]{Institute A}
\addaffiliation[city={City},
                country={Country}]{Institute B}
```

### Keywords, abstract, and bibliography

Keywords are separated by a comma. This means
```latex
\keywords{Something \and Something else}
```
needs to be changed to
```latex
\keywords{Something, Something else}
```
The abstract is still typeset using `\begin{abstract}` and authors are free to use whatever macros they like.

The style for the references is defined by the journal style, so remove `\bibliographystyle{alpha}`.

### The final conversion.

Putting everything together we end up with the converted `iacrtrans` template to the `iacrcc` style.

```latex
\documentclass{iacrcc}
\addauthor[inst={1,2},
           email={jane@institute},
           orcid={0000-1111-2222-3333}]{Jane Doe}
\addauthor[inst=1,
           email={john@institute},
           orcid={1111-2222-3333-4444}]{John Doe}
\addaffiliation[city={City},
                country={Country}]{Institute A}
\addaffiliation[city={City},
                country={Country}]{Institute B}
\title{My New Paper}
\begin{document}
\maketitle
\keywords{Something, Something else}
\begin{abstract}
  In this paper we prove that the One-Time-Pad has perfect security.
\end{abstract}
\section{Introduction}
We use RSA~\cite{RSA78}.
\bibliography{mybibliography}
\end{document}
```
### What else is there?

This was designed to get you started in the basic conversion from `llncs` to `iacrcc`.  There are other features for anonymous submission versions and final versions. These are mentioned in [the
full documentation](https://publish.iacr.org/iacrcc).
