report: images
	@echo "Build Word document report..."
	pandoc --bibliography report.bibtex -f markdown+implicit_figures report.md --reference-doc=format.docx -o ../output/report.docx
	@echo "done.  See output/report.docx"

pdf:
	@echo "Build PDF report..."
	pandoc report.md -o ../output/report.pdf
	@echo "done.  See output/report.docx"

.PHONY: images
images: 
	@echo "Rebuild diagrams..."
	cd .. && /Users/joelegner/.local/share/virtualenvs/voided_shaft-rLIRrrxW/bin/python "/Users/joelegner/Google Drive/Projects/Self-Directed Study/voided_shaft/fdot_demo.py"
	@echo "done."

