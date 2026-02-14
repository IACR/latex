This example illustrates the use of biblatex, with a bibtex file that
contains a mixture of UTF-8 encoded characters and TeX codes.  Note
that we use lualatex to process this. If we use pdflatex then the
encoding of the .meta file will be T1, which is incorrect. pdflatex does
not properly handle UTF-8 in \write.