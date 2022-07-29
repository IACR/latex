# Tools to process metadata.

This directory contains `meta.py`, which is a python script that parses `jobname.meta` and
produces various outputs, including:

* a JSON file for downstream hosting. It's ok to include LaTeX in this, since it would be run
  through mathjax.
* a crossref XML file for deposit and DOI assignment
* an XMP file containing citations in JATS schema (TBD).

The crossref format is perhaps most difficult, since it is a complex
schema that is currently at [version
5.3.1](https://data.crossref.org/reports/help/schema_doc/5.3.1/index.html).
There is a [sample submission
file](https://gitlab.com/crossref/schema/-/blob/master/best-practice-examples/journal.article5.3.0.xml),
but it glosses over the most difficult part, namely how to encode
mathematics. You can also [test an
upload](https://data.crossref.org/reports/parser.html).

## Converting TeX to JATS or mathml

There are three TeX formats that may have to be converted:
* author names, with TeX character codes but hopefully nothing else.
* titles, with inline mathematics and TeX character codes
* abstracts, which could contain just about anything in LaTeX.

For the crossref schema, title occurs within
`journal_article/titles/title` and
`journal_article/jats:abstract`. Within `journal_article/titles/title`
there are relatively few elements that can occur, namely
`b,em,font,i,m:math,ovl,scp,strong,sub,sup,tt,u`. The `m:math`
namespace in crossref refers to the MATHML schema.

Abstracts are much more complicated, since they might be expected to
contain just about any LaTeX macros, including `itemize`, `enumerate`,
diagrams, and display mathematics constructions. Within the crossref
schema these are from the JATS namespace
[jats:abstract](https://www.crossref.org/documentation/schema-library/markup-guide-metadata-segments/abstracts/)

Titles are vital, but they are generally much simpler than abstracts
since they usually only include inline mathematics and TeX character
codes. Unfortunately they also commonly contain things like `\mathbb`
and `\mathrm` from the `amsmath` package. Some converters only know
about the macros from TeX and core LaTeX.

### Converters from TeX

There are several approaches for converting TeX to a format that can
be included in crossref XML.

#### latex2mathml

[latex2mathml](https://github.com/roniemartinez/latex2mathml) is a pure python library
that attempts to compile mathml from latex. The syntax for this is
```
mathml_string = latex2mathml.converter.convert(latex_string)
```
In my experience this does pretty well for titles.

#### pandoc

`pandoc` is an entire document format that competes in some ways with LaTeX. More importantly,
the `pandoc` binary and python library `pypandoc` allows conversion between a large number of
formats, including `jats` and `latex`. The syntax for this conversion is:
```
jats_text = pypandoc.convert_text(text, 'jats', 'latex')
```
The resulting `jats_text` is sufficient for inclusion in the jats:abstract tag of crossref.

#### LaTeXML

[latexml](https://math.nist.gov/~BMiller/LaTeXML/) is a perl script
that converts LaTeX documents into an intermediary XML format. It can
then be converted to HTML with embedded MATHML. We have not
investigated this much.

#### TeXSoup

Strictly speaking this doesn't convert TeX to mathml or JATS, but is a parser to generate
a logical tree with its own node objects.

#### Tex2py and PyLaTeX

I'm not sure what these are, but apparently they use TeXSoup.
See [this page](https://zditect.com/blog/50151171.html)