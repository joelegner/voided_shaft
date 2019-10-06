# Voided Shaft

## Introduction

This repository represents my final semester project at the University of South Florida.

## Report

The report deliverable is a word document called `report.docx` which is generated using [Pandoc](pandoc.org).

### Format

1. Source file uses [Pandoc's flavor of Markdown syntax](https://pandoc.org/MANUAL.html#pandocs-markdown).

1. 

1. Inline math goes in single dollar signs `$ ... $` while display math goes in double dollar signs `$$ ... $$`.

1. Bibliography entries are put in using `@name` where `name` is contained in the `report.bibtex` file.

### Report Generation

To generate the report, navigate to the `docs` dirctory and type `make`.

```bash
$ cd docs/
$ make
```

The resulting file `report.docx` will be located in the `output` directory.

