# Build script for the Antora documentation

# Build the UI
cd ui/antora-ui-default
gulp bundle
cd ../../

rm ui/ui-bundle.zip
cp ui/antora-ui-default/build/ui-bundle.zip ui/ui-bundle.zip

# Post processing
python3 post_processing.py

# Build the documentation
npx antora antora-playbook.yml --stacktrace
