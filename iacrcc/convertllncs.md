# Migrating from `llncs` to `iacrcc`

Converting a paper from Springer’s `llncs` LaTeX style file (as used
in Crypto, Eurocrypt, Asiacrypt, TCC and PKC) to IACR’s `iacrcc` LaTeX
style file means adjusting how some of the meta-data is provided.
Concretely, the biggest change involves adjusting the title, author
and affiliation information. This guide doesn't cover every detail,
and the full documentation is
[located here](https://publish.iacr.org/iacrcc).

### Our starting point

Let’s use a slightly adjusted version of the LNCS template as an
example:

```

\documentclass[runningheads]{llncs}
\begin{document}
\title{Contribution Title}
\titlerunning{Abbreviated paper title}
\author{First Author\inst{1}\orcidID{0000-1111-2222-3333} \and
Second Author\inst{2,3}\orcidID{1111-2222-3333-4444} \and
Third Author\inst{3}\orcidID{2222-3333-4444-5555}}
\institute{Princeton University, Princeton NJ 08544, USA \and
Springer Heidelberg, Tiergartenstr. 17, 69121 Heidelberg, Germany
\email{lncs@springer.com}\\
\url{http://www.springer.com/gp/computer-science/lncs} \and
ABC Institute, Rupert-Karls-University Heidelberg, Heidelberg, Germany\\
\email{\{abc,lncs\}@uni-heidelberg.de}}
\maketitle
\begin{abstract}
The abstract should briefly summarize the contents of the paper in
15--250 words.
\keywords{First keyword \and Second keyword \and Another keyword.}
\end{abstract}
\section{Introduction}
We use RSA~\cite{RSA78}.
\bibliographystyle{splncs04}
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

The conversion starts by changting the `llncs` document class to the `iacrcc`
document class. Simply change
```
\documentclass[runningheads]{llncs}
```
to
```
\documentclass{iacrcc}
```

### Title

The title and related information should be provided differently using a number of options. Instead of:
```
\title{Contribution Title}
\titlerunning{Abbreviated paper title}
```
One should use
```
\title[running={Abbreviated paper title}]{Contribution Title}.
```
If macros (or math) are used in the title then make sure to provide a plaintext version using the `plaintext` option
on `\title`.

### Author and affiliations

Author and affiliation information are provided one at-a-time. Moreover, e-mail addresses and webpages are linked
to an author (not the affiliation). So the `llncs` code

```
\author{First Author\inst{1}\orcidID{0000-1111-2222-3333} \and
Second Author\inst{2,3}\orcidID{1111-2222-3333-4444} \and
Third Author\inst{3}\orcidID{2222-3333-4444-5555}}
\institute{Princeton University, Princeton NJ 08544, USA \and
Springer Heidelberg, Tiergartenstr. 17, 69121 Heidelberg, Germany
\email{lncs@springer.com}\\
\url{http://www.springer.com/gp/computer-science/lncs} \and
ABC Institute, Rupert-Karls-University Heidelberg, Heidelberg, Germany\\
\email{\{abc,lncs\}@uni-heidelberg.de}}
```
needs to be converted into

```
\addauthor[inst=1,
           orcid={0000-1111-2222-3333},
           email={lncs@springer.com},
           onclick={http://www.springer.com/gp/computer-science/lncs}]{First Author}
\addauthor[inst={2,3},
           orcid={1111-2222-3333-4444},
           email={abc@uni-heidelberg.de}]{Second Author}
\addauthor[inst=3,
           orcid={2222-3333-4444-5555},
           email={lncs@uni-heidelberg.de}]{Third Author}
```
and the affiliations become
```
\addaffiliation[city={Princeton},
                state={NJ},
                postcode={08544},
                country={USA}]{Princeton University}
\addaffiliation[street={Tiergartenstr. 17},
                postcode={69121},
                city={Heidelberg},
                country={Germany}]{Springer Heidelberg}
\addaffiliation[department={ABC Institute},
                city={Heidelberg},
                country={Germany}]{Rupert-Karls-University Heidelberg}
```

### Keywords, abstract, and bibliography

Keywords are defined before the abstract and separated by a comma. This means
```
\keywords{First keyword \and Second keyword \and Another keyword.}
```
needs to be changed to
```
\keywords{First keyword, Second keyword, Another keyword}
```
The abstract is still typeset using `\begin{abstract}` and authors are free to
use whatever macros they like.

The style for the references is defined by the journal style, so remove
`\bibliographystyle{splncs04}`.

### The final conversion.

Putting everything together we end up with the converted llncs template to the `iacrcc` style.

```

\documentclass{iacrcc}
\begin{document}
\title[running={Abbreviated paper title}]{Contribution Title}
\addauthor[inst=1,
           orcid={0000-1111-2222-3333},
           email={lncs@springer.com},
           onclick={http://www.springer.com/gp/computer-science/lncs}]{First Author}
\addauthor[inst={2,3},
           orcid={1111-2222-3333-4444},
           email={abc@uni-heidelberg.de}]{Second Author}
\addauthor[inst=3,
           orcid={2222-3333-4444-5555},
           email={lncs@uni-heidelberg.de}]{Third Author}
\addaffiliation[city={Princeton},
                state={NJ},
                postcode={08544},
                country={USA}]{Princeton University}
\addaffiliation[street={Tiergartenstr. 17},
                postcode={69121},
                city={Heidelberg},
                country={Germany}]{Springer Heidelberg}
\addaffiliation[department={ABC Institute},
                city={Heidelberg},
                country={Germany}]{Rupert-Karls-University Heidelberg}
\maketitle
\keywords{First keyword, Second keyword, Another keyword}
\begin{abstract}
The abstract should briefly summarize the contents of the paper in
15--250 words.
\end{abstract}
\section{Introduction}
We use RSA~\cite{RSA78}.
\bibliography{mybibliography}
\end{document}
```
### What else is there?

This was designed to get you started in the basic conversion from
`llncs` to `iacrcc`.  There are other features for anonymous
submission versions and final versions. These are mentioned in [the
full documentation](https://publish.iacr.org/iacrcc).
