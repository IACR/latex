
TEXFILES=test2.tex test2.bib

test2.pdf: $(TEXFILES)
	lualatex test2
	biber -g biber.config test2
	lualatex test2
	lualatex test2

clean:
	rm test2.pdf test2.blg test2.aux test2.log test2.bbl test2.out test2.meta test2.run.xml test2.bcf test2.abstract
