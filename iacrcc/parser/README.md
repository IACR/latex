# Parser for .meta files.

The style file of this package produces a .meta file with a format
that is similar to yaml. This directory contains the reference parser
for the data format. It parses the .meta file and produces a JSON file
that is suitable for downstream processing.

There are tests for this parser in ../tests where it runs compilation
on test LaTeX files, producing the expected .meta format from the
current instance of the package in this repository.

Warning: the IACR/latex-submit application expects the JSON to be
in a format that can be parsed by a pydantic class called `Metadata`.
If you change the format you should run tests there.