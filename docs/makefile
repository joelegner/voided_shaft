TEMPLATEDIR = .
BUILDDIR = ../output
IMGDIR = images

.PHONY: all
all: docx pdf

docx: images report-processed.md
	@echo "Build Word document report..."
	pandoc --bibliography report.bibtex -f markdown+implicit_figures --filter pandoc-fignos report-processed.md --reference-doc=format.docx -o '../output/Joe Legner Report Fall 2019.docx'
	@echo "done.  See output/Joe Legner Report Fall 2019.docx"

pdf: report-processed.md
	@echo "Build PDF report..."
	pandoc report-processed.md --filter pandoc-fignos -V geometry:margin=1in -o ../output/report.pdf
	@echo "done.  See output/report.pdf"

.PHONY: images
images: 
	@echo "Rebuild diagrams..."
	cd .. && /Users/joelegner/.local/share/virtualenvs/voided_shaft-rLIRrrxW/bin/python "/Users/joelegner/Google Drive/Projects/Self-Directed Study/voided_shaft/fdot_demo.py"
	@echo "done."

# Makefile for homework app


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  pdf 	Makes the homework.pdf"
	@echo "  clean	Removes all build files."

.PHONY: clean
clean:
	-rm -rf $(BUILDDIR)/*

report-processed.md: report.md
	# cp report.md report-processed.md
	pipenv run python3 report.py > report-processed.md


.PHONY: open
open:
	open -a "PDF Studio 2018.app" $(BUILDDIR)/report.pdf 
