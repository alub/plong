texc = xelatex

report.pdf: report.tex

%.pdf: %.tex
	($(texc) $< || (rm -f $@ && false)) && $(texc) $<

clean:
	rm -f *.{aux,bib,log,toc}

empty: clean
	rm -f report.pdf

.PHONY: empty clean
