# Preparing a final version using `iacrcc`

The requirements on the information provided with your final version are different from a preprint or submission document using the `iacrcc` LaTeX style file. Concretely, the biggest differences involve a more complete set of meta-data needed when your document is published. Some advice on preparing your final version is provided here. This guide doesn't cover every detail, and the full documentation is [located here](https://publish.iacr.org/iacrcc).

### Our starting point

Let’s use a very simple simple template written for the `iacrcc` LaTeX style file as an example:

```latex
\documentclass{iacrcc}
\addauthor[inst={1,2}]{Jane Doe}
\addauthor[inst=1]{John Doe}
\addaffiliation{National Security Agency}
\addaffiliation{Europol}
\title{My Final Paper}
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

The conversion starts by informing the `iacrcc` document class to preprare a final version. Simply change

```latex
\documentclass{iacrcc}
```
to
```latex
\documentclass[version=final]{iacrcc}
```

### Affiliations

In the example only the minimum information about the affiliations are provided: the name.

```latex
\addaffiliation{National Security Agency}
\addaffiliation{Europol}
```

It is *mandatory* to provide country information for each affiliation when providing the final version. It is *recommended* to provide the Research Organization Registry ([ROR](https://ror.org)) identifier for the provided organization. There is an [online tool](https://publish.iacr.org/funding) to help you find ROR identifiers. This example could be extended to:

```latex
\addaffiliation[country={USA},
                ror={0047bvr32}]{National Security Agency}
\addaffiliation[country={NL},
                ror={05sj3q575}]{Europol}
```

### Authors

In the example only the minimum information about the authors are provided: the name and index to the affiliation(s).

```latex
\addauthor[inst={1,2}]{Jane Doe}
\addauthor[inst=1]{John Doe}
```
For the final version it is *mandatory* that at least one author provides an e-mail address. It is *recommended* to provide the Open Researcher and Contributor ID ([ORCID](https://orcid.org/)) as a persistent digital identifier.

```latex
\addauthor[inst={1,2},
           email={jane@institute},
           orcid={0000-1111-2222-3333}]{Jane Doe}
\addauthor[inst=1,
           email={john@institute},
           orcid={1111-2222-3333-4444}]{John Doe}
```
### Abstract

For the final version it is *mandatory* to provide a text version of the abstract used for indexing and production of the HTML journal pages. This can be done in the `\begin{textabstract}` environment.

```latex
\begin{textabstract}
In this paper we prove that the One-Time-Pad has perfect security.
\end{textabstract}
```
### License

For the final version it is *mandatory* to provide a supported license. At present the only acceptable license is [CC-by](https://creativecommons.org/licenses/by/2.0/). Specify this in the preamble.

```latex
\license{CC-by}
```
### Funding information

For the final version it is *recommended* to provide funding information whenever this is in scope. For the identification of the funding agency one can use either an identifier from the [Crossref funder registry](https://www.crossref.org/services/funder-registry/) or an identifier from the Research Organization Registry ([ROR](https://ror.org)).

```latex
\addfunding[fundref={100000001},
            grantid={CNS-1237235},
            country={United States}]{National Science Foundation}
\addfunding[ror={00pn5a327},
            country={United States}]{Rambus}
```
Note that `\addfunding` does **not** automatically create footnotes or an acknowledgements section to identify funding - it only collects the metadata for indexing. If you wish to include such visible annotations, you can use the `footnote` option on `\addauthor`, or the `\genericfootnote`, or add a separate acknowledgements section. Some funding agencies have specific requirements or phrases for how they want to be acknowledged in the paper.

### The final conversion.

Putting everything together we end up with the final version in the `iacrcc` style.

```latex
\documentclass[version=final]{iacrcc}
\license{CC-by}
\addauthor[inst={1,2},
           email={jane@institute},
           orcid={0000-1111-2222-3333}]{Jane Doe}
\addauthor[inst=1,
           email={john@institute},
           orcid={1111-2222-3333-4444}]{John Doe}
\addaffiliation[country={USA},
                ror={0047bvr32}]{National Security Agency}
\addaffiliation[country={NL},
                ror={05sj3q575}]{Europol}
\title{My Final Paper}
\begin{document}
\maketitle
\keywords{Something, Something else}
\begin{abstract}
  In this paper we prove that the One-Time-Pad has perfect security.
\end{abstract}
\begin{textabstract}
In this paper we prove that the One-Time-Pad has perfect security.
\end{textabstract}
\section{Introduction}
We use RSA~\cite{RSA78}.
\bibliography{mybibliography}
\end{document}
```
