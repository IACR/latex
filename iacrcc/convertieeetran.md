# Migrating from `ieeetrans` to `iacrcc`

Converting a paper from IEEE's `ieeetran` LaTeX style file to IACR’s `iacrcc` LaTeX style file means adjusting how some of the meta-data is provided. Concretely, the biggest change involves adjusting the title, author and affiliation information. This guide doesn't cover every detail, and the full documentation is [located here](https://publish.iacr.org/iacrcc).

### Our starting point

Let’s use a slightly adjusted version of the [IEEE template](https://www.ieee.org/conferences/publishing/templates.html) as an example:

```latex
\documentclass[conference]{IEEEtran}
\begin{document}
\title{Conference Paper Title}
\author{\IEEEauthorblockN{First Author}
\IEEEauthorblockA{\textit{department one} \\
\textit{organization one}\\
City, Country \\
author1@mail.com, 0000-1111-2222-3333}
\and
\IEEEauthorblockN{Second Author}
\IEEEauthorblockA{\textit{department two} \\
\textit{organization two}\\
City, Country \\
author2@mail.com, 1111-2222-3333-4444}
}
\maketitle
\begin{abstract}
Abstract text.
\end{abstract}
\begin{IEEEkeywords}
component, formatting, style, styling, insert
\end{IEEEkeywords}
\section{Introduction}
We use RSA~\cite{RSA78}.
\bibliographystyle{ieeetran}
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

The conversion starts by changing the `ieeetran` document class to the `iacrcc` document class. Simply change

```latex
\documentclass[conference]{IEEEtran}
```
to
```latex
\documentclass{iacrcc}
```

### Title

The title and related information should be provided in the same way (although `iacrcc` supports various optional parameters). If macros (or math) are used in the title then make sure to provide a plaintext version using the `plaintext` option on `\title`.

### Author and affiliations

Author and affiliation information are provided one at-a-time in separate blocks. The `ieeetrans` code

```latex
\author{\IEEEauthorblockN{First Author}
\IEEEauthorblockA{\textit{department one} \\
\textit{organization one}\\
City one, Country one \\
author1@mail.com, 0000-1111-2222-3333}
\and
\IEEEauthorblockN{Second Author}
\IEEEauthorblockA{\textit{department two} \\
\textit{organization two}\\
City two, Country two \\
author2@mail.com, 1111-2222-3333-4444}
}
```
needs to be converted into

```latex
\addauthor[inst=1,
           orcid={0000-1111-2222-3333},
           email={author1@mail.com}]{First Author}
\addauthor[inst=2,
           orcid={1111-2222-3333-4444},
           email={author2@mail.com}]{Second Author}
```
and the affiliations become
```latex
\addaffiliation[city={city one},
                country={Country one},
                department={department one}]{organization one}
\addaffiliation[city={city two},
                country={Country two},
                department={department two}]{organization two}
```

### Keywords, abstract, and bibliography

Keywords are defined *before* the abstract and separated by a comma. This means
```latex
\begin{IEEEkeywords}
component, formatting, style, styling, insert
\end{IEEEkeywords}
```
needs to be changed to
```latex
\keywords{component, formatting, style, styling, insert}
```
The abstract is still typeset using `\begin{abstract}` and authors are free to use whatever macros they like.

The style for the references is defined by the journal style, so remove `\bibliographystyle{ieeetran}`.

### The final conversion.

Putting everything together we end up with the converted `ieeetran` template to the `iacrcc` style.

```latex
\documentclass{iacrcc}
\begin{document}
\title{Conference Paper Title}
\addauthor[inst=1,
           orcid={ORCID-author-one},
           email={author1@mail.com}]{First Author}
\addauthor[inst=2,
           orcid={ORCID-author-two},
           email={author2@mail.com}]{Second Author}
\addaffiliation[city={city one},
                country={Country one},
                department={department one}]{organization one}
\addaffiliation[city={city two},
                country={Country two},
                department={department two}]{organization two}
\maketitle
\keywords{component, formatting, style, styling, insert}
\begin{abstract}
Abstract text.
\end{abstract}
\section{Introduction}
We use RSA~\cite{RSA78}.
\bibliography{mybibliography}
\end{document}
```
### What else is there?

This was designed to get you started in the basic conversion from `ieeetran` to `iacrcc`.  There are other features for anonymous submission versions and final versions. These are mentioned in [the
full documentation](https://publish.iacr.org/iacrcc).
