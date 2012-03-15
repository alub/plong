texc = xelatex

userDoc.pdf: userDoc.tex $(wilcard images/*)

%.pdf: %.tex
	($(texc) $< || (rm -f $@ && false)) && $(texc) $<

clean:
	rm -f *.{aux,bib,log,toc}

empty: clean
	rm -f userDoc.pdf

.PHONY: empty clean
