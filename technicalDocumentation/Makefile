texc = xelatex

technicalDoc.pdf: technicalDoc.tex

%.pdf: %.tex
	$(texc) $<

clean:
	rm -f *.{aux,bib,log,toc}

empty: clean
	rm -f technicalDoc.pdf
