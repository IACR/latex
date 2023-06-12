TEXFILES=main.tex intro.tex other.tex main.bib

pdflatex: $(TEXFILES)
	pdflatex -recorder main
	bibtex main
	pdflatex -recorder main
	pdflatex -recorder main

clean:
	rm -f main.pdf main.aux main.log main.out main.fls main.output main.bbl main.blg main.abstract main.meta



