texc = xelatex

userDoc.pdf: userDoc.tex

%.pdf: %.tex
	$(texc) $<

clean:
	rm -f *.{aux,bib,log,toc}

empty: clean
	rm -f userDoc.pdf
