texc = xelatex

report.pdf: report.tex

%.pdf: %.tex
	$(texc) $<

clean:
	rm -f *.{aux,bib,log,toc}

empty: clean
	rm -f report.pdf
