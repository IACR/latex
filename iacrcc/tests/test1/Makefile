TEXFILES=main.tex test1.bib

test1.pdf: $(TEXFILES)
	lualatex main
	bibtex main
	lualatex main
	lualatex main

clean:
	rm main.pdf main.blg main.aux main.log main.bbl main.out main.meta main.abstract


