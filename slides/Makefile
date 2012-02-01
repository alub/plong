texc = xelatex

slides.pdf: slides.tex

%.pdf: %.tex
	$(texc) $<

clean:
	rm -f *.{aux,log,nav,out,snm,toc}

empty: clean
	rm -f slides.pdf
