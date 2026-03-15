PANDOC ?= pandoc
INPUT ?= manuscript/sovereignty_teleology_master_FINAL.md
OUTPUT ?= output/$(basename $(notdir $(INPUT))).pdf
PANDOC_DEFAULTS := pandoc/defaults.yaml
IMAGE ?= theology-pdf
WORKDIR ?= $(CURDIR)
QUARTO_IMAGE ?= quarto-pdf
QUARTO_ZIP ?=

.PHONY: pdf clean docker-build docker-pdf move-quarto-zips quarto-zip-list quarto-zip-pdf quarto-zip-pdf-all

pdf: $(OUTPUT)

$(OUTPUT): $(INPUT) $(PANDOC_DEFAULTS) templates/academic_template.tex filters/pandoc_filters.lua | output
	$(PANDOC) --defaults=$(PANDOC_DEFAULTS) -o $(OUTPUT) $(INPUT)

output:
	@mkdir -p output

clean:
	rm -f output/*.pdf output/*.log output/*.aux output/*.out output/*.toc

# Build the container with all dependencies
container: docker-build

docker-build:
	docker build -t $(IMAGE) .

# Build the PDF inside Docker using the mounted working tree
# Example: make docker-pdf INPUT=manuscript/sovereignty_teleology_master_FINAL.md

docker-pdf: docker-build
	docker run --rm -v $(WORKDIR):/work -w /work $(IMAGE) make pdf INPUT=$(INPUT) OUTPUT=$(OUTPUT)

move-quarto-zips:
	python3 scripts/move_quarto_zips_to_scaffolds.py

quarto-zip-list:
	python3 scripts/build_quarto_zip_project.py --list

quarto-zip-pdf:
	python3 scripts/build_quarto_zip_project.py $(if $(QUARTO_ZIP),--zip $(QUARTO_ZIP),) --image $(QUARTO_IMAGE)

quarto-zip-pdf-all:
	python3 scripts/build_quarto_zip_project.py --all --image $(QUARTO_IMAGE)
