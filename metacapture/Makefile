METACAPTURE_FILES = metacapture.sty metacapture-doc.tex metacapture-doc.pdf metacapture-doc.bib metacapture-sample.tex
IACRJ_FILES = iacrj.cls iacrj-doc.tex iacrj-doc.pdf iacrj-template.tex README.iacrj

all: metacapture.tar.gz iacrj.tar.gz

metacapture.tar.gz: $(METACAPTURE_FILES)
	ctanify --notds --pkgname=metacapture $(METACAPTURE_FILES)

iacrj.tar.gz: $(IACRJ_FILES)
	ctanify --notds --pkgname=iacrj $(IACRJ_FILES)

