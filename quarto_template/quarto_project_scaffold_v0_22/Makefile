.PHONY: assemble validate render pdf all clean

OUTPUT := output/sovereignty_teleology.pdf
RAW_OUTPUT := output/manuscript/sovereignty_teleology.pdf

assemble:
	python3 scripts/assemble.py

validate: assemble
	python3 scripts/validate.py

render: validate
	quarto render manuscript/master.qmd --to pdf
	@if [ -f "$(RAW_OUTPUT)" ]; then mv "$(RAW_OUTPUT)" "$(OUTPUT)"; fi

pdf: render

all: pdf

clean:
	rm -f manuscript/master.qmd
	rm -rf output/*
