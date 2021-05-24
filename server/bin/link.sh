pushd ../luncho_typescript-aurelia; yarn install; yarn link; popd
pushd ../app; yarn link "luncho_typescript-aurelia"; popd
