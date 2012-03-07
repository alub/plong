texc = xelatex -shell-escape

setup_doc.pdf: setup_doc.tex

%.pdf: %.tex
	($(texc) $< || (rm -f $@ && false)) && $(texc) $<

clean:
	rm -f *.{aux,bib,log,toc}

empty: clean
	rm -f setup_doc.pdf

.PHONY: empty clean
