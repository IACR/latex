
all: test3.pdf

test3.pdf: $(TEXFILES)
	lualatex test3
	biber test3
	lualatex test3
	lualatex test3

clean:
	rm test3.pdf test3.blg test3.aux test3.log test3.bbl test3.out test3.meta test3.run.xml test3.bcf
