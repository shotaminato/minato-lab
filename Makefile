
# Build script for the Antora documentation

pages:
	python3 post_processing.py
	npx antora antora-playbook.yml --stacktrace

all: ui pages

.PHONY: ui
ui:
	cd ui/antora-ui-default; \
	gulp bundle; \
	cd ../../; \
	rm ui/ui-bundle.zip; \
	cp ui/antora-ui-default/build/ui-bundle.zip ui/ui-bundle.zip; \

