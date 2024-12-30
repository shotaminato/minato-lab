cd ui/antora-ui-default
gulp bundle
cd ../../

rm ui/ui-bundle.zip
cp ui/antora-ui-default/build/ui-bundle.zip ui/ui-bundle.zip

npx antora antora-playbook.yml --stacktrace
