TEXFILES=main.tex test5.bib

test1.pdf: $(TEXFILES)
	lualatex main
	bibtex main
	lualatex main
	lualatex main

clean:
	rm -f main.pdf main.blg main.aux main.log main.bbl main.out main.meta main.run.xml main.bcf main.abstract main.fdb_latexmk main.fls main.dvi

