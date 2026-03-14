PANDOC ?= pandoc
INPUT ?= manuscript/sovereignty_teleology_master_FINAL.md
OUTPUT ?= output/$(basename $(notdir $(INPUT))).pdf
PANDOC_DEFAULTS := pandoc/defaults.yaml
IMAGE ?= theology-pdf
WORKDIR ?= $(CURDIR)

.PHONY: pdf clean docker-build docker-pdf

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
