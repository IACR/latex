TEXFILES=test1.tex test1.bib

test1.pdf: $(TEXFILES)
	pdflatex test1
	bibtex test1
	pdflatex test1
	pdflatex test1

clean:
	rm test1.pdf test1.blg test1.aux test1.log test1.bbl test1.out test1.meta


