
TEXFILES=main.tex test2.bib

test2.pdf: $(TEXFILES)
	lualatex main
	biber main
	lualatex main
	lualatex main

clean:
	rm main.pdf main.blg main.aux main.log main.bbl main.out main.meta main.run.xml main.bcf main.abstract
