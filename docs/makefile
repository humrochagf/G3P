NAME = g3p

html:
	rst2html ${NAME}.rst ${NAME}.html

odt:
	rst2odt ${NAME}.rst ${NAME}.odt

pdf:
	rst2pdf ${NAME}.rst -o ${NAME}.pdf

latex:
	rst2newlatex ${NAME}.rst ${NAME}.tex
	pdflatex ${NAME}.tex
	pdflatex ${NAME}.tex

clean:
	rm -f ${NAME}.aux ${NAME}.html ${NAME}.odt ${NAME}.log ${NAME}.out ${NAME}.pdf ${NAME}.tex
