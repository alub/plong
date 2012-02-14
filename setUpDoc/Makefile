texc = xelatex

setUpDoc.pdf: setUpDoc.tex

%.pdf: %.tex
	$(texc) $<

clean:
	rm -f *.{aux,bib,log,toc}

empty: clean
	rm -f setUpDoc.pdf
