
TEXFILES=main.tex main.bib

bibtex: $(TEXFILES)
	touch usebibtex
	latexmk -pdf main
	mv main.pdf bibtex.pdf

biblatex: $(TEXFILES)
	rm -f usebibtex
	latexmk -pdf main
	mv main.pdf biblatex.pdf

zipfile: $(TEXFILES)
	zip main.zip main.tex main.bib

clean:
	rm -f main.pdf main.blg main.aux main.log main.bbl main.out main.meta main.run.xml main.bcf main.abstract main.fdb_latexmk main.fls main.dvi usebibtex main.zip
