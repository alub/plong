texc = xelatex

report.pdf: report.tex report.bib

%.pdf: %.tex
	($(texc) $< || (rm -f $@ && false)) && $(texc) $<
	bibtex $*.aux
	$(texc) $<

clean:
	-rm -f *.{aux,bbl,blg,log,toc}

mrproper: clean
	-rm -f report.pdf

.PHONY: mrproper clean
