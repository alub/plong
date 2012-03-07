texc = xelatex

setup_doc.pdf: setup_doc.tex

%.pdf: %.tex
	$(texc) $<

clean:
	rm -f *.{aux,bib,log,toc,pyg}

empty: clean
	rm -f setup_doc.pdf
