TEXFILES = main.tex test3.bib

all: main.pdf

main.pdf: $(TEXFILES)
	lualatex main
	biber main
	lualatex main
	lualatex main

clean:
	rm -f main.pdf main.blg main.aux main.log main.bbl main.out main.meta main.run.xml main.bcf main.abstract main.fdb_latexmk main.fls main.dvi

